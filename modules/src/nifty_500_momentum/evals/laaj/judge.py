import numpy as np
import json
import os
import random
from typing import List, Dict, Any

from nifty_500_momentum.data.manager import DataManager
from nifty_500_momentum.llm import llm, StructuredLLMInput

from .prompt import LaajSystemPrompt
from .evaluation import LLMJudgeEval



class LLMJudge:
    def __init__(self, 
                 data_manager: DataManager,
                 num_of_samples_checks: int = 10):
        self.dm = data_manager
        self.llm = llm
        
        self.num_of_sample_checks = num_of_samples_checks


    def _load_and_pair_data(self,
                            analysis_id: str,
                            strategy_name: str) -> List[Dict[str, Any]]:
        """
        Parses the specific JSON structure provided by the user.
        Joins 'filtered_news' and 'analysis_results' by ticker.
        """
        shortlist_data = self.dm.storage.load_shortlist(strategy_name=strategy_name)
        results_data = self.dm.storage.load_analyst_state(analysis_id=analysis_id)

        #shortlisted_tickers = shortlist_data.get("shortlisted_tickers", [])
        static_signals = shortlist_data.get("tickers_results", {})
        
        news_map = results_data.get("filtered_news", {})
        results_map = results_data.get("analysis_results", {})
        
        paired_data = []
        
        # Iterate through analysis results to find matching news
        for ticker, analysis in results_map.items():
            news_items = news_map.get(ticker, [])
            paired_data.append({
                "ticker": ticker,
                "static_signals": static_signals.get(ticker, {}),
                "news": news_items,
                "analysis": analysis
            })
            
        return paired_data


    def _select_samples(self, data: List[Dict]) -> List[Dict]:
        """
        Selects 10 High Scoring (>=7) and 10 Medium-to-Low Scoring (<7) tickers.
        """
        high_scoring = [d for d in data if d['analysis'].get('conviction_score', 0) >= 7]
        low_med_scoring = [d for d in data if d['analysis'].get('conviction_score', 0) < 7]

        # Random sample (up to 10)
        selected_high = random.sample(high_scoring, min(len(high_scoring), self.num_of_sample_checks // 2))
        selected_low = random.sample(low_med_scoring, min(len(low_med_scoring), self.num_of_sample_checks // 2))
        
        print(f"Sampling: Selected {len(selected_high)} High-Conviction and {len(selected_low)} Low/Med-Conviction tickers.")
        
        return selected_high + selected_low


    def evaluate_performance(self,
                             analysis_id: str = None,
                             strategy_name: str = None) -> Dict[str, Any]:
        """
        Main execution loop for the LLM Judge.
        """
        all_data = self._load_and_pair_data(analysis_id=analysis_id,
                                            strategy_name=strategy_name)
        if not all_data:
            return {"error": "No data found"}

        samples = self._select_samples(all_data)
        eval_results: List[LLMJudgeEval] = []
        
        print(f"--- Starting LLM Judge Evaluation on {len(samples)} Tickers ---")

        for item in samples:
            ticker = item['ticker']
            static = item['static_signals']
            news = item['news']
            analysis = item['analysis']
            
            # Skip if no news was present (Agent couldn't have done much)
            if not news:
                continue

            # 1. Format Evidence (News)
            news_text = ""
            for n in news[:5]: # Context limit
                title = n.get('title', 'Unknown Title')
                source = n.get('source', 'Unknown Source')
                date = n.get('published_dt', 'Unknown Date')
                news_text += f"- [{date}] {source}: {title}\n"
                
            # 2. Format Evidence (technical signals)
            technical_signals = f"Technical Signals:\n{static['reason']}. Supporting metrics:\n"
            for key, value in static['metrics'].items():
                technical_signals += f"- {key}: {value}\n"

            # 2. Format Student Submission (The Agent's Analysis)
            agent_output = json.dumps(analysis, indent=2)

            # 3. Construct the Judge Prompt
            prompt = f"""
            INPUT DATA (Technical Signals provided)
            {technical_signals}
            INPUT DATA (News provided to Analyst):
            {news_text}
            ANALYST'S OUTPUT:
            {agent_output}
            """

            # 4. Call LLM (Using a generic request wrapper here for flexibility)
            inp = StructuredLLMInput(
                messages=[
                    {"role": "system", "content": LaajSystemPrompt},
                    {"role": "user", "content": prompt}
                ]
            )
            response = self.llm.generate_structured(inp=inp, output_model=LLMJudgeEval)
            
            eval_results.append(response)

        # 5. Aggregate Statistics
        if not eval_results:
            return {"status": "Failed to generate evaluations"}

        avg_grade = np.mean([x.grade for x in eval_results])
        
        return {
            "summary": {
                "total_samples": len(eval_results),
                "average_judge_score": round(avg_grade, 2),
                "model_used": self.llm.model
            },
            "details": [eval_res.model_dump(mode='json') for eval_res in eval_results]
        }
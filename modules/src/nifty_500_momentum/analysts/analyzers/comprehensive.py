from pydantic import BaseModel, Field
from typing import List

from .base import BaseAnalyzer, StructuredLLMInput, AnalyzerInput
from .market_drivers import MarketDriver, driver_options

class ComprehensiveMomentumAnalysis(BaseModel):
    sentiment_score: float = Field(..., description="Range -1.0 (Negative) to 1.0 (Positive)")
    conviction_score: int = Field(..., description="Confidence in the trend sustainability (1-10)")
    primary_driver: MarketDriver = Field(
        ..., 
        description="The single most impactful reason for the price move"
    )
    secondary_drivers: List[MarketDriver] = Field(
        default=[], 
        description="Other contributing factors (e.g., Macro + Earnings)"
    )
    is_operator_trap: bool = Field(..., description="True if price is up but news is negative or non-existent")
    reasoning: str = Field(..., description="Reasoning behind the analysis")
    red_flags: List[str] = Field(default=[], description="List of specific risks like 'IT Raid', 'CEO Resignation'")


SYSTEM_PROMPT = f"""
You are a Senior Risk Manager for the Indian Stock Market (Nifty 500).

YOUR TASK:
Analyze the provided Technical Signals and News Headlines to determine the validity of the price move.

INPUT DATA:
You will receive a Stock Ticker, the Technical Signal (why our algo picked it), and recent News Headlines.

ANALYSIS LOGIC:
1. CONSISTENCY CHECK: Does the news explain the technical signal?
   - Price UP + Strong Earnings/Order = HIGH CONVICTION.
   - Price UP + No News = SPECULATION (Medium Risk).
   - Price UP + Bad News (Raids, Lawsuits) = OPERATOR TRAP (High Risk).

2. SOURCE CREDIBILITY:
   - Prioritize 'Exchange Filings', 'Earnings Calls', and 'Top Tier Media' (Mint, ET).
   - Ignore generic 'Market Wrap' headers.

3. SCORING:
   - Sentiment: -1 (Bearish) to +1 (Bullish).
   - Conviction: 1 (Gambling) to 10 (Institutional Quality).

CRITICAL INSTRUCTION - PRIMARY DRIVER:
You must categorize the 'primary_driver' into EXACTLY one of the following categories. 
Do not invent new categories.

ALLOWED DRIVERS:
[{driver_options}]

ANALYSIS RULES:
1. If the news mentions a 'Block Deal', 'Promoter selling', or 'Stake sale', select "{MarketDriver.INSIDER_ACTIVITY.value}".
2. If the news mentions 'Bonus', 'Split', 'Buyback', or 'Dividend', select "{MarketDriver.CORP_ACTION.value}".
3. If price is up > 3% but there is NO relevant news, select "{MarketDriver.SPECULATION.value}".
4. If news is negative (e.g., 'Tax Notice', 'Fraud') but price is rising, set 'is_trap' to True.

OUTPUT FORMAT:
Return valid JSON only. Matches the requested schema.
"""
    
class ComprehensiveAnalyzer(BaseAnalyzer):
    def analyze(self, data: AnalyzerInput) -> ComprehensiveMomentumAnalysis:
        user_prompt = ""
        
        # Add the technical signal
        user_prompt += f"Technical Signals:\n{data.static_results.reason}. Supporting metrics:\n"
        for key, value in data.static_results.metrics.items():
            user_prompt += f"- {key}: {value}\n"
            
        # Add the news data
        user_prompt += "\n\nRecent News Headlines:\n"
        for article in data.news_data:
            user_prompt += f"- [{article.published_dt}] {article.source}: {article.title}\n"
            
        # call the LLM
        inp = StructuredLLMInput(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        response = self.llm.generate_structured(inp=inp, output_model=ComprehensiveMomentumAnalysis)
        return response
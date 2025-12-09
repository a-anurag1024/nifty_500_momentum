from typing import Dict
from .strategies.base import MomentumStrategy, StaticScoutResult
from .strategies.explosive_breakout import ExplosiveBreakoutStrategy
from .strategies.golden_momentum import GoldenMomentumStrategy
from .strategies.reversal_hunter import ReversalHunterStrategy
from .strategies.trendsurfer import TrendSurferStrategy


static_momentum_strategies: Dict[str, MomentumStrategy] = {
    "explosive_breakout": ExplosiveBreakoutStrategy(),
    "golden_momentum": GoldenMomentumStrategy(),
    "reversal_hunter": ReversalHunterStrategy(),
    "trendsurfer": TrendSurferStrategy(),
}
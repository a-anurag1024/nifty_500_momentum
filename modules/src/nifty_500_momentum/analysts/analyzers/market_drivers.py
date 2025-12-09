from enum import Enum

class MarketDriver(str, Enum):
    # --- FUNDAMENTAL DRIVERS ---
    EARNINGS = "Earnings/Guidance"          # Q-Results, Guidance Up/Down
    ORDER_WIN = "Order/Contract Win"        # New huge projects (Common in Infra/Defense)
    EXPANSION = "Capacity/Product Launch"   # New Factory, FDA Approval, New Car Launch
    
    # --- STRATEGIC EVENTS ---
    MERGERS_ACQ = "M&A/Strategic Tie-up"    # Mergers, Acquisitions, JVs
    CORP_ACTION = "Corporate Action"        # Buyback, Bonus Issue, Stock Split, Dividend
    MANAGEMENT = "Management Change"        # CEO Resignation, New Appointments
    
    # --- EXTERNAL FACTORS ---
    REGULATORY = "Regulatory/Govt Policy"   # PLI Schemes, Tax Changes, RBI/SEBI Actions
    LEGAL = "Legal/Litigation"              # Court Rulings, Lawsuits, Settlements
    MACRO = "Macro/Sector Trend"            # Budget, Inflation, Commodity Prices (Oil/Steel)
    
    # --- MARKET FLOWS ---
    INSIDER_ACTIVITY = "Insider/Block Deal" # Promoters buying/selling, Large FII/DII trades
    RATING_CHANGE = "Analyst Upgrade/Downgrade" # Brokerage reports raising/cutting targets
    INCLUSION = "Index Inclusion/Exclusion" # Added to MSCI/Nifty Next 50 (Passive flows)
    
    # --- UNCERTAIN ---
    SPECULATION = "Speculation/Technical"   # Pump & Dump, Operator activity, No News
    NOISE = "Noise/Unknown"                 # Irrelevant news found


driver_options = ", ".join([f'"{d.value}"' for d in MarketDriver])
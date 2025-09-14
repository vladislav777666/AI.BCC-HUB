from pydantic import BaseModel
from typing import List, Dict

class Features(BaseModel):
    client_code: int
    age: int
    status: str
    city: str
    avg_monthly_balance_KZT: float
    top3_categories: List[str]
    spend_by_category: Dict[str, float]
    spend_3m_total: float
    trips_count_3m: int
    salary_incoming_avg: float
    deposit_balance: float
    fx_tx_count_3m: int
    push_opt_in: bool
    large_out: float
    invest_count: int
    gold_count: int
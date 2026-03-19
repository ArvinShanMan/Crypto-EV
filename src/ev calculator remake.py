import numpy
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

#win_rate = between 0 and 1
#loss_rate = 1 - win_rate
#win_amount = positive number
#num_trades = positive integer

@dataclass(slots=True)
class DataPoint:
    loss_rate: float
    win_rate: float
    win_amount: float
    num_trades: int

    def __post_init__(self):
        if self.win_rate > 0 and self.win_rate <= 1:
            pass
        else:
            raise ValueError("Win rate must be between 0 and 1")
        if self.win_amount <= 0:
            raise ValueError("Win amount must be greater than 0")
        else:
            pass
        if self.num_trades <= 0:
            raise ValueError("Number of trades must be a positive integer")
        else:
            pass
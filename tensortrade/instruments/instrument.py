# Copyright 2019 The TensorTrade Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License


from typing import Union
from sympy import Symbol

from .quantity import Quantity
from .trading_pair import TradingPair

registry = {}


class Instrument:
    """A financial instrument for use in trading."""

    def __init__(self, symbol: Union[Symbol, str], precision: int, name: str = None):
        self._symbol = Symbol(symbol) if isinstance(symbol, str) else symbol
        self._precision = precision
        self._name = name

        registry[symbol] = self

    @property
    def symbol(self) -> str:
        return str(self._symbol)

    @property
    def precision(self) -> int:
        return self._precision

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other: 'Instrument') -> bool:
        return self.symbol == other.symbol and self.precision == other.precision and self.name == other.name

    def __ne__(self, other: 'Instrument') -> bool:
        return self.symbol != other.symbol or self.precision != other.precision or self.name != other.name

    def __rmul__(self, other: float) -> Quantity:
        return Quantity(instrument=self, size=other)

    def __truediv__(self, other):
        if isinstance(other, Instrument):
            return TradingPair(self, other)

    def __hash__(self):
        return hash(self.symbol)

    def __str__(self):
        return str(self.symbol)

    def __repr__(self):
        return str(self)


# Crypto
BTC = Instrument('BTC', 8, 'Bitcoin')
ETH = Instrument('ETH', 8, 'Ethereum')
XRP = Instrument('XRP', 8, 'XRP')
NEO = Instrument('NEO', 8, 'NEO')
BCH = Instrument('BCH', 8, 'Bitcoin Cash')
LTC = Instrument('LTC', 8, 'Litecoin')
ETC = Instrument('ETC', 8, 'Ethereum Classic')
XLM = Instrument('XLM', 8, 'Stellar Lumens')
LINK = Instrument('LINK', 8, 'Chainlink')
ATOM = Instrument('ATOM', 8, 'Cosmos')
DAI = Instrument('DAI', 8, 'Dai')
USDT = Instrument('USDT', 8, 'Tether')

# FX
USD = Instrument('USD', 2, 'U.S. Dollar')
EUR = Instrument('EUR', 2, 'Euro')
JPY = Instrument('JPY', 2, 'Japanese Yen')
KWN = Instrument('KWN', 2, 'Korean Won')
AUD = Instrument('EUR', 2, 'Australian Dollar')

# Commodities
XAU = Instrument('XAU', 2, 'Gold futures')
XAG = Instrument('XAG', 2, 'Silver futures')

# Stocks

# Hard Currency
GOLD = Instrument('XAU', 1, 'Gold')


#PredictIt
TRUMP_PRESIDENT = Instrument('TRUMP_PRESIDENT', 2, 'Will Donald Trump be president at year-end 2018?')
WARREN = Instrument('WARREN', 2, 'Will Elizabeth Warren be re-elected to the U.S. Senate in Massachusetts in 2018?')
CRUZ = Instrument('CRUZ', 2, 'Will Ted Cruz be re-elected to the U.S. Senate in Texas in 2018?')
MANCHIN = Instrument('MANCHIN', 2, 'Will Joe Manchin be re-elected to the U.S. Senate in West Virginia in 2018?')
SANDERS = Instrument('SANDERS', 2, 'Will Bernie Sanders be re-elected to the U.S. Senate in Vermont in 2018?')
NELSON = Instrument('NELSON', 2, 'Will Bill Nelson be re-elected to the U.S. Senate in Florida in 2018?')
DONNELLY = Instrument('DONNELLY', 2, 'Will Joe Donnelly be re-elected to the U.S. Senate in Indiana in 2018?')
TRUMP_IMPEACH = Instrument('TRUMP_IMPEACH', 2, 'Will Donald Trump be impeached by year-end 2018?')
FL_SENATE = Instrument('FL_SENATE', 2, 'Who will win the 2018 Florida Republican Senate primary?')
MANAFORT = Instrument('MANAFORT', 2, 'Will Trump pardon Manafort by year-end 2018?')
CALEXIT = Instrument('CALEXIT', 2, 'Will "Calexit" initiative qualify for the 2018 ballot in California?')
TRUMP_APPROVAL = Instrument('TRUMP_APPROVAL', 2, 'Will Trump\'s Gallup approval be 50% or higher at any point before year-end 2018?')
RYAN = Instrument('RYAN', 2, 'Will Paul Ryan be re-elected to Congress in 2018?')
PELOSI = Instrument('PELOSI', 2, 'Will Nancy Pelosi be re-elected to Congress in 2018?')
HURD = Instrument('HURD', 2, 'Will Will Hurd be re-elected to Congress in 2018?')
TESTER = Instrument('TESTER', 2, 'Will Jon Tester be re-elected to the U.S. Senate in Montana in 2018?')
HEITKAMP = Instrument('HEITKAMP', 2, 'Will Heidi Heitkamp be re-elected to the U.S. Senate in North Dakota in 2018?')
DENHAM = Instrument('DENHAM', 2, 'Will Jeff Denham be re-elected to Congress in 2018?')
BALDWIN = Instrument('BALDWIN', 2, 'Will Tammy Baldwin be re-elected to the U.S. Senate in Wisconsin in 2018?')
MCCASKILL = Instrument('MCCASKILL', 2, 'Will Claire McCaskill be re-elected to the U.S. Senate in Missouri in 2018?')
KNIGHT = Instrument('KNIGHT', 2, 'Will Steve Knight be re-elected to Congress in 2018?')
BROWN = Instrument('BROWN', 2, 'Will Sherrod Brown be re-elected to the U.S. Senate in Ohio in 2018?')
STABENOW = Instrument('STABENOW', 2, 'Will Debbie Stabenow be re-elected to the U.S. Senate in Michigan in 2018?')
HEINRICH = Instrument('HEINRICH', 2, 'Will Martin Heinrich be re-elected to the U.S. Senate in New Mexico in 2018?')
MENENDEZ = Instrument('MENENDEZ', 2, 'Will Bob Menendez be re-elected to the U.S. Senate in New Jersey in 2018?')

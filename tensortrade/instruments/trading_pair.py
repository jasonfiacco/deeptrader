
from numbers import Number

from tensortrade.base.exceptions import InvalidTradingPair, IncompatibleTradingPairOperation
from tensortrade.instruments.quantity import Price


class TradingPair:
    """A pair of financial instruments to be traded on a specific exchange."""

    def __init__(self, base: 'Instrument', quote: 'Instrument'):

        if base == quote:
            raise InvalidTradingPair(base, quote)

        self._base = base
        self._quote = quote

    @property
    def base(self):
        return self._base

    @property
    def quote(self):
        return self._quote

    def __rmul__(self, other):
        if not isinstance(other, Number):
            raise IncompatibleTradingPairOperation(other, self)
        return Price(other, self)

    def __eq__(self, other):
        if isinstance(other, TradingPair):
            if str(self) == str(other):
                return True
        return False

    def __str__(self):
        return '{}/{}'.format(self.base.symbol, self.quote.symbol)

    def __repr__(self):
        return str(self)

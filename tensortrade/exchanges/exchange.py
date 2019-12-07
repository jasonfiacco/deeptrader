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
# limitations under the License.

import uuid
import pandas as pd
import numpy as np

from abc import abstractmethod
from typing import Dict, Union, List
from gym.spaces import Box

from tensortrade import Component
from tensortrade.trades import Trade
from tensortrade.features import FeaturePipeline
from tensortrade.wallets import Portfolio

TypeString = Union[type, str]


class Exchange(Component):
    """An abstract exchange for use within a trading environments.

    Arguments:
        base_instrument: The exchange symbol of the instrument to store/measure value in.
        dtype: A type or str corresponding to the dtype of the `observation_space`.
        feature_pipeline: A pipeline of feature transformations for transforming observations.
    """
    registered_name = "exchanges"

    def __init__(self, dtype: TypeString = np.float32, feature_pipeline: FeaturePipeline = None, portfolio: Portfolio = None, **kwargs):
        self._dtype = self.default('dtype', dtype)
        self._feature_pipeline = self.default('feature_pipeline', feature_pipeline)
        self._window_size = self.default('window_size', 1, kwargs)
        self._min_trade_amount = self.default('min_trade_amount', 1e-6, kwargs)
        self._max_trade_amount = self.default('max_trade_amount', 1e6, kwargs)
        self._min_trade_price = self.default('min_trade_price', 1e-8, kwargs)
        self._max_trade_price = self.default('max_trade_price', 1e8, kwargs)

        self._portfolio = self.default('portfolio', portfolio)

        self._observe_wallets = self.default('observe_wallets', None, kwargs)

        if isinstance(self._observe_wallets, list):
            self._observe_balances = self._observe_wallets
            self._observe_locked_balances = self._observe_wallets
        else:
            self._observe_balances = self.default('observe_balances', None, kwargs)
            self._observe_locked_balances = self.default('observe_locked_balances', None, kwargs)


        self.id = uuid.uuid4()

    @property
    def window_size(self) -> int:
        """The window size of observations."""
        return self._window_size

    @window_size.setter
    def window_size(self, window_size: int):
        self._window_size = window_size

    @property
    def dtype(self) -> TypeString:
        """A type or str corresponding to the dtype of the `observation_space`."""
        return self._dtype

    @dtype.setter
    def dtype(self, dtype: TypeString):
        self._dtype = dtype

    @property
    def feature_pipeline(self) -> FeaturePipeline:
        """A pipeline of feature transformations for transforming observations."""
        return self._feature_pipeline

    @feature_pipeline.setter
    def feature_pipeline(self, feature_pipeline: FeaturePipeline):
        self._feature_pipeline = feature_pipeline

    @property
    def portfolio(self) -> Portfolio:
        """The portfolio of instruments currently held on this exchange."""
        return self._portfolio

    @portfolio.setter
    def portfolio(self, portfolio: Portfolio):
        self._portfolio = portfolio

    @property
    @abstractmethod
    def trades(self) -> List[Trade]:
        """A list of trades made on the exchange since the last reset."""
        raise NotImplementedError

    @property
    @abstractmethod
    def observation_columns(self) -> List[str]:
        """The final columns provided by the observation space, after any feature transformations."""
        raise NotImplementedError

    @property
    def observation_space(self) -> Box:
        """The final shape of the observations generated by the exchange, after any feature transformations."""
        n_features = len(self.observation_columns)

        low = np.tile(self._min_trade_price, n_features)
        high = np.tile(self._max_trade_price, n_features)

        if self._window_size > 1:
            low = np.tile(low, self._window_size).reshape((self._window_size, n_features))
            high = np.tile(high, self._window_size).reshape((self._window_size, n_features))

        return Box(low=low, high=high, dtype=self._dtype)

    @property
    @abstractmethod
    def has_next_observation(self) -> bool:
        """If `False`, the exchange's data source has run out of observations.

        Resetting the exchange may be necessary to continue generating observations.

        Returns:
            Whether or not the specified instrument has a next observation.
        """
        raise NotImplementedError

    @abstractmethod
    def _next_observation(self) -> Union[pd.DataFrame, np.ndarray]:
        raise NotImplementedError()

    def next_observation(self) -> np.ndarray:
        """Generate the next observation from the exchange.
        Returns:
            The next multi-dimensional list of observations.
        """
        observation = self._next_observation()

        if isinstance(observation, pd.DataFrame):
            observation = observation.fillna(0, axis=1)
            return observation.values

        return observation

    @abstractmethod
    def current_price(self, symbol: str) -> float:
        """The current price of an instrument on the exchange, denoted in the base instrument.

        Arguments:
            symbol: The exchange symbol of the instrument to get the price for.

        Returns:
            The current price of the specified instrument, denoted in the base instrument.
        """
        raise NotImplementedError

    @abstractmethod
    def quote_price(self, trading_pair: 'TradingPair') -> float:
        """The quote price of a trading pair on the exchange, denoted in the base instrument.

        Arguments:
            trading_pair: The `TradingPair` to get the quote price for.

        Returns:
            The quote price of the specified trading pair, denoted in the base instrument.
        """
        raise NotImplementedError

    @abstractmethod
    def is_pair_tradeable(self, trading_pair: 'TradingPair') -> bool:
        """Whether or not the specified trading pair is tradeable on this exchange.

        Args:
            trading_pair: The `TradingPair` to test the tradeability of.

        Returns:
            A bool designating whether or not the pair is tradeable.
        """
        raise NotImplementedError()

    @abstractmethod
    def execute_trade(self, trade: Trade) -> Trade:
        """Execute a trade on the exchange, accounting for slippage.

        Arguments:
            trade: The trade to execute.

        Returns:
            The filled trade.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        """Reset the feature pipeline, initial balance, trades, performance, and any other temporary stateful data."""
        if self._feature_pipeline is not None:
            self.feature_pipeline.reset()

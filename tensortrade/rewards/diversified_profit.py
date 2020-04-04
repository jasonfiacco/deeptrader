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

import pandas as pd
import numpy as np
import math

from typing import Callable

from tensortrade.rewards import RewardScheme


class DiversifiedProfit(RewardScheme):
    """A reward scheme that rewards the agent for increasing its net worth, while penalizing more volatile strategies.
    """

    def __init__(self,
                 return_algorithm: str = 'sharpe',
                 risk_free_rate: float = 0.,
                 target_returns: float = 0.,
                 window_size: int = 1):
        """
        Args:
            return_algorithm (optional): The risk-adjusted return metric to use. Options are 'sharpe' and 'sortino'. Defaults to 'sharpe'.
            risk_free_rate (optional): The risk free rate of returns to use for calculating metrics. Defaults to 0.
            target_returns (optional): The target returns per period for use in calculating the sortino ratio. Default to 0.
        """
        algorithm = self.default('return_algorithm', return_algorithm)

        self._return_algorithm = self._return_algorithm_from_str(algorithm)
        self._risk_free_rate = self.default('risk_free_rate', risk_free_rate)
        self._target_returns = self.default('target_returns', target_returns)
        self._window_size = self.default('window_size', window_size)

    def _return_algorithm_from_str(self, algorithm_str: str) -> Callable[[pd.DataFrame], float]:
        assert algorithm_str in ['sharpe', 'sortino']

        if algorithm_str == 'sharpe':
            return self._sharpe_ratio
        elif algorithm_str == 'sortino':
            return self._sortino_ratio

    def _sharpe_ratio(self, returns: pd.Series) -> float:
        """Return the sharpe ratio for a given series of a returns.

        References:
            - https://en.wikipedia.org/wiki/Sharpe_ratio
        """
        return (np.mean(returns) - self._risk_free_rate + 1E-9) / (np.std(returns) + 1E-9)

    def _sortino_ratio(self, returns: pd.Series) -> float:
        """Return the sortino ratio for a given series of a returns.

        References:
            - https://en.wikipedia.org/wiki/Sortino_ratio
        """
        downside_returns = returns.copy()
        downside_returns[returns < self._target_returns] = returns ** 2

        expected_return = np.mean(returns)
        downside_std = np.sqrt(np.std(downside_returns))

        return (expected_return - self._risk_free_rate + 1E-9) / (downside_std + 1E-9)

    def _get_log_cum_returns(self, portfolio: 'Portfolio') -> float:
        t_f = portfolio.performance.index[-1]

        log_cum_returns = (1/t_f) * (math.log(portfolio.net_worth/portfolio.initial_net_worth))
        return log_cum_returns

    def _get_simple_profit(self, portfolio: 'Portfolio') -> float:
        returns = portfolio.performance['net_worth'].pct_change().dropna()
        returns = (1 + returns[-self._window_size:]).cumprod() - 1
        if len(returns) < 1:
            simple_profit = 0
        else:
            simple_profit = returns.iloc[-1]
        return simple_profit

    def _standard_log_returns(self, portfolio: 'Portfolio') -> float:
        t_f = portfolio.performance.index[-1]
        returns_in_raw_percent = 1 + portfolio.performance['net_worth'].pct_change().dropna()
        profit_this_step = (returns_in_raw_percent[-1:])
        return (1/t_f) * math.log(profit_this_step)


    def get_reward(self, portfolio: 'Portfolio') -> float:
        """Return the reward corresponding to the selected risk-adjusted return metric."""
        #USING SHARPE RATIO
        # returns = portfolio.performance['net_worth'][-(self._window_size + 1):].pct_change().dropna()
        # risk_adjusted_return = self._return_algorithm(returns)



        #Calculate log_cum_returns
        log_returns = self._standard_log_returns(portfolio)

        #Calculate portfolio diversity, which is between 0 and 1.
        #1 means not diversified. small number means very diversified
        weights = portfolio.weights[-1:].values[0]
        diversity = np.dot(weights, weights)

        #Calculate how much the weights have changed
        weights_change_list = (portfolio.weights[-(1):].values[0]) - (portfolio.weights[-(2):].values[0])
        weights_change = sum(weights_change_list)

        #Reward function
        #reward = risk_adjusted_return + (1/diversity)
        #reward = simple_profit + 10*(1/diversity)
        reward = log_returns




        #Reward function
        #reward = risk_adjusted_return + (1/diversity)
        reward = simple_profit + .2*(1/diversity)

        return reward


import operator

from tensortrade.data import Lambda, Module, Select, BinOp
from tensortrade.wallets import Wallet


def create_wallet_source(wallet: Wallet, include_worth=True):
    exchange_name = wallet.exchange.name
    symbol = wallet.instrument.symbol

    with Module(exchange_name + ":/" + symbol) as wallet_ds:
        free_balance = Lambda("free", lambda w: w.balance.size, wallet)
        locked_balance = Lambda("locked", lambda w: w.locked_balance.size, wallet)
        total_balance = Lambda("total", lambda w: w.total_balance.size, wallet)
        is_empty = Lambda("is_empty", lambda w: (1 if w.total_balance.size<10 else 0), wallet)

        nodes = [free_balance, locked_balance, total_balance, is_empty]

        if include_worth:
            price = Select(lambda node: node.name.endswith(symbol))(wallet.exchange)
            worth = BinOp("worth", operator.mul)(price, total_balance)
            nodes += [worth]

    return wallet_ds

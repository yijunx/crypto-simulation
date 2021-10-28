# how to download the csvs
import fastquant as fq

start = "2021-1-1"
end = "2021-10-27"


import pandas as pd
from enum import Enum


COIN_NAMES = [
    # "BTC",
    # "ETH",
    "ADA",
    "1INCH",
    "HNT",
    "AAVE",
    "DOT",
    "DOGE",
]

# for c in COIN_NAMES:

#     df: pd.DataFrame = fq.get_crypto_data(f'{c}/USDT', start, end)
#     df.to_csv(f'{c}.csv')


starting_cash = 1.0
baseline_total = starting_cash
strategy_total = starting_cash
stratege_reset_interval_days = 10


coin_data = [pd.read_csv(f"{c}.csv") for c in COIN_NAMES]
coin_quantities = [0 for c in COIN_NAMES]
initial_coin_quantities = [0 for c in COIN_NAMES]


total_days = len(coin_data[0])
total_type_of_coins = len(coin_data)
i = 0


# CONFIG 2 VALUES BELOW
starting_offset = 200
stratege_reset_interval_days = 10


class ColEnum(int, Enum):
    close = 4
    open = 1
    high = 2
    low = 3


while i + starting_offset < total_days:
    if i % stratege_reset_interval_days == 0:
        if i > 0:
            # selling at close price
            strategy_total = sum(
                [
                    n * price
                    for n, price in zip(
                        coin_quantities,
                        [x.iloc[i + starting_offset, ColEnum.close] for x in coin_data],
                    )
                ]
            )
            baseline_total = sum(
                [
                    n * price
                    for n, price in zip(
                        initial_coin_quantities,
                        [x.iloc[i + starting_offset, ColEnum.close] for x in coin_data],
                    )
                ]
            )
            print(
                f"After {i} days, with strategy: {strategy_total}, baseline: {baseline_total}"
            )
        # buying at open
        coin_quantities = [
            strategy_total / total_type_of_coins / closing_price
            for closing_price in [
                x.iloc[i + starting_offset, ColEnum.close] for x in coin_data
            ]
        ]
        if i == 0:
            initial_coin_quantities = [x for x in coin_quantities]

    if i + starting_offset == total_days - 1:
        strategy_total = sum(
            [
                n * price
                for n, price in zip(
                    coin_quantities,
                    [x.iloc[i + starting_offset, ColEnum.close] for x in coin_data],
                )
            ]
        )
        baseline_total = sum(
            [
                n * price
                for n, price in zip(
                    initial_coin_quantities,
                    [x.iloc[i + starting_offset, ColEnum.close] for x in coin_data],
                )
            ]
        )

        print(
            f"FINALLY!!! After {i} days, with strategy: {strategy_total}, baseline: {baseline_total}"
        )

    i += 1

for coin_name, a_coin_data in zip(COIN_NAMES, coin_data):
    print(coin_name)
    start = a_coin_data.iloc[0 + starting_offset, ColEnum.close]
    end = a_coin_data.iloc[-1, ColEnum.close]
    ratio = end / start
    print(f"starting at {start}, ending at {end}, with ratio {ratio}")
    a_coin_data.iloc[:, ColEnum.close].plot()

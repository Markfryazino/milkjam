from collections import defaultdict


class StupidEmulator:
    fee = 0.001
    pairs = ['btcusdt']

    @staticmethod
    def count_usdt(balances, rates):
        res = 0
        for key, val in balances.items():
            if key == 'usdt':
                res += val
            else:
                res += val * rates[key + 'usdt']
        return res

    @staticmethod
    def make_order(balances, query, rates):
        delta = defaultdict(float)
        for key, val in query.items():
            delta[key[:3]] += val
            delta[key[3:]] -= val * rates[key] * (1. + StupidEmulator.fee)

        for key, val in delta.items():
            if key not in balances:
                balances[key] = 0.
            balances[key] += val

        print(query, delta)

        return delta, balances

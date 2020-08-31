from collections import defaultdict


class StupidEmulator:
    fee = 0.001

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
    def make_order(self, balances, query, rates):
        delta = defaultdict(float)
        for key, val in query.items():
            mod = int(val > 0)
            delta[key[:3]] += val * mod
            delta[key[3:]] -= val * rates[key] * (1. + StupidEmulator.fee) * mod

        for key, val in delta.items():
            balances[key] += val
        return delta, balances

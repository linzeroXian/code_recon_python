class PerformanceCalculator:
    def __init__(self, a_performance, a_play):
        self.performance = a_performance
        self.play = a_play
        self.amount = self.get_amount()
        self.volume_credits = self.get_volume_credits()

    def get_amount(self):
        result = 0
        play = self.play
        if play['type'] == "tragedy":
            result = 40000
            if self.performance['audience'] > 30:
                result += 1000 * (self.performance['audience'] - 30)
        elif play['type'] == "comedy":
            result = 30000
            if self.performance['audience'] > 20:
                result += 10000 + 500 * (self.performance['audience'] - 20)
            result += 300 * self.performance['audience']
        else:
            raise ValueError(f"unknown type: {play['type']}")
        return result

    def get_volume_credits(self):
        result = 0
        result += max(self.performance['audience'] - 30, 0)
        if self.play['type'] == "comedy":
            result += self.performance['audience'] // 5
        return result


def creat_statement_data(invoice, plays):
    def enrich_performance(a_performance):
        calculator = PerformanceCalculator(a_performance, play_for(a_performance))
        res = a_performance.copy()
        res['play'] = calculator.play
        res['amount'] = calculator.amount
        res['volume_credits'] = calculator.volume_credits
        return res

    def play_for(a_performance):
        return plays[a_performance['playID']]

    def amount_for(a_performance):
        return PerformanceCalculator(a_performance, play_for(a_performance)).amount

    def volume_credits_for(a_performance):
        return PerformanceCalculator(a_performance, play_for(a_performance)).volume_credits

    def total_volume_credits(statement_data):
        return sum(perf['volume_credits'] for perf in statement_data['performances'])

    def total_amount(statement_data):
        return sum(perf['amount'] for perf in statement_data['performances'])

    res = {}
    res['customer'] = invoice['customer']
    res['performances'] = [enrich_performance(perf) for perf in invoice['performances']]
    res['total_amount'] = total_amount(res)
    res['total_volume_credits'] = total_volume_credits(res)
    return res

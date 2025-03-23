def creat_statement_data(invoice, plays):
    def enrich_performance(a_performance):
        calculator = createPerformanceCalculator(a_performance, play_for(a_performance))
        res = a_performance.copy()
        res['play'] = calculator.play
        res['amount'] = calculator.amount
        res['volume_credits'] = calculator.volume_credits
        return res

    def play_for(a_performance):
        return plays[a_performance['playID']]

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


def createPerformanceCalculator(a_performance, a_play):
    if a_play['type'] == "tragedy":
        return TragedyCalculator(a_performance, a_play)
    elif a_play['type'] == "comedy":
        return ComedyCalculator(a_performance, a_play)
    else:
        raise ValueError(f"unknown type: {a_play['type']}")


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
            raise ValueError(f"bad thing")
        elif play['type'] == "comedy":
            raise ValueError(f"bad thing")
        else:
            raise ValueError(f"unknown type: {play['type']}")
        return result

    def get_volume_credits(self):
        return max(self.performance['audience'] - 30, 0)


class TragedyCalculator(PerformanceCalculator):
    def __init__(self, a_performance, a_play):
        super().__init__(a_performance, a_play)

    def get_amount(self):
        result = 40000
        if self.performance['audience'] > 30:
            result += 1000 * (self.performance['audience'] - 30)
        return result


class ComedyCalculator(PerformanceCalculator):
    def __init__(self, a_performance, a_play):
        super().__init__(a_performance, a_play)

    def get_amount(self):
        result = 30000
        if self.performance['audience'] > 20:
            result += 10000 + 500 * (self.performance['audience'] - 20)
        result += 300 * self.performance['audience']
        return result

    def get_volume_credits(self):
        # 调用父类的原始计算逻辑
        base_credits = super().get_volume_credits()
        print('base_credits:', base_credits)
        # 叠加子类的新逻辑（如观众数除以5）
        return base_credits + self.performance["audience"] // 5

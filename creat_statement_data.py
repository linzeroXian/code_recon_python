def creat_statement_data(invoice, plays):
    def enrich_performance(a_performance):
        res = a_performance.copy()
        res['play'] = play_for(res)
        res['amount'] = amount_for(res)
        res['volume_credits'] = volume_credits_for(res)
        return res

    def play_for(a_performance):
        return plays[a_performance['playID']]

    def amount_for(a_performance):
        result = 0
        play = a_performance['play']
        if play['type'] == "tragedy":
            result = 40000
            if a_performance['audience'] > 30:
                result += 1000 * (a_performance['audience'] - 30)
        elif play['type'] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance['audience'] - 20)
            result += 300 * a_performance['audience']
        else:
            raise ValueError(f"unknown type: {play['type']}")
        return result

    def volume_credits_for(a_performance):
        result = 0
        result += max(a_performance['audience'] - 30, 0)
        # if play_for(a_performance)['type'] == "comedy":
        if a_performance['play']['type'] == "comedy":
            result += a_performance['audience'] // 5
        return result

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

def statement(invoice, plays):
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
        # play = play_for(a_performance)
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
        result = 0
        for perf in statement_data['performances']:
            result += perf['volume_credits']
        return result

    def total_amount(statement_data):
        result = 0
        for perf in statement_data['performances']:
            result += perf['amount']
        return result

    statement_data = {}
    statement_data['customer'] = invoice['customer']
    # statement_data['performances'] = invoice['performances']
    statement_data['performances'] = [enrich_performance(perf) for perf in invoice['performances']]
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(statement_data)

    return renderPlainText(statement_data)


def renderPlainText(statement_data):
    def usd(a_number):
        return "${:,.2f}".format(a_number / 100)

    result = f"Statement for {statement_data['customer']}\n"
    for perf in statement_data['performances']:
        result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
    result += f"Amount owed is {usd(statement_data['total_amount'])}\n"
    result += f"You earned {statement_data['total_volume_credits']} credits\n"

    return result


if __name__ == '__main__':
    import json

    # 打开并读取 JSON 文件
    with open("invoice.json", "r", encoding="utf-8") as file:
        invoice = json.load(file)[0]

    with open("play.json", "r", encoding="utf-8") as file:
        plays = json.load(file)

    print(statement(invoice, plays))

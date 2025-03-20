def statement(invoice, plays):
    return renderPlainText(invoice, plays)


def renderPlainText(invoice, plays):
    def total_amount():
        result = 0
        for perf in invoice['performances']:
            result += amount_for(perf)
        return result

    def total_volume_credits():
        result = 0
        for perf in invoice['performances']:
            result += volume_credits_for(perf)
        return result

    def usd(a_number):
        return "${:,.2f}".format(a_number / 100)

    def volume_credits_for(a_performance):
        result = 0
        result += max(a_performance['audience'] - 30, 0)
        if play_for(a_performance)['type'] == "comedy":
            result += a_performance['audience'] // 5
        return result

    def play_for(a_performance):
        return plays[a_performance['playID']]

    def amount_for(a_performance):
        result = 0
        play = play_for(a_performance)
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

    result = f"Statement for {invoice['customer']}\n"
    for perf in invoice['performances']:
        result += f" {play_for(perf)['name']}: {usd(amount_for(perf))} ({perf['audience']} seats)\n"
    result += f"Amount owed is {usd(total_amount())}\n"
    result += f"You earned {total_volume_credits()} credits\n"

    return result


if __name__ == '__main__':
    import json

    # 打开并读取 JSON 文件
    with open("invoice.json", "r", encoding="utf-8") as file:
        invoice = json.load(file)[0]

    with open("play.json", "r", encoding="utf-8") as file:
        plays = json.load(file)

    print(statement(invoice, plays))

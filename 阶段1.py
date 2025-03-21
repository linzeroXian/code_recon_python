from creat_statement_data import creat_statement_data


def statement(invoice, plays):
    return renderPlainText(creat_statement_data(invoice, plays))


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

from creat_statement_data import creat_statement_data


def statement(invoice, plays):
    return renderPlainText(creat_statement_data(invoice, plays))


def usd(a_number):
    return "${:,.2f}".format(a_number / 100)


def renderPlainText(data):
    result = f"Statement for {data['customer']}\n"
    for perf in data['performances']:
        result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
    result += f"Amount owed is {usd(data['total_amount'])}\n"
    result += f"You earned {data['total_volume_credits']} credits\n"

    return result


def html_statement(invoice, plays):
    return render_html(creat_statement_data(invoice, plays))


def render_html(data):
    result = f"<h1>Statement for {data['customer']}</h1>\n"
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>\n"
    for perf in data['performances']:
        result += f" <tr><td>{perf['play']['name']}</td><td>{perf['audience']}</td>"
        result += f"<td>{usd(perf['amount'])}</td></tr>\n"
    result += "</table>\n"
    result += f"<p>Amount owed is <em>{usd(data['total_amount'])}</em></p>\n"
    result += f"<p>You earned <em>{data['total_volume_credits']}</em> credits</p>\n"
    return result


def preview_html(html_content):
    import webbrowser
    # 将 HTML 内容保存到一个临时文件
    with open("temp.html", "w") as file:
        file.write(html_content)

    # 使用默认浏览器打开该文件
    webbrowser.open("temp.html")


if __name__ == '__main__':
    import json

    # 打开并读取 JSON 文件
    with open("invoice.json", "r", encoding="utf-8") as file:
        invoice = json.load(file)[0]

    with open("play.json", "r", encoding="utf-8") as file:
        plays = json.load(file)

    print(statement(invoice, plays))

    print(html_statement(invoice, plays))

    preview_html(html_statement(invoice, plays))

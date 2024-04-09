import re
import requests
import json
import os
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import quote

import csv


def read():
    with open("links.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            yield row[0], row[1]


def write(content):
    # write

    with open('links.csv', 'a', newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(content)


def clear():

    with open('links.csv', 'a', newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows([])


html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h1>{title}</h1>
<p>{text}</p>
</body>
</html>
"""
# htmls = []
# num = 0
def get_data(url, start_url, htmls = [], num = 0):

    # global htmls, num
        
    headers = {
        'Authorization': '59E0B1B8-C959-9581-1BC8-6EC37B04F9C3_7792978491928BD3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }
    
    rsp = requests.get(url, headers=headers)
    with open('test.json', 'w', encoding='utf-8') as f:        # 将返回数据写入 test.json 方便查看
        f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))
    
    with open('test.json', encoding='utf-8') as f:
        if (temp := json.loads(f.read()).get('resp_data').get('topics')) != None:

            for topic in temp:
                content = topic.get('question', topic.get('talk', topic.get('task', topic.get('solution'))))
                # print(content)
                text = content.get('text', '')
                text = re.sub(r'<[^>]*>', '', text).strip()
                try:
                    enter_place = text.index('\n')
                    # print("换行符位置：", enter_place)
                except ValueError:
                    # print("未找到换行符")
                    enter_place = 100000
                text = text.replace('\n', '<br>')
                tmp = 0
                for i in range(len(text)):
                    if tmp > 100 or tmp > enter_place + 3:
                        break
                    if text[i] in ['\n', '\r', '\r\n', '\u2028', '\u2029', '\u0085', '。', ';', '；', '?', '？', '！', '!']:
                        break
                    # if is_chinese_punctuation(text[i]):
                    #     break

                    tmp += 1
                title = str(num + 1) + '. ' + text[:tmp]
                num += 1

                if content.get('images'):
                    soup = BeautifulSoup(html_template, 'html.parser')
                    for img in content.get('images'):
                        url = img.get('large').get('url')
                        img_tag = soup.new_tag('img', src=url)
                        soup.body.append(img_tag)
                        html_img = str(soup)
                        html = html_img.format(title=title, text=text)
                else:
                    html = html_template.format(title=title, text=text)

                if topic.get('question'):
                    answer = topic.get('answer').get('text', "")
                    soup = BeautifulSoup(html, 'html.parser')
                    answer_tag = soup.new_tag('p')
                    answer_tag.string = answer
                    soup.body.append(answer_tag)
                    html_answer = str(soup)
                    html = html_answer.format(title=title, text=text)

                htmls.append(html)

    next_page = rsp.json().get('resp_data').get('topics')
    if next_page:
        create_time = next_page[-1].get('create_time')
        if create_time[20:23] == "000":
            end_time = create_time[:20]+"999"+create_time[23:]
        else :
            res = int(create_time[20:23])-1
            end_time = create_time[:20]+str(res).zfill(3)+create_time[23:] # zfill 函数补足结果前面的零，始终为3位数
        end_time = quote(end_time)
        if len(end_time) == 33:
            end_time = end_time[:24] + '0' + end_time[24:]
        next_url = start_url + '&end_time=' + end_time
        print(next_url)
        get_data(next_url, start_url, htmls, num)

    return htmls

def make_pdf(htmls, title):
    html_files = []
    for index, html in enumerate(htmls):
        file = str(index) + ".html"
        html_files.append(file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(html)

    options = {
        "user-style-sheet": "test.css",
        "page-size": "Letter",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "cookie": [
            ("cookie-name1", "cookie-value1"), ("cookie-name2", "cookie-value2")
        ],
        "outline-depth": 10,
    }
    try:
        pdfkit.from_file(html_files, f"{title}.pdf", options=options)
    except Exception as e:
        pass

    for file in html_files:
        os.remove(file)

    print("已制作电子书在当前目录！")




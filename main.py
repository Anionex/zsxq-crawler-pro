import crawl

if __name__ == '__main__':
    now = 0
    # 初始化一个空列表来存储标题
    titles = []
    # 打开文件并读取每一行，确保使用正确的编码
    with open('titles.txt', 'r', encoding='utf-8') as file:
        for title in file:
            # 移除每行末尾的换行符，并将结果添加到列表中
            titles.append(title.strip())

    # 现在 titles 列表包含了所有的标题
    print(titles)  # 打印列表，确认内容

    with open('urls.txt', 'r') as file:
        for line_number, start_url in enumerate(file, start=1):
            # 每行的末尾通常会有一个换行符，我们可以使用 strip() 来移除它
            start_url = start_url.strip()
            if start_url == "":
                print("End.")
                break

            tmp = crawl.get_data(start_url, start_url, [] ,0)
            while not tmp:
                tmp = crawl.get_data(start_url, start_url, [], 0)

            print(tmp)
            crawl.make_pdf(tmp, titles[now])
            now += 1
    # start_url = 'https://api.zsxq.com/v2/groups/48884882458148/topics?scope=all&count=20'
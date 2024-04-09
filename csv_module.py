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


def get_links():
    pass


if __name__ == "__main__":
    get_links()
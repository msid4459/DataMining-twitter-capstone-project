from newspaper import Article
import csv,codecs
import sys
import os
import requests

# Get the real url of the website
def get_page_url(url):
    try:
        response = requests.get(url)
        return response.url
    except:
        return None

# Read articles from tweets.csv file
def read_articles():
    path = "articles.csv"
    csv_file = open(path, encoding='utf-8')
    csv_reader = csv.reader(csv_file)
    articles = []
    for item in csv_reader:
        if csv_reader.line_num == 1:
            continue
        articles.append(item)
    csv_file.close()

    return articles

def main():
    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    create_file("news.csv")
    create_file("papers.csv")
    create_file("others.csv")
    articles = read_articles()
    x = 0
    for item in articles:
        x = x + 1
        # if x < 30050:
        #     continue
        if x % 50 == 0:
            print(str(x) + ": " + item[2])
        real_url = get_page_url(item[2])
        if real_url:
            a = Article(real_url)
            if a.is_valid_url():
                write_csv("news.csv", item)
            elif item[1].lower().find("introduction") is not -1 and item[1].lower().find("result") is not -1:
                write_csv("papers.csv", item)
            else:
                write_csv("others.csv", item)

# Create a new .csv file if it doesn't exist
def create_file(path):
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:  # newline='' is used to delete the blank line after the header
            csv_write = csv.writer(f)
            csv_head = ["title", "content", "hyperlink"]
            csv_write.writerow(csv_head)

# Write the content into .csv file
def write_csv(path, item):
    title = item[0]
    content = item[1]
    hyperlink = item[2]
    f = codecs.open(path, 'a+', 'utf-8')
    writer = csv.writer(f)
    data_row = [title, content, hyperlink]
    writer.writerow(data_row)
    f.close()

main()
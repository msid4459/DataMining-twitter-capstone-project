import requests
import re
import os
import time
from readability.readability import Document
import csv,codecs
import chardet
import os


# Write the article detail into the .csv file
def write_csv(title, content, hyperlink, writer):
    title = chinese_trans_to_english(title)
    content = chinese_trans_to_english(content)
    data_row = [title, content, hyperlink]
    writer.writerow(data_row)

# Read tweets from tweets.csv file
def read_tweets():
    path = "diabetes.csv"
    csv_file = open(path, encoding='utf-8')
    csv_reader = csv.reader(csv_file)
    hyperlinks = []

    for item in csv_reader:
        if csv_reader.line_num == 1:
            continue
        if item[2] is not '':
            urls = item[2].split(",")
            for url in urls:
                if url is not '':
                    hyperlinks.append(url)
    csv_file.close()
    hyperlinks = list(set(hyperlinks))
    return hyperlinks

# Get the response from the url, and encode the content with the same encoding as the original web page
def get_one_page(url):
    try:
        headers = {
            'Connection': 'close',
        }
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(e)
        return None

def main():
    # Create a new .csv file if it doesn't exist
    path = "articles.csv"
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:     # newline='' is used to delete the blank line after the header
            csv_write = csv.writer(f)
            csv_head = ["title", "content", "hyperlink"]
            csv_write.writerow(csv_head)

    path = "articles.csv"
    f = codecs.open(path, 'a+', 'utf-8')
    writer = csv.writer(f)

    hyperlinks = read_tweets()
    x = 0
    print(len(hyperlinks))
    for url in hyperlinks:
        x = x + 1
        # if x < 30050:
        #     continue
        if x % 50 == 0:
            print(str(x) + ": " + url)
        # time.sleep(1)
        if url is not '':
            html = get_one_page(url)    # html is the source code of the website
            if html and html.strip() is not "":
                title, content = get_main_content(html)
                title = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub('', title)
                content = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub('', content)
                if "Welcome home!" not in content and "to open this menu" not in content :
                    content = preprocessing_article(content).strip()
                    if len(content) > 2000 and title is not "":     # Delete the non-article content
                        write_csv(title, content, url, writer)
    f.close()

# Get the main content from a html format text
def get_main_content(html):
    readable_title = Document(html).short_title()
    readable_article = Document(html).summary()
    text_p = re.sub(r'</?div.*?>', '', readable_article)
    text_p = re.sub(r'((</p>)?<a href=.*?>|</a>(<p>)?)', '', text_p)
    text_p = re.sub(r'<select>.*?</select>', '', text_p)

    return readable_title, text_p;

# Do all preprocessing operations
def preprocessing_article(article):
    pure_text = re.sub(r'</?\w+[^>]*>','',article)
    pure_text = pure_text.replace("\n","")
    pure_text = pure_text.replace("&#13;", "")
    return pure_text

# Translate the non-English punctuations to English punctuations
def chinese_trans_to_english(string):
    E_pun = u',.!?[]()<>"\'\'"'
    C_pun = u'，。！？【】（）《》“‘’”'
    table= {ord(f):ord(t) for f,t in zip(C_pun,E_pun)}
    return string.translate(table)

main()
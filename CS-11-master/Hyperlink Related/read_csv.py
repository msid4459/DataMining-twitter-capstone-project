import csv
import sys
def read_csv():
    path = "articles.csv"
    csv_file = open(path, encoding='utf-8')
    csv.field_size_limit(500 * 1024 * 1024)
    csv_reader = csv.reader(csv_file)
    contents = []
    for item in csv_reader:
        if csv_reader.line_num == 1:
            continue
        contents.append(item[1])
    csv_file.close()

    return contents

def main():
    contents = read_csv()
    for content in contents:
        print(content)

main()
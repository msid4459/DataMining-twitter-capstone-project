import csv,codecs
import os
import nltk
nltk.download('punkt')
import sys

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

    # Read articles by type
    file_name = "news"
    input_path = file_name + ".csv"
    csv_file = open(input_path, encoding='utf-8')
    csv_reader = csv.reader(csv_file)
    articles = []
    for item in csv_reader:
        if csv_reader.line_num == 1:
            continue
        articles.append(item)
    csv_file.close()

    # Create the file
    output_path = "processed_" + file_name +".csv"
    if not os.path.exists(output_path):
        with open(output_path, 'w', newline='') as f:  # newline='' is used to delete the blank line after the header
            csv_write = csv.writer(f)
            csv_head = ["title", "content", "hyperlink", "type"]
            csv_write.writerow(csv_head)

    # Write information into the file
    f = codecs.open(output_path, 'a+', 'utf-8')
    writer = csv.writer(f)
    for item in articles:
        item[1] = item[1].replace("\t","").strip()
        item[1] = ' '.join(item[1].split())
        item[1] = item[1].replace("â€œ", "“")
        item[1] = item[1].replace('â€', '”')
        item[1] = item[1].replace('â€™', '’')
        item[1] = item[1].replace('â€˜', '‘')
        item[1] = item[1].replace('â€”', '–')
        item[1] = item[1].replace('â€“', '—')
        item[1] = item[1].replace('â€¢', '-')
        item[1] = item[1].replace('â€¦', '…')
        item[1] = item[1].replace('â€�', '')

        item[1] = chinese_trans_to_english(item[1])
        data_row = [item[0], item[1], item[2], file_name]
        writer.writerow(data_row)
    print(articles[6])
    f.close()

# Translate the non-English punctuations to English punctuations
def chinese_trans_to_english(string):
    E_pun = u',.!?[]()<>"\'\'"'
    C_pun = u'，。！？【】（）《》“‘’”'
    table= {ord(f):ord(t) for f,t in zip(C_pun,E_pun)}
    return string.translate(table)
main()
import csv,codecs
import os
import warnings
import nltk
nltk.download('punkt')
import sys
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

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


    # Read drug_list.csv file
    input_path = "drug_list.csv"
    csv_file = open(input_path, encoding='utf-8')
    csv_reader = csv.reader(csv_file)
    keywords = []
    for item in csv_reader:
        if csv_reader.line_num == 1:
            continue
        keywords.append(item[1])
    csv_file.close()

    # Read news.csv file
    file_name = "others"
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
    output_path = "keywordsResult.csv"
    if not os.path.exists(output_path):
        with open(output_path, 'w', newline='') as f:  # newline='' is used to delete the blank line after the header
            csv_write = csv.writer(f)
            csv_head = ["sentence", "type"]
            csv_write.writerow(csv_head)

    # Write information into the file
    key_sentences = []

    for item in articles:
        item[1] = item[1].replace(".", ". ")
        sentences = nltk.sent_tokenize(item[1])
        for sentence in sentences:
            for keyword in keywords:
                if keyword.lower() in sentence.lower():
                    key_sentences.append(sentence)

    key_sentences = list(set(key_sentences))
    key_sentences.sort()

    for key_sentence in key_sentences:
        f = codecs.open(output_path, 'a+', 'utf-8')
        writer = csv.writer(f)
        data_row = [key_sentence, file_name]
        writer.writerow(data_row)
        f.close()

main()
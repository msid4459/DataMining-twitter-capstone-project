import csv,codecs
import os
import sys
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.summarization.summarizer import summarize


class ArticleSummarizer():
    _file_name = ""

    def __init__(self, file_name):
        self._file_name = file_name

    def write_summary(self):
        input_path = self._file_name + ".csv"
        csv_file = open(input_path, encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        articles = []
        for item in csv_reader:
            if csv_reader.line_num == 1:
                continue
            articles.append(item)
        csv_file.close()

        # Create the file
        output_path = self._file_name + "_summary.csv"
        if not os.path.exists(output_path):
            with open(output_path, 'w', newline='') as f:  # newline='' is used to delete the blank line after the header
                csv_write = csv.writer(f)
                csv_head = ["title", "summary", "hyperlink"]
                csv_write.writerow(csv_head)

        # Write information into the file
        for item in articles:
            item[1] = item[1].replace(".", ". ")
            title = item[0]
            try:
                summary = summarize(item[1])
            except:
                continue
            hyperlink = item[2]
            f = codecs.open(output_path, 'a+', 'utf-8')
            writer = csv.writer(f)
            data_row = [title, summary, hyperlink]
            writer.writerow(data_row)
            f.close()

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

    summarizer = ArticleSummarizer("papers")
    summarizer.write_summary()

main()
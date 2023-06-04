# -*- coding: utf-8 -*-
"""
Module to extract data from Google Scholar pages
"""
import codecs
import requests
from bs4 import BeautifulSoup
def main():
    """
    Main function to extract data from a list of Google Scholar pages
    """
    with codecs.open('GSCHOLARlist.tsv', 'r', 'utf-8-sig') as scholar_file:
        link_list = scholar_file.readlines()  # generates a list in RAM with links
    scholar_file.close()
    with codecs.open('GSCHOLARresults.tsv', 'w', 'utf-8-sig') as results_file:
        results_file.write('Name\tCitations\tCitations Since 2013\tH-index\tH-index Since 2013\n')  # headers for tsv
        print('Begin of extraction,', len(link_list) - 1, 'items to go')
        counter = 0  # counter to keep track of scraping progress
        h_index_accumulator = 0
        total_citations = 0
        for link in link_list[1:]:
            link = link.split('\t')  # link <- list separating line from file read by tabs
            if '\r\n' in link[0]:  # tests if line endings use \r\n or just \n
                link[0] = link[0].replace('\r\n', '\t')  # replaces \n with \t to facilitate writing
            else:
                link[0] = link[0].replace('\n', '\t')
            print(counter, ': Extracting: %s' % link[0])
            counter += 1  # current line indicated by the counter
            html = requests.get(link[1], timeout=10).content  # html <- html of the current page being checked
            soup = BeautifulSoup(html, "lxml")  # parsing of the read html
            data_list = soup.findAll('td', {'class': 'gsc_rsb_std'})  # finds target occurrences on the page


            if len(data_list) > 0:
                citations = data_list[0].getText()
            else:
                citations = "N/A"
            if len(data_list) > 2:
                h_index = data_list[2].getText()
            else:
                h_index = "N/A"
            if citations.isdigit():
                total_citations += int(citations)
            else:
                print("Invalid citation count:", citations)

            if h_index.replace('.', '', 1).isdigit():
                h_index_accumulator += float(h_index)
            else:
                print("Invalid h-index value:", h_index)

            results_file.write('%s\t%s\t%s\t%s\t%s\n' % (link, citations, data_list, h_index, ""))
            # writes line to output file
    results_file.close()  # close output file
    print('Average H-Index:', h_index_accumulator / counter)
    print('Total Citations:', total_citations)
if __name__ == '__main__':
    main()

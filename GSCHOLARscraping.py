import requests
from bs4 import BeautifulSoup
import codecs

with codecs.open('GSCHOLARlist.tsv', 'r', 'utf-8-sig') as scholar:
    link_list = scholar.readlines()[1:]  # skip header

with codecs.open('GSCHOLARresults.tsv', 'w', 'utf-8-sig') as results:
    results.write('Link\tCitations 2018\tH-index 2018\tCitations Total\tH-index Total\n')  # headers of the tsv file

    for i, link in enumerate(link_list):
        link = link.strip()  # remove leading/trailing whitespaces
        print(f'{i}: Extracting: {link}')

        response = requests.get(link, timeout=10)
        if response.ok:
            parsed_html = BeautifulSoup(response.content, "lxml")
            data_list = parsed_html.findAll('td', {'class': 'gsc_rsb_std1'})
            citations_2018, h_index_2018, citations_total, h_index_total = [int(data_list[i].getText()) for i in [0, 1, 2, 3]]
            results.write(f"{link}\t{citations_2018}\t{h_index_2018}\t{citations_total}\t{h_index_total}\n")
            print(data_list)

print('Extraction completed')

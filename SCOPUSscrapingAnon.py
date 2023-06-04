# -*- coding: utf-8 -*-
"""
Module to extract data from Scopus pages
"""
import codecs
import os
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
chromedriver = "chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
with codecs.open('SCOPUSlist.tsv', 'r', 'utf-8-sig') as scholar:
    link_list = scholar.readlines()
with codecs.open('SCOPUSresults.tsv', 'w', 'utf-8-sig') as results:
    results.write('ScopusID\tH-Index\tDocuments by author\tCited by\n')
    print('Begin of extraction,', len(link_list) - 1, 'items to go')
    counter = 0
    h_index_accumulator = 0
    docs_accumulator = 0
    citations_accumulator = 0
    driver = webdriver.Chrome(chromedriver)
    for link in link_list[1:]:
        link = link.split('\t')
        link[0] = link[0].rstrip()
        print(counter, ': Extracting: %s' % link[0])
        counter += 1
        driver.get(link[1])
        soup = BeautifulSoup(driver.page_source, "lxml")
        h_index = soup.find('section', id='authorDetailsHindex')
        h_index = h_index.find('span', {'class': 'fontLarge'}).getText() if h_index else 'N/A'
        docs = soup.find('section', id='authorDetailsDocumentsByAuthor')
        docs = docs.find('span', {'class': 'fontLarge'}).getText() if docs else 'N/A'
        citations = soup.find('section', id='authorDetailsTotalCitations')
        citations = citations.find('span', {'class': 'btnText'}).getText() if citations else 'N/A'
        if h_index != 'N/A':
            h_index_accumulator += float(h_index)
        if docs != 'N/A':
            docs_accumulator += int(docs)
        if citations != 'N/A':
            citations_accumulator += int(citations)
        writing_tuple = [h_index, docs, citations]
        results.write('%s\t%s\t%s\t%s\n' % ((link[1].split('=')[-1]).rstrip(), writing_tuple[0], writing_tuple[1], writing_tuple[2]))
    driver.quit()

# coding: utf-8
"""
Created on Aug 27 2018

"""

import codecs
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os


def get_metrics_info(a_soup):
    metrics = []
    for item in a_soup.findAll('div', {'class': 'stats-item'}):
        metrics += item.find('div', {'class': 'stat-data'}).find('p')
    metrics[:2] = [i.replace('.', '') for i in metrics[:2]]
    del(metrics[3])
    return metrics
# function que extrai dados alvo da pagina


# geckodriver = "../scripts/geckodriver"    # path do geckodriver para firefox
chromedriver = "chromedriver"    # path do chromedriver
os.environ["webdriver.chrome.driver"] = chromedriver

with codecs.open('Publonslist.tsv', 'r', 'utf-8-sig') as research:      # abre arquivo
    link_list = research.readlines()    # extrai linhas do arquivo em uma lista
research.close()                        # fecha arquivo

with open('PublonsAnonScraping.txt', 'w') as log:
    with codecs.open('PublonsResults.tsv', 'w', 'utf-8-sig') as results:    # abre arquivo de output
        results.write('ResearcherID\tTotal in Pub. List\tWith Citation Data\tSum of Times Cited\t'
                      'Average Citations/Article\tH-index\tVerified Reviews\n')   # escreve headers
        print ('Begin of extraction,', len(link_list) - 1, 'items to go')
        citation_acumulator = 0
        h_index_acumulator = 0
        existent_h_index_counter = 0
        article_acumulator = 0
        total_reviews = 0
        counter = 1  # counter para acompanhar progresso
        driver = webdriver.Chrome(chromedriver)
        # driver = webdriver.Firefox()
        for link in link_list[1:]:  # for para percorrer a lista de links
            link = link.split('\t')  # extrai link de cada item da lista
            if '\r\n' in link[1]:  # testa finais de linha para verificar se usam \n ou \r\n
                link[1] = link[1].replace('\r\n', '\t')  # troca final por \t
            else:
                link[1] = link[1].replace('\n', '\t')
            print (counter, ': Extracting: %s' % link[1])
            counter += 1  # incrementa counter para acompanhar progresso
            driver.get(link[0])  # acessa link alvo
            try:
                elements = driver.find_elements(By.XPATH, '//*[@id="researcher-profile-page-content"]/div/nav/ol/li[2]/a/span')
                # clica no button para mostrar citation metrics
            except IndexError:
                print ('%s apparently got no citation metrics' % link[1])  # exception caso button esteja ausente
                continue
            try:
                WebDriverWait(driver, 10).until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="researcher-profile-page-content"]/div/div[2]/div/div[2]/div/div[3]/div[1]/div'
                               '/div[2]/p')))
                while True:
                    root = BeautifulSoup(driver.page_source, 'lxml')  # parsing inicial
                    data = get_metrics_info(root.find('div', {'class': 'researcher-profile-details'}).find
                                            ('div', {'class': 'individual-stats'}).find
                                            ('div', {'class': 'stats-container'}))
                    if '-' not in data:
                        break
                if data != '' and data != '-':
                    reviews = root.findAll('h5')[-1]
                    if reviews.getText() != 'Verified reviews':
                        reviews = 'NA'
                    else:
                        reviews = reviews.findNext('p').getText()
                        total_reviews += int(reviews)
                    results.write(link[0].split('/')[-1] + '\t' + '%s\t%s\t%s\t%s\t%s\t%s\n' %
                                  (data[0], data[1], data[2], data[3], data[4], reviews))
                    article_acumulator += int(data[0])
                    if data[2] > 0:
                        citation_acumulator += int(data[1])
                        h_index_acumulator += float(data[2])
                        existent_h_index_counter += 1
                else:
                    results.write(link[0].split('/')[-1] + '\t' + 'NA\tNA\tNA\tNA\tNA\tNA\n')
                # aguarda carregamento da pagina para escrever no arquivo de output
            except selenium.common.exceptions.TimeoutException:
                results.write(link[0].split('/')[-1] + '\t' + 'NA\tNA\tNA\tNA\tNA\tNA\n')
    try:
        log.write('Average H-Index: %s\n' % str(h_index_acumulator/existent_h_index_counter))
    except ZeroDivisionError:
        print ('No one in this list had a H-index')
    log.write('Total sum of citations: %s\n' % str(citation_acumulator))
    log.write('Total articles: %s\n' % str(article_acumulator))
    log.write('Total reviews: %s\n' % str(total_reviews))
results.close()
log.close()
driver.quit()       # fecha chrome

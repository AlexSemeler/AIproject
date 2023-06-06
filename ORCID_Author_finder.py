
import os
from codecs import open
from bs4 import BeautifulSoup
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
def get_orcids():
    """
    This function searches for ORCIDs of authors in a given directory of TSV files and writes the results to new TSV files.
    """
    path = os.getcwd()  # get current working directory
    counter = 1
    driver = webdriver.Chrome()  # initialize Chrome driver
    for file in [f for f in os.listdir(path) if f.startswith('Aut') and f.endswith('tsv')]:
        # loop through TSV files in directory
        with open(file, 'r', 'utf-8-sig') as temp:
            # open file for reading
            text = temp.readlines()[1:]
            names = {x.split('\t')[1]: [] for x in text}
            titles = [y.split('\t')[0].replace('\n', '') for y in text]
        for author in names:
            query = author.replace(' ', '%20')
            driver.get('https://orcid.org/orcid-search/search?searchQuery=%s' % query)
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'tbody')))
            root = BeautifulSoup(driver.page_source, 'lxml').find_all('tr', {'class': 'ng-star-inserted'})
            for j in root:
                comp = unidecode(author.lower())
                data = [unidecode(y.getText().lower()) for y in j.find_all('td')[:3]]
                if data[1] in comp and data[2] in comp:
                    names[author].append(data[0].replace('\n', '').replace(' ', ''))
                else:
                    break
        with open('orcids-%s.tsv' % counter, 'w', 'utf-8-sig') as results:
            # open file for writing
            results.write('Autor\tTítulo\tORCIDs encontrados\n')
            for person, title, orcids in zip(names.keys(), titles, names.values()):
                results.write('%s\t%s\t' % (person, title))
                if len(orcids) == 0:
                    results.write('ORCID não encontrado\n')
                else:
                    if len(orcids) > 1:
                        for item in orcids[:-1]:
                            results.write('%s, ' % item)
                    results.write('%s\n' % orcids[-1])
        counter += 1
    driver.quit()  # close Chrome driver
if __name__ == "__main__":
    get_orcids(

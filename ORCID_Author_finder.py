import codecs
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Read list of names from TSV file
with codecs.open('Authors_names.tsv', 'r', encoding='utf-8-sig') as input_file:
    names = [line.strip() for line in input_file]

# Open output file for writing
with codecs.open('ORCIDresults.tsv', 'w', encoding='utf-8-sig') as output_file:
    # Write header row to output file
    output_file.write('Name\tORCID\n')

    # Loop over names
    for name in names:
        # Open webpage using Selenium
        driver = webdriver.Chrome()
        driver.get('https://orcid.org/search?q=' + name)

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Search for name and ORCID in parsed HTML
        name_element = soup.find('div', {'class': 'search-result-name'})
        orcid_element = soup.find('div', {'class': 'search-result-orcid'})

        # Store extracted values in variables
        if name_element is not None:
            name_value = name_element.text.strip()
        else:
            name_value = 'N/A'

        if orcid_element is not None:
            orcid_value = orcid_element.text.strip()
        else:
            orcid_value = 'N/A'

        # Write extracted information to output file
        output_file.write(name_value + '\t' + orcid_value + '\n')

        # Close Selenium driver
        driver.quit()


import os
from glob import glob
import shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

URL = r'http://localhost:8089/search/basic.xhtml'

N = 292119 # ICSD collection codes size

DOWNLOADS_PATH = r'C:/Users/mita3616/Downloads'

input_ids = {"General Attributes": "content_form:uiSimpleSearch:input",
             "Authors":"content_form:uiBibliographyAuthors:input_input",
             "Title of Journal":"content_form:uiBibliographyJournals:input_input",
             "Title of Article":"content_form:uiBibliographyArticles:input_input",
             "Composition":"content_form:uiChemistrySearchSumForm:input",
             "Number of Elements":"content_form:uiChemistrySearchElCount:input:input",
             "Cell Parameters":"content_form:uiCellParameter:input",
             "Cell Volume":"content_form:uiCellVolume:input:input",
             "Tolerance":"content_form:uiCellGlobalTolerance:input:input",
             "PDF Number":"content_form:uiPDFNumber:input_input",
             "ICSD Code":"content_form:uiCodeCollection:input:input"}

css_selectors = ['#content_form\:uiSimpleSearch\:componentInputInput',
                 '#content_form\:uiBibliographyAuthors\:input_input',
                 '#content_form\:uiBibliographyJournals\:input_input',
                 '#content_form\:uiBibliographyArticles\:input_input',
                 '#content_form\:uiChemistrySearchSumForm\:input',
                 '#content_form\:uiChemistrySearchElCount\:input\:input',
                 '#content_form\:uiCellParameter\:input',
                 '#content_form\:uiCellVolume\:input\:input',
                 '#content_form\:uiCellGlobalTolerance\:input\:input',
                 '#content_form\:uiPDFNumber\:input_input',
                 '#content_form\:uiCodeCollection\:input\:input']

css_selectors = dict(zip(input_ids.keys(), css_selectors))

# CSS Selectors
download_button_css_selector = "#display_form\:listViewTable\:0\:btnEntryDownloadCif"
search_summary_css_selector = '#content_form\:j_idt311 > tbody > tr > td.ui-panelgrid-cell.countPanelCol2 > label'
run_query_button_css_selector = '#content_form\:btnRunQuery'
count_button_css_selector = '#content_form\:btnCountMaskSearch'
result_css_selector = '#display_form\:listViewTable_data'

# XPaths
search_summary_xpath = '/html/body/div[2]/div[2]/form/div[3]/div[2]/div/div[2]/table/tbody/tr/td[2]/label'
next_link_xpath = '/html/body/div[2]/div[2]/form[1]/div/div[1]/div[2]/div/div/div[2]/a[3]'
results_table_xpath = '/html/body/div[2]/div[2]/form[1]/div/div[1]/div[2]/div/div/div[1]/table/tbody'
paginator_xpath = '/html/body/div[2]/div[2]/form[1]/div/div[1]/div[2]/div/div/div[2]/span[1]'

class Scraper():
    def __init__(self):
            self.search_results = []

            options = Options()
            # options.headless = True
            options.add_argument('InPrivate')
            options.add_argument('--headless=new')
            self.driver = webdriver.Edge(options=options)
            self.driver.get(URL)
            # self.driver.implicitly_wait(5)
            self.wait = WebDriverWait(self.driver, 10)
            
            for k in input_ids.keys():
                 k_fun_name = k.lower().replace(' ', '_')
                 setattr(self, f'search_{k_fun_name}', lambda s : self.search(s, field_name=k))

    def search(self, search_input, field_name="General Attributes"):
        self.driver.get(URL)

        if not isinstance(search_input, str):
            search_input = str(search_input)

        field = self.driver.find_element(by=By.CSS_SELECTOR, value=css_selectors[field_name])
        field.clear()
        field.send_keys(search_input)
        self.count_results()

        self.wait.until_not(
            EC.text_to_be_present_in_element((By.XPATH, search_summary_xpath), '-')
        )

        count = self.driver.find_element(By.XPATH, search_summary_xpath)

        self.match_count = int(count.text)
        if count.text != '0':
            self.run_query()
            self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, results_table_xpath))
            )

    def download_all_results_on_page(self):
        cif_download_buttons = self.driver.find_elements(By.XPATH, "//button[@title='download item as cif file']")
        for b in cif_download_buttons:
            b.click()

    def count_results(self):
        self.driver.find_element(By.CSS_SELECTOR, count_button_css_selector).click()

    def run_query(self):
        self.driver.find_element(By.CSS_SELECTOR, run_query_button_css_selector).click()


    def next_page(self):
        paginator = self.driver.find_element(By.XPATH, paginator_xpath).text
        next_page = self.driver.find_element(By.XPATH, next_link_xpath)
        next_page.click()
        self.wait.until_not(EC.presence_of_element_located((By.XPATH, f"//tr[@data-ri='{paginator}']")))
    
    def previous_page(self):
        paginator = self.driver.find_element(By.XPATH, paginator_xpath).text
        previous_page = self.driver.find_element(By.CSS_SELECTOR, "#display_form\:listViewTable_paginator_bottom > a.ui-paginator-prev.ui-state-default.ui-corner-all")
        previous_page.click()
        self.wait.until_not(EC.presence_of_element_located((By.XPATH, f"//tr[@data-ri='{paginator}']")))

def wait_for_download(file_path):
    get_fs = lambda : os.stat(file_path).st_size
    
    while True:
        try: 
            fs = get_fs()
            sleep(0.3)
            break
        except FileNotFoundError:
            pass
    
    while fs != get_fs():
        fs = get_fs()
        sleep(0.3)
    return

def look_for_downloads():
    files = glob(r"C:/Users/mita3616/Downloads/EntryWithCollCode*.cif")
    numbers = []
    if files:
        for f in files:
            if any(f'({n})' in f for n in range(10)): 
                files.remove(f)   
            else:
                n = f.split('EntryWithCollCode')[1].split('.cif')[0]
                numbers.append(int(n))
        return max(numbers)
    else:
        return 0


def download_all_results(driver):
    pages = (scraper.match_count // 10) - 1
    # Download first page
    scraper.download_all_results_on_page()
    if pages > 1:
        # Flip page and download all and repeat for all pages
        for p in range(pages):
            scraper.next_page()
            scraper.wait.until(EC.text_to_be_present_in_element_value)
            scraper.download_all_results_on_page()
    return

if __name__ == '__main__':
    print("ICSD CIF DOWNLOADER")
    print(30*"=")
    print('\n')
    print('Initializing scraper...')
    scraper = Scraper()
    # while True:
    #     try: pass
    #     except KeyboardInterrupt: break
    print(f'Scraper initialized at {URL}')
    print('Looking for downloads...')

    n_start = look_for_downloads() + 1
    print(f'Starting from collection code no. {n_start}')
    batch_size = bs = 10
    stale_ref_error_count = 0
    while n_start < 292119:
        old_n_start = n_start #backup variable for exception
        if n_start % bs != 1:   
            n_stop = n_start + bs - n_start % bs
        else:
            n_stop = n_start + bs - 1

        scraper.search_icsd_code(f'{n_start}-{n_stop}')
        download_all_results(scraper)
        
        n_start = n_stop + 1

        for i in range(n_start, N + 1, bs):
            stale_ref_error_count = 0
            while True:
                if (stale_ref_error_count >= 5):
                    print('Restarting driver...')
                    scraper.driver.close()
                    scraper = Scraper()
                try:
                    print(f'Downloading CIF with ICSD collection code {i} to {i+bs-1}...')
                    scraper.search_icsd_code(f'{i}-{i+bs-1}')
                    download_all_results(scraper)
                    break
                except TimeoutException:
                    print('Timed out, retrying.')
                except StaleElementReferenceException:
                    print('Stale reference error, retrying.')
                    stale_ref_error_count += 1

            # assure that it reattempts with the same number
            # try:
            #     fname = f'{DOWNLOADS_PATH}/EntryWithCollCode{i}.cif'
            #     wait_for_download(fname)
            #     shutil.move(fname, r'E:/ICSD')
            # except:
            #     print("Something went wrong.")
            #     break

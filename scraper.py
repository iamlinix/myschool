from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert
from model import Base, Score
from breakpoint import load as LoadBreakpoint, store as SaveBreakpoint
from sqlalchemy.orm import Session
import argparse
import time
import random

def accept_tnc(browser: WebDriver):
    checkbox = browser.find_element(By.ID, 'checkBoxTou')
    accept_btn = browser.find_element(By.ID, 'acceptButton')
    if checkbox is not None and accept_btn is not None:
        checkbox.click()
        accept_btn.click()

def select_state(browser: WebDriver, target_state: str):
    target_state = ('state-' + target_state).lower()
    browser.implicitly_wait(2)
    dropdown = browser.find_element(By.ID, 'dropdown-2')
    if dropdown is None:
        return
    dropdown.click()
    states = dropdown.find_elements(By.TAG_NAME, 'li')
    for state in states:
        label = state.find_element(By.TAG_NAME, 'label')
        attr_for = label.get_attribute('for').lower()
        if attr_for == target_state:
            label.find_element(By.TAG_NAME, 'span').click()
            break
    browser.find_element(By.ID, 'go').click()


def jump_to_breakpoint(browser: WebDriver) -> (int, int):
    page, index = LoadBreakpoint()
    if page > 0:
        browser.get('%s&pagenumber=%d' % (browser.current_url, page + 1))
        wait = WebDriverWait(browser, timeout=300)
        result_section = browser.find_element(By.CLASS_NAME, 'showing-results')
        wait.until(lambda d: result_section.is_displayed())
    return page, index


def get_comparative_numbers(element: WebElement) -> (int, int, int, int, int, int, int):
    reading, general_low, general_high, sim_low, sim_high, sim_avg, all_avg = 0, 0, 0, 0, 0, 0, 0
    try:
        reading = int(element.text.strip())
        generals = element.find_element(By.XPATH, "./span/table/tbody/tr[@class='selected-school-row']/td/span[@class='err']").get_attribute('innerHTML').split(' - ')
        general_low = int(generals[0])
        general_high = int(generals[1])
        cols = element.find_elements(By.XPATH, "./span/table/tbody/tr[@class='sim-all-row']/td")
        all_avg = int(cols[1].find_element(By.XPATH, './span[@class="sim-avg"]').get_attribute('innerHTML'))
        sim_avg = int(cols[0].find_element(By.XPATH, './span[@class="sim-avg"]').get_attribute('innerHTML'))
        sims = cols[0].find_element(By.XPATH, './span[@class="err"]').get_attribute('innerHTML').split(' - ')
        sim_low = int(sims[0])
        sim_high = int(sims[1])
    except:
        pass
    return reading, general_low, general_high, sim_low, sim_high, sim_avg, all_avg

def traverse_schools(browser: WebDriver, page: int, start_index: int):
    link_index = start_index

    while True:
        schools = browser.find_elements(By.CLASS_NAME, 'school-section')
        school_links = []

        for school in schools:
            school_links.append(school.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        
        if link_index > 0:
            school_links = school_links[start_index:]

        for link in school_links:
            browser.switch_to.new_window('tab')
            browser.get(link)

            wait = WebDriverWait(browser, timeout=300)
            top_section = browser.find_element(By.CLASS_NAME, 'topsection-wrapper')
            wait.until(lambda d: top_section.is_displayed())

            headers = top_section.find_element(By.TAG_NAME, 'h1').text.split(',')
            school_name = headers[0].strip()
            suburb = headers[1].strip()
            state = headers[2].strip()

            ts = time.time()
            while True:
                try:
                    fact_div = browser.find_element(By.CLASS_NAME, 'school-facts')
                except NoSuchElementException:
                    if time.time() - ts > 300:
                        exit(-1)
                    time.sleep(0.5)
                    continue
                break

            
            facts = fact_div.find_elements(By.XPATH, './ul/li')
            school_sector = facts[0].find_element(By.XPATH, './div[@class="col2"]').text
            school_type = facts[1].find_element(By.XPATH, './div[@class="col2"]').text
            year_range = facts[2].find_element(By.XPATH, './div[@class="col2"]').text
            school_location = facts[3].find_element(By.XPATH, './div[@class="col2"]').text
            
            naplan_menu = browser.find_element(By.CSS_SELECTOR, 'ul.flex.w-100.dropdown-menu').find_elements(By.TAG_NAME, 'li')[1]
            naplan_menu.click()
            naplan_menu.find_elements(By.TAG_NAME, 'li')[0].click()

            owls = browser.find_elements(By.CLASS_NAME, 'owl-item')
            owl_links = []
            for owl in owls:
                try:
                    owl_links.append(owl.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                except:
                    pass
            for link in owl_links:
                browser.get(link)
                table = browser.find_element(By.ID, 'similarSchoolsTable')
                rows = table.find_elements(By.XPATH, './tbody/tr')
                with Session(engine) as session:
                    for row in rows:
                        cols = row.find_elements(By.XPATH, './td')
                        grade = cols[0].text.strip()
                        reading, r_gen_low, r_gen_high, r_sim_low, r_sim_high, r_sim_avg, r_all_avg = get_comparative_numbers(cols[1])
                        writing, w_gen_low, w_gen_high, w_sim_low, w_sim_high, w_sim_avg, w_all_avg = get_comparative_numbers(cols[2])
                        spelling, s_gen_low, s_gen_high, s_sim_low, s_sim_high, s_sim_avg, s_all_avg = get_comparative_numbers(cols[3])
                        grammar, g_gen_low, g_gen_high, g_sim_low, g_sim_high, g_sim_avg, g_all_avg = get_comparative_numbers(cols[4])
                        numeracy, n_gen_low, n_gen_high, n_sim_low, n_sim_high, n_sim_avg, n_all_avg = get_comparative_numbers(cols[5])

                        stmt = insert(Score).values(
                            school_name = school_name,
                            suburb = suburb,
                            state = state,
                            year = link.split('/')[-1],
                            grade = grade,
                            school_sector = school_sector,
                            school_type = school_type,
                            school_location = school_location,
                            year_range = year_range,
                            reading = reading,
                            reading_low = r_gen_low,
                            reading_high = r_gen_high,
                            reading_sim_avg = r_sim_avg,
                            reading_sim_low = r_sim_low,
                            reading_sim_high = r_sim_high,
                            reading_all_avg = r_all_avg,
                            writing = writing,
                            writing_low = w_gen_low,
                            writing_high = w_gen_high,
                            writing_sim_avg = w_sim_avg,
                            writing_sim_low = w_sim_low,
                            writing_sim_high = w_sim_high,
                            writing_all_avg = w_all_avg,
                            spelling = spelling,
                            spelling_low = s_gen_low,
                            spelling_high = s_gen_high,
                            spelling_sim_avg = s_sim_avg,
                            spelling_sim_low = s_sim_low,
                            spelling_sim_high = s_sim_high,
                            spelling_all_avg = s_all_avg,
                            grammar = grammar,
                            grammar_low = g_gen_low,
                            grammar_high = g_gen_high,
                            grammar_sim_avg = g_sim_avg,
                            grammar_sim_low = g_sim_low,
                            grammar_sim_high = g_sim_high,
                            grammar_all_avg = g_all_avg,
                            numeracy = numeracy,
                            numeracy_low = n_gen_low,
                            numeracy_high = n_gen_high,
                            numeracy_sim_avg = n_sim_avg,
                            numeracy_sim_low = n_sim_low,
                            numeracy_sim_high = n_sim_high,
                            numeracy_all_avg = n_all_avg,
                            total = reading + writing + spelling + grammar + numeracy
                        )
                        dup_stmt = stmt.on_duplicate_key_update({'state': state})
                        session.execute(dup_stmt)
                    session.commit()
                time.sleep(1)
            SaveBreakpoint(page, link_index)
            
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(1)
            link_index += 1

        try:
            pages = browser.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'a')
            if len(pages) == 0:
                return
            
            next_page = pages[-1]
            arrow = next_page.find_elements(By.XPATH, './i[@class="pag_arrow_right"]')
            if len(arrow) > 0:
                browser.get(next_page.get_attribute('href'))
                wait = WebDriverWait(browser, timeout=300)
                result_section = browser.find_element(By.CLASS_NAME, 'showing-results')
                wait.until(lambda d: result_section.is_displayed())
            page += 1
            link_index = 0
        except:
            return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='myschool',
        description='scrape NAPLAN scores from myschool.com.au'
    )
    parser.add_argument('-s', '--state', type=str, default='QLD')
    args = parser.parse_args()

    engine = create_engine('mysql+mysqlconnector://linx:qwer1234@localhost/score?charset=utf8mb4', echo=True)
    Base.metadata.create_all(engine)

    browser = webdriver.Chrome()
    browser.get('https://www.myschool.edu.au/')
    browser.maximize_window()

    accept_tnc(browser)
    select_state(browser, args.state)
    page, index = jump_to_breakpoint(browser)
    traverse_schools(browser, page, index)

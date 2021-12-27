import csv
import urllib.parse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())

with open("logistics\\feedback-forms\\assignment-survey\\data\\au-2021.csv", "r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        project_num = int(row["8059386: Which project are you reviewing?"].split(":")[0][-2:])
        rating = row["8059590: On a scale from 1 (least) to 5 (most), how satisfied are you with this rubric?"]
        good = urllib.parse.quote(row["8059591: In what ways was this rubric helpful to you?"])
        bad = urllib.parse.quote(row["8059592: In what ways could this rubric be more helpful?"])
        time = row["8533354: How much time did you spend on this project in hours?"]

        url = f"https://docs.google.com/forms/d/e/1FAIpQLSfGp2BS_43Fb31hHfU93gMElt6vCIj-JKwTESmzcO7fDGmmQw/viewform?usp=pp_url&entry.2132275369=Project&entry.1922030867={project_num}&entry.965640654={rating}&entry.100630209={good}&entry.1538245296={bad}&entry.1774918602={time}"

        driver.get(url)

        button = driver.find_element_by_xpath('//div/span/span[text()="Next"]')

        button.click()

        button = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//div/span/span[text()="Next"]')))

        button.click()

        button = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//div/span/span[text()="Submit"]')))

        button.click()

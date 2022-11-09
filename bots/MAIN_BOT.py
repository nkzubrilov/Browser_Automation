from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from seleniumwire import undetected_chromedriver as uc

import json
import time
import random


class MainBot:
    # URL should be specified for every bot

    URL = "https://bot.incolumitas.com/"

    def __init__(self, profile_id):
        self.profile_id = profile_id

    @property
    def __profile(self):
        # extract a set of profile options from the json file and nominate it as a private property

        with open('../helper/profiles.json', 'r') as file:
            profiles = json.load(file)
            for prof in profiles:
                if prof['id'] == self.profile_id:
                    return prof
            print(f"Profile with id {self.profile_id} doesn't exist!")

    def _get_driver(self):
        # all the webdriver options should be in this private method

        sw_options = {
            'proxy': {
                'http': f'http://{self.__profile["proxy username"]}:{self.__profile["proxy pass"]}@{self.__profile["proxy ip"]}',
                'https': f'http://{self.__profile["proxy username"]}:{self.__profile["proxy pass"]}@{self.__profile["proxy ip"]}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

        service = Service(executable_path='../helper/chromedriver.exe')
        driver = uc.Chrome(service=service, use_subprocess=True, seleniumwire_options=sw_options,
                           user_data_dir=self.__profile["user_data_dir"]+self.__profile["id folder"])
        driver.implicitly_wait(5)

        return driver

    def __crawl(self):
        # this private method is for testing functionality. Its content shouldn't be inherited by other bots!

        username = "lincoln"
        email = "lincoln@gmail.com"
        delay = random.random()

        driver = self._get_driver()

        driver.get(self.URL)
        driver.maximize_window()

        # try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Text input']")))
        element = driver.find_element(By.XPATH, "//input[@placeholder='Text input']")

        startmove = driver.find_element(By.ID, "moreInfo")
        ActionChains(driver).move_to_element(startmove).move_by_offset(50, 2).perform()

        username_element = driver.find_element(By.XPATH, "//input[@placeholder='Text input']")
        username_str = username_element.get_attribute('value')

        ActionChains(driver).move_to_element(username_element).double_click(username_element).pause(1).send_keys(
            Keys.BACKSPACE).perform()

        for c in username:
            endtime = time.time() + delay
            username_element.send_keys(c)
            time.sleep(endtime - time.time())

        driver.find_element(By.XPATH, "//input[@placeholder='Email input']").clear()
        email_element = driver.find_element(By.XPATH, "//input[@placeholder='Email input']")
        email_str = username_element.get_attribute('value')

        ActionChains(driver).move_to_element(email_element).double_click(email_element).pause(1).send_keys(
            Keys.BACKSPACE).perform()

        for c in email:
            endtime = time.time() + delay
            email_element.send_keys(c)
            time.sleep(endtime - time.time())

        no_of_cookies_select = Select(
            driver.find_element(By.CSS_SELECTOR, "#formStuff > div:nth-child(3) > div > div > select"))
        no_of_cookies_select.select_by_index(1)

        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                            "#formStuff > div:nth-child(4) > div > label > input[type=checkbox]").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "#smolCat").click()
        time.sleep(4)
        driver.find_element(By.CSS_SELECTOR, "#submit").click()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        time.sleep(1)
        driver.switch_to.alert.accept()

        score = driver.find_element("xpath", "//span[@id='botScore']//span[1]//span[1]")
        print(score.text)

        time.sleep(30)


# bot = MainBot(1)
# bot.start()

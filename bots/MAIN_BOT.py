from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

import json
import time
import random
import threading


class MainBot:

    NUMBER_OF_THREADS = 1

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

    def __set_driver(self):
        # all the webdriver options should be in this private method

        prx = Proxy()
        prx.proxy_type = ProxyType.MANUAL
        prx.http_proxy = self.__profile['proxy']
        prx.ftpProxy = self.__profile['proxy']
        prx.socks_proxy = self.__profile['proxy']
        prx.socks_version = 5
        prx.ssl_proxy = self.__profile['proxy']

        capabilities = webdriver.DesiredCapabilities.CHROME
        prx.add_to_capabilities(capabilities)

        options = Options()
        options.add_argument(r'--user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data\Profile 2')
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        service = Service(executable_path='../helper/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options, desired_capabilities=capabilities)

        stealth(driver,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
                )

        return driver

    def start(self):
        # this is a method-starter that implemented multy-threading functionality

        threads = []
        for i in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.__crawl, name="Thread:" + str(i))
            time.sleep(3)
            print('Running thread:', threading.active_count())
            threads.append(t)
            t.start()

    def __crawl(self):
        # this private method is for testing functionality. Its content shouldn't be inherited by other bots!

        driver = self.__set_driver()

        URL = "https://bot.incolumitas.com/"
        username = "lincoln"
        email = "lincoln@gmail.com"
        delay = random.random()

        driver.get(URL)
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

        driver.quit()


bot = MainBot(2)
bot.start()

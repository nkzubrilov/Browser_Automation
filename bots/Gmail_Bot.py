from MAIN_BOT import MainBot

from selenium.webdriver import ActionChains, Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep
import threading
import random


class GmailBot(MainBot):

    URL = 'https://mail.google.com'

    @property
    def __whitelist(self):
        with open('../helper/whitelist.txt') as file:
            whitelist = [mail.strip() for mail in file.readlines()]

        return whitelist


    def login(self):
        # this method is for manual logging for every profile first time

        driver = super()._get_driver()
        driver.maximize_window()
        driver.get('https://mail.google.com')
        sleep(1000)

    def __main_thread(self, url):
        driver = self._get_driver()
        try:
            self.__run(driver, url)
        finally:
            driver.quit()

    def start(self):
        t = threading.Thread(target=self.__main_thread, name=f"Thread: {threading.active_count()}", args=(self.URL,))
        print('Running thread:', threading.active_count())
        t.start()
        sleep(5)

    def __check_spam(self, driver):
        while True:
            messages = driver.find_elements(By.XPATH, '//div[@class="ae4 UI nH oy8Mbf"]//div[@class="yW"]/span[@class="bA4"]')
            checkboxes = driver.find_elements(By.XPATH, '//div[@class="ae4 UI nH oy8Mbf"]//div[@role="checkbox"]')
            emails = driver.find_elements(By.XPATH, '//div[@class="ae4 UI nH oy8Mbf"]//div[@class="yW"]//span[@class="zF"][1]')
            elements = list(zip(messages, checkboxes, emails))

            for element in elements:
                msg, checkbox, mail = element[0], element[1], element[2].get_attribute('email')

                if len(elements) > 10 and not elements.index(element) % 3:
                    ActionChains(driver).scroll_to_element(msg).pause(random.gauss(5, 1)).perform()
                else:
                    ActionChains(driver).move_to_element(msg).pause(random.gauss(5, 1)).perform()

                if mail in self.__whitelist:
                    ActionChains(driver).move_to_element(checkbox).pause(random.random()).click().perform()
                sleep(random.gauss(1, 0.3))

            not_spam_btn = driver.find_element(By.XPATH, '//*[@class="Bn" and text()="Not spam"]')
            try:
                ActionChains(driver).move_to_element(not_spam_btn).pause(random.random()).click().pause(random.gauss(0.9, 0.3)).perform()
            except ElementNotInteractableException:
                print('No more unchecked messages in spam folder')
                break

            next_page_btn = driver.find_element(By.XPATH, '//div[@class="D E G-atb PY"]//div[contains(@class, "T-I J-J5-Ji amD T-I-awG HeQuj")][2]')
            if next_page_btn.get_attribute('aria-disabled') == 'true':
                print('No more unchecked messages in spam folder')
                break
            else:
                next_page_btn.click()
                sleep(random.gauss(1.2, 0.5))

    def __check_inbox(self, driver):

        while True:
            messages = driver.find_elements(By.XPATH, '//div[@class="yW"]//span[@class="zF"][1]/../../../..'
                                                      '//span[contains(@class, "T-KT") and @aria-label!="Starred"]/../..'
                                                      '//div[@class="yW"]//span[@class="zF"][1]')
            checkboxes = driver.find_elements(By.XPATH, '//div[contains(@class, "ae4 aDM nH oy8Mbf")]//tr[contains(@class,'
                                                        ' "zA zE")]//span[contains(@class, "T-KT") and @aria-label!="Starred"]'
                                                        '/../..//div[@role="checkbox"]')
            elements = list(zip(messages, checkboxes))

            if elements:
                for element in elements:
                    msg, checkbox, mail = element[0], element[1], element[0].get_attribute('email')

                    if len(elements) > 10 and not elements.index(element) % 3:
                        ActionChains(driver).scroll_to_element(msg).pause(random.gauss(5, 1)).perform()
                    else:
                        ActionChains(driver).move_to_element(msg).pause(random.gauss(5, 1)).perform()

                    if mail in self.__whitelist:
                        ActionChains(driver).move_to_element(checkbox).pause(random.random()).click().perform()
                    sleep(random.gauss(1, 0.3))

                more_btn = driver.find_element(By.XPATH, '//div[@class="Cq aqL" and @gh="mtb"]//div[@class="T-I J-J5-Ji nf T-I-ax7 L3"]')
                ActionChains(driver).move_to_element(more_btn).pause(random.random()).click().pause(random.random()).perform()

                add_star = driver.find_element(By.XPATH, '//div[@class="J-N-Jz" and text()="Add star"]')
                ActionChains(driver).move_to_element(add_star).pause(random.random()).click().pause(random.gauss(1, 0.3)).perform()
                driver.implicitly_wait(1)

            next_page_btn = driver.find_element(By.XPATH, '//div[@class="D E G-atb"]//div[contains(@class, "T-I J-J5-Ji amD T-I-awG HeQuj")][2]')
            if next_page_btn.get_attribute('aria-disabled') == 'true':
                print('No more unchecked messages in inbox folder')
                break
            else:
                next_page_btn.click()
                sleep(random.gauss(1.2, 0.5))

    def __reply_and_forward(self, driver):

        with open('../helper/replies.txt') as file:
            replies = file.readlines()

        while True:
            try:
                msg = driver.find_element(By.XPATH, '//div[@class="BltHke nH oy8Mbf" and @role="main"]//div[@class="yW"]//span[@class="zF"]')
            except NoSuchElementException:
                break
            ActionChains(driver).move_to_element(msg).pause(random.random()).click().pause(random.random()).perform()
            driver.implicitly_wait(3)

            reply_button = driver.find_element(By.XPATH, '//span[@class="ams bkH"]')
            ActionChains(driver).move_to_element(reply_button).pause(random.random()).click().pause(random.gauss(1, 0.3)).perform()
            driver.implicitly_wait(3)

            reply_text = random.choice(replies)
            textbox = driver.find_element(By.XPATH, '//div[@class="Am aO9 Al editable LW-avf tS-tW"]')
            send_btn = driver.find_element(By.XPATH, '//div[@class="T-I J-J5-Ji aoO v7 T-I-atl L3"]')

            ActionChains(driver).move_to_element(textbox).pause(random.random()).click().pause(random.gauss(1, 0.3)).perform()
            for c in reply_text:
                textbox.send_keys(c)
                sleep(random.gauss(1, 0.2))
            ActionChains(driver).move_to_element(send_btn).pause(random.random()).click().pause(random.gauss(1, 0.3)).perform()
            driver.implicitly_wait(3)

            forward_button = driver.find_element(By.XPATH, '//span[@class="ams bkG"]')

    def __run(self, driver, url):
        driver.maximize_window()
        driver.get(url)
        WebDriverWait(driver, 60).until(EC.url_contains('mail.google.com'))

        random.gauss(8, 3)
        try:
            more_button = driver.find_element(By.XPATH, '//span[@class="J-Ke n4 ah9"]')
            ActionChains(driver).move_to_element(more_button).pause(random.random()).click().pause(random.random()).perform()
        except NoSuchElementException:
            pass
        finally:
            spam_folder = driver.find_element(By.XPATH, '//div[@class="TN bzz aHS-bnv"]/div[@class="qj "]')
            ActionChains(driver).move_to_element(spam_folder).pause(random.random()).click().pause(random.random()).\
                move_by_offset(230, random.randint(-50, 50)).perform()
        sleep(random.gauss(5, 2))

        self.__check_spam(driver)

        inbox_folder = driver.find_element(By.XPATH, '//div[@class="TN bzz aHS-bnt"]/div[@class="qj "]')
        ActionChains(driver).move_to_element(inbox_folder).pause(random.random()).click().pause(random.random()). \
            move_by_offset(230, random.randint(-50, 50)).perform()
        sleep(random.gauss(5, 2))

        self.__check_inbox(driver)

        starred_folder = driver.find_element(By.XPATH, '//div[@class="TN bzz aHS-bnw"]/div[@class="qj "]')
        ActionChains(driver).move_to_element(starred_folder).pause(random.random()).click().pause(random.random()). \
            move_by_offset(230, random.randint(-50, 50)).perform()
        sleep(random.gauss(5, 2))

        self.__reply_and_forward(driver)


bot = GmailBot(1)
bot.start()


from MAIN_BOT import MainBot

import time
import threading


class GmailBot(MainBot):

    NUMBER_OF_THREADS = 2
    URL = 'https://mail.google.com'

    def login(self):
        # this method is for manual logging for every profile first time

        driver = super()._get_driver()
        driver.maximize_window()
        driver.get('https://mail.google.com')
        time.sleep(1000)

    def __main_thread(self, url):
        driver = self._get_driver()
        try:
            self.__run(driver, url)
        finally:
            driver.quit()

    def start(self):
        for num in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.__main_thread, name=f"Thread: {threading.active_count()}", args=(self.URL,))
            print('Running thread:', threading.active_count())
            t.start()
            time.sleep(5)

    def __run(self, driver, url):
        driver.get(url)
        time.sleep(1000)


bot = GmailBot(2)
bot.start()
bot2 = GmailBot(1)
bot2.start()

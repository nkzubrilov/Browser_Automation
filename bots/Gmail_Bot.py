from MAIN_BOT import MainBot

import time


class GmailBot(MainBot):

    def login(self):
        # this method is for manual logging for every profile first time

        driver = super()._get_driver()
        driver.maximize_window()
        driver.get('https://mail.google.com')
        time.sleep(1000)


bot = GmailBot(2)
bot.login()

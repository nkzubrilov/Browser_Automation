import time

from MAIN_BOT import MainBot


class GmailBot(MainBot):

    def login(self):
        # this method is for manual logging for every profile first time

        driver = super()._get_driver()
        driver.get('https://gmail.com')
        time.sleep(100)


bot = GmailBot(1)
bot.login()

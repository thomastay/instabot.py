#!/usr/bin/env/python
from likerbot import init_bot, run_bot
from postbot import Postbot
import time
import threading
import configparser

class Scheduler:
    """
    Custom class which runs the bot
    """
    def __init__(self):
        self.status = "Not Running"

    def start(self):
        self.getDetails() #Grabs passwords from login.ini
        self.post_bot = Postbot(self.username, self.passwd)
        self.post_bot_thread = threading.Thread(target = self.schedule_post)
        self.liker_bot = init_bot(self.username, self.passwd)

    def run(self):
        run_bot(self.liker_bot)
        self.post_bot_thread.start()

    def stop(self):
        self.liker_bot.logout()
        self.post_bot_thread.join()

    def schedule_post(self, sleep_time = 5000):
        """
        Schedules a post
        post() returns true if it posted a post, if not it returns false
        """
        if self.post_bot is not None:
            while self.post_bot.post():
                print ("Postbot: Postbot is sleeping")
                time.sleep(sleep_time)

    def getDetails(self):
        self.config = configparser.ConfigParser()
        self.config.read("login.ini")
        self.username = self.config["LOGIN"]["username"]
        self.passwd = self.config["LOGIN"]["password"]


def main():
    """
    Runs the liker bot
    """
    username, passwd = getDetails()
    post_bot_thread = threading.Thread(target = schedule_post)
    liker_bot = init_bot(username, passwd)
    post_bot_thread.start()
    run_bot(liker_bot)


if __name__ == "__main__":
    main()

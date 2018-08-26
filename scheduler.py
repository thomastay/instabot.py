#!/usr/bin/env/python
from likerbot import init_bot, run_bot
from postbot import post
import time
import threading
import configparser

def schedule_post(sleep_time = 5000):
    """
    Schedules a post
    post() returns true if it posted a post, if not it returns false
    """
    while post():
        print ("Postbot: Postbot is sleeping")
        time.sleep(sleep_time)

def getDetails():
    config = configparser.ConfigParser()
    config.read("login.ini")
    username = config["LOGIN"]["username"]
    passwd = config["LOGIN"]["password"]
    return (username, passwd)


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

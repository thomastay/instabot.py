#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import configparser
import sqlite3
from InstagramAPI import InstagramAPI

"""
Posts automatically based on the posts_db database
First reads the posts database and checks whether there is a post that
hasn't been opened.
If there is, it posts that post, prints a helpful message to the screen, then returns true
If not, it prints a helpful error message and then returns false
"""

config = configparser.ConfigParser()
config.read("login.ini")
username = config["LOGIN"]["username"]
passwd = config["LOGIN"]["password"]
posts_db_name = "posts_db.db"
posts_db = sqlite3.connect(posts_db_name, timeout=0,
                                isolation_level=None) # added a posts database
posts_db_c = posts_db.cursor()

posts_db_c.execute('SELECT filename, title, tags FROM posts WHERE post_date IS NULL')
toPost = posts_db_c.fetchone()
filename = "/home/thomas/insta-bot/img/" + toPost[0]
title = toPost[1]
#Handle tags
tagList = toPost[2].split(", ")
tagStr = '#' + " #".join(tagList)
captionStr = "{0} {1}".format(title, tagStr)
print ("Found image at: {0}\nCaption: {1}".format(filename, captionStr))
#Login using Instagram API
api = InstagramAPI(username, passwd)
api.login()  # login
isUploaded = api.uploadPhoto(filename, caption="This is real stuff #truth #deep")
posts_db_c.execute("UPDATE posts SET post_date = '2018-08-14' WHERE filename = '{0}'".format(toPost[0]))

#Close
posts_db_c.close()
posts_db.commit()


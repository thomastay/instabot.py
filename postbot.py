#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import configparser
import sqlite3
from datetime import datetime
from InstagramAPI import InstagramAPI
from InstagramAPI.exceptions import SentryBlockException

class Postbot():
    def __init__(self, username, password, posts_db_name = "posts_db.db"):
        self.status = "Not posting"
        self.username = username
        self.password = password
        self.posts_db_name = posts_db_name
        self.posts_db = sqlite3.connect(posts_db_name, timeout=0,
                                        isolation_level=None) # added a posts database
        self.posts_db_c = self.posts_db.cursor()

    def post(self):
        """
        Posts automatically based on the posts_db database
        First reads the posts database and checks whether there is a post that
        hasn't been opened.
        If there is, it posts that post, prints a helpful message to the screen, then returns true
        If not, it prints a helpful error message and then returns false
        """
        self.status = "Posting"
#Check the Posts database and select a file
        self.posts_db_c.execute('SELECT filename, title, tags FROM posts WHERE post_date IS NULL')
        self.toPost = self.posts_db_c.fetchone()
        if self.toPost is None:
            print ("Postbot: No more posts left in the database. Please update.")
            return False

        self.filename = "/home/thomas/insta-bot/img/" + self.toPost[0]
        self.title = self.toPost[1]

#Handle tags
        self.tagList = self.toPost[2].split(", ")
        self.tagStr = '#' + " #".join(self.tagList)
        self.captionStr = "{0} {1}".format(self.title, self.tagStr)
        print ("Postbot: Found image at: {0}\nCaption: {1}".format(self.filename, self.captionStr))

#Login using Instagram API
        self.api = InstagramAPI(self.username, self.passwd)
        print ("Postbot: ", end='')
        self.api.login()  # login
        self.isUploaded = False
        try:
            self.isUploaded = self.api.uploadPhoto(self.filename, caption=self.captionStr)
            print ("Postbot: {0}".format("Uploaded successfully" if self.isUploaded else "Upload failed"))
            if self.isUploaded:
                self.todayStr = datetime.today().strftime("%Y-%m-%d %H:%M")
                self.posts_db_c.execute("UPDATE posts SET post_date = '{1}' WHERE filename = '{0}'".format(
                    self.toPost[0], self.todayStr))
        except (RuntimeError, SentryBlockException) as error:
            print ("Unable to upload photo because of the following reasons:")
            print (error)
            #self.posts_db_c.execute("UPDATE posts SET post_date = \
            #        '2000-00-00' WHERE filename = '{0}'".format(self.toPost[0]))

#Close
        self.posts_db.commit()
        return isUploaded

    def stop(self):
        self.posts_db_c.close()
        self.posts_db.commit()
        self.status = "Closed"
        return False

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import configparser
from InstagramAPI import InstagramAPI

config = configparser.ConfigParser()
config.read("login.ini")
username = config["LOGIN"]["username"]
passwd = config["LOGIN"]["password"]
ig = InstagramAPI(username, passwd)
ig.login()

# get Self user feed
ig.getSelfUserFeed()

# get response json and assignment value to MediaList Variable
# dict type data
MediaList = ig.LastJson

# get first media for example delete media
Media = MediaList['items'][0]

# get media ID

MediaID = Media['id']
MediaType = Media['media_type']

# call deleteMedia Method
# deleteMedia return BOOL {true|false}
isDeleted = ig.deleteMedia(MediaID, media_type=MediaType)

if isDeleted:
    print("Your Media {0} has been deleted".format(
        MediaID
    ))
else:
    print("Your Media Not Deleted")

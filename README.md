# Instagram Follower

A simple program to follow users on Instagram.

## Getting Started

Edit config.json to your liking then run main.py.

## config.json

* username - Instagram username
* password - Instagram password
* accounts - A list of accounts with followers you'd like to follow
* followLimit - Number of users to follow when running the program
* followPrivate - true if you'd like to follow private users, false otherwise
* followAnon - true if you'd like to follow users with the default profile picture, false otherwise
* blacklist - Name of a text file containing a user ID per line that you don't want to follow again
* blacklistAll - true if you'd like to add all currently followed users to the blacklist before beginning, false otherwise (must be set to false to begin the unfollowing process)
* delay - Number of seconds to wait between each API action
* width - Number of characters to center the program output around

## Prerequisites

* Working on Python 2.7.16 or Python 3.6.8
* [InstagramAPI](https://github.com/LevPasha/Instagram-API-python)

## To-Do

- [ ] Update README with examples
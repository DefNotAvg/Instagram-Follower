from __future__ import print_function
from InstagramAPI import InstagramAPI
from time import sleep
import json
import sys
import os
import math

def load_from_json(file):
	try:
		with open(file, 'r') as myfile:
			return json.load(myfile)
	except IOError:
		with open(file, 'w') as myfile:
			json.dump({}, myfile)
		return {}

config = load_from_json('config.json')
username = config['username']
password = config['password']
accounts = config['accounts']
follow_limit = config['followLimit']
blacklist = config['blacklist']
blacklist_all = config['blacklistlistAll']
delay = config['delay']
width = config['width']

def blockPrint():
	sys.stdout = open(os.devnull, 'w')

def enablePrint():
	sys.stdout = sys.__stdout__

def center(text, spacer=' ', length=width, clear=False, display=True):
	if clear:
		os.system('cls' if os.name == 'nt' else 'clear')
	count = int(math.ceil((length - len(text)) / 2))
	if count > 0:
		if display:
			print(spacer * count + text + spacer * count)
		else:
			return (spacer * count + text + spacer * count)
	else:
		if display:
			print(text)
		else:
			return text

def header(full=True):
	center(' ', clear=True)
	center('Instagram Follower by @DefNotAvg')
	center('-', '-')
	if full:
		center('Signed in as @{}'.format(username))
		center('-', '-')

def smart_sleep(delay):
	if delay > 0:
		for a in range(delay, 0, -1):
			print('{}\r'.format(center('Sleeping for {} seconds...'.format(str(a)), display=False)), end='')
			sleep(1)
		center('Sleeping for {} seconds complete!'.format(str(delay)))

def gather_followers(username, count):
	followers = []
	try:
		blockPrint()
		api.searchUsername(username)
		api_result = api.LastJson
		user_id = api_result['user']['pk']
		enablePrint()
	except KeyError:
		if api_result['message'] == 'User not found':
			center('Unable to find @{} on Instagram.'.format(username))
			return followers
		else:
			center('Please increase delay in config.json before proceeding.')
			quit()
	with open(blacklist, 'r') as myfile:
		already_followed = myfile.read().splitlines()
	center('Gathering followers from @{}...'.format(username))
	center(' ')
	next_max_id = True
	while next_max_id and len(followers) < count:
		if next_max_id is True:
			next_max_id = ''
		api.getUserFollowers(user_id, maxid=next_max_id)
		api_request = api.LastJson
		old_len = len(followers)
		followers.extend([(item['pk'], item['username']) for item in api_request.get('users', [])])
		next_max_id = api_request.get('next_max_id', '')
		followers = [item for item in followers if str(item[0]) not in already_followed]
		center('Gathered {} followers!!'.format(str(len(followers) - old_len)))
		if next_max_id and len(followers) < count:
			smart_sleep(delay)
		center(' ')
	if len(followers) == 1:
		center('Successfully gathered {} follower in total!!'.format(len(followers)))
	else:
		center('Successfully gathered {} followers in total!!'.format(len(followers)))
	return followers[:count]

def follow(to_follow):
	count = 0
	if len(to_follow) == 1:
		center('{} user to follow...'.format(str(len(to_follow))))
	else:
		center('{} users to follow...'.format(str(len(to_follow))))
	center(' ')
	for item in to_follow:
		api.follow(item[0])
		if api.LastJson['friendship_status']['following']:
			center('Successfully followed @{}!!'.format(item[1]))
			with open(blacklist, 'a') as myfile:
				myfile.write('\n{}'.format(str(item[0])))
			count += 1
		else:
			center('Follow request sent to @{}!!'.format(item[1]))
			with open(blacklist, 'a') as myfile:
				myfile.write('\n{}'.format(str(item[0])))
			count += 1
		smart_sleep(delay)
		center(' ')
	if count == 1:
		center('Successfully followed {} user!!'.format(str(count)))
	else:
		center('Successfully followed {} users!!'.format(str(count)))

header(False)
blockPrint()
api = InstagramAPI(username, password)
if(api.login()):
	enablePrint()
	center('Signed in as @{}'.format(username))
	center('-', '-')
	if blacklist_all:
		api.getSelfUsersFollowing()
		following = [item['pk'] for item in api.LastJson['users']]
		with open(blacklist, 'w') as myfile:
			myfile.write('\n'.join([str(user_id) for user_id in following]))
		if len(following) == 1:
			center('Successfully added {} user to {}!!'.format(str(len(following)), blacklist))
		else:
			center('Successfully added {} users to {}!!'.format(str(len(following)), blacklist))
		quit()
	to_follow = []
	for username in accounts:
		for item in gather_followers(username, int(math.ceil(follow_limit / len(accounts)))):
			to_follow.append(item)
	header()
	if to_follow:
		follow(to_follow[:follow_limit])
	else:
		center('No users to follow.')
else:
	enablePrint()
	center('Failed to login.')
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
follow_private = config['followPrivate']
follow_anon = config['followAnon']
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

def gather_followers(account, count):
	followers = []
	try:
		blockPrint()
		api.searchUsername(account)
		api_result = api.LastJson
		user_id = api_result['user']['pk']
		enablePrint()
	except KeyError:
		if api_result['message'] == 'User not found':
			center('Unable to find @{} on Instagram.'.format(account))
			return followers
		else:
			center('Please increase delay in config.json before proceeding.')
			quit()
	with open(blacklist, 'r') as myfile:
		already_followed = myfile.read().splitlines()
	center('Gathering followers from @{}...'.format(account))
	center(' ')
	next_max_id = True
	while next_max_id and len(followers) < count:
		if next_max_id is True:
			next_max_id = ''
		api.getUserFollowers(user_id, maxid=next_max_id)
		api_request = api.LastJson
		old_len = len(followers)
		followers.extend([(item['pk'], item['username'], item['is_private'], item['has_anonymous_profile_picture']) for item in api_request.get('users', [])])
		next_max_id = api_request.get('next_max_id', '')
		followers = [item for item in followers if str(item[0]) not in already_followed]
		if not follow_private:
			followers = [item for item in followers if not item[2]]
		if not follow_anon:
			followers = [item for item in followers if not item[3]]
		followers = followers[:count]
		if len(followers) - old_len == 1:
			center('Gathered 1 follower!!')
		else:
			center('Gathered {} followers!!'.format(str(len(followers) - old_len)))
		if next_max_id and len(followers) < count:
			smart_sleep(delay)
		center(' ')
	if len(followers) == 1:
		center('Successfully gathered 1 follower in total!!')
	else:
		center('Successfully gathered {} followers in total!!'.format(len(followers)))
	return followers

def follow(to_follow):
	count = 0
	if len(to_follow) == 1:
		center('1 user to follow...')
	else:
		center('{} users to follow...'.format(str(len(to_follow))))
	center(' ')
	for item in to_follow:
		api.follow(item[0])
		if api.LastJson['friendship_status']['following']:
			count += 1
			center('Successfully followed @{}!! [{}/{}]'.format(item[1], str(count), str(follow_limit)))
			with open(blacklist, 'a') as myfile:
				myfile.write('\n{}'.format(str(item[0])))
		else:
			count += 1
			center('Follow request sent to @{}!! [{}/{}]'.format(item[1], str(count), str(follow_limit)))
			with open(blacklist, 'a') as myfile:
				myfile.write('\n{}'.format(str(item[0])))
		smart_sleep(delay)
		center(' ')
	if count == 1:
		center('Successfully followed 1 user!!')
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
			center('Successfully added 1 user to {}!!'.format(blacklist))
		else:
			center('Successfully added {} users to {}!!'.format(str(len(following)), blacklist))
		quit()
	to_follow = []
	count = follow_limit
	for i in range(0, len(accounts)):
		for item in gather_followers(accounts[i], int(math.ceil((count - len(to_follow)) / (len(accounts) - i)))):
			to_follow.append(item)
	header()
	if to_follow:
		follow(to_follow[:follow_limit])
	else:
		center('No users to follow.')
else:
	enablePrint()
	center('Failed to login.')
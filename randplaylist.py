#!/usr/bin/python
import hashlib
import random
import string
import json
import requests
import os
import sys

#creds should have 3 things in order on a line by themselves:
#username, password, site URL without trailing /
CRED=""
if not os.path.exists("./creds"):
	if not os.path.exists(os.getenv("HOME")+"/.creds"):
		sys.exit("No credentials file exists")
	else:
		CRED=os.getenv("HOME")+"/.creds"
else:
	CRED="./creds"
		
f = open(CRED, "r")
u=f.readline().rstrip()
password=f.readline().rstrip()
site=f.readline().rstrip()

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

s=get_random_alphanumeric_string(12)

tohash=password+s
t=hashlib.md5(tohash).hexdigest()

BASE=site+"/rest/"
#v="1.16.1" SUBSONIC
v="1.15.0" #AIRSONIC
c="randomplaylist"
randplay=0
musicfolder=0
X=0

print("Emptying Playlist")
totalz=requests.get(BASE+"getPlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(randplay)).json()['subsonic-response']['playlist']['songCount']
while requests.get(BASE+"getPlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(randplay)).json()['subsonic-response']['playlist']['songCount'] > 1:
	result=requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIndexToRemove=1").json()
	totalz=totalz-1
	sys.stdout.write('\r'+str(totalz)+" remain")
	sys.stdout.flush()

ADD=200
FIRST=1
Z=0

print("Adding songs")
while Z < ADD:
	sys.stdout.write('\r'+"Adding "+str(ADD-Z)+" more to reach "+str(ADD))
	sys.stdout.flush()
	for X in requests.get(BASE+"getRandomSongs"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&size="+str(1)+"&musicFolderId="+str(musicfolder)).json()['subsonic-response']['randomSongs']['song']:
		song=requests.get(BASE+"getSong"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(X['id'])+"").json()['subsonic-response']['song']
        	rating=song.get('averageRating',3.0)
		starred=song.get('starred',0)
		if float(rating) > 2.0:
			if str(starred) == '0':
				result=requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIdToAdd="+X['id']).json()
				Z+=1
				if FIRST == 1:
					FIRST=0
					result=requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIndexToRemove=0").json()

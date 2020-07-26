#!/usr/bin/python
import hashlib
import random
import string
import json
import requests


#creds should have 3 things in order on a line by themselves:
#username, password, site URL without trailing /
f = open("creds", "r")
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
v="1.16.1"
c="randomplaylist"
randplay=23


print "Emptying Playlist"

while requests.get(BASE+"getPlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(randplay)).json()['subsonic-response']['playlist']['songCount'] > 1:
	#print requests.get(BASE+"getPlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(randplay)).json()['subsonic-response']['playlist']['songCount']
	print requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIndexToRemove=1").json()

ADD=50
FIRST=1

print "Adding songs"
for X in requests.get(BASE+"getRandomSongs"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&size="+str(ADD)+"&musicFolderId=2").json()['subsonic-response']['randomSongs']['song']:
	song=requests.get(BASE+"getSong"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(X['id'])+"").json()['subsonic-response']['song']
        rating=song.get('averageRating',3.0)
	if float(rating) > 2.0:
		print requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIdToAdd="+X['id']).json()
		if FIRST == 1:
			FIRST=0
			print requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIndexToRemove=0").json()

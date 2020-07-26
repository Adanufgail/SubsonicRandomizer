#!/usr/bin/python
import hashlib
import random
import string
import json
import requests

f = open("creds", "r")
password=f.readline().rstrip()

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

s=get_random_alphanumeric_string(12)

tohash=password+s



t=hashlib.md5(tohash).hexdigest()

#response = requests.get("http://api.open-notify.org/iss-now.json")
#print(response.json()['iss_position'])

BASE="https://subsonic.hildetieoloramar.com/rest/"
u="adanufgail"
v="1.16.1"
c="randomplaylist"
randplay=23



while requests.get(BASE+"getPlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(randplay)).json()['subsonic-response']['playlist']['songCount'] > 1:
	#print requests.get(BASE+"getPlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&id="+str(randplay)).json()['subsonic-response']['playlist']['songCount']
	print requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIndexToRemove=1").json()

ADD=50
FIRST=1

for X in requests.get(BASE+"getRandomSongs"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&size="+str(ADD)+"&musicFolderId=2").json()['subsonic-response']['randomSongs']['song']:
	print requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIdToAdd="+X['id']).json()
	if FIRST == 1:
		FIRST=0
		print requests.get(BASE+"updatePlaylist"+"?u="+u+"&f=json&v="+v+"&c="+c+"&t="+t+"&s="+s+"&playlistId="+str(randplay)+"&songIndexToRemove=0").json()

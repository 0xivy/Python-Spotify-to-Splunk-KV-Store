import requests
import base64
from secrets import clientID, clientSecret
import json
from urllib3.exceptions import InsecureRequestWarning


authurl = "https://accounts.spotify.com/api/token"
authheaders ={}
authdata ={}


def getAccessToken(clientID, clientSecret):
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    authheaders['Authorization'] = "Basic " + base64_message
    authdata['grant_type'] = "client_credentials"
    res = requests.post(authurl, headers=authheaders, data=authdata)
    responseObject = res.json()
    accessToken = responseObject['access_token']
    return accessToken


def getPlaylistTracks(accessToken, playlistID):
    playlistEndpoint = f"https://api.spotify.com/v1/playlists/{playlistID}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(playlistEndpoint, headers=getHeader)
    playlistObject = res.json()
    return playlistObject

#Api requests
token = getAccessToken(clientID, clientSecret)
playlistID = "37i9dQZF1DWUa8ZRTfalHk?si=e5c18f8b0a784dee"

tracklist = getPlaylistTracks(token,playlistID)
trackListv2 = tracklist['tracks']['items']
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(trackListv2, f, ensure_ascii=False, indent=4)


nameList =[]
for x in trackListv2:
    song = x['track']['name']
    nameList.append(song)
with open(r'nameList.txt', 'w') as fp:
    for item in nameList:
        fp.write("%s\n" % item)
    print('Done')

artistList =[]
for x in trackListv2:
    song = x['track']['album']['artists'][0]['name']
    artistList.append(song)
with open(r'artistList.txt', 'w') as fp:
    for item in artistList:
        fp.write("%s\n" % item)
    print('Done')
    
albumList =[]
for x in trackListv2:
    song = x['track']['album']['name']
    albumList.append(song)
with open(r'albumList.txt', 'w') as fp:
    for item in albumList:
        fp.write("%s\n" % item)
    print('Done')

songlist = [{'name': x, 'artist': y, 'album': z} for x, y, z in zip(nameList, artistList, albumList)]
tobesent = json.dumps(songlist)

with open('final.json', 'w', encoding='utf-8') as f:
    json.dump(songlist, f, ensure_ascii=False, indent=4)

URL1 = "https://localhost:8089/servicesNS/nobody/<app-name>/storage/collections/data/<KV Store Collection Name>/batch_save"
headers = {"Content-Type": "application/json"}
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
sendtokv = requests.post(url=URL1, headers=headers, auth=('username', 'password'), verify=False, data=(tobesent))
print (sendtokv)

import urllib.request
import json

key = "AIzaSyB2otynAukXBQp0t6YAZvvNXk3XaLQ5y_c"





speakerOffset = 40

#List of channels : mention if you are pasting channel id or username - "id" or "forUsername"
ytids = [["UCla1QqkSKcWXjfig0xe7iTw","id"], ["UC873OURVczg_utAk8dXx_Uw","id"], ["TheMakersMuse", "forUsername"], 
    ["UCUxc0iEpV8wZV4WLOui0RwQ", "id"], ["UCe1Aj6VEO299Yq4WkXdoD3Q", "id"], ["UCIRiWCPZoUyZDbydIqitHtQ", "id"]]
#examples:
#["UCd_WBvzBg1UbHE8j8MIL5Ng","id"]
#["electrickeye91","forUsername"]

maxResults = 1000





print(len(ytids))
 
for i in range (0, len(ytids)):
    print(i)
    self_ytids = []
    self_ytids.append(ytids[i])
    #self_ytids.append(ytids[i+1])

    newstitles = []
    for ytid,ytparam in self_ytids:
        urld = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&"+ytparam+"="+ytid+"&key="+key
        with urllib.request.urlopen(urld) as url:
            datad = json.loads(url.read())
        uploadsdet = datad['items']
        #get upload id from channel id
        uploadid = uploadsdet[0]['contentDetails']['relatedPlaylists']['uploads']

        #retrieve list
        urld = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults="+str(maxResults)+"&playlistId="+uploadid+"&key="+key
        with urllib.request.urlopen(urld) as url:
            datad = json.loads(url.read())

        for data in datad['items']:
            ntitle =  data['snippet']['title']
            nlink = data['contentDetails']['videoId']
            
            newstitles.append([nlink,ntitle])


    print("The length is ", len(newstitles))
    for link,title in newstitles:
        print(link, title)
        f = open("speaker" + str(i+1+speakerOffset) + ".txt", "a")
        f.write("https://www.youtube.com/watch?v=" + link + "\n")
        f.close()

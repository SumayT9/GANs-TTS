import urllib.request
import json
import urllib
from pyyoutube import Api

api = Api(api_key='AIzaSyB2otynAukXBQp0t6YAZvvNXk3XaLQ5y_c')





speakerOffset = 26
playlist_ids = ["PLkDaE6sCZn6Ec-XTbcX1uRg2_u4xOEky0", "PLkDaE6sCZn6E7jZ9sN_xHwSHOdjUxUW_b", 
    "PLkDaE6sCZn6E7jZ9sN_xHwSHOdjUxUW_b", "PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF",
    "PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF", "PLkDaE6sCZn6F6wUI9tvS_Gw1vaFAx6rd6"
    ]






for i in range (0, len(playlist_ids)):
    #This array will contain all the URLs for the 
    urls = []
    self_playlist_ids = []
    self_playlist_ids.append(playlist_ids[i])

    for playlist in self_playlist_ids:
        playlist_item_by_playlist = api.get_playlist_items(playlist_id=playlist, count=1000)

        #Gets every video in playlist item
        for item in playlist_item_by_playlist.items:
            videoId = item.snippet.resourceId.videoId
            print(item.snippet.resourceId.videoId)
            urls.append("https://www.youtube.com/watch?v=" + videoId)

            #This code is just here for development to see the video titles so we can make sure we're getting the right videos. 
            #Remove this later once we have the code working and the right channels plugged in
            params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % videoId}
            url = "https://www.youtube.com/oembed"
            query_string = urllib.parse.urlencode(params)
            url = url + "?" + query_string
            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                try:
                    data = json.loads(response_text.decode())
                except Exception as e:
                    print("---COULD NOT GET VIDEO: "+str(type(e))+"---\n"+str(e)+"\n")
                print(data['title'])
        for url in urls:
            print(url)
            f = open("speaker" + str(i+1+speakerOffset) + ".txt", "a")
            f.write(url + "\n")
            f.close()
     
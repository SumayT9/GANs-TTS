import urllib.request
import json
import urllib

api = Api(api_key='AIzaSyB2otynAukXBQp0t6YAZvvNXk3XaLQ5y_c')

playlist_ids = ["PLkDaE6sCZn6Ec-XTbcX1uRg2_u4xOEky0", "PLkDaE6sCZn6E7jZ9sN_xHwSHOdjUxUW_b", 
    "PLkDaE6sCZn6E7jZ9sN_xHwSHOdjUxUW_b", "PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF",
    "PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF", "PLkDaE6sCZn6F6wUI9tvS_Gw1vaFAx6rd6"
    ]

for playlist in playlist_ids:
    #This array will contain all the URLs for the 
    urls = []

    
    playlist_item_by_playlist = api.get_playlist_items(playlist_id=playlist, count=5)

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
            data = json.loads(response_text.decode())
            print(data['title'])
    for url in urls:
        print(url)
        f = open("playlist" + str(int(i/2)+1) + ".txt", "a")
        f.write(url + "\n")
        f.close()

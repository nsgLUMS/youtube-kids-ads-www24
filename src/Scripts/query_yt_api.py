from googleapiclient.discovery import build
from json import loads,dumps
import time
import csv



def GetVideosFromChannel(api_key,channel_id):
    # This function gets the 10 most popular videos from the channel and writes them into a text file 'videos.txt'
    # Arguments: 
    #           api_key (string): Your api key to be used to make requests
    #           channel_id (string): The channel id of the Youtube Channel
    youtube = build('youtube','v3',developerKey=api_key)
    
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=10,
        order="viewCount",
        regionCode="US",
        type = "video"
    )
    response = request.execute()
    
    # print(dumps(response,sort_keys=True,indent=4))
    
    
    

    videosList = []
    for vid in response["items"]:
        videoID = (vid['id']['videoId'])
        videosList.append(videoID)
    
    return videosList
    
def GetChannelName(api_key,channelID,rank):
    # This function gets the channel name given the channel ID and writes it into the videos.txt file
    # (Intermediate function for formatting purposes)
    # Arguments: 
    #           api_key (string): Your api key to be used to make requests
    #           channel_id (string): The channel id of the Youtube Channel
    youtube = build('youtube','v3',developerKey=api_key)
    
    request = youtube.channels().list(
        part="snippet",
        id = channelID
    )
    response = request.execute()
    
    
    channel_title = response['items'][0]['snippet']['title']
    
    return channel_title

def main():
    
    key = "API_KEY"
    
    # change this number to whichever channel rank you're starting with
    channel_rank = 1
    
    # populate this list with the channel IDs
    channel_list = []
    
    
    
    header = ["Rank","Channel Title","Channel ID", "Videos"]
    data = []
    for i in range(0,len(channel_list)):
        temp = []
        temp.append(channel_rank)
        temp.append(GetChannelName(key,channel_list[i],channel_rank))
        temp.append(channel_list[i])
        temp.append(GetVideosFromChannel(key,channel_list[i]))
        channel_rank+=1
        
        data.append(temp)
        
   
     
    with open('videos.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)
        
    
    
        

if __name__ == "__main__":
    main()
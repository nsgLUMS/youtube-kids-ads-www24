from googleapiclient.discovery import build
import csv

api_key = "API_KE"
youtube = build("youtube", "v3", developerKey=api_key)

with open('viewcount1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Channel Name', 'video id', 'views'])  

    file_path = 'ul_list.txt'
    with open(file_path, 'r') as file:
        file_content = file.readlines()
        count = 0
        for line in file_content:
            video_id = line.strip()  
            count += 1
            response = youtube.videos().list(part="statistics", id=video_id).execute()
            response2 = youtube.videos().list(part="snippet", id=video_id).execute()
            
            if len(response["items"])!=0:
                view_count = response["items"][0]["statistics"]["viewCount"]
                channel_name = response2["items"][0]["snippet"]["channelTitle"]
                writer.writerow([channel_name, video_id, view_count]) 
                print(video_id)
            else:
                writer.writerow(["private", video_id, ""])

    print(count)

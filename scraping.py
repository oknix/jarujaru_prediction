# 参考: https://qiita.com/NakaokaRei/items/06f6fa98714aaa649810#fn5

import os
import time
import requests

from tqdm import tqdm
import pandas as pd

API_KEY = ''
CHANNEL_ID = 'UChwgNUWPM-ksOP3BbfQHS5Q'

base_url = 'https://www.googleapis.com/youtube/v3'
url = base_url + '/search?key=%s&channelId=%s&part=snippet,id&maxResults=50&order=date'
infos = []

while True:
    time.sleep(60)
    response = requests.get(url % (API_KEY, CHANNEL_ID))
    if response.status_code != 200:
        print('error')
        print(response)
        break
    result = response.json()
    infos.extend([
        [item['id']['videoId'], item['snippet']['title'], item['snippet']['description'], item['snippet']['publishedAt']]
        for item in result['items'] if item['id']['kind'] == 'youtube#video'
    ])

    if 'nextPageToken' in result.keys():
        if 'pageToken' in url:
            url = url.split('&pageToken')[0]
        url += f'&pageToken={result["nextPageToken"]}'
    else:
        print('finished')
        break

videos = pd.DataFrame(infos, columns=['videoId', 'title', 'description', 'publishedAt'])
# videos.to_csv('data/video1.csv', index=None)

stat_url = base_url + '/videos?key=%s&id=%s&part=statistics'

len_block = 50
video_ids_per_block = []
video_ids = videos.videoId.values

count = 0
end_flag = False
while not end_flag:
    start = count * len_block
    end = (count + 1) * len_block
    if end >= len(video_ids):
        end = len(video_ids)
        end_flag = True

    video_ids_per_block.append(','.join(video_ids[start:end]))

    count += 1

stats = []
for block in tqdm(video_ids_per_block):
    time.sleep(60)
    response = requests.get(stat_url % (API_KEY, block))
    if response.status_code != 200:
        print('error')
        break
    result = response.json()
    stats.extend([item['statistics'] for item in result['items']])

stasas = pd.DataFrame(stats)
# videos = pd.read_csv('videos.csv')
# stasas = pd.read_csv('stats.csv')
pd.merge(videos, stasas, left_index=True, right_index=True).to_csv('data/jarujaru_data3.csv')

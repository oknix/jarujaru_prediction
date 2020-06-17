import re
import pandas as pd

info = []
df = pd.read_csv('data/jarujaru_data.csv')
for row, item in df.iterrows():
    if 'ネタのタネ' in item['title']:
        title  = 'x' + item['title']
        title = re.split('[『』]', title)[1]
        if item['viewCount'] >= 250000:
            label = 2
        elif 100000 <= item['viewCount'] < 250000:
            label = 1
        elif item['viewCount'] < 100000:
            label = 0
        info.extend([[title, item['viewCount'], item['publishedAt'], item['likeCount'], item['dislikeCount'], item['commentCount'], label]])

pd.DataFrame(info, columns=['title', 'viewCount', 'publishedAt', 'likeCount', 'dislikeCount', 'commentCount', 'label']).to_csv('data/jarujaru_norm.csv')

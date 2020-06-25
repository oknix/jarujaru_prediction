import re
import pandas as pd

info = []
df = pd.read_csv('data/jarujaru_data.csv')
df['score'] = (df['commentCount'] / df['viewCount']) * (df['likeCount'] - 1.5 * df['dislikeCount']).tolist()
for row, item in df.iterrows():
    if 'ネタ' in item['title']:
        title  = item['title']
        title = re.split('[『』]', title)[1]
        if item['score'] >= 10:
            label = 2
        elif 0 <= item['score'] < 10:
            label = 1
        elif item['score'] < 0:
            label = 0
        info.extend([[title, item['viewCount'], item['publishedAt'], item['likeCount'], item['dislikeCount'], item['commentCount'], item['score'], label]])

pd.DataFrame(info, columns=['title', 'viewCount', 'publishedAt', 'likeCount', 'dislikeCount', 'commentCount', 'score', 'label']).to_csv('data/jarujaru_norm2.csv')

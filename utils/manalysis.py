# 参考: https://qiita.com/NakaokaRei/items/06f6fa98714aaa649810#fn5

import pandas as pd

import MeCab
from gensim import corpora
from gensim import matutils

mecab = MeCab.Tagger('mecabrc')

#形態素解析をして、名詞だけ取り出す
def tokenize(text):
    node = mecab.parseToNode(text)
    while node:
        if node.feature.split(',')[0] == '名詞' or node.feature.split(',')[0] == '形容詞' or node.feature.split(',')[0] == '動詞':
            yield node.surface.lower()
        node = node.next

#記事群のdictについて、形態素解析をしてリストに返す
def get_words(contents):
    ret = []
    for  content in contents:
        ret.append(get_words_main(content))
    return ret

#一つの記事を形態素解析して返す
def get_words_main(content):
    return [token for token in tokenize(content)]

def vec2dense(vec, num_terms):
    return list(matutils.corpus2dense([vec], num_terms=num_terms).T[0])


if __name__ == "__main__":
    df = pd.read_csv('../data/jarujaru_norm.csv')
    words = get_words(df['title']) #ここに形態素解析されたタイトル入る

    # 辞書を作る
    dictionary = corpora.Dictionary(words)
    dictionary.filter_extremes(no_below=2, keep_tokens=['チャラ','男','番長'])
    dictionary.save('../data/jarujaru.dict')

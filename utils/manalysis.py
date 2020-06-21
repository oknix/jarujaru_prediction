# 参考: https://qiita.com/NakaokaRei/items/06f6fa98714aaa649810#fn5

import pandas as pd

import MeCab
from gensim import corpora
from gensim import matutils

# mecab = MeCab.Tagger('mecabrc')
# NEologdを使用
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

# 辞書に含めない単語
NG_WORDS = ["奴"]

#タイトルを形態素解析をして、名詞、形容詞、動詞だけ取り出す
def tokenize(text):
    node = mecab.parseToNode(text)
    while node:
        if node.feature.split(',')[0] == '名詞' or node.feature.split(',')[0] == '形容詞' or node.feature.split(',')[0] == '動詞':
            yield node.surface.lower()
        node = node.next

#各タイトルについて、形態素解析した結果をリストで返す
def get_words(contents):
    ret = []
    for  content in contents:
        ret.append(get_words_main(content))
    return ret

#必要な単語を取得 NG_WORDSは含めない
def get_words_main(content):
    return [token for token in tokenize(content) if token not in NG_WORDS]

def vec2dense(vec, num_terms):
    return list(matutils.corpus2dense([vec], num_terms=num_terms).T[0])


if __name__ == "__main__":
    df = pd.read_csv('../data/jarujaru_norm.csv')
    words = get_words(df['title']) #ここに形態素解析されたタイトル入る
    # print(words)
    # 辞書を作る
    dictionary = corpora.Dictionary(words)
    dictionary.filter_extremes(no_below=2, keep_tokens=['チャラ','男','番長'])
    dictionary.save('../data/jarujaru.dict')

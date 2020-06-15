# 参考: https://qiita.com/NakaokaRei/items/06f6fa98714aaa649810#fn5

import utils.manalysis as analysis
import pandas as pd
import pickle
from gensim import corpora
from gensim import matutils

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

df = pd.read_csv('data/jarujaru_norm.csv')
words = analysis.get_words(df['title']) #ここに形態素解析されたタイトル入る

# 辞書を作る
dictionary = corpora.Dictionary(words)
dictionary.filter_extremes(no_below=2, keep_tokens=['チャラ','男','番長'])
dictionary.save('data/jarujaru.dict')
courpus = [dictionary.doc2bow(word) for word in words]

# Bag-of-words形式に変換
data_all = [analysis.vec2dense(dictionary.doc2bow(words[i]),len(dictionary)) for i in range(len(words))]

#トレーニング・テストデータの設定
train_data = data_all
X_train, X_test, y_train, y_test = train_test_split(train_data, df['label'], test_size=0.2, random_state=1)

#データの標準化
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

#学習モデルの作成
clf = SVC(C = 1, kernel = 'rbf')
clf.fit(X_train_std, y_train)
with open('data/model.pickle', mode='wb') as fp:
     pickle.dump(clf, fp)

score = clf.score(X_test_std, y_test)
print("{:.3g}".format(score))
predicted = clf.predict(X_test_std)

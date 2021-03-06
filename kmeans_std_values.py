import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# read dataset file
wine = np.loadtxt(open("winequality-red.csv", "rb"), delimiter=",", skiprows=1)
wine2 = pd.read_csv('winequality-red.csv')

X = wine[:,:-1]

X = StandardScaler().fit_transform(X)

# make quality scores to class
bins = (2.9, 5.9, 6.9, 8.9)
group_names = [0, 1, 2] # normal good great
wine2['quality'] = pd.cut(wine2['quality'], bins=bins, labels=group_names)


# X is feature, y is quality label
y = wine2['quality']

print(y.value_counts())

# do kmeans with 6 clusters and fit & predict
y_pred = KMeans(n_clusters=3).fit_predict(X)
y_gt = list(y)

c = np.argsort(np.bincount(y_pred))

y_pred[y_pred == c[0]] = 12
y_pred[y_pred == c[1]] = 11
y_pred[y_pred == c[2]] = 10
y_pred = y_pred - 10

d = pd.Series(y_pred)
print(d.value_counts())

count = 0
for i in range(len(y_gt)):
    if y_gt[i] == y_pred[i]:
        count += 1

print("accracy:", float(count)/len(y_gt))

# feature selection

new_X = np.c_[X[:, 1], X[:, 4], X[:, 7]] # volatile acidity, chlorides, density
new_y_pred = KMeans(n_clusters=3).fit_predict(new_X)

new_c = np.argsort(np.bincount(new_y_pred))

new_y_pred[new_y_pred == new_c[0]] = 12
new_y_pred[new_y_pred == new_c[1]] = 11
new_y_pred[new_y_pred == new_c[2]] = 10
new_y_pred = new_y_pred - 10

d = pd.Series(new_y_pred)
print(d.value_counts())

count = 0
for i in range(len(y_gt)):
    if y_gt[i] == new_y_pred[i]:
        count += 1

print("accracy:", float(count) / len(y_gt))


model = TSNE(learning_rate=100)
transformed = model.fit_transform(X)
new_transformed = model.fit_transform(new_X)


# make figure and show
plt.figure(1)
plt.scatter(transformed[:, 0], transformed[:, 1], c=y_pred)

plt.figure(2)
plt.scatter(transformed[:, 0], transformed[:, 1], c=y_gt)

plt.figure(3)
plt.scatter(new_transformed[:, 0], new_transformed[:, 1], c=new_y_pred)

plt.figure(4)
plt.scatter(new_transformed[:, 0], new_transformed[:, 1], c=y_gt)
plt.show()
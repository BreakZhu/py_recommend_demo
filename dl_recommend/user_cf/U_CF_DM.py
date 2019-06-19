import math
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split

ratingPath = '../../data/ratings.csv'
moviePath = '../../data/movies.csv'
ratings = pd.read_csv(ratingPath)
# print(ratings.describe())
# print(ratings.head())

movies = pd.read_csv(moviePath, index_col=None)
# print(movies.describe())
print(movies.head())


def save(path, model):
    np.save(path, model)


def load(path):
    try:
        model = np.load(path)
    except IOError:
        return None
    return model


# 统计打分的次数
data = pd.merge(ratings, movies, on='movieId')
rating_count_by_movie = data.groupby(['movieId', 'title'], as_index=False)['rating'].count()
rating_count_by_movie.columns = ['movieId', 'title', 'rating_count']
rating_count_by_movie.sort_values(by=['rating_count'], ascending=False, inplace=True)
# print(rating_count_by_movie[:10])

# 得到打分的平均值及方差
rating_stddev = data.groupby(['movieId', 'title']).agg({'rating': ['mean', 'std']})
# print(rating_stddev.head(10))

moviesDF = pd.read_csv(moviePath, index_col=None)
ratingsDF = pd.read_csv(ratingPath, index_col=None)

trainRatingsDF, testRatingsDF = train_test_split(ratingsDF, test_size=0.2)
# print("total_movie_count:" + str(len(set(ratingsDF['movieId'].values.tolist()))))
# print("total_user_count:" + str(len(set(ratingsDF['userId'].values.tolist()))))
# print("train_movie_count:" + str(len(set(trainRatingsDF['movieId'].values.tolist()))))
# print("train_user_count:" + str(len(set(trainRatingsDF['userId'].values.tolist()))))
# print("test_movie_count:" + str(len(set(testRatingsDF['movieId'].values.tolist()))))
# print("test_user_count:" + str(len(set(testRatingsDF['userId'].values.tolist()))))

# 我们得到用户-电影的评分矩阵，使用pandas的数据透视功能，同时，我们得到电影id和用户id与其对应索引的映射关系
trainRatingsPivotDF = pd.pivot_table(trainRatingsDF[['userId', 'movieId', 'rating']], columns=['movieId'],
                                     index=['userId'], values='rating', fill_value=0)
moviesMap = dict(enumerate(list(trainRatingsPivotDF.columns)))
usersMap = dict(enumerate(list(trainRatingsPivotDF.index)))
ratingValues = trainRatingsPivotDF.values.tolist()


# 余弦相似度计算两个list 之间的距离 a.b = ||a||||b||cos0
def calCosineSimilarity(list1, list2):
    res = 0
    denominator1 = 0
    denominator2 = 0
    for (val1, val2) in zip(list1, list2):
        res += (val1 * val2)
        denominator1 += val1 ** 2
        denominator2 += val2 ** 2
    return res / (math.sqrt(denominator1 * denominator2))

userSimMatrix = load('./model/_user_sim_matrix.npy')
# 需要计算用户之间的相似度矩阵，对于用户相似度矩阵，这是一个对称矩阵，同时对角线的元素为0，
# 所以我们只需要计算上三角矩阵的值即可
if userSimMatrix is None:
    userSimMatrix = np.zeros((len(ratingValues), len(ratingValues)), dtype=np.float32)  # 定义对角阵 用户与用户之间的对角阵
    for i in range(len(ratingValues) - 1):  # 所有用户的长度
        print("the {} row".format(i))
        for j in range(i + 1, len(ratingValues)):  # 相似用户从下一个用户开始
            # 计算当前用户与下一用户的相似度
            userSimMatrix[i, j] = calCosineSimilarity(ratingValues[i], ratingValues[j])
            userSimMatrix[j, i] = userSimMatrix[i, j]  # 对称矩阵赋值
    # 保存用户相似度矩阵
    # allow_pickle: 布尔值, 允许使用Python
    # pickles保存对象数组(可选参数, 默认即可)
    # fix_imports: 为了方便Pyhton2中读取Python3保存的数据(可选参数, 默认即可)
    save('./model/_user_sim_matrix', userSimMatrix)


# 我们要找到与每个用户最相近的K个用户，用这K个用户的喜好来对目标用户进行物品推荐，这里K=10，
# 下面的代码用来计算与每个用户最相近的10个用户
userMostSimDict = dict()
for i in range(len(ratingValues)):
    userMostSimDict[i] = sorted(enumerate(list(userSimMatrix[i])), key=lambda x: x[1], reverse=True)[:10]
# 得到了每个用户对应的10个兴趣最相近的用户之后，我们计算用户对每个没有观看过的电影的兴趣分：
# 用户，电影的二位矩阵
userRecommendValues = np.zeros((len(ratingValues), len(ratingValues[0])), dtype=np.float32)
for i in range(len(ratingValues)):  # 迭代用户影片评分
    for j in range(len(ratingValues[i])):  # 影片j评分
        if ratingValues[i][j] == 0:   # 如果没有评分证明没有看过影片
            val = 0
            for (user, sim) in userMostSimDict[i]:
                val += (ratingValues[user][j] * sim)
            userRecommendValues[i, j] = val   # 填入评分

# 我们为每个用户推荐10部电影
userRecommendDict = dict()
for i in range(len(ratingValues)):
    userRecommendDict[i] = sorted(enumerate(list(userRecommendValues[i])), key=lambda x: x[1], reverse=True)[:10]

userRecommendList = []
for key, value in userRecommendDict.items():
    user = usersMap[key]
    for (movieId, val) in value:
        userRecommendList.append([user, moviesMap[movieId]])

recommendDF = pd.DataFrame(userRecommendList, columns=['userId', 'movieId'])
recommendDF = pd.merge(recommendDF, moviesDF[['movieId', 'title']], on='movieId', how='inner')
print(recommendDF.tail(10))


import xgboost as xgb
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.externals import joblib
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from scipy.sparse import hstack


def xgb_feature_encode(libsvmFileNameInitial):
    # load 样本数据
    X_all, y_all = load_svmlight_file(libsvmFileNameInitial)
    # 训练/测试数据分割
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.3, random_state=42)
    # 定义模型
    xgboost = xgb.XGBClassifier(nthread=4, learning_rate=0.08,
                                n_estimators=50, max_depth=5, gamma=0, subsample=0.9, colsample_bytree=0.5)
    # 训练学习
    xgboost.fit(X_train, y_train)

    # 预测及 AUC 评测
    y_pred_test = xgboost.predict_proba(X_test)[:, 1]
    xgb_test_auc = roc_auc_score(y_test, y_pred_test)
    print('xgboost test auc: %.5f' % xgb_test_auc)

    # xgboost 编码原有特征
    X_train_leaves = xgboost.apply(X_train)
    X_test_leaves = xgboost.apply(X_test)
    # 训练样本个数
    train_rows = X_train_leaves.shape[0]
    # 合并编码后的训练数据和测试数据
    X_leaves = np.concatenate((X_train_leaves, X_test_leaves), axis=0)
    X_leaves = X_leaves.astype(np.int32)

    (rows, cols) = X_leaves.shape

    # 记录每棵树的编码区间
    cum_count = np.zeros((1, cols), dtype=np.int32)

    for j in range(cols):
        if j == 0:
            cum_count[0][j] = len(np.unique(X_leaves[:, j]))
        else:
            cum_count[0][j] = len(np.unique(X_leaves[:, j])) + cum_count[0][j - 1]

    print('Transform features genenrated by xgboost...')
    # 对所有特征进行 ont-hot 编码，注释部分是直接使用 onehot 函数，结果输出保证是 libsvm 格式也可以使用
    # sklearn 中的 dump_svmlight_file 操作，这个文件代码是参考别人的代码，这些点都是可以优化的。

    # onehot=OneHotEncoder()
    # onehot.fit(X_leaves)
    # x_leaves_encode=onehot.transform(X_leaves)
    for j in range(cols):
        keyMapDict = {}
        if j == 0:
            initial_index = 1
        else:
            initial_index = cum_count[0][j - 1] + 1
        for i in range(rows):
            if X_leaves[i, j] not in keyMapDict:
                keyMapDict[X_leaves[i, j]] = initial_index
                X_leaves[i, j] = initial_index
                initial_index = initial_index + 1
            else:
                X_leaves[i, j] = keyMapDict[X_leaves[i, j]]

    # 基于编码后的特征，将特征处理为 libsvm 格式且写入文件
    print('Write xgboost learned features to file ...')
    xgbFeatureLibsvm = open('xgb_feature_libsvm', 'w')
    for i in range(rows):
        if i < train_rows:
            xgbFeatureLibsvm.write(str(y_train[i]))
        else:
            xgbFeatureLibsvm.write(str(y_test[i - train_rows]))
        for j in range(cols):
            xgbFeatureLibsvm.write(' ' + str(X_leaves[i, j]) + ':1.0')
        xgbFeatureLibsvm.write('\n')
    xgbFeatureLibsvm.close()


def xgboost_lr_train(xgbfeaturefile, origin_libsvm_file):
    # load xgboost 特征编码后的样本数据
    X_xg_all, y_xg_all = load_svmlight_file(xgbfeaturefile)
    X_train, X_test, y_train, y_test = train_test_split(X_xg_all, y_xg_all, test_size=0.3, random_state=42)

    # load 原始样本数据
    X_all, y_all = load_svmlight_file(origin_libsvm_file)
    X_train_origin, X_test_origin, y_train_origin, y_test_origin = train_test_split(X_all, y_all, test_size=0.3,
                                                                                    random_state=42)

    # lr 对原始特征样本模型训练
    lr = LogisticRegression(n_jobs=-1, C=0.1, penalty='l1')
    lr.fit(X_train_origin, y_train_origin)
    joblib.dump(lr, 'lr_orgin.m')
    # 预测及 AUC 评测
    y_pred_test = lr.predict_proba(X_test_origin)[:, 1]
    lr_test_auc = roc_auc_score(y_test_origin, y_pred_test)
    print('基于原有特征的 LR AUC: %.5f' % lr_test_auc)

    # lr 对 load xgboost 特征编码后的样本模型训练
    lr = LogisticRegression(n_jobs=-1, C=0.1, penalty='l1')
    lr.fit(X_train, y_train)
    joblib.dump(lr, 'lr_xgb.m')
    # 预测及 AUC 评测
    y_pred_test = lr.predict_proba(X_test)[:, 1]
    lr_test_auc = roc_auc_score(y_test, y_pred_test)
    print('基于 Xgboost 特征编码后的 LR AUC: %.5f' % lr_test_auc)

    # 基于原始特征组合 xgboost 编码后的特征
    X_train_ext = hstack([X_train_origin, X_train])
    del (X_train)
    del (X_train_origin)
    X_test_ext = hstack([X_test_origin, X_test])
    del (X_test)
    del (X_test_origin)

    # lr 对组合后的新特征的样本进行模型训练
    lr = LogisticRegression(n_jobs=-1, C=0.1, penalty='l1')
    lr.fit(X_train_ext, y_train)
    joblib.dump(lr, 'lr_ext.m')
    # 预测及 AUC 评测
    y_pred_test = lr.predict_proba(X_test_ext)[:, 1]
    lr_test_auc = roc_auc_score(y_test, y_pred_test)
    print('基于组合特征的 LR AUC: %.5f' % lr_test_auc)


if __name__ == '__main__':
    xgb_feature_encode("map_data/agaricus.txt.train")
    xgboost_lr_train("xgb_feature_libsvm","map_data/agaricus.txt.train")

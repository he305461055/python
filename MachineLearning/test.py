import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from numpy._distributor_init import NUMPY_MKL
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV,RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

def test():
    data = pd.read_csv("C:/Users/Administrator/Desktop/mushrooms.csv")
    #print(data.iloc[1:['class','cap-shape']])
    #print(data.ix[1])
    #print(data.head(6))
    #print(data.isnull().sum()) ##查看每列空值的数目
    #print(data['class'].unique())
    #print(data.head(6))
    labelencoder = LabelEncoder()##非数字标签转换成数字
    for col in data.columns:
        data[col] = labelencoder.fit_transform(data[col])
    #print(data['stalk-color-above-ring'].unique())
    #print(data.groupby('class').size())
    #print(data.groupby('class').mean().unstack())
    print(data.head())

    ax=sns.boxplot(x='class', y='stalk-color-above-ring', data=data)
    ax = sns.stripplot(x="class", y='stalk-color-above-ring',
                       data=data, jitter=True,
                       edgecolor="gray")

    #sns.plt.title("Class w.r.t stalkcolor above ring",fontsize=12)
    #plt.show()

    X = data.iloc[:,1:23]
    #print(X)
    y = data.iloc[:, 0]
    #print(y)
    #print(data.iloc[:,0:3].head().corr())
    #print(data.iloc[:,0:3].head().cov())
    #################################################标准化数据
    scaler = StandardScaler()#通过删除平均值和缩放到单位方差来标准化特征
    X=scaler.fit_transform(X)# Scale the data to be between -1 and 1 #适合标签编码器并返回编码标签
    #print(X)

    #################################################主程序分析
    pca=PCA()
    #pca=PCA(n_components=1)
    pca.fit_transform(X)
    #covariance=pca.get_covariance()
    #covariance
    explained_variance=pca.explained_variance_
    #print(explained_variance)
    #print(pca.explained_variance_ratio_)
    N=data.values
    pca = PCA(n_components=2)
    x = pca.fit_transform(N)
    #print(x)

    ###将数据分解成训练和测试数据集
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=4)#将阵列或矩阵分解成随机列和测试子集
                                                                                         # #test_size=0.2表示取原数据的20%
                                                                                         #random_state随便写个值就好了，相当于ID，同一个ID每次生成就认为是同一组数据
    print(X_train)
    print('##########')
    print(X_test)
    print('##########')
    print(y_test)
    print('##########')
    print(y_train)
    '''
    ##逻辑回归
    model_LR= LogisticRegression()
    model_LR.fit(X_train,y_train) #训练模型

    y_prob = model_LR.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities #概率估计。
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    #print(y_pred)
    #print(model_LR.score(X_test, y_pred)) #平均精度
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)#计算混淆矩阵来评估分类的准确性
    #print(confusion_matrix)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)#曲线下的计算面积（AUC）来自预测分数
    #######
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)#############计算接收器工作特性（ROC）####假定可能性，真实可能性，阀值

    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则

    ##########################逻辑回归（调整模型）
    LR_model= LogisticRegression()
    tuned_parameters = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000] ,
                        'penalty':['l1','l2']
                       }

    LR= GridSearchCV(LR_model, tuned_parameters,cv=10)#对估计器的指定参数值进行详尽搜索。
    LR.fit(X_train,y_train)
    #print(LR.best_params_)###在保存数据上给出最佳结果的参数设置。
    y_prob = LR.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities #在具有最佳发现参数的估计器上调用predict_proba。
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    LR.score(X_test, y_pred) ##如果估计器已被重新设计，则返回给定数据的分数。

    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)#计算混淆矩阵来评估分类的准确性

    auc_roc=metrics.classification_report(y_test,y_pred) ##构建显示主要分类指标的文本报告
    #print(auc_roc)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)#曲线下的计算面积（AUC）来自预测分数

    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则



    LR_ridge= LogisticRegression(penalty='l2')
    LR_ridge.fit(X_train,y_train)
    y_prob = LR_ridge.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    LR_ridge.score(X_test, y_pred)#返回给定测试数据和标签的平均精度。
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)
    confusion_matrix
    auc_roc=metrics.classification_report(y_test,y_pred)

    auc_roc=metrics.roc_auc_score(y_test,y_pred)#曲线下的计算面积（AUC）来自预测分数
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则

    ###################高斯朴素贝叶斯
    model_naive = GaussianNB()
    model_naive.fit(X_train, y_train)#根据X，y拟合高斯朴素贝叶斯
    y_prob = model_naive.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    model_naive.score(X_test, y_pred)#返回给定测试数据和标签的平均精度。
    scores = cross_val_score(model_naive, X, y, cv=10, scoring='accuracy')#通过交叉验证评估分数
    scores.mean()
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)
    auc_roc=metrics.classification_report(y_test,y_pred)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则

    ######支持向量机
    svm_model= SVC()
    #####支持向量机无多项式内核
    tuned_parameters = {
     'C': [1, 10, 100,500, 1000], 'kernel': ['linear','rbf'],
     'C': [1, 10, 100,500, 1000], 'gamma': [1,0.1,0.01,0.001, 0.0001], 'kernel': ['rbf'],
     #'degree': [2,3,4,5,6] , 'C':[1,10,100,500,1000] , 'kernel':['poly']
        }
    ##GridSearchCV提供的网格搜索从通过调整参数**指定的参数值网格中全面生成候选，GridSearchCV实例实现了通用的估计器API：在数据集上“拟合”时，将对参数值的所有可能组合进行评估，
    ### 保留最佳组合。 但是在这里证明在计算上是昂贵的。所以我选择了RandomizedSearchCV。RandomizedSearchCV通过参数实现随机搜索，
    # 其中每个设置从可能的参数值的分布中进行采样。 这与穷举搜索有两个主要好处：1）可以独立于参数数量和可能的值选择预算。 2）添加不影响性能的参数不会降低效率。

    model_svm = RandomizedSearchCV(svm_model, tuned_parameters,cv=10,scoring='accuracy',n_iter=20)#随机搜索超参数。
    model_svm.fit(X_train, y_train)
    #print(model_svm.best_estimator_)#通过搜索选择的估计器，即在左侧数据上给出最高分数（或指定的最小损失）的估计器。 如果refit = False，则不可用。
    #print(model_svm.best_score_)##best_estimator的分数在左边的数据。
    #print(model_svm.cv_results_)
    #print(model_svm.best_params_)#最佳参数
    y_pred= model_svm.predict(X_test)##使用最好的参数调用估计器的预测
    #print(metrics.accuracy_score(y_pred,y_test))#精度分类得分##y_test与y_pred的匹配度，就是他们2个有多少个值是一样的，normalize如果为False，则返回正确分类样品的数量。 否则，返回正确分类样本的分数。
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)#计算混淆矩阵来评估分类的准确性
    auc_roc=metrics.classification_report(y_test,y_pred)#构建显示主要分类指标的文本报告
    auc_roc=metrics.roc_auc_score(y_test,y_pred)#曲线下的计算面积（AUC）来自预测分数
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则


    ####支持多项式内核的向量机
    svm_model= SVC()
    tuned_parameters = {
     'C': [1, 10, 100,500, 1000], 'kernel': ['linear','rbf'],
     'C': [1, 10, 100,500, 1000], 'gamma': [1,0.1,0.01,0.001, 0.0001], 'kernel': ['rbf'],
     'degree': [2,3,4,5,6] , 'C':[1,10,100,500,1000] , 'kernel':['poly']
        }
    model_svm = RandomizedSearchCV(svm_model, tuned_parameters,cv=10,scoring='accuracy',n_iter=20)##随机搜索超参数。
    model_svm.fit(X_train, y_train)
    print(model_svm.best_score_)
    print(model_svm.cv_results_)
    print(model_svm.best_params_)
    y_pred= model_svm.predict(X_test)
    print(metrics.accuracy_score(y_pred,y_test))
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)#计算混淆矩阵来评估分类的准确性
    auc_roc=metrics.classification_report(y_test,y_pred)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)#曲线下的计算面积（AUC）来自预测分数
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则

    '''
    '''
    #########尝试默认模型

    model_RR=RandomForestClassifier()#随机森林分类器。
    model_RR.fit(X_train,y_train)
    y_prob = model_RR.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    print(model_RR.score(X_test, y_pred))#返回给定测试数据和标签的平均精度。
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)#计算混淆矩阵来评估分类的准确性
    print(confusion_matrix)
    auc_roc=metrics.classification_report(y_test,y_pred)
    print(auc_roc)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)#曲线下的计算面积（AUC）来自预测分数
    print(auc_roc)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则
    plt.figure(figsize=(10, 10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, color='red', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.axis('tight')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    '''
    '''
    ###因此，默认的随机森林模型给我们最好的准确性。
    ###让我们调整随机森林的参数只是为了知识的目的
    ###有3个功能可以调整，以提高随机森林的性能
    ###1）max_features 2）n_estimators 3）min_sample_leaf
    ###A）max_features：这些是允许在单个树中尝试的功能的最大数量。 1）自动：这将简单地将所有在每个树中有意义的特征都放在一起。我们根本就不对单个树进行任何限制。 2）sqrt：该选项将取决于个人运行中功能总数的平方根。例如，如果变量的总数为100，那么我们只能在单个树中占用10个。 3）log2：另一个选项是记录功能输入的基础2。
    ###增加max_features通常可以提高模型的性能，就像现在我们有更多数量的选项被考虑。但是，当然，你可以通过增加max_features降低算法的速度。因此，您需要达到正确的平衡，并选择最佳的max_features。
    ###B）n_estimators：这是您在进行最大投票或预测的平均值之前要建立的树数。较高数量的树木可以提供更好的性能，但会使您的代码变慢。您应该选择与您的处理器可以处理的高价值，因为这将使您的预测变得更强大和更稳定。
    ###C）min_sample_leaf：Leaf是决策树的结束节点。较小的叶片使得模型更容易在列车数据中捕获噪声。因此，重要的是尝试不同的值来获得良好的估计。
    model_RR=RandomForestClassifier()
    tuned_parameters = {'min_samples_leaf': range(10,100,10), 'n_estimators' : range(10,100,10),
                        'max_features':['auto','sqrt','log2']
                        }
    ###n_jobs该参数告诉引擎允许使用多少个处理器。 值“-1”表示没有限制，而值“1”表示只能使用一个处理器。
    RR_model= RandomizedSearchCV(model_RR, tuned_parameters,cv=10,scoring='accuracy',n_iter=20,n_jobs= -1)##随机搜索超参数。
    RR_model.fit(X_train,y_train)
    print(RR_model.cv_results_)
    print(RR_model.best_score_)
    print(RR_model.best_params_)
    y_prob = RR_model.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    print(RR_model.score(X_test, y_pred))#返回给定测试数据和标签的平均精度。
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)#计算混淆矩阵来评估分类的准确性
    print(confusion_matrix)
    auc_roc=metrics.classification_report(y_test,y_pred)
    print(auc_roc)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)#曲线下的计算面积（AUC）来自预测分数
    print(auc_roc)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)####曲线下的计算面积（AUC）使用梯形规则
    plt.figure(figsize=(10, 10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, color='red', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.axis('tight')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    '''

    '''
    ####默认决策树模型
    model_tree = DecisionTreeClassifier()###决策树分类器。
    model_tree.fit(X_train, y_train)
    y_prob = model_tree.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    print(model_tree.score(X_test, y_pred))
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)
    print(confusion_matrix)
    auc_roc=metrics.classification_report(y_test,y_pred)
    print(auc_roc)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)
    print(auc_roc)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.figure(figsize=(10, 10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, color='red', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.axis('tight')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()

    #####因此，默认决策树模型为我们提供了最佳的准确性分数
    #####我们调整决策树模型的超参数
    #####1）标准：决策树使用多种算法来决定在两个或多个子节点中分割节点。决策树将节点分解在所有可用变量上，然后选择导致最均匀的子节点的分割。 基尼和熵的细节需要详细解释。
    #####2）max_depth（树的最大深度（垂直深度））：用于控制过拟合，因为较高的深度将允许模型学习特定于特定样本的关系。
    #####max_features和min_samples_leaf与Random Forest分类器相同
    model_DD = DecisionTreeClassifier()

    tuned_parameters= {'criterion': ['gini','entropy'], 'max_features': ["auto","sqrt","log2"],
                       'min_samples_leaf': range(1,100,1) , 'max_depth': range(1,50,1)
                      }
    DD_model= RandomizedSearchCV(model_DD, tuned_parameters,cv=10,scoring='accuracy',n_iter=20,n_jobs= -1,random_state=5)##随机搜索超参数。
    DD_model.fit(X_train, y_train)
    print(DD_model.cv_results_)
    print(DD_model.best_score_)
    print(DD_model.best_params_)
    y_prob = DD_model.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    print(DD_model.score(X_test, y_pred))
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)
    print(confusion_matrix)
    auc_roc=metrics.classification_report(y_test,y_pred)
    print(auc_roc)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)
    print(auc_roc)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.figure(figsize=(10, 10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, color='red', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.axis('tight')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    '''

    ###########神经网络
    ###########应用默认神经网络模型
    '''
    mlp = MLPClassifier()#####多层感知器分类器。
    mlp.fit(X_train,y_train)
    y_prob = mlp.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    mlp.score(X_test, y_pred)
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)
    print(confusion_matrix)
    auc_roc=metrics.classification_report(y_test,y_pred)
    print(auc_roc)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)
    print(auc_roc)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.figure(figsize=(10, 10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, color='red', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.axis('tight')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()

    ####调整神经网络的超参数
    # 对于我来说，调谐模型的计算价格是昂贵的。 所以我没有运行这个。 也欢迎任何即兴创作的建议。:)
    # 1）hidden_layer_sizes：网络中隐藏层的数量（默认为100）。大量可能会过滤数据。
    # 2）激活：隐藏层的激活功能。 A）物流Sigmoid函数'logistic'返回f（x）= 1 /（1 + exp（-x））。 B）'tanh'，双曲线tan函数返回f（x）= tanh（x）。 C）'relu'，整数线性单位函数返回f（x）= max（0，x）
    # 3）α：L2惩罚（正则化项）参数（默认为0.0001）
    # 4）max_iter：最大迭代次数。 求解器迭代直到收敛（由'tol'确定）或这个迭代次数（默认为200）

    mlp_model = MLPClassifier()#####多层感知器分类器。

    tuned_parameters = {'hidden_layer_sizes': range(1, 200, 10), 'activation': ['tanh', 'logistic', 'relu'],
                        'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10], 'max_iter': range(50, 200, 50)
                        }
    print(1)
    model_mlp= RandomizedSearchCV(mlp_model, tuned_parameters,cv=10,scoring='accuracy',n_iter=5,n_jobs= -1,random_state=5)
    print(1)
    model_mlp.fit(X_train, y_train)
    print(1)
    print(model_mlp.cv_results_)
    print(model_mlp.best_score_)
    print(model_mlp.best_params_)
    y_prob = model_mlp.predict_proba(X_test)[:,1] # This will give you positive class prediction probabilities
    y_pred = np.where(y_prob > 0.5, 1, 0) # This will threshold the probabilities to give class predictions.
    print(model_mlp.score(X_test, y_pred))
    confusion_matrix=metrics.confusion_matrix(y_test,y_pred)
    print(confusion_matrix)
    auc_roc=metrics.classification_report(y_test,y_pred)
    print(auc_roc)
    auc_roc=metrics.roc_auc_score(y_test,y_pred)
    print(auc_roc)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.figure(figsize=(10,10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate,true_positive_rate, color='red',label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],linestyle='--')
    plt.axis('tight')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    '''


if __name__=='__main__':
     #test()
     #squares = map(lambda x: x ** 2, range(10))
     #print(list(squares))
     import matplotlib.pyplot as plt

     #plt.plot([1,2,3],[4,5,6])
     #plt.show()
     x = [1, 2, 3]
     y = [5, 7, 4]

     x2 = [1, 2, 3]
     y2 = [10, 14, 12]
     plt.plot(x,y,label='First Line')
     plt.plot(x2,y2,label='Second Line')
     plt.xlabel('Plot Number')
     plt.ylabel('Important var')
     plt.title('Interesting Graph\nCheck it out')
     plt.legend()
     plt.show()
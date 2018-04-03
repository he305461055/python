import numpy as np
import matplotlib.pyplot as plt
#适合小规模数据
#课本案例（无核函数）
#对小规模数据点进行分类

traindatadir='F:/MachineLearning-master/'

class optStruct:
    def __init__(self, dataMatIn, classLabels, C, toler,KTup):  # Initialize the structure with the parameters
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = np.shape(dataMatIn)[0]
        self.alphas = np.mat(np.zeros((self.m, 1)))
        self.b = 0
        self.eCache = np.mat(np.zeros((self.m, 2)))  # first column is valid flag
        for i in range(self.m):
            self.K[:,i] = kernelTrans(self.X,self.X[i,:],KTup)

def loadDataSet(fileName):
    """
    对文件进行逐行解析，从而得到第行的类标签和整个特征矩阵
    Args:
        fileName 文件名
    Returns:
        dataMat  特征矩阵
        labelMat 类标签
    """
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

def selectJrand(i, m):
    """
    随机选择一个整数
    Args:
        i  第一个alpha的下标
        m  所有alpha的数目
    Returns:
        j  返回一个不为i的随机数，在0~m之间的整数值
    """
    j = i
    while j == i:
        j = int(np.random.uniform(0, m))
    return j

def clipAlpha(aj, H, L):
    """clipAlpha(调整aj的值，使aj处于 L<=aj<=H)
    Args:
        aj  目标值
        H   最大值
        L   最小值
    Returns:
        aj  目标值
    """
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

#误差缓存
def calcEk(oS, k):
    """calcEk（求 Ek误差：预测值-真实值的差）
    该过程在完整版的SMO算法中陪出现次数较多，因此将其单独作为一个方法
    Args:
        oS  optStruct对象
        k   具体的某一行
    Returns:
        Ek  预测结果与真实结果比对，计算误差Ek
    """
    fXk = float(np.multiply(oS.alphas, oS.labelMat).T * (oS.X * oS.X[k, :].T)) + oS.b
    Ek = fXk - float(oS.labelMat[k])
    return Ek

#内循环中启发式方法
def selectJ(i, oS, Ei):  # this is the second choice -heurstic, and calcs Ej
    """selectJ（返回最优的j和Ej）
    内循环的启发式方法。
    选择第二个(内循环)alpha的alpha值
    这里的目标是选择合适的第二个alpha值以保证每次优化中采用最大步长。
    该函数的误差与第一个alpha值Ei和下标i有关。
    Args:
        i   具体的第i一行
        oS  optStruct对象
        Ei  预测结果与真实结果比对，计算误差Ei
    Returns:
        j  随机选出的第j一行
        Ej 预测结果与真实结果比对，计算误差Ej
    """
    maxK = -1
    maxDeltaE = 0
    Ej = 0
    # 首先将输入值Ei在缓存中设置成为有效的。这里的有效意味着它已经计算好了。
    oS.eCache[i] = [1, Ei]

    # print 'oS.eCache[%s]=%s' % (i, oS.eCache[i])
    # print 'oS.eCache[:, 0].A=%s' % oS.eCache[:, 0].A.T
    # """
    # # 返回非0的：行列值
    # nonzero(oS.eCache[:, 0].A)= (
    #     行： array([ 0,  2,  4,  5,  8, 10, 17, 18, 20, 21, 23, 25, 26, 29, 30, 39, 46,52, 54, 55, 62, 69, 70, 76, 79, 82, 94, 97]),
    #     列： array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0])
    # )
    # """
    # print 'nonzero(oS.eCache[:, 0].A)=', nonzero(oS.eCache[:, 0].A)
    # # 取行的list
    # print 'nonzero(oS.eCache[:, 0].A)[0]=', nonzero(oS.eCache[:, 0].A)[0]
    # 非零E值的行的list列表，所对应的alpha值
    validEcacheList = np.nonzero(oS.eCache[:, 0].A)[0]
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:  # 在所有的值上进行循环，并选择其中使得改变最大的那个值
            if k == i:
                continue  # don't calc for i, waste of time

            # 求 Ek误差：预测值-真实值的差
            Ek = calcEk(oS, k)
            deltaE = abs(Ei - Ek)
            #选择具有最大步长的j
            if (deltaE > maxDeltaE):
                maxK = k
                maxDeltaE = deltaE
                Ej = Ek
        return maxK, Ej
    else:  # 如果是第一次循环，则随机选择一个alpha值
        j = selectJrand(i, oS.m)

        # 求 Ek误差：预测值-真实值的差
        Ej = calcEk(oS, j)
    return j, Ej

def innerL(i, oS):
    """innerL
    内循环代码
    Args:
        i   具体的某一行
        oS  optStruct对象
    Returns:
        0   找不到最优的值
        1   找到了最优的值，并且oS.Cache到缓存中
    """

    # 求 Ek误差：预测值-真实值的差
    Ei = calcEk(oS, i)

    # 约束条件 (KKT条件是解决最优化问题的时用到的一种方法。我们这里提到的最优化问题通常是指对于给定的某一函数，求其在指定作用域上的全局最小值)
    # 0<=alphas[i]<=C，但由于0和C是边界值，我们无法进行优化，因为需要增加一个alphas和降低一个alphas。
    # 表示发生错误的概率：labelMat[i]*Ei 如果超出了 toler， 才需要优化。至于正负号，我们考虑绝对值就对了。
    '''
    # 检验训练样本(xi, yi)是否满足KKT条件
    yi*f(i) >= 1 and alpha = 0 (outside the boundary)
    yi*f(i) == 1 and 0<alpha< C (on the boundary)
    yi*f(i) <= 1 and alpha = C (between the boundary)
    '''
    if ((oS.labelMat[i] * Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i] * Ei > oS.tol) and (oS.alphas[i] > 0)):
        # 选择最大的误差对应的j进行优化。效果更明显
        j, Ej = selectJ(i, oS, Ei)
        alphaIold = oS.alphas[i].copy()
        alphaJold = oS.alphas[j].copy()

        # L和H用于将alphas[j]调整到0-C之间。如果L==H，就不做任何改变，直接return 0
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L == H:
            print("L==H")
            return 0

        # eta是alphas[j]的最优修改量，如果eta==0，需要退出for循环的当前迭代过程
        # 参考《统计学习方法》李航-P125~P128<序列最小最优化算法>
        eta = 2.0 * oS.X[i, :] * oS.X[j, :].T - oS.X[i, :] * oS.X[i, :].T - oS.X[j, :] * oS.X[j, :].T
        if eta >= 0:
            print("eta>=0")
            return 0

        # 计算出一个新的alphas[j]值
        oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej) / eta
        # 并使用辅助函数，以及L和H对其进行调整
        oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
        # 更新误差缓存
        updateEk(oS, j)

        # 检查alpha[j]是否只是轻微的改变，如果是的话，就退出for循环。
        if (abs(oS.alphas[j] - alphaJold) < 0.00001):
            print("j not moving enough")
            return 0

        # 然后alphas[i]和alphas[j]同样进行改变，虽然改变的大小一样，但是改变的方向正好相反
        oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i] * (alphaJold - oS.alphas[j])
        # 更新误差缓存
        updateEk(oS, i)

        # 在对alpha[i], alpha[j] 进行优化之后，给这两个alpha值设置一个常数b。
        # w= Σ[1~n] ai*yi*xi => b = yj Σ[1~n] ai*yi(xi*xj)
        # 所以：  b1 - b = (y1-y) - Σ[1~n] yi*(a1-a)*(xi*x1)
        # 为什么减2遍？ 因为是 减去Σ[1~n]，正好2个变量i和j，所以减2遍
        b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.X[i, :] * oS.X[i, :].T - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.X[i, :] * oS.X[j, :].T
        b2 = oS.b - Ej - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.X[i, :] * oS.X[j, :].T - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.X[j, :] * oS.X[j, :].T
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]):
            oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]):
            oS.b = b2
        else:
            oS.b = (b1 + b2) / 2.0
        return 1
    else:
        return 0

def updateEk(oS, k):  # after any alpha has changed update the new value in the cache
    """updateEk（计算误差值并存入缓存中。）
    在对alpha值进行优化之后会用到这个值。
    Args:
        oS  optStruct对象
        k   某一列的行号
    """

    # 求 误差：预测值-真实值的差
    Ek = calcEk(oS, k)
    oS.eCache[k] = [1, Ek]

#完整版的SMO算法
def smoP(dataMatIn, classLabels, C, toler, maxIter):
    """
    完整SMO算法外循环，与smoSimple有些类似，但这里的循环退出条件更多一些
    Args:
        dataMatIn    数据集
        classLabels  类别标签
        C   松弛变量(常量值)，允许有些数据点可以处于分隔面的错误一侧。
            控制最大化间隔和保证大部分的函数间隔小于1.0这两个目标的权重。
            可以通过调节该参数达到不同的结果。
        toler   容错率
        maxIter 退出前最大的循环次数
    Returns:
        b       模型的常量值
        alphas  拉格朗日乘子
    """

    # 创建一个 optStruct 对象
    oS = optStruct(np.mat(dataMatIn), np.mat(classLabels).transpose(), C, toler)
    iter = 0
    entireSet = True
    alphaPairsChanged = 0

    # 循环遍历：循环maxIter次 并且 （alphaPairsChanged存在可以改变 or 所有行遍历一遍）
    # 循环迭代结束 或者 循环遍历所有alpha后，alphaPairs还是没变化
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0

        #  当entireSet=true or 非边界alpha对没有了；就开始寻找 alpha对，然后决定是否要进行else。
        if entireSet:
            # 在数据集上遍历所有可能的alpha
            for i in range(oS.m):
                # 是否存在alpha对，存在就+1
                alphaPairsChanged += innerL(i, oS)
                print("fullSet, iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged))
            iter += 1
        # 对已存在 alpha对，选出非边界的alpha值，进行优化。
        else:
            # 遍历所有的非边界alpha值，也就是不在边界0或C上的值。
            nonBoundIs = np.nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i, oS)
                print("non-bound, iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged))
            iter += 1

        # 如果找到alpha对，就优化非边界alpha值，否则，就重新进行寻找，如果寻找一遍 遍历所有的行还是没找到，就退出循环。
        if entireSet:
            entireSet = False  # toggle entire set loop
        elif (alphaPairsChanged == 0):
            entireSet = True
        print("iteration number: %d" % iter)
    return oS.b, oS.alphas

#训练算法,简易smo算法
def smoSimple(dataMatIn,classLabels,C,toler,maxIter):
    """smoSimple

        Args:
            dataMatIn    特征集合
            classLabels  类别标签
            C   松弛变量(常量值)，允许有些数据点可以处于分隔面的错误一侧。
                控制最大化间隔和保证大部分的函数间隔小于1.0这两个目标的权重。
                可以通过调节该参数达到不同的结果。
            toler   容错率（是指在某个体系中能减小一些因素或选择对某个系统产生不稳定的概率。）
            maxIter 退出前最大的循环次数
        Returns:
            b       模型的常量值
            alphas  拉格朗日乘子
        """
    dataMatrix = np.mat(dataMatIn)
    # 矩阵转置 和 .T 一样的功能
    labelMat = np.mat(classLabels).transpose()
    m,n = np.shape(dataMatrix)
    #初始化 b 和alphas(alpha有点类似权重值。)
    b = 0
    alphas = np.mat(np.zeros((m,1)))
    #在没有任何alphs改变的情况下遍历数据次数
    iter = 0
    while(iter < maxIter):
        # w = calcWs(alphas, dataMatIn, classLabels)
        # print("w:", w)

        #记录alpha是否已经进行优化，每次循环时设为0，然后再对整个集合顺序遍历
        alphaPairsChanged = 0
        for i in range(m):
            #print('alphas=',alphas)
            #print('labelMat',labelMat)
            #print('multiply(alphas,labelMat)=',np.multiply(alphas,labelMat))
            # 我们预测的类别 y[i] = w^Tx[i]+b; 其中因为 w = Σ(1~n) a[n]*lable[n]*x[n]
            fxi =  float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b
            #预测值跟真实值对比，计算误差Ei
            Ei = fxi -float(labelMat[i])

            # 约束条件 (KKT条件是解决最优化问题的时用到的一种方法。我们这里提到的最优化问题通常是指对于给定的某一函数，求其在指定作用域上的全局最小值)
            # 0<=alphas[i]<=C，但由于0和C是边界值，我们无法进行优化，因为需要增加一个alphas和降低一个alphas。
            # 表示发生错误的概率：labelMat[i]*Ei 如果超出了 toler， 才需要优化。至于正负号，我们考虑绝对值就对了。
            # 检验训练样本(xi, yi)是否满足KKT条件
            #yi*f(i) >= 1 and alpha = 0 (outside the boundary)
            #yi*f(i) == 1 and 0<alpha< C (on the boundary)
            #yi*f(i) <= 1 and alpha = C (between the boundary)

            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i]>0)):
                #如果满足优化条件，我们就随机选取非i的一个点，进行优化比较
                j = selectJrand(i,m)
                #预测j的结果
                fxj = float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fxj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()

                #L和H用于将alphas[j]调整到0-C之间。如果L==H，就不做任何改变，直接执行continue语句
                #labelMat[i]!=labelMat[j]表示异侧，就相减，否则是同侧，就相加。
                if (labelMat[i]!=labelMat[j]):
                    L = max(0,alphas[j] - alphas[i])
                    H = min(C,C + alphas[j] - alphas[i])
                else:
                    L = max(0,alphas[j] + alphas[i]-C)
                    H = min(C,alphas[j] + alphas[i])

                #如果相同，就没有发优化了
                if L == H:
                    print("L==H")
                    continue
                #eta是alphas[j]的最优修改量，如果eta==0，需要退出for循环的当前迭代过程
                #参考《统计学习方法》李航-P125~P128<序列最小最优化算法>
                eta = 2.0*dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta>=0:
                    print('eta>=0')
                    continue

                #计算出一个新的alphas[j]值
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                # 并使用辅助函数，以及L和H对其进行调整
                alphas[j] = clipAlpha(alphas[j],H,L)
                # 检查alpha[j]是否只是轻微的改变，如果是的话，就退出for循环。
                if (abs(alphas[j] - alphaJold) < 0.00001):
                    print("j not moving enough")
                    continue
                # 然后alphas[i]和alphas[j]同样进行改变，虽然改变的大小一样，但是改变的方向正好相反
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                # 在对alpha[i], alpha[j] 进行优化之后，给这两个alpha值设置一个常数b。
                # w= Σ[1~n] ai*yi*xi => b = yj- Σ[1~n] ai*yi(xi*xj)
                # 所以：  b1 - b = (y1-y) - Σ[1~n] yi*(a1-a)*(xi*x1)
                # 为什么减2遍？ 因为是 减去Σ[1~n]，正好2个变量i和j，所以减2遍
                b1 = b -  Ei -labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b -  Ej -labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0<alphas[i]) and (C>alphas[i]):
                    b=b1
                elif (0<alphas[j]) and (C>alphas[j]):
                    b=b2
                else:
                    b=(b1+b2)/2.0
                alphaPairsChanged+=1
                print("iter:%d i:%d,pairs changed %d" %(iter,i,alphaPairsChanged))
        # 在for循环外，检查alpha值是否做了更新，如果在更新则将iter设为0后继续运行程序
        # 知道更新完毕后，iter次循环无变化，才推出循环。
        if (alphaPairsChanged == 0):
            iter += 1
        else:
            iter = 0
        print("iteration number:%d" %iter)
    return b,alphas

def calcWs(alphas, dataArr, classLabels):
    """
    基于alpha计算w值
    Args:
        alphas        拉格朗日乘子
        dataArr       feature数据集
        classLabels   目标变量数据集
    Returns:
        wc  回归系数
    """
    X = np.mat(dataArr)
    labelMat = np.mat(classLabels).transpose()
    m, n = np.shape(X)
    w = np.zeros((n, 1))
    for i in range(m):
        w += np.multiply(alphas[i] * labelMat[i], X[i, :].T)
    return w

def plotfig_SVM(xMat, yMat, ws, b, alphas):
    """
    参考地址：
       http://blog.csdn.net/maoersong/article/details/24315633
       http://www.cnblogs.com/JustForCS/p/5283489.html
       http://blog.csdn.net/kkxgx/article/details/6951959
    """

    xMat = np.mat(xMat)
    yMat = np.mat(yMat)

    # b原来是矩阵，先转为数组类型后其数组大小为（1,1），所以后面加[0]，变为(1,)
    b = np.array(b)[0]
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # 注意flatten的用法
    ax.scatter(xMat[:, 0].flatten().A[0], xMat[:, 1].flatten().A[0])

    # x最大值，最小值根据原数据集dataArr[:, 0]的大小而定
    x = np.arange(-1.0, 10.0, 0.1)

    # 根据x.w + b = 0 得到，其式子展开为w0.x1 + w1.x2 + b = 0, x2就是y值
    y = (-b-ws[0, 0]*x)/ws[1, 0]
    ax.plot(x, y)

    for i in range(np.shape(yMat[0, :])[1]):
        if yMat[0, i] > 0:
            ax.plot(xMat[i, 0], xMat[i, 1], 'cx')
        else:
            ax.plot(xMat[i, 0], xMat[i, 1], 'kp')

    # 找到支持向量，并在图中标红
    for i in range(100):
        if alphas[i] > 0.0:
            ax.plot(xMat[i, 0], xMat[i, 1], 'ro')
    plt.show()

def kernelTrans(X,A,KTup):
     m,n = np.shape(X)
     K = np.mat(np.zeros((m,1)))
     if KTup[0]=='lin':
         K = X*A.T
     elif KTup[0]=='rbf':
         for j in range(m):
             deltaRow = X[j,:] - A
             K[j] = deltaRow*deltaRow.T
         K = np.exp(K/(-1*KTup[1]**2))
     else:raise NameError('Houston We Have a Problem--\ That Kernel is not recognized')
     return K
'''
if __name__ == "__main__":
    # 获取特征和目标变量
    dataArr, labelArr = loadDataSet(traindatadir+'input/6.SVM/testSet.txt')
    # print labelArr
    # b是常量值， alphas是拉格朗日乘子
    #b, alphas = smoSimple(dataArr, labelArr, 0.6, 0.001, 40)
    b, alphas = smoP(dataArr, labelArr, 0.6, 0.001, 40)
    print('/n/n/n')
    print('b=', b)
    print ('alphas[alphas>0]=', alphas[alphas > 0])
    print ('shape(alphas[alphas > 0])=',np.shape(alphas[alphas > 0]))
    for i in range(100):
        if alphas[i] > 0:
            print(dataArr[i], labelArr[i])
    # 画图
    ws = calcWs(alphas, dataArr, labelArr)
    plotfig_SVM(dataArr, labelArr, ws, b, alphas)
'''
###如果想对其分类，还是得先得到超平面，上面已经帮我们做了
def fenlei():
    dataArr, labelArr = loadDataSet(traindatadir + 'input/6.SVM/testSet.txt')
    b, alphas = smoP(dataArr, labelArr, 0.6, 0.001, 40) #这里最后的参数没有用，无视它
    ws = calcWs(alphas, dataArr, labelArr)
    #现在对数据进行分类
    datMat=np.mat(dataArr)
    m,n=np.shape(datMat)
    #truevalue大于0，那就属于1类，小于0就属于-1类，可以通过labelArr来判断是非正确
    for i in range(m):
        truevalue=datMat[i] * np.mat(ws) + b
        if  truevalue>0:
             print('这是1类,','truevalue===',truevalue,',labelArr[%d]====' %i,labelArr[i])
        elif truevalue<0:
            print('这是-1类,', 'truevalue===', truevalue, ',labelArr[%d]====' % i, labelArr[i])

#利用核函数进行分类的径向基测试函数
def testRbf(k1=0.01):
    dataArr,labelArr = loadDataSet(traindatadir+'input/6.SVM/testSetRBF.txt')
    b,alphas = smoP(dataArr,labelArr,200,0.0001,10000,('rbf',k1))
    dataMat=np.mat(dataArr)
    labelMat= np.mat(labelArr).transpose()
    svInd=np.nonzero(alphas.A>0)[0]
    sVs=dataMat[svInd]
    labelSV = labelMat[svInd]
    print("there are %d Support Vectors" %np.shape(sVs)[0])
    m,n=np.shape(dataMat)
    errorCount = 0
    for i in range(m):
        KernelEval = kernelTrans(sVs,dataMat[i,:],('rbf',k1))
        predict = KernelEval.T*np.multiply(labelSV,alphas[svInd]) + b
        if np.sign(predict)!= np.sign(labelArr[i]):
            errorCount+=1
    print("the training error rate is:%f" %(float(errorCount)/m) )
    dataArr,labelArr = loadDataSet(traindatadir+'input/6.SVM/testSetRBF2.txt')
    errorCount=0
    dataMat=np.mat(dataArr)
    labelMat=np.mat(labelArr).transpose()
    m,n = np.shape(dataMat)
    for i in range(m):
        KernelEval = kernelTrans(sVs,dataMat[i,:],('rbf',k1))
        predict = KernelEval.T*np.multiply(labelSV,alphas[svInd]) + b
        if np.sign(predict)!= np.sign(labelArr[i]):
            errorCount+=1
    print("the training error rate is:%f" %(float(errorCount)/m) )

testRbf()
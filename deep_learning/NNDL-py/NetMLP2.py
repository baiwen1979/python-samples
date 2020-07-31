# coding=utf-8
"""NetMLP2.py
~~~~~~~~~~~~~~
改进版的多层感知器神经网络，实现了前向反馈神经网络的随机梯度下降学习算法。
改进： 增加了交叉熵（cross-entropy）价值函数，正规化和更好的网络权重初始化
"""
#### 导人库
# 标准库
import json
import random
import sys
# 第三方库
import numpy as np

#### 二次和交叉熵价值函数 ####
# 工具类：表示交叉熵（Cross Entropy）价值函数
class CrossEntropyCost(object):
    @staticmethod
    def fn(a, y):
        """价值函数，返回关于激活值a和期望输出y的代价"""
        return np.sum(np.nan_to_num(-y * np.log(a)-(1-y) * np.log(1-a)))
    
    @staticmethod
    def delta(z, a, y):
        """计算输出层的输出误差"""
        return a - y

# 工具类：表示二次（Quadratic）价值函数
class QuadraticCost(object):
    @staticmethod
    def fn(a, y):
        """价值函数，返回关于激活值a和期望输出y的代价"""
        return 0.5 * np.linalg.norm(a - y) ** 2

    @staticmethod
    def delta(z, a, y):
        """计算输出层的输出误差"""
        return (a - y) * sigmoid_prime(z)


# 主类：NetMLP, 改进的多层感知器神经网络
class NetMLP(object):
   
    # 构造方法
    def __init__(self, sizes, cost = CrossEntropyCost):
        """ 列表型参数sizes用来指定多层感知器神经网络各层的神经元个数。
        例如，如列表[2, 3, 1]表示三层的神经网络，其中第一层有2个神经元，
        第二层和第三层分别有3个和1个神经元。
        权重weights的初始化默认使用default_weight_initializer方法进行，
        这是一个新的改进版的权重初始化方法。
        """
        # 属性：层数(int)，即sizes列表的长度
        self.num_layers = len(sizes)
        # 属性：各层的神经元个数
        self.sizes = sizes
        # 调用默认的权重初始化方法
        self.default_weight_initializer()
        # 属性：价值函数
        self.cost = cost
    
    # 默认的权重初始化方法
    def default_weight_initializer(self):
        """默认的权重初始化方法采用改进版的初始化方式：
        将隐藏层的输入权重weights初始化为均值为0，标准偏差为神经元输入连接个数
        的平方根分之一的高斯随机变数
        偏置biases仍初始化为均值为0，标准偏差为1的高斯随机变数
        """
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x)/np.sqrt(x) 
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]
    # 大权重初始化方法
    def large_weight_initializer(self):
        """大权重初始化方法采用旧的初始化方式：
        网络隐藏层和输出层的偏置biases和连接权重weights按照高斯分布
        （均值为0，方差为1）随机初始化。
        """
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x) 
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    # 计算前向反馈(输出)
    def feedforward(self, a):
        '''返回以a为输入的网络输出'''
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    # 随机梯度下降训练
    def SGD(self, training_data, epochs, mini_batch_size, eta,
            lmbda = 0.0,
            evaluation_data=None,
            monitor_evaluation_cost=False,
            monitor_evaluation_accuracy=False,
            monitor_training_cost=False,
            monitor_training_accuracy=False):
        """使用小批量随机梯度下降训练神经网络。
        其中训练数据参数training_data是一个二元组(x,y)的列表，表示训练数据的输入及其期望的输出；
        epochs表示训练周期数；mini_batch_size表示采样时所用小批量的大小；eta为学习频率；
        lmbda为正规化参数；evaluation_data表示验证和测试数据；可以通过设置相应的标志，监测评估
        数据和测试数据的代码和精度；
        该方法返回一个包含4个列表的元组：关于评估数据的（每周期）代价，评估数据的精度，训练数据的
        代价，训练数据的精度。所有的值在每个训练周期结束时进行评估。比如，如果我们训练30个周期，则
        次元组的第一个元素则为30个包含每个周期的评估数据代价的元素的列表。如果没有设置的标志，则相应
        的列表为空。
        """
        # 获得评估数据集的大小
        if evaluation_data: n_data = len(evaluation_data)
        # 获得训练数据集的大小
        n = len(training_data)
        # 评估代价和评估精度
        evaluation_cost, evaluation_accuracy = [], []
        # 训练代价和训练精度
        training_cost, training_accuracy = [], []
        # 对于每个训练周期
        for j in xrange(epochs):
            # 随机地对训练数据进行重排
            random.shuffle(training_data)
            # 将训练数据划分为指定大小的(mini_batch_size)小批量训练数据集
            mini_batches = [training_data[k: k + mini_batch_size] 
                                for k in xrange(0, n, mini_batch_size)]
            # 对每个小批量训练集进行使用反向传播的梯度下降算法更新网络的权重和偏置
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta, lmbda, n)
            print "Epoch %s training complete" % j
            # 监测训练代价
            if monitor_training_cost:
                cost = self.total_cost(training_data, lmbda)
                training_cost.append(cost)
                print "Cost on training data: {}".format(cost)
            # 监测训练精度
            if monitor_training_accuracy:
                accuracy = self.accuracy(training_data, convert=True)
                training_accuracy.append(accuracy)
                print "Accuracy on training data: {} / {}".format(accuracy, n)
            # 监测评估代价
            if monitor_evaluation_cost:
                cost = self.total_cost(evaluation_data, lmbda, convert=True)
                evaluation_cost.append(cost)
                print "Cost on evaluation data: {}".format(cost)
            # 监测评估精度
            if monitor_evaluation_accuracy:
                accuracy = self.accuracy(evaluation_data)
                evaluation_accuracy.append(accuracy)
                print "Accuracy on evaluation data: {} / {}".format(
                    self.accuracy(evaluation_data), n_data)
            print
        # 返回评估和训练结果（代价和精度）
        return evaluation_cost, evaluation_accuracy, training_cost, training_accuracy

    # 使用小批量梯度下降更新网络权重和偏置
    def update_mini_batch(self, mini_batch, eta, lmbda, n):
        """通过利用反向传播到单个小批量的应用梯度下降来更新网络的权重和偏置。mini_batch是二元组(x,y)
        的列表，eta是学习频率，lmbda为正规化参数，n为整个训练数据集的大小"""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # 1: 输入训练样本集，由mini_batch参数提供
        # 2: 对于每个训练样本x及其期望输出y
        for x, y in mini_batch:
            # 调用反向传播算法函数计算与训练样本x相关的代价梯度值
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        # 3: 梯度下降：更新权重和偏置向量
        self.weights = [(1 - eta * (lmbda / n)) * w - (eta / len(mini_batch)) * nw 
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta / len(mini_batch)) * nb 
                       for b, nb in zip(self.biases, nabla_b)]

    # 使用反向传播算法计算和训练样本x相关代价的梯度值
    def backprop(self, x, y):
        """返回一个二元组(nabla_b, nabla_w)，表示价值函数的梯度值。
        nabla_b和nabla_w是numpy数组的逐层列表"""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # 1. 输入(训练样本集)x: 设置输入层的激活值
        activation = x
        activations = [x] # 用来存储各层所有激活值的列表
        zs = [] # 用来存储各层z向量的列表

        # 2. 前向反馈: 对于每一层,计算相应的z向量和激活向量a
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
               
        # 3. 输出误差: 使用BP1方程计算输出（L层）误差向量
        delta = (self.cost).delta(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # 4. 反向传播误差: 对于从后往前的每一层L - 1, L - 2, ... 2 依次计算各层的误差向量误差
        for l in xrange(2, self.num_layers):
            # BP2
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            # BP3
            nabla_b[-l] = delta
            # BP4  
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        # 5. 输出: 成本函数关于偏置b和权重w的梯度
        return (nabla_b, nabla_w)
    
    # 计算准确度（精度）
    def accuracy(self, data, convert=False):
        """返回data中神经网络输出正确结果的数量。神经网络的输出假设为最后一层具有最高激
        活值神经元的索引。
        如果数据集data是验证或测试数据（通常情况），标志convert应该设为False。如果
        数据集data是训练数据，则设置为True. 鉴于结果y在不同数据集中表示方法的不同，
        需要设置此标志，表示是否需要在不同的表示中进行转换。对于不同数据集使用不同的表示
        方式可能看起来奇怪，为何不使用同样的表示方式呢？ 这样做是为了效率 -- 该程序通常
        评估训练数据中的代价以及其他数据集中的准确度，这些都是不同类型的计算，并且使用不
        同的表示可以加快速度。关于表示方式的更多细节可在mnist_loader.load_data_wrapper
        中找到
        """
        if convert:
            results = [(np.argmax(self.feedforward(x)), np.argmax(y))
                       for (x, y) in data]
        else:
            results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in data]
        return sum(int(x == y) for (x, y) in results)
    
    # 计算总代价
    def total_cost(self, data, lmbda, convert=False):
        """返回数据集data的总代价。如果数据集为训练数据（通常情况），标志convert
        应设置为False， 否则（验证和测试数据）为True。
        """
        cost = 0.0
        for x, y in data:
            a = self.feedforward(x)
            if convert: y = vectorized_result(y)
            cost += self.cost.fn(a, y) / len(data)
        cost += 0.5 * (lmbda/len(data)) * sum(
            np.linalg.norm(w) ** 2 for w in self.weights)
        return cost
    
    # 保存神经网络
    def save(self, filename):
        """保存神经网络到filename中."""
        data = {
            "sizes": self.sizes,
            "weights": [w.tolist() for w in self.weights],
            "biases": [b.tolist() for b in self.biases],
            "cost": str(self.cost.__name__)
        }
        f = open(filename, "w")
        json.dump(data, f)
        f.close()

# 加载神经网络
def load(filename):
    """从文件filename加载神经网络，返回一个神经网络的实例."""
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(data["sizes"], cost = cost)
    net.weights = [np.array(w) for w in data["weights"]]
    net.biases = [np.array(b) for b in data["biases"]]
    return net   

#### 辅助函数
def vectorized_result(j):
    """返回一个第j个位置为1.0，而其他位置为0的10维单位向量。
    此函数用来将一个数字(0...9)转换为一个神经网络的相应的期望输出
    """
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

def sigmoid(z):
    """sigmoid激活函数。计算某层神经元的加权输入向量z的激活值。其中参数z是一个
    向量或Numpy数组
    """
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_prime(z):
    """返回sigmoid函数的导数"""
    return sigmoid(z) * (1 - sigmoid(z))




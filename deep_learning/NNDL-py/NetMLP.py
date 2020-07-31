# coding=utf-8
#### 导人库
# 标准库
import random
# 第三方库
import numpy as np

# 类：NetMLP, 多层感知器的神经网络
class NetMLP(object):
   
    # 构造方法
    def __init__(self, sizes):
        """ 列表型参数sizes用来指定多层感知器神经网络各层的神经元个数。例如，如列表
        [2, 3, 1]表示三层的神经网络，其中第一层有2个神经元，第二层和第三层分别有3个
        和1个神经元。网络隐藏层和输出层的偏置biases和连接权重weights按照高斯分布
        （均值为0，方差为1）随机初始化。第一层假设为输入层，此层的神经元无需设置偏置，
        因为偏置仅仅是用来根据后面各层（隐藏层）计算输出的。
        """
        # 属性：层数(int)，即sizes列表的长度
        self.num_layers = len(sizes)
        # 属性：隐藏和输出层的神经元偏置(list<mat>)，使用高斯分布进行随机初始化
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        # 属性：隐藏和输出层神经元的连接权重(list<mat>)，使用高斯分布进行随机初始化
        self.weights = [np.random.randn(y, x) 
                        for x, y in zip(sizes[:-1], sizes[1:])]

    # 计算前向反馈(输出)
    def feedforward(self, a):
        '''返回以a为输入的网络输出'''
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    # 随机梯度下降(Stochastic Gradient Descent)训练
    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data = None):
        """使用小批量随机梯度下降训练神经网络。其中训练数据参数training_data是一个二元组(x,y)的
        列表，表示训练数据的输入及其期望的输出；epochs表示训练周期数；mini_batch_size表示采样时
        所用小批量的大小；eta为学习速率；如果提供了可选的测试数据test_data，该程序将在每个训练周期
        后对网络进行评估，并输出测试进度。这对进度跟踪很有用，但会显著地降低速度"""
        n_test = 0
        # 获得测试数据的大小
        if test_data: n_test = len(test_data)
        # 获得训练数据的大小
        n = len(training_data)
        # 对于每个训练周期
        for j in xrange(epochs):
            # 随机地对训练数据进行重排
            random.shuffle(training_data)
            # 将训练数据划分为指定大小的(mini_batch_size)小批量训练数据集
            mini_batches = [training_data[k: k + mini_batch_size] 
                                for k in xrange(0, n, mini_batch_size)]
            # 对每个小批量训练集进行使用反向传播的梯度下降算法更新网络的权重和偏置
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            # 若提供测试数据，则对当前训练结果进行测试评估，并输出
            if test_data:
                print("Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test))
            else:
                print("Epoch {0} complete".format(j))

    # 使用小批量梯度下降更新网络权重和偏置
    def update_mini_batch(self, mini_batch, eta):
        """通过应用梯度下降和反向传播更新单个小批量的网络的权重和偏置。mini_batch是二元组(x,y)
        的列表，并且eta是学习速率"""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # 1: 输入训练样本集，由mini_batch参数提供
        # 2: 对于每个训练样本x及其期望输出y
        for x, y in mini_batch:
            # 调用反向传播算法函数与训练样本x相关的代价梯度值
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        # 3: 梯度下降：更新权重和偏置向量
        self.weights = [w - (eta / len(mini_batch)) * nw 
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
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
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

    # 网络评估函数，并返回神经网络输出正确结果的测试次数
    def evaluate(self, test_data):
        """返回神经网络输出正确结果的测试次数。神经网络的输出假定为最后一层
        中具有最高激活值神经元的索引"""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)
    
    # 计算成本函数关于输出激活值的偏导数向量
    def cost_derivative(self, output_activations, y):
        """返回用来作为输出层激活值的偏导数向量"""
        return (output_activations - y)
    

# 辅助函数：Sigmoid激活函数
def sigmoid(z):
    """sigmoid激活函数。计算某层神经元的加权输入向量z的激活值。其中参数z是一个
    向量或Numpy数组
    """
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_prime(z):
    """返回sigmoid函数的导数"""
    return sigmoid(z) * (1 - sigmoid(z))


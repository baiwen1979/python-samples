# coding=utf-8

import MnistLoader as loader
import NetMLP as network
import NetMLP2 as network2

def testNet():
    training_data, validation_data, test_data = loader.load_data_wrapper()
    net = network.NetMLP([784, 30, 10])
    net.SGD(training_data, 30, 10, 0.01, test_data = test_data)

def testNet2():
    training_data, validation_data, test_data = loader.load_data_wrapper()
    net = network2.NetMLP([784, 30, 10], cost = network2.CrossEntropyCost)
    net.SGD(training_data[:1000], 30, 10, 0.5,lmbda = 5.0,
        evaluation_data = validation_data[:100],
        monitor_evaluation_accuracy = True,
        monitor_evaluation_cost = True,
        monitor_training_accuracy = True,
        monitor_training_cost = True)

def main():
    testNet()
    # testNet2()

if __name__ == '__main__':
    main()

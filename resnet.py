#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf
import tensorlayer as tl
import time
import logging
import sys
from data import DATA


def build_network(x, is_train=True, reuse=False):
    with tf.variable_scope("nn", reuse=reuse):
        tl.layers.set_name_reuse(reuse)
        network = tl.layers.InputLayer(x, name='input')
        network = tl.layers.Conv2d(network, n_filter=64, filter_size=(5, 5), strides=(1, 1), padding='SAME', name='cnn0')
        network = tl.layers.BatchNormLayer(network, name='norm0', act=tf.nn.relu, is_train=is_train)
        for i in range(3):
            network_ = tl.layers.Conv2d(network, n_filter=64, filter_size=(5, 5), strides=(1, 1), padding='SAME', name='res_cnn1_%s' % i)
            network_ = tl.layers.BatchNormLayer(network_, act=tf.nn.relu, is_train=is_train, name='res_norm1_%s' % i)
            network_ = tl.layers.Conv2d(network_, n_filter=64, filter_size=(5, 5), strides=(1, 1), padding='SAME', name='res_cnn2_%s' % i)
            network_ = tl.layers.BatchNormLayer(network_, act=tf.nn.relu, is_train=is_train, name='res_norm2_%s' % i)
            network = tl.layers.ElementwiseLayer([network, network_], tf.add, name='res_add_%s' % i)
            
        network = tl.layers.Conv2d(network, n_filter=1, filter_size=(1, 1), strides=(1, 1), padding='SAME', name='cnn1')
        network = tl.layers.BatchNormLayer(network, name='norm1', act=tf.nn.relu, is_train=is_train)
        network = tl.layers.FlattenLayer(network, name='flatten0')
        network = tl.layers.DenseLayer(network, n_units=64, act = tf.nn.relu, name='relu0')
        network = tl.layers.DenseLayer(network, n_units=2, act = tf.identity,  name='output')
        return network


def main_test_cnn_layer(N, start_from = -1):
    f_channel = 2
    db = DATA(N)
    sess = tf.InteractiveSession()

    # Define the batchsize at the begin, you can give the batchsize in x and y_
    # rather than 'None', this can allow TensorFlow to apply some optimizations
    # – especially for convolutional layers.
    batch_size = 256

    X_val, y_val = db.load_vld()
    X_test, y_test = db.load_tst()
    X_train, y_train = db.load_trn()

    x = tf.placeholder(tf.float32, shape=[batch_size, N, N, f_channel])   # [batch_size, height, width, channels]
    y_ = tf.placeholder(tf.int64, shape=[batch_size,])

    network = build_network(x, is_train=True, reuse=False)
    
    y = network.outputs
    cost = tl.cost.cross_entropy(y, y_, 'cost')
    correct_prediction = tf.equal(tf.argmax(y, 1), y_)
    acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    network_test = build_network(x, is_train=False, reuse=True)
    cost_test = tl.cost.cross_entropy(network_test.outputs, y_, 'cost')
    correct_prediction_test = tf.equal(tf.argmax(network_test.outputs, 1), y_)
    acc_test = tf.reduce_mean(tf.cast(correct_prediction_test, tf.float32))

    # train
    n_epoch = 101
    learning_rate = 0.0001
    print_freq = 5
    checkpoint_freq = 5

    train_params = network.all_params
    train_op = tf.train.AdamOptimizer(learning_rate, beta1=0.9, beta2=0.999,
        epsilon=1e-08, use_locking=False).minimize(cost, var_list=train_params)

    tl.layers.initialize_global_variables(sess)
    if start_from >= 0:
        load_params = tl.files.load_npz(name="nn"+str(start_from)+".npz")
        tl.files.assign_params(sess, load_params, network)
    network.print_params()
    network.print_layers()
    

    print('   learning_rate: %f' % learning_rate)
    print('   batch_size: %d' % batch_size)

    for epoch in range(start_from+1, n_epoch):
        start_time = time.time()
            
        for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):
            feed_dict = {x: X_train_a, y_: y_train_a}
            feed_dict.update( network.all_drop )        # enable noise layers
            sess.run(train_op, feed_dict=feed_dict)

        if epoch % print_freq == 0:
            print("Epoch %d of %d took %fs" % (epoch, n_epoch, time.time() - start_time))
            train_loss, train_acc, n_batch = 0, 0, 0
            for X_train_a, y_train_a in tl.iterate.minibatches(X_train, y_train, batch_size, shuffle=True):
                dp_dict = tl.utils.dict_to_one( network.all_drop )    # disable noise layers
                feed_dict = {x: X_train_a, y_: y_train_a}
                feed_dict.update(dp_dict)
                err, ac = sess.run([cost_test, acc_test], feed_dict=feed_dict)
                train_loss += err; train_acc += ac; n_batch += 1
            print("   train loss: %f" % (train_loss/ n_batch))
            print("   train acc: %f" % (train_acc/ n_batch))
            val_loss, val_acc, n_batch = 0, 0, 0
            for X_val_a, y_val_a in tl.iterate.minibatches(X_val, y_val, batch_size, shuffle=True):
                dp_dict = tl.utils.dict_to_one( network.all_drop )    # disable noise layers
                feed_dict = {x: X_val_a, y_: y_val_a}
                feed_dict.update(dp_dict)
                err, ac = sess.run([cost_test, acc_test], feed_dict=feed_dict)
                val_loss += err; val_acc += ac; n_batch += 1
            print("   val loss: %f" % (val_loss/ n_batch))
            print("   val acc: %f" % (val_acc/ n_batch))

        if epoch % checkpoint_freq == 0:
            tl.files.save_npz(network.all_params, name="nn"+str(epoch)+".npz")
            

    print('Evaluation')
    test_loss, test_acc, n_batch = 0, 0, 0
    for X_test_a, y_test_a in tl.iterate.minibatches(X_test, y_test, batch_size, shuffle=True):
        dp_dict = tl.utils.dict_to_one( network.all_drop )    # disable noise layers
        feed_dict = {x: X_test_a, y_: y_test_a}
        feed_dict.update(dp_dict)
        err, ac = sess.run([cost_test, acc_test], feed_dict=feed_dict)
        test_loss += err; test_acc += ac; n_batch += 1
    print("   test loss: %f" % (test_loss/n_batch))
    print("   test acc: %f" % (test_acc/n_batch))

    sess.close()


if __name__ == '__main__':
    logging.basicConfig(filename='resnet.log', level=logging.DEBUG)
    if len(sys.argv) > 1:
        main_test_cnn_layer(9, int(sys.argv[1]))
    else:
        main_test_cnn_layer(9)

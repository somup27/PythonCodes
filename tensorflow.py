# -*- coding: utf-8 -*-
"""tensorflow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/146DJYxXxQazESPltEAkfZOsi5JvQT4c8
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST",one_hot = True)

x_train, y_train = mnist.train.next_batch(60000)
x_test, y_test = mnist.test.images, mnist.test.labels

features = tf.placeholder(shape = [None,784], dtype = 'float')
labels = tf.placeholder(shape = [None, 10], dtype = 'float')

batch_size = 1000
epochs = 250
n_classes = 10
layer1_size = 100
layer2_size = 300

weight1 = tf.Variable(tf.random_normal(shape = [784,layer1_size]))
bias1 = tf.Variable(tf.random_normal(shape = [layer1_size]))

weight2 = tf.Variable(tf.random_normal(shape = [layer1_size,layer2_size]))
bias2 = tf.Variable(tf.random_normal(shape = [layer2_size]))

weight3 = tf.Variable(tf.random_normal(shape = [layer2_size,n_classes]))
bias3 = tf.Variable(tf.random_normal(shape = [n_classes]))

layer1 = tf.matmul(features,weight1) + bias1
layer1 = tf.nn.relu(layer1)

layer2 = tf.matmul(layer1,weight2) + bias2
layer2 = tf.nn.relu(layer2)

final_layer = tf.matmul(layer2,weight3)+bias3

cost = tf.nn.softmax_cross_entropy_with_logits(logits = final_layer, labels = labels)
cost = tf.reduce_mean(cost)
optimizer = tf.train.AdamOptimizer(learning_rate = 0.005).minimize(cost)

with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  for epoch in range(epochs):
    start = 0
    epoch_cost = 0
    while start < 60000:
      end = start + batch_size
      batch_x, batch_y = x_train[start:end], y_train[start:end]
      opt, c = sess.run([optimizer,cost], feed_dict = {features: batch_x, labels: batch_y})
      epoch_cost += c
      start += batch_size
    print("Finished epoch",epoch+1," out of",epochs," Cost:",epoch_cost)
  correct = tf.equal(tf.argmax(final_layer,1),tf.argmax(labels,1))
  accuracy = tf.reduce_mean(tf.cast(correct,'float'))
  accuracy = sess.run(accuracy, feed_dict = {features:x_test, labels:y_test})
  print("Model trained with testing accuracy of: ",accuracy)
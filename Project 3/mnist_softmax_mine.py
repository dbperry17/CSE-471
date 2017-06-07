from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf
x = tf.placeholder(tf.float32, [None, 784])
#W = tf.Variable(tf.zeros([784, 10]))
#b = tf.Variable(tf.zeros([10]))

#y = tf.nn.softmax(tf.matmul(x, W) + b)
# This is equivalent to y = f(x) = Softmax(Wx+b)

#Now we want this: 
#h = sigmoid(W_1*x + b_1)
#y = softmax(W_2*h + b_2)
#We want one hidden layer with 500 neurons in it.

#weights for the input to hidden layer
W_1 = tf.Variable(tf.random_normal ([784, 500]))
#instead of zeroes use random initialization


#weights for the hidden to output layer
W_2 = tf.Variable(tf.random_normal ([500, 10]))
#instead of zeroes use random initialization
#500 for the hidden layer of 500 neurons,
#10 because we want "to produce 10-dimensional
#vectors of evidence for the difference classes."
#(Same reason W above is [784, 10])

b_1 = tf.Variable(tf. random_normal ([500]))
#biases for hidden layer

b_2 = tf.Variable(tf. random_normal ([10]))
#biases for output layer

h = tf.nn.sigmoid(tf.matmul(x, W_1)+ b_1)
#output of hidden layer h = sigmoid(W_ih *X + b_ih)

y = tf.nn.softmax(tf.matmul(h, W_2) + b_2)
#Softmax output layer


#Note to self: DO NOT ALTER THE CODE BELOW. Project 3b says training and
#              testing remain the same.


#training
y_ = tf.placeholder(tf.float32, [None, 10])
#cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
#First line is "numerically unstable", so use the following instead:
cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

#launch in interactive session
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
for _ in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

#evaluating the model
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

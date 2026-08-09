1. Tensorflow is one of the most popular deep learning framework. You can develop and train models using Python and several other languages.

![1.png](./images/1.png)

Then easily deploy them in cloud or on-prem, in browser or on mobile devices, no matter what language you use. 

![2.png](./images/2.png)

2. Tensorflow is a powerful machine learning library that is developed by Google Brain team and it powers many google services like google search. 

At its core, it is very similar to Numpy but with GPU support. It supports distributive computing across multiple devices and servers.

It also includes a Just-In-Time Compiler (JIT) compiler to create computational graph. It does this by extracting the computation graph from a python function and then running independent operations in parallel. These computation graphs can be exported to a portable format. This means, we can train a tensorflow model in one environment like use python on windows machine can also be run on android device using java. 

Most of the time, we will use high level APIs like Keras but when you need more flexibility, you will use the low-level Python API handling tensors directly. 

Tensorflow runs not only on Windows, Linux and Mac but also on mobile devices using tensorflow lite, including Android and iOS both.

If you don't want to use python API then you can use C++, Java, Go and swift APIs. There is even a Javascript implementation called TensorFlow.js which can be used in the browser by running the tensorflow model in the browser directly. Tensorflow lite can be used for android and iOS.

There is tensorflow extended which is a set of libraries built by google to productionize tensorflow projects. So, this includes tools for data validation, pre-processing, model analysis and you can save these models using REST APIs using tensorflow serving. 

Tensorflow serving is very important because it is very easy to create ML solutions that have one or two users but what happens when you scale to a hundreds of thousands of users ? Then there is tensorboard which is great for visualization.

Finally, Tensorboard Hub provides to easily download and reuse pretrained models.

3. Neural Networks and Images:

Let's see Fashion-MNIST dataset. It is made up of Zalando's images. It contains a training set of 60,000 images and a test set of 10,000 images. Each image is 28x28 pixels and the images are in grayscale, associated with the labels from 10 classes.  

Each training and test example assigned to one of the following labels.

![3.png](./images/3.png)

Now, this is what the neural network that we use to help us classify the 10 categories of the FASHION-MNIST dataset looks like. 

![4.png](./images/4.png)

We had 784 input nodes and each of these node corresponds to a pixel of that image. We then have two hidden layers with 128 and 64 nodes. The output layer has 10 nodes corresponding to the 10 different categories. You have to find which class has the highest probability so that more likely the image belongs to that class.

Check the notebook `1.ipynb` for the code.

4.  


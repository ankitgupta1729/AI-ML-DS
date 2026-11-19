## 01_sentiment-analysis-with-logistic-regression

### 01_lecture-logistic-regression

1. 01_01_welcome-to-the-nlp-specialization.en
==========================================

>> I want you to meet my friends, Younes and Lukasz, the instructors of this specialization. >> Hi, everyone. >> Welcome to the specialization. >> I know Younes for many years. He is an instructor at Stanford University and has also helped me create the deep learning specialization. Over the years, Younes has taught hundreds of students learning AI and machine learning and NLP and other topics for the first time and he's also mentor students on a huge variety of AI related projects.

So I really thrilled to have you with us. >> Thanks for the introduction and it is always great working with you. >> Lukasz is a member of the Google Brain team where he does research on deep learning and NLP. So everything from machine translation to parsing, he is the co-author of Google's TensorFlow system as well as of the transformer network. And so his work has had a huge influence on all of NLP and AI. I'm really excited to also have Lukasz as an instructor of the specialization.

>> Thanks for the introduction, Andrew. >> Younes and Lukasz will walk you through the most important concepts in natural language processing. NLP has changed a lot over the last several decades. The field has started off using primarily rule-based systems where someone might code of a rule like you see the word good, then assume this is a positive customer review to then using probabilistic systems that perform much better. But still require a lot of hand engineering to know where NLP relies much more on machine learning and deep learning.

>> More recently with the rise of powerful computers, we can now train end-to-end systems that would have been impossible to train a few years ago. We can now capture more complicated patterns and we can use these models in question answering in chatbots, and then other applications. >> Many of these applications are built with attention models, which you are going to learn in this specialization. A few years ago, these models would take weeks or even months to train.

But with attention, you can train these models in just a few hours. >> In this specialization, you learn to build NLP technologies including the same technologies as what's deployed in many large commercial systems. In the first course, you learn about classification and vector spaces. Younes, can you tell us a bit about the first course? >> Sure, in course one, you will learn to distinguish between pieces of text with positive sentiments and negative sentiments.

You will do so using logistic regression and naive Bayes classifiers. You will also learn to represent words, queries and documents including other pieces of text as numbers in vectors. You will build your first machine translation system and you will learn about locality sensitive hashing which is just a method, that will help you with efficient search. >> Thanks Younes. After the first course, you then go on to the second course in which you learn probabilistic models in NLP.

So these are things like given a few words, what is the probability of the next word being the word the versus of, versus something else. So these are algorithms that all of us are maybe using almost every day. And in this specialization, you will learn how to build these algorithms yourself. After the first two courses with the foundation that that gives you, you then go on to the third course which teaches you sequence models. And finally, in the fourth course, you learn about attention models and this will take you up to state of the art NLP models useful things like chatbots question answering and text summarization.

Younes, you want to say a few words about that? >> By the time you complete course four, you will be able to implement state of the art neural machine translation, summarization, question answering and chatbots. We will show you how you can combine attention and parallel computing to build these systems from the ground up. These models have high impact in industry. They could be used, for example, to automate call centers or businesses can use them to make sense of large volumes of data.

>> I'm really excited for everyone to get started to take these courses, learn these technologies and to go build some great NLP systems. >> Let's get started. >> Awesome, see you in the classroom. >> Let's jump in.

2. 01_02_welcome-to-course-1.en
============================

Welcome to this first course of NLP in which you'll learn about classification and vector spaces. You'll also learn about the application of these ideas to problems like sentiment analysis and word translation. For example, let's say you have 1,000 product reviews, so pieces of texts written by users. Can you build a system to automatically go through all of these product reviews to figure out what fraction of them are positive reviews versus negative reviews?

This course will teach you how. Lukasz, can you say a few words about this first course? Sure. In the first week, you'll learn how to represent text as a vector and build a classifier that will classify whether a sample text is a positive sentiment or a negative one. You will use logistic regression for that. In the second week, you'll use the Naive Bayes classifier on the same problem. In the third week, you'll learn about vector space models. You'll learn how to represent text documents like tweets, articles, queries, or any object that contains of text as a vector.

This is important in information retrieval, in indexing, in relevancy ranking, and also in information filtering. For example, when you look up a query online, the algorithm relies on all of these concepts to give you back your results. Finally, in week 4, you will build your first simple machine translation system and you'll make use of locality sensitive hashing to improve the performance of nearest neighbor search. Thanks, Younes and Lukasz. With that, let's get started and go on to the next video.

3. 01_04_week-introduction.en
==========================

Welcome to the first week of Course 1. This week is all about logistic regression, which is a very important tool used in many applications in NLP. Logistic regression algorithms are particularly useful because they are easy to train and provide you with a good baseline result. This week you'll use logistic regression for sentiment analysis of tweets. You will first process your data, then you train your model and finally, you will test the accuracy of your model.

We've designed these courses so that each week I'll give you the overview of the material and Younes will give you the details. Take it away, Younes. Okay, Great. Follow me.

4. 01_05_supervised-ml-sentiment-analysis.en
=========================================

![1.png](./images/1.png)
![2.png](./images/2.png)
![3.png](./images/3.png)
![4.png](./images/4.png)
![5.png](./images/5.png)
![6.png](./images/6.png)
![7.png](./images/7.png)

Welcome and this week you're going to learn about supervised machine learning and specifically you're going to learn about logistic regression. In order for you to implement logistic regression, you need to take a few steps. In this video you will learn about the steps required in order to implement this algorithm, so let's take a look. In supervised machine learning you have input features X and a set of labels Y. Now to make sure you're getting the most accurate predictions based on your data, your goal is to minimize your error rates or cost as much as possible.

And to do this, you're going to run your prediction function which takes in parameters data to map your features to output labels Y hat. Now the best mapping from features to labels is achieved when the difference between the expected values Y and the predicted values Y hat is minimized. Which the cost function does by comparing how closely your output Y hat is to your label Y. Then you can update your parameters and repeat the whole process until your cost is minimized.

So let's take a look at the supervised machine learning classification task of sentiment analysis. In this example you have the tweet, let's say, I'm happy because I'm learning NLP. And the objective in this task is to predict whether a Tweet has a positive or a negative sentiment. And you'll do this by starting with a training set where tweets with a positive sentiment have a label of one, and the tweets with a negative sentiment have a label of zero.

For this task you will be using your logistic regression classifier which assigns its observations to two distinct classes. Next up I'll show you how to do this. So to get started building a logistic regression classifier that's capable of predicting sentiments of an arbitrary tweet. You will first process the raw tweets in your training sets and extract useful features. Then you will train your logistic regression classifier while minimizing the cost.

And finally you'll be able to make your predictions. So in this video you learned about the steps required for you to classify a tweet. Given the tweet, you should classify it to either be positive or negative. In order for you to do so, you first have to extract the features. Then you have to train your model. And then you have to classify the tweet based off your trained model. In the next video, you're going to learn how to extract these features. So let's take a look at how you can do that.

5. 01_07_vocabulary-feature-extraction.en
======================================

![8.png](./images/8.png)
![9.png](./images/9.png)
![10.png](./images/10.png)

Hello. Welcome back. In this video, you're going to learn how to represent a text as a vector. In order for you to do so, you first have to build a vocabulary and that will allow you to encode any text or any tweet as an array of numbers. So let's dive in and see how you can do this. Picture a list of tweets, visually it would look like this. Then your vocabulary, V, would be the list of unique words from your list of tweets. To get that list, you'll have to go through all the words from all your tweets and save every new word that appears in your search.

So in this example, you'd have the word I, then the word, am and happy, because, and so forth. But note that the word I and the word am would not be repeated in the vocabulary. Let's take this tweets and extract features using your vocabulary. To do so, you'd have to check if every word from your vocabulary appears in the tweet. If it does like in the case of the word I, you would assign a value of 1 to that feature, like this. If it doesn't appear, you'd assign a value of 0, like that.

In this example, the representation of your tweet would have six ones and many zeros. These correspond to every unique word from your vocabulary that isn't in the tweet. Now, this type of representation with a small relative number of non-zero values is called a sparse representation. Now let's take a closer look at this representation of these tweet. In the last slides, I walked you through extracting features to represent the tweet based on a vocabulary and I arrived at this vector.

This representation would have a number of features equal to the size of your entire vocabulary. This would have a lot of features equal to 0 for every tweet. With the sparse representation, a logistic regression model would have to learn n plus 1 parameters, where n would be equal to the size of your vocabulary and you can imagine that for large vocabulary sizes, this would be problematic. It would take an excessive amount of time to train your model and much more time than necessary to make predictions.

Given a text, you learned how to represent this text as a vector of dimension V. Specifically, you did this for a tweet and you were able to build a vocabulary of dimension V. Now as V gets larger and larger, you will face certain problems. In the next video, you will learn to identify these problems.

6. 01_09_negative-and-positive-frequencies.en
==========================================

![11.png](./images/11.png)
![12.png](./images/12.png)
![13.png](./images/13.png)
![14.png](./images/14.png)
![15.png](./images/15.png)

We'll now learn to generates counts, which you can then use as features into your logistic regression classifier. Specifically, given a word, you want to keep track of the number of times, that's where it shows up as the positive class. Given another word you want to keep track of the number of times that word showed up in the negative class. Using both those counts, you can then extract features and use those features into your logistic regression classifier.

So let's take a look at how you can do that. It is helpful to first imagine how these two classes would look. Here for instance, you could have a corpus consisting of four tweets. Associated with that corpus, you would have a set of unique words, your vocabulary. In this example, your vocabulary would have eight unique words. For this particular example of sentiment analysis, you have two classes. One class associated with positive sentiment and the other with negative sentiment.

So taking your corpus, you'd have a set of two tweets that belong to the positive class, and the sets of two tweets that belong to the negative class. Let's take the sets of positive tweets. Now, take a look at your vocabulary. To get the positive frequency in any word in your vocabulary, you will have to count the times as it appears in the positive tweets. For instance, the word happy appears one time in the first positive tweet, and another time in the second positive tweet.

So it's positive frequency is two. The complete table looks like this. Feel free to take a pause and check any of its entries. The same logic applies for getting the negative frequency. However, for the sake of clarity, look at some example, the word am appears two times in the first tweet and another time in the second one. So it's negative frequency is three. Take a look at the entire table for negative frequencies and feel free to check its values. So this is the entire table with the positive and negative frequencies for your corpus.

In practice when coding, this table is a dictionary mapping from a word class there to its frequency. So it maps the word and its corresponding class to the frequency or the number of times that's where it showed up in the class. You now know how to create a frequency dictionary, which maps a word and the class to the number of times that word showed up in the corresponding class. In the next video, you're going to use your frequency dictionary to represent a tweet.

7. 01_10_feature-extraction-with-frequencies.en
============================================

![16.png](./images/16.png)
![17.png](./images/17.png)
![18.png](./images/18.png)
![19.png](./images/19.png)
![20.png](./images/20.png)


Welcome back. You previously learned to encode a tweet as a vector of dimension V. You will now learn to encode a tweet or specifically represented as a vector of dimension 3. In doing so, you'll have a much faster speed for your logistic regression classifier, because instead of learning V features, you only have to learn three features. Let's take a look at how you can do this. You just saw that the frequency of a word in a class is simply the number of times that the word appears on the set of tweets belonging to that class and that this table is basically a dictionary mapping from word class pairs, to frequencies, or it just tells us how many times each word showed up in its corresponding class.

Now that you've built your frequencies dictionary, you can use it to extract useful features for sentiment analysis. What does a feature look like? Let's look at the arbitrary tweet m. The first feature would be a bias unit equal to 1. The second is the sum of the positive frequencies for every unique word on tweet m. The third is the sum of negative frequencies for every unique word on the tweet. So to extract the features for this representation, you'd only have to sum frequencies of words.

Easy. For instance, take the following tweets. Now let's look at the frequencies for the positive class from the last lecture. The only words from the vocabulary that don't appear on these tweets are happy and because. Now let's take a look at the second feature from the representation that you saw on the last slide. To get this value, you need to sum the frequencies of the words from the vocabulary that appear on the tweet. At the end, you get a value equal to eight.

Now let's get the value of the third feature. It is the sum of negative frequencies of the words from the vocabulary that appear on the tweet. For this example, you should get 11 after summing up the underlined frequencies. So far, this tweets, this representation would be equal to the vector 1, 8, 11. You now know how to represent a tweet as a vector of dimension 3. In the next video you will learn to pre-process your tweets and as a result, you will use those pre-processed words as words of your vocabulary.

8. 01_12_preprocessing.en
======================

![21.png](./images/21.png)
![22.png](./images/22.png)
![23.png](./images/23.png)
![24.png](./images/24.png)
![25.png](./images/25.png)
![26.png](./images/26.png)
![27.png](./images/27.png)

Hello, you will now learn about two major concepts of preprocessing. The first thing you'll learn about is called stemming and the second thing you will learn about is called stop words, and specifically you will learn how to use stemming and stop words to preprocess your texts. Let's take a look at how you can do this. Let's process this tweet. First, I remove all the words that don't add significant meaning to the tweets, aka stop words and punctuation marks.

In practice, you would have to compare your tweet against two lists. One with stop words in English and another with punctuation. These lists are usually much larger, but for the purpose of this example, they will do just fine. Every word from the tweet that also appears on the list of stop words should be eliminated. So you'd have to eliminate the word and, the word are, the word a, and the word at. The tweet without stop words looks like this. Note that the overall meaning of the sentence could be inferred without any effort.

Now, let's eliminate every punctuation mark. In this example, there are only exclamation points. The tweet without stop words and punctuation looks like this. However, note that in some contexts you won't have to eliminate punctuation. So you should think carefully about whether punctuation adds important information to your specific NLP task or not. Tweets and other types of texts often have handles and URLs, but these don't add any value for the task of sentiment analysis.

Let's eliminate these two handles and this URL. At the end of this process, the resulting tweets contains all the important information related to its sentiment. Tuning GREAT AI model is clearly a positive tweet and a sufficiently good model should be able to classify it. Now that the tweet from the example has only the necessary information, I will perform stemming for every word. Stemming in NLP is simply transforming any word to its base stem, which you could define as the set of characters that are used to construct the word and its derivatives.

Let's take the first word from the example. Its stem is tun, because adding the letter e, it forms the word tune. Adding the suffix ed, forms the word tuned, and adding the suffix ing, it forms the word tuning. After you perform stemming on your corpus, the word tune, tuned, and tuning will be reduced to the stem tun. So your vocabulary would be significantly reduced when you perform this process for every word in the corpus. To reduce your vocabulary even further without losing valuable information, you'd have to lowercase every one of your words.

So the word GREAT, Great and great would be treated as the same exact word. This is the final preprocess tweet as a list of words. Now that you're familiar with stemming and stop words, you know the basics of texts processing. In the next video, you can use your process_tweet function to extract a matrix x, which represents all the tweets in your data set.

9. 01_14_putting-it-all-together.en
================================

![28.png](./images/28.png)
![29.png](./images/29.png)
![30.png](./images/30.png)
![31.png](./images/31.png)

You will now use everything that you learned to create a matrix that corresponds to all the features of your training example. Specifically, I will walk you through an algorithm that allows you to generate this x matrix. Let's take a look at how you can build it. Previously, you saw how to preprocess a tweet like this one to get a list of words that contain all the relevant information for the sentiment analysis tasks in NLP. With that list of words, you would be able to get a nice representation using a frequency dictionary mapping.

And finally, get a vector with a bias unit and two additional features that store the sum of the number of times that every word on your process tweets appear in positive tweets and the sum of the number of times they appear in negative ones. In practice, you would have to perform this process on a set of m tweets. So given a set of multiple raw tweets, you would have to preprocess them one by one to get these sets of lists of words one for each of your tweets.

And finally, you'd be able to extract features using a frequencies dictionary mapping. At the end, you would have a matrix, X with m rows and three columns where every row would contain the features for each one of your tweets. The general implementation of this process is rather easy. First, you build the frequencies dictionary, then initialize the matrix X to match your number of tweets. After that, you'll want to go over through your sets of tweets carefully deleting stop words, stemming, deleting URLs, and handles and lower casing.

And finally, extract the features by summing up the positive and negative frequencies of the tweets. For this week's assignment, you've been provided some helper functions, build_freqs and process_tweet. However, you'll have to implement the function to extract the features of a single tweet. That was a lot of code, but at least now you have your X matrix. And in the next video, we will show you how you can feed in that X matrix into your logistic regression classifier.

Let's take a look at how you can do that.

10. 01_16_logistic-regression-overview.en
=====================================

![32.png](./images/32.png)
![33.png](./images/33.png)
![34.png](./images/34.png)
![35.png](./images/35.png)
![36.png](./images/36.png)
![37.png](./images/37.png)
![38.png](./images/38.png)
![39.png](./images/39.png)


You will now get an overview of logistic regression. Previously, you learned to extract features, and now you will use those extracted features to predict whether a tweet has a positive sentiment or a negative sentiment. Logistic regression makes use of a sigmoid function which outputs a probability between zero and one. Let's take a look at the overview of logistic regression. Just a quick recap. In supervised machine learning, you have input features and a sets of labels.

To make predictions based on your data, you use a function with some parameters to map your features to output labels. To get an optimum mapping from your features to labels, you minimize the cost function which works by comparing how closely your output Y hat is to the true labels Y from your data. After which the parameters are updated and you repeat the process until your cost is minimized. For logistic regression, this function F is equal to the sigmoid function.

The function used to classify in logistic regression H is the sigmoid function and it depends on the parameters Theta and then the features vector X superscripts i, where i is used to denote the ith observation or data points. In the context of tweets, that's the ith tweets. Visually, the sigmoid function has this form and it approaches zero as the dot product of Theta transpose X, over here, approaches minus infinity and one as it approaches infinity.

For classification, a threshold is needed. Usually, it is set to be 0.5 and this value corresponds to a dot product between Theta transpose and X equal to zero. So whenever the dot product is greater or equal than zero, the prediction is positive, and whenever the dot product is less than zero, the prediction is negative. So let's look at an example in the now familiar context of tweets and sentiment analysis. Look at the following tweet. After a preprocessing, you should end up with a list like this.

Note that handles are deleted, everything is in lowercase and the word tuning is reduced to its stem, tun. Then you would be able to extract features given a frequencies dictionary and arrive at a vector similar to the following. With a bias units over here and two features that are the sum of positive and negative frequencies of all the words in your processed tweets. Now assuming that you already have an optimum sets of parameters Theta, you would be able to get the value of the sigmoid function, in this case, equal to 4.92, and finally, predict a positive sentiment.

Now that you know the notation for logistic regression, you can use it to train a weight factor Theta. In the next video, you will learn about the mechanics behind training such a logistic regression classifier.

11. 01_18_logistic-regression-training.en
=====================================

![40.png](./images/40.png)
![41.png](./images/41.png)
![42.png](./images/42.png)
![43.png](./images/43.png)

In the previous video, you learned how to classify whether a tweet has a positive sentiment or negative sentiment, using a theta that I have given you. In this video, you will learn your own theta from scratch, and specifically, I'll walk you through an algorithm that allows you to get your theta variable. Let's see how you can do this. To train your logistic regression classifier, iterate until you find the set of parameters theta, that minimizes your cost function.

Let us suppose that your loss only depends on the parameters theta1 and theta2, you would have a cost function that looks like this contour plots on the left. On the right, you can see the evolution of the cost function as you iterate. First, you would have to initialize your parameters theta. Then you will update your theta in the direction of the gradient of your cost function. After a 100 iterations, you would be at this point, after 200 here, and so on.

After many iterations, you derive to a point near your optimum costs and you'd end your training here. Let's look at this process in more detail. First, you'd have to initialize your parameters vector theta. Then you'd use the logistic function to get values for each of your observations. After that, you'd be able to calculate the gradients of your cost function and update your parameters. Finally, you'd be able to compute your cost J and determine if more iterations are needed according to a stop-parameter or maximum number of iterations.

As you might have seen in the other courses, this algorithm is known as gradient descent. Now, that you have your theta variable, you want to evaluate your theta, meaning you want to evaluate your classifier. Once you put in your theta into your sigmoid function, do get a good classifier or do you get a bad classifier? In the next video, we will show you how you can do this.

12. 01_20_logistic-regression-testing.en
====================================

![44.png](./images/44.png)
![45.png](./images/45.png)
![46.png](./images/46.png)
![47.png](./images/47.png)
![48.png](./images/48.png)
![49.png](./images/49.png)

Now that you have your theta, you will use this theta to predict our new data points. For example, given a new tweet, you will use this theta to say whether this tweet is positive or negative. In doing so, you want to analyze whether your model generalizes well or not. In this video, we will show you whether your model generalizes well or not, and specifically, we'll show you how to compute the accuracy of your model. Let's take a look at how you can do this.

For this, you will need X_val and Y_val. Data that was set-aside during trainings, also known as the validation sets and Theta, the sets of optimum parameters that you got from training on your data. First, you will compute the sigmoid function for X_val with parameters Theta, then you will evaluate if each value of h of Theta is greater than or equal to a threshold value, often set to 0.5. For example, if your h X Theta is equal to the following vector, 0.3, 0.8, 0.5, etc., up to the number of examples from your validation set, you're going to assert if each of its components is greater than or equal to 0.5.

So is 0.3 greater than or equal to 0.5? No. So our first prediction is equal to 0. Is 0.8 greater than or equal to 0.5? Yes. So our prediction for the second example is 1. Is 0.5 greater than or equal to 0.5? Yes. So our third prediction is equal to 1, and so on. At the end, you will have a vector populated with zeros and ones indicating predicted negative and positive examples, respectively. After building the predictions vector, you can compute the accuracy of your model over the validation sets.

To do so, you will compare the predictions you have made with the true value for each observation from your validation data. If the values are equal and your prediction is correct, you'll get a value of 1 and 0 otherwise. For instance, if your prediction was correct, like in this case where your prediction and your label are both equal to 0, your vector will have a value equal to 1 in the first position. Conversely, if your second prediction wasn't correct, because your prediction and label disagree, your vector will have a value of 0 in the second position and so on and so forth.

After you have compared the values of every prediction with the true labels of your validation set, you can get the total times that your predictions were correct by summing up the vector of the comparisons. Finally, you'll divide that number over the total number m of observations from your validation sets. This metric gives an estimate of the times that's your logistic regression will correctly work on unseen data. So if your accuracy is equal to 0.5, it means that 50 percent of the time, your model is expected to work well.

For instance, if your Y_val and prediction vectors for five observations look like this, you'll compare each of their values and determine whether they match or not. After that, you'll have the following vector with a single 0 in the third position where the prediction and the label disagree. Next, you have to sum the number of times that your predictions were right and divide that number by the total number of observations in your validation sets. For example, you get an accuracy equal to 80 percent.

Congratulations on finishing the first week of this specialization. You learned many concepts this week. The first thing you learned is you learned how to preprocess a text. You learned how to extract features from that text. You learned how to use those extracted features and train a model using those. Then you learned how to test your model. In this week's programming exercise, you're going to get a chance to implement all these concepts that we spoke about.

Feel free to go ahead and do the programming exercise. There's also an optional video at the end of this week which covers the intuition behind the cost function for logistic regression. If you don't want to watch that video, feel free to go to next week, where you will learn about a new classification algorithm known as naive Bayes.

13. 01_22_logistic-regression-cost-function.en
==========================================

![50.png](./images/50.png)
![51.png](./images/51.png)
![52.png](./images/52.png)
![53.png](./images/53.png)
![54.png](./images/54.png)

Good to see you again. In this optional video, you're going to learn about the intuition behind the logistic regression cost function. Specifically, you will understand why the cost function is designed that way. You will see what happens when you predict the true label and you'll see what happens, when you predict the wrong label. Let's dive in and see how this logistic regression cost function is designed. Let's have a look now at the equation of the cost function, while this might look like a big complicated equation, it's actually rather straightforward, once you break it down into its components.

First, have a look at the left hand side of the equation where you find a sum over the variable m, which is just the number of training examples in your training set. This indicates that you're going to sum over the cost of each training example. Out front, there is a -1/m, indicating that when combined with the sum, this will be some kind of average. The minus sign ensures that your overall costs will always be a positive number as you'll see clearly later in this video.

Inside the square brackets, the equation has two terms that are added together. To consider what each of these terms contribute to the cost function for each training example, let's have a look at each of them separately. The term on the left is the product of y superscript i, which is the label for each training example, multiplied by the log of the prediction, which is the logistic regression function applied to each training example. Represented as h of superscript i, and a parameter theta.

Now, consider the case when your label is 0. In this case, the function h can return any value, and the entire term will be 0 because 0 times anything is just 0. What about the case when your label is 1? If your prediction is close to 1, then the log of your prediction will be close to 0, because, as you may recall, the log of 1 is 0. And the product will also be near 0. If your label is 1, and your prediction is close to 0, then this term blows up and approaches negative infinity.

Intuitively, now, you can see that this is the relevant term in your cost function when your label is 1. When your prediction is close to the label value, the loss is small, and when your label and prediction disagree, the overall cost goes up. Now consider the term on the right hand side of the cost function equation, in this case, if your label is 1, then the 1- y term goes to 0. And so any value returned by the logistic regression function will result in a 0 for the entire term, because again, 0 times anything is just 0.

If your label is 0, and the logistic regression function returns a value close to 0, then the products in this term will again be close to 0. If on the other hand your label is 0 and your prediction is close to 1, then the log term will blow up and the overall term will approach to negative infinity. From this exercise you can see now that there is one term in the cost function that is relevant when your label is 0, and another that is relevant when the label is 1.

In each of these terms, you're taking the log of a value between 0 and 1, which will always return a negative number, and so the minus sign out front ensures that the overall cost will always be a positive number. Now, let's have a look at what the cost function looks like for each of the labels. 0 and 1, overall possible prediction values. First, we're going to look at the loss when the label is 1. In this plot, you have your prediction value on the horizontal axis and the cost associated with a single training example on the vertical axis.

In this case J, of theta simplifies to just negative log h(x(theta). When your prediction is close to 1, the loss is close to 0. Because your prediction agrees well with the label. And when the prediction is close to 0, the loss approaches infinity, because your prediction and the label disagree strongly. The opposite is true when the label is 0. In this case J(theta) reduces to just minus log(1- h(x, theta). Now when your prediction is close to 0, the loss is also close to 0.

And when your prediction is close to 1, the loss approaches infinity. You now understand how the logistic regression cost function works. You saw what happened when you predicted a 1 and the true label was a 1. You also saw what happened when you predicted a 0, and the true label was a 0. In the next week, you will learn about Naive Bayes, which is a different type of classification algorithm, which also allows you to predict whether a tweet is positive or negative.

14. 01_24_week-conclusion.en
========================

Great job getting through the first week of Course 1. You now know how to train a logistic regression classifier. In this week's programming assignment, you'll be preparing text data and building, training and testing your own logistic regression model, it's really exciting. We created a quiz at the end that contains some of the questions you may be asked in an interview about these topics. Next week, you'll explore another NLP classification method called Naive Bayes.

Good luck with the programming assignment. >> Good luck.

### 05_heroes-of-nlp-chris-manning-optional

1. 05_01_andrew-ng-with-chris-manning.en
=====================================

Welcome to this interview series. To kick it off, I'm delighted to have with us today, Chris Manning. Chris is, I believe, the most highly cited NLP researcher in the world. He is a Professor of Computer Science and Linguistics at Stanford University. He's also the Director of the Stanford AI Lab, which is a role I had previously as well. Chris is well known globally as a leader in applying deep learning to natural language processing, and has done well-known research on tree recursive neural networks, sentiment analysis, neural network dependency parsing, the GloVe algorithm, and a lot more.

He's taught at Carnegie Mellon, the University of Sydney, and at Stanford University. Welcome, Chris. Thank you, Andrew. It's great to have a chance to chat. Even though you and I Chris have had the opportunity to work together on many occasions, one thing I've actually never asked you before is, how did you get started working in AI? I know that one of the unusual aspects of your background is that you majored in linguistics and then wound up being a Computer Science Professor doing NLP.

Tell us about your arc getting started in AI. Sure. My background in some sense isn't as a AI person. That's not really where I began. As an undergrad, I have a major in computer science and math. But I also got very interested in linguistics and did a major and honors in linguistics. Coming off of that, to a fair extent, my starting off point was a much more cognitive science viewpoint of human language seemed fascinating. These teeny little human beings somehow managed to learn it, at a time where, in general, their cognitive abilities don't seem that great.

How could human language learning take place? In linguistics, by far the dominant belief in the second half of the 20th century was the thinking of Noam Chomsky. Noam Chomsky was just the eminent person in linguistics in the same way that I guess for the first half of the 20th century, maybe R. A. Fisher was the dominant person in statistics. Chomsky had this very strong position that humans cannot possibly just be learning languages from data alone and that they must be innate machinery in people's brains that allow them to learn languages.

That's a very big topic. Even back then, it seemed to me just unbelievable given this evolutionary, extremely recent development of human language. I was interested in the idea of how could you go about learning languages. That led me to start to look at machine learning. Starting off first at the end of my undergrad, which was the late 1980s. These days, machine learning is such a big and dominant field. It's so big and dominant that the terms artificial intelligence and machine learning are two-thirds of the same thing because the vast majority of what you see in AI, it's machine learning.

But at that time, it just wasn't like that at all. The machine learning was this very scruffy on the side offshoot of AI that almost no one worked in. There was these series of two or three books edited by Jaime Carbonell and Tom Mitchell from CMU who'd started to put together some papers on machine learning. The early decision tree algorithms this is while I was still in Australia. The early decision tree algorithms in AI, the ID3 algorithm that still had seen decision tree learning.

Machine learning barely existed. But I was interested in these ideas of how you could go about getting computers to learn. That was the entree that led me down the path that's turned me into an AI researcher. It was a big deal, or maybe non-intuitive at the time, that you should use data to learn from language rather than code up by hand a CFG grammar or something to truly understand a language which is what people were trying to do back then. The dominant way in which people did natural language processing was by humans and of course that wasn't only affected by the NLP, that corresponded to the dominant thinking and AI at that time as well.

This was the era of knowledge-based systems where what was seen is what we needed, was to get subject-matter experts for which knowledge engineers would encode their knowledge in knowledge representation systems, and that all of this hand engineering would lead us to Intelligence. Even back then you were an early believer in machine learning for NLP? Absolutely. Right at the moment, transformer-based architectures have really become the dominant thing in neural networks.

We started going out of order here so maybe we should get back to them later. The interesting thing about transformer architectures is that they're built around an idea of attention. You can think of attention as giving you a soft tree structure where you can point at from one word to another, and that allows you to build a tree structure. We've done some really interesting work especially my PhD student John Hewitt, looking at what do transformer models learn when trained on billions of words of a human language.

You can actually show that these models learn all kinds of things about the structure of a language. One of the things they learn is that they learn some of these co-reference facts so that they'll learn that she refers back to Susan, and that it is referring to the bottle and sentences. But they also actually do learn this hierarchical context-free grammar structure of languages, just from a pile of sequence of words in a text alone, which is actually a really neat result.

Because language can be reasonably described as this nested context-free grammar like tree like structure, a neural network or sufficiently large neural network will transform network discovers aspects of that just from the data. Yeah. In fact, you're in the lead up to modern views on transformers. Your group at Stanford did some of the very influential early work. I know that for a long time in the pre-deep learning days you did a lot of work on statistical machine translation.

Then as deep learning started to make inroads into NLP, you and your PhD student Thang Luong, actually published one of the earliest papers on neural machine translation and helped lay the foundation with the bi-linear attention matrix, you helped lay some of the foundations of the modern transformer model. Do you want to just tell us a bit about that? Sure. Really, before starting work in neural networks again, I actually did a tiny bit of neural network work back in the 90s and the days when Dave Rumelhart was at Stanford that it really barely got into that.

In the 2000s decades certainly everything that I was doing was using probabilistic modeling techniques, putting probabilities over symbolic structures to describe human languages which is by far the dominant approach in that decade. One part of that work that I worked on for about a decade was building machine translation models. The dominant models were referred to as statistical phrase-based machine translation those days. A lot of techniques were worked out pretty well in that time, so there's a fairly well worked out architecture where you had these factorized machine translation models, where part of that was that you had phrase tables which gave you probabilities of translating a phrase in one language to a phrase in another language so that they did the local parts of translation.

Then you were combining it with what's called in natural language processing, a language model. Language model is a term of art that's very dominant in natural language processing. A language model means something that gives you probability distributions over sequences of words in a language. That's just been a really dominant, powerful idea in NLP because it lets you just tell whenever you want to have words next to words, what other words are likely or unlikely.

This basic idea of a language model has used context-sensitive spelling corrections. When you have something like Google correcting your spelling in context beautifully, there's a language model. Speech recognition systems use language models and these machine translation systems that also use language models. We had architectures and they worked reasonably well. When Google first came out with Machine Learning, they just learned from data machine translation systems, they were using these statistical phrase-based machine translation systems.

If I back up just for a tiny little bit of story, when Google first launched machine translation, they licensed very traditional, old rule-based machine translation system and that was the system that was originally developed by this company SYSTRAN whose roots go back really to the 1950s, from the earliest explorations of machine translation, but they had that for a couple of years and then seeing the advances that are being made in probabilistic models from machine translation they affected over to that and then things got much better.

Remember, Franz Och was really a real thought leader in helping Google scale to training the traditional models on tons more data and just dramatically improve the performance of Google Translate. Yeah, absolutely. At that point, Franz Och was one or maybe even the leading person doing statistical phrase-based MT models and he went to Google and lead a team that then Google had the sort of leading large-scale implementation of statistical phrase-based MT models.

They actually work pretty reasonably. They already achieved the goal that you could just sort of feed any web page and dozens of languages in and get something that was two-thirds comprehensible. You could workout basically what it was saying about what topic and that was reasonable, but that was sort of great for 2007 to 2010. But 2010 to 2014, which was the same period where Andrew and me were doing those tree recursive neural network we were just talking about.

In that period, statistical phrase-based machine translation stalled. There weren't really very good ideas for making further progress and a little bit of progress was being made by just throwing more data in, more data helps. That's still true model machine learning, but the models didn't have enough capacity for it to help a lot. An idea that people were working on a huge amount, including me in those years were saying, well, surely the solution is to make more use of grammatical structure of human languages and how machine translation systems, so really the dominant research area was trying to use syntax-based machine translation systems, but that had seemed a good idea, but that barely ever worked, Basically the result was that for some language pairs, that it didn't work at all, it just wasn't better than the statistical phrase-based machine translation systems.

Whereas for some other language pairs that had sort of more different grammatical structures, actually English, Chinese, machine translation was a good example. It definitely did help a bit, you could show some real gains. But the solution ironically turned out to be to pay less attention to the syntax and more attention to the data. Correct, yeah. That work kind of got blown out of the water when people started exploring using new methods for machine translation.

I was going to say it was the first big success of neural methods in NLP; whether that's true or not depends on whether you count speech as part of NLP or not because really, speech recognition was the first huge success of neural network methods applied to human language problems. But for text-based work, really, the first thing that was just sort of knocked you out was building neural machine translation systems. It was a very successful domain because it's a domain where there's sort of lots of data available, here's a lot of text in a pair of languages that you could start the train big neural network models, and was first done by Ilya Sutskever and a couple of colleagues at Google.

For having modeling a sequence of anything, like a sequence of words or sequence of DNA. That the dominant model is recurrent neural networks which adjustment models that work on simply sequences. Remember, what they've seen before in a limited way, it's the continuous neural version of a hidden Markov model. Essentially, what they showed is, if you make no use of the structure of human languages at all. This is undermining all that work on syntax-based models.

Was that if you just build very large recurrent neural networks that were then deep. Until that point, most of the neural network modeling in NLP was that if we had two layers we call it deep. If we had three layers or four layers we were really pushing it. They were immediately pushing it out to eight layer deep recurrent neural networks. This is where you stop getting into systems issues of needing to run out on a machine with eight GPUs to get, which is the trend that's continue to.

We can maybe talk more about. They showed the much larger neural network just trading big sequence models and two sequence models. One of them is encoder, encodes a source language than another round as a generator and generates a sequence of words in the target language. Could already gives you a pretty good machine translation system. Not quite as good as the state-of-the-art at that point. But it was close enough to the state-of-the-art seem tantalizing.

Since all they were doing was plugging two neural networks together. The thing that if you're not counting the library code for having recurrent neural net units, some in particular LSTMs, long short-term memory units was very influential and allowing this work to work. You only needed your 500 lines of Python code around the neural network library. You could have an almost state-of-the-art machine translation system that seems just super intriguing. But they're also seeing something crude and missing there.

Then very quickly after that Kyunghyun Cho who was working with Yoshua Bengio and Montreal. Well, actually not only Kyunghyun Cho also Dima Bahdanau now I should mention, is the first author on the paper, who was then my youngest student in Montreal. It's really actually, Dima, who develop the idea of you could build an attention-based model. The idea of an attention-based models at any point in the sequence, you could calculate out a connection to other words in perhaps the same, perhaps a different sequence.

Then using that attention, you could calculate a new vector to influence what happens next. In particular, in this machine translation contexts, you'll have started your translation and your translation was starting to say the pilot. Then you'd calculate attention back into the source sentence in the other language and work out essentially what words in the source you wanted to be translating next based on what you've translated so far. Rather than having to remember the entire of the source sentence and your current neural network state, you could do with a human translator actually does.

Dynamically look back at the source sentence and work out what to translate next. This idea of attention has just been transformative. It's increasingly being used also in vision systems. Systems but knowledge graphs and other areas of work on neural networks. Then shortly after the Cho and Dima paper. You and Thang wrote a paper on bi-linear attention. How did that come about? In early work, we're really starting with another student Danqi Chen that we'd looked at this idea of neural tensor networks, where what we'd wanted to do is be able to combine together vectors and have them influence each other but use another vector.

We've done that by putting tensor which is the multi-dimensional generalization of matrices in between them. That idea was going on and other pieces of work in my group at the time. But here we just wanted to get an attention score. So in Dima and Cho's work what they'd done and say that, okay, we wanted attention score between these two vectors. Let's feed them through a little neural net, a little multi-layer perceptron, and calculate those attention score, whereas it seem to me that we'll wait.

No, I could just do this simple thing of bi-linear attention, where there are these two vectors. If I put a matrix between them and I multiply vector times matrix by vector, I just get a number out. So that is bi-linear attention sometimes referred to as multiplicative attention. It's a simpler and more directly interpretable idea of attention because in some sense the simplest idea of attention is to say, "well you have two vectors just dot-product them together, you get a score of the similarity." But that's too rigid because you want to say, "well, maybe I only want to pay attention to parts of the vector, and maybe I want to know if that the top part of one vector is similar to the bottom part of the other vector." So by sticking a matrix into the middle, you can then modulate the similarity calculation.

That's a natural measure of similarity and very easily learnable by neural networks. In some sense, it's a general light. How ideas develop and spread is always complex. There are a lot of ideas in the air at any one time. But in some sense, what's become dominant in the modern work with transformer-based models essentially does build off that notion, but adding in an extra idea on top of that. It's a similar idea where instead of having a giant matrix in the middle, which requests a lot of parameters, if you have a low-rank approximation to that matrix in the middle to what you were using then that comes very close to the modern transformer model.

Exactly, so in our initial work, we just had a full rank matrix in the middle of the floor of that. If you have a full rank matrix with a lot of parameters, the obvious way to have less parameters is to say, "well no, I can have two, I can regard that matrix as being the product of two low-rank matrices." Then once you have that idea, rather than multiplying them together, you can say, "well, I can sort of apply those to low-rank matrices to the vectors on each side, which is more efficient." Computationally, it's something to do, and that's exactly what modern transformer models do.

You take your two vectors, you multiply each by a low-rank matrix, and then you take the dot product between those, which is exactly equivalent to saying, "I form the matrix by multiplying two low rate matrices, and then I do my vector matrix-vector product, but done more efficiently." In fact, not to jump around too much. I feel like this is not the first time in your career that you really advance the field by making observations about matrix multiplications, if I look at the work that your team did on GloVe, the word embeddings, I feel like the heart of that idea was also simplifying what was the roles of the complex set of neural network-like stuff into just a set of matrix multiplications.Due top of that, still find GloVe to this day a very elegant paper because it's really simplified what was previously a very complicated set of ideas for learning word embeddings into Simpler.

Take the inner product between the word embeddings formulation. Thank you. I do think that GloVe paper some senses. One of its main contributions was giving a better understanding. I mean, it's not that it worked better than the other methods that then recently being developed, but it was interesting. Let's try and think about what's going on here and how these methods relate to other things that have been explored. So the general topic here is word vectors of coming up with a real vector representation that gives you the meaning of word, and which now in your NLP deep-learning courses.

Essentially, often the first idea you really see because it's a very useful notion and a fairly simple one. This has been done quite successfully by a couple of pieces of work in In the few years around 2010 to 2013, but had been done in very mechanistic neural net ways. Here's the architecture and the algorithm. Run this and run it in those days often for weeks because we didn't have very fast powerful computers and out and it will pop great word vectors.

We were interested. This was work with postdoc Jeffrey Pennington. We were interested in actually trying to understand better what was happening in terms of the math of these models. Something that we were intrigued by was, actually there was an older tradition. The LSA or Latent Semantic Analysis tradition of having vector representations of word meaning which exploited classical linear algebra. The latent semantic analysis models and linear algebra terms were neither more or less than the singular value decomposition or using the singular value decomposition on word count, co-occurrence count, matrices, and then reducing rank via getting rid of small singular values.

That's fascinating. One trend that overlays all of this work that you've observed and participated in for the last many years is the scaling of NLP models. It seems like [unclear] models are getting larger, like GPT-3. There are really many models in the sequence. For how long do you think this will continue? Do you think someday, if ever, we'll go back to building smaller models? In 2018, BERT came out and it showed that you could do fantastically well on a bunch of tasks, including question answering, natural language inference, text classification, named entity recognition, parsing.

Making use of this pre-trained large language model where you're training a large transformer just on a few billion words of text to predict gapped words in sentences. But just doing that simple task, gave these really good language representations, which then could just be used in a very simple manner with something like a softmax classifier to provide great solutions for downstream NLP tasks. That was an amazing success. The idea of representation learning that many of us have been talking about for a decade or so, saying that, neural networks is about representation learning.

Learning that's useful, intermediate representations. This was really showing that this was really working for building representations of language that can then be very easily applied to higher natural language understanding downstream tasks. But BERT already used a huge amount of data and compute. It was trained on billions of words of language and it was trained on large numbers of computers for quite a long time. But since BERT, there's been a lot of further progress, but it's essentially just come from scaling up to compute more and more.

As always, I'm leaving a few things out. There have also been a couple of new ideas. There's been ideas like doing relative attention which has improved things. To a first approximation, what's really been driving the gains is just by throwing more and more compute at the problem, running even bigger models on even more data. Andrew, you often use the slogan, AI is the new electricity. In some of the talks I've been given recently, discussing this trend of bigger and bigger models, I I have been turning it around and saying that electricity is the new AI, because if you look at what's been happening, people are now training models, not just 10 times or 100 times bigger than the BERT model, they're training models that 10,000, 100,000 times bigger than the BERT model and the computational energy demands to train those models is going up accordingly.

That's suddenly push progress. I think that trend can't possibly continue much further, I mean, yeah, part of it is just we're running out of texts and we're running out of computers to train up a big models on. Going from BERT to GPT-3, if I remember, it was massive scaling compute and modest scaling of data. So maybe we have enough text data, we just need another 100 or 1000 or 10,000 times faster computers. You're right that the scaling of compute was vastly bigger than scaling of data.

But nevertheless, the amount of data that's now being used is actually quite substantial. I mean, there's suddenly more data, but there are actually using a substantial quantity of quality data. But yeah, I buy the point that to the extent that clever systems people can give us three orders of magnitude more powerful not TPUs, even without more texts data, these models are going to be better and probably will be better in the coming years. But, I don't ultimately believe that's the path to artificial intelligence, or the interesting path at this point for further improving natural language processing.

Let me ask a really savvy controversial question. Several weeks ago, one of our mutual friends made a comment about this direction, that said, " Maybe the scale is a path to AGI." You know that conversation where one of our mutual friends made that own's comment. What are your thoughts on that? I think there's a place that, that idea is coming from. The really cool thing about the GPT-3 model that was recently released by OpenAI was the discovery that then really motivated their subsequent work that with these really humungous language models.

That they can actually achieve a generality where they can be used for all kinds of tasks without actually having to train them to do any task. Rob (phonetic), conventionally, if we wanted to do different tasks with a neural network, we just take data for that task and train a model for that task with these large pre-trained language models, but we sort got to a halfway house where he had a baseline. Very good language representations have been pre-trained, but still we then just fine tune for every different tasks so we find tune there's a question on string model and when we'd start again and fine tune that.

Something else like summarization or something like that. What they discovered with GPT-3 is that actually didn't need to do that anymore. That instead, you could just hint to the model what you'd like her to do by giving it a couple of examples. You'd say, " Okay, I'm interested in translation". If here's the sentence, what I'd like you to produce is this sentence which is a translation of that into Spanish and if you gave it a couple of examples of what you wanted it to do the model would get the idea and then you could give it more sentences and they'll translate it.

But it didn't lead to translation, you could give it some questions and tell it you wanted answers and it'd give answers to other questions. The sudden mind-blowing thing about GPT-3 is to a first approximation, you can give it all kinds of tasks, even weird ones that you wouldn't expect it to really know why it knows that and it'll just do them. Sometimes the things that linguists interested in as a weird sentence manipulations. You know, if I give you a sentence, can you turn it into a question sentence or can you turn it into a relative clause that modifies the person and any of those things you'd just give it a little task to GPT-3 and it will do it.

That's the sense in which should actually offer the vision of general intelligence rather than what's been the main state of AI over the last decade, which was these very narrow AIs where you just trained system for one particular thing. Here is a movie recommender, here is an object recognizer and images, here's is natural language question answer. It's intriguing because of its general intelligence. But I don't actually believe it represents something that's a path to the goal artificial general intelligence particular data and.

Which used to happen to be flexible cognitive agent like human beings, because it is just this humongous, pre-trained model, trained on an amount of data that is just massively more than a little human beings sees before they are confident, that human language. To have something that's like a human being, you have to have something that can flexibly learn different tasks as it's exposed to them. The big GPT-3 model, it's no longer learning at all. It's been exposed to so much data training time, that it can do all sorts of different tasks by effectively pattern-matching to something that saw somewhere along the line.

That's actually an area that there's also starting to be a lot of work on right at the moment in deep learning as the idea of Meta learning, instead how do you build systems that are good at learning how to learn new tasks, and I think that's actually closer to the kind of intelligence we have to be seeking if we are aiming at having artificial general intelligence. Chris, in your career, you've mentored tons of very successful undergraduate students, Masters students, PhD students, and today there are many people applying to be a student in your lab.

I'm curious, in your view what makes a good researcher in your lab at Stanford? What characteristics do you like to see in people applying to be a member of your lab? There are definitely people that come from different backgrounds. I suddenly do actually like some of my students to know something about and really be interested in human languages and their structure. I certainly like to have some people that have backgrounds in human languages and some linguistics, but that's certainly not all of them.

I've had other people who are AI machine learning, or other quantitive of students who have no background at all, apart from like all human beings, they are native speakers of some language or another. I think the dominant thing is that you have to have creativity and a scientific thinking. There are lots of people around who can read papers and do whatever is in them. The secret of being successful, is that you can think a bit differently and say, "Wait a minute, these people are doing things like this.

In fact, almost everyone is doing things like this, but maybe there's another way it could be approached that is better." Really I think that's core scientific training of trying to aim to break things in the sense of find why these ideas had actually a great way to do things and to think of different approaches which might work better. How does a student become creative? That's a good question. Yeah, I believe that you can make progress on this, and I think it's a matter of taking a mindset of being critical when you read things and it's time to explore around and do different things.

Rather than just reading papers and thinking, "Oh, this is a good way to do things." I think you really want to be concentrating on being awake as you read, and trying to think, " Well, what are they assuming? Why are they doing it this way rather than some other way?" While a lot of times you'll experiments will fail, but I think when they fail, you're already learning more than if you're simply implementing the algorithm that's in the paper, because you definitely really learned very much by doing that.

Occasionally you might see something that half works, and then that might give you an idea of, "Well, maybe there's something here, and if I modified it and push that and had a second vector of what people do now, then it might work interestingly better." I think the practice of exploring out and thinking in those directions is the way that you build these skills of coming up with something new. I find that most creative people read incredibly widely and wind up making strange connections that someone else wouldn't have made between linguistics and computer science or between some other weird thing and deep learning.

Yeah, I think that's also a really good strategy. Thanks Chris. This has been great. Before we wrap up, I think a lot of the learners watching this video are looking to build a career in AI and looking to build a career in NLP. Do you have any final words of advice to someone watching this, looking to advance their career in AI? Sure. It's a great time for you to do this, that there's just huge opportunities all over industry and also in academia for people with skills in AI machine learning, natural language processing.

You'll be greatly in demand. This is a great thing to do. But I think nevertheless you want to think thoughtfully about how to develop your career and this is maybe connected with what Andrew, you were just saying about reading widely. Because the reality is that the world and the skills that are useful develop quickly. We've talked about earlier in this hour that really when I started off I was being taught about rule-based NLP and then there started to be machine learning models and probabilistic models.

There are other things that went by in the meantime like support vector machines and large margin models. Then there was the return of neural networks to dominance. But neural networks were actually an idea that had been around since the 1950s. At the moment, deep learning and neural networks seem so dominant. It seems like nothing else can possibly be relevant to know, the only thing I should learn is how to be state of the art in building neural network models.

But that's not how the world has been in the past. Around 2008, that's what we thought of probabilistic AI models. They were obviously wide and dominant and they were the thing to know. But really progress is made by taking old ideas and rediscovering them and putting them together with some stuff that's being learned in the meantime, and further raising the bar on where we can get to. Its sure to be the case that lots of different ideas are going to be useful in various ways in the future.

To be successful long-term, it both helps to have a richness of background, it definitely helps to have some length of areas of computer science, areas of math, statistics, linguistics, different ideas. But you also have to accept that this is an area where you have to adapt and move on to new ideas. I think one of the ways in which I've been very successful is not by inventing a whole new field single-handedly, but being able to see where promising ideas were emerging and moving while starting to think about those and moving to do work in them fairly quickly.

That adept to keeping your antennas up for interesting ideas that are starting to appear and being adaptable and willing to explore and make use of new ideas, that's the way that you keep your thinking vibrant. Yeah. I think AI machine learning and NLP of obvious moves so fast as. I think all of us just have to keep learning. Absolutely. Thanks Chris. This has been a great and its really interesting to hear the story of how you managed doing all this work over these many years.

Then I find that inspiring to think that maybe there's someone watching this that will follow in some of your footsteps and themselves maybe end up a professor somewhere or doing great research. Much as you have. Thank you. Thank you Andrew. It's been been fun chatting. A final fact I can tell people listening is for a whole bunch of years Andrew and me were actually office mates. Well, we had offices next door to each other on the corridor. Once upon a time, I had opportunities often to see Andrew in the corridor and pass a few thoughts.

I don't get those chances as often anymore so it's fun getting a chance to chat. Thanks Chris. Those were good days. I remember we shared a wall so If I hit my wall in my office you were on the other side. Those were great times. Thanks Chris. Okay. See you. For more interviews with NLP thought leaders, checkout the DeepLearning.AI YouTube channel or enroll in the NLP specialization on Coursera.

## 02_sentiment-analysis-with-naive-bayes

1. 01_01_week-introduction.en
==========================

Welcome to week two, this week you'll tackle a new method for classification called naive bayes. This is another method that's really useful because it's easy to train, and provides a quick baseline for your task. With the upcoming exercises, you'll get more practice handling text, loading in data, and doing inference. You'll become familiar with techniques such as Laplacian smoothing, and log likelihood analysis. Let's dive into the details. >> Okay, here we go.

2. 01_02_probability-and-bayes-rule.en
===================================

![55.png](./images/55.png)
![56.png](./images/56.png)
![57.png](./images/57.png)
![58.png](./images/58.png)
![59.png](./images/59.png)
![60.png](./images/60.png)
![61.png](./images/61.png)

This video will give you an overview of Bayes rule and go over some probability. Don't worry if your math is a little bit rusty. We'll go through this together, step-by-step. Probability is fundamental to many applications in NLP. You'll see how you can use it to help classify whether a tweet is positive or negative. Let's get started. To start, we are going to first review what's probabilities and conditional probabilities are, how they operate, and how they can be expressed mathematically.

Then I'll go over how to derive Bayes rule from the definition of conditional probabilities. Bayes rule is applied in many different fields, ranging from medicine to education and is used extensively in NLP. Once you understand the theory behind Bayes rule, you can use it to perform sentiment analysis on tweets, which will be this week's assignments. Then in the next course, you'll implement auto-correct using its basic formulation as well. Imagine you have an extensive corpus of tweets that can be categorized as either positive or negative sentiment, but not both.

Within that corpus, the word happy is sometimes being labeled positive and sometimes negative. Let's explore why this situation is occurring. One way to think about probabilities is by counting how frequently events occur. Suppose you define event A as a tweets being labeled positive, then the probability of event A, shown as P of A here, is calculated as the ratio between the counts of positive tweets in the corpus divided by the total number of tweets in the corpus.

In this example, that number comes out to 13 over 20, or 0.65. You could also express this value as a percentage, 65 percent positive. It's worth noting that the complimentary probability here, which is the probability of the tweets expressing a negative sentiment is just equal to one minus the probability of a positive sentiment. Note that for this to be true, all tweets must be categorized as either positive or negative but not both. Let's define Event B in a similar way by counting tweets containing the word happy.

In this case, the total number of tweets containing the word happy, shown here as N-happy is 4. Here's another way of looking at it. Take a look at the section of the diagram were tweets are labeled positive and also contain the word happy. In the context of this diagram, the probability that a tweet is labeled positive and also contains the word happy is just the ratio of the area of the intersection divided by the area of the entire corpus. In other words, if there were 20 tweets in the corpus, and three of them are labeled positive and also contain the word happy, then the associated probability is 3 divided by 20 or 0.15.

You now know how to calculate the probability of an intersection. You know how to calculate the probability of a word, namely happy with the probability of being positive. In the next video, we will talk about Naive Bayes.

3. 01_04_bayes-rule.en
===================

![62.png](./images/62.png)
![63.png](./images/63.png)
![64.png](./images/64.png)
![65.png](./images/65.png)
![66.png](./images/66.png)
![67.png](./images/67.png)
![68.png](./images/68.png)
![69.png](./images/69.png)

Welcome. We will be looking at conditional probabilities to help us understand Bayes rule. In other words, if I tell you, you can guess what the weather is like given that we are in California and it is winter, then you'll have a much better guess than if I just asked you to guess what the weather is like. In order to derive Bayes rule, let's first take a look at the conditional probabilities. Now think about what happens if, instead of the entire corpus, you only consider tweets that contain the word happy.

This is the same as saying, given that a tweet contains the word happy with that, you would be considering only the tweets inside the blue circle, where many of the positive tweets are now excluded. In this case, the probability that a tweet is positive, given that it contains the word happy, simply becomes the number of tweets that are positive and also contain the word happy. We divide that by the number that contain the word happy. As you can see by this calculation, your tweet has a 75 percent likelihood of being positive if it contains the word happy.

You could make the same case for positive tweets. The purple area denotes the probability that a positive tweet contains the word happy. In this case, the probability is 3 over 13, which is 0.231. With all of this discussion of the probability of missing certain conditions, we are talking about conditional probabilities. Conditional probabilities could be interpreted as the probability of an outcome B knowing that event A already happened, or given that I'm looking at an element from set A, the probability that it's also belongs to set B.

Here's another way of looking at this with a Venn diagram you saw before. Using the previous example, the probability of a tweet being positive, given that it has the word happy, is equal to the probability of the intersection between the tweets that are positive and the tweets that have the word happy divided by the probability of a tweet given from the corpus having the word happy. Let's take a closer look at the equation from the previous slide. You could write a similar equation by simply swapping the position of the two conditions.

Now, you have the conditional probability of a tweet containing the word happy, given that it is a positive tweet. Armed with both of these equations, you're now ready to derive Bayes rule. To combine these equations, note that the intersection represents the same quantity, no matter which way it's written. Knowing that, you can remove it from the equation, with a little algebraic manipulation, you are able to arrive at this equation. This is now an expression of Bayes rule in the context of the previous sentiment analysis problem.

More generally, Bayes rule states that the probability of x given y is equal to the probability of y given x times the ratio of the probability of x over the probability of y. That's it. You just arrived at the basic formulation of Bayes rule, nicely done. To wrap up, you just derive Bayes rule from expressions of conditional probability. Throughout the rest of this course, you'll be using Bayes rule for various applications in NLP. The main takeaway for now is that, Bayes rule is based on the mathematical formulation of conditional probabilities.

That's with Bayes rule, you can calculate the probability of x given y if you already know the probability of y given x and the ratio of the probabilities of x and y. That's great work. I'll see you later. Congratulations. You now have a good understanding of Bayes rule. In the next video, you'll see how you can start applying Bayes rule to a model known as Naive Bayes. This will allow you to start building your sentiment analysis classifier using just probabilities.

4. 01_06_naive-bayes-introduction.en
=================================

![70.png](./images/70.png)
![71.png](./images/71.png)
![72.png](./images/72.png)
![73.png](./images/73.png)
![74.png](./images/74.png)
![75.png](./images/75.png)
![76.png](./images/76.png)
![77.png](./images/77.png)
![78.png](./images/78.png)
![79.png](./images/79.png)
![80.png](./images/80.png)
![81.png](./images/81.png)
![82.png](./images/82.png)
![83.png](./images/83.png)
![84.png](./images/84.png)
![85.png](./images/85.png)

Welcome. Last week you learnt how to classify tweets using logistic regression. This week, we will solve the same problem using a method called the Naive Bayes. It's a very good, quick and dirty baseline for many texts classification tasks. The concepts you learned will be used later throughout the specialization. Naive Bayes is an example of supervised machine learning and shares many similarities with the logistic regression method you used in the previous assignments.

It's called naive because this method makes the assumption that the features you're using for classification are all independent. Which in reality is rarely the case. As you will see, however, it still works nicely as a simple method for sentiment analysis. As before, you will begin with two corpora. One for the positive tweets and one for the negative tweets. You need to extract the vocabulary or all the different words that appear in your corpus, along with their counts.

You get the word counts for each occurrence of a word in the positive corpus, then do the same for the negative corpus just like you did before. Then you're going to get a total count of all the words in your positive corpus and do the same again for your negative corpus. That is, you're just summing over the rows of this table. For positive tweets, there is a total of 13 words and for negative tweets, a total of 12 words. This is the first new step for Naive Bayes and it's very important because it allows you to compute the conditional probabilities of each word given the class as you're about to see.

Now divide the frequency of each word in a class by it's corresponding sum of words in the class. For the word I, the conditional probability for the positive class would be 3//13. You store that value in a new table with the corresponding value, 0.24. Now for the word I in the negative class, you get 3/12. You store that in your new table with the corresponding value, 0.25. Now apply the same procedure for each word in your vocabulary to complete the table of conditional probabilities.

One key property of this table is that if you sum over all the probabilities for each class, you will get 1. Let's investigate this table further to see what these numbers mean. First, note how many words have a nearly identical conditional probability, like I'm learning and then NLP. The interesting thing here is words that are equally probable don't add anything to the sentiment. In contrast to these neutral words, look at some of these other words like happy, sad, and not.

They have a significant difference between probabilities. These are your power words tending to express one sentiment or the other. These words carry a lot of weight in determining your tweet sentiments. Now let's take a look at because. As you can see, it only appears in the positive corpus. It's conditional probability for the negative class is 0. When this happens, you have no way of comparing between the two corpora, which will become a problem for your calculations.

To avoid this, you will smooth your probability function. Say you get a new tweet from one of your friends and the tweet says, "I'm happy today, I'm learning." You want to use the table of probabilities to predict the sentiments of the whole tweet. This expression is called the Naive Bayes inference condition rule for binary classification. This expression says that you're going to take the product across all of the words in your tweets of the probability for each word in the positive class divide it by the probability in the negative class.

Let's calculate this product for this tweet. For each word, select it's probabilities from the table. For I, you get a positive probability of 0.2 and a negative probability of 0.2. The ratio that goes into the product is just 0.2/0.2. For am, you also get 0.2/0.2. For happy, you get 0.14/0.10. For today, you don't find any word in the table, meaning this word is not in your vocabulary. So you won't include any term in the score. For the second occurrence of I again, you'll have 0.2/0.2.

For the second occurrence of I'm, you'll have 0.2/0.2 and learning gets 0.10/0.10. Now note that's all the neutral words in the tweet, like I and I'm, just cancel out in the expression. What you end up is with 0.14/ 0.10, which is equal to 1.4. This value is higher than one, which means that overall, the words in the tweets are more likely to correspond to a positive sentiment. So you conclude that the tweet is positive. So far, you've created a table to store the conditional probabilities of words in your vocabulary and applied the Naive Bayes inference condition rule for binary classification of a tweet.

Great. Next, you'll look into some issues with this implementation and how to fix them. Now you have seen how Naive Bayes can be used to classify the sentiment of a tweet. In the next video, we will simplify the calculations before we implement it.

5. 01_08_laplacian-smoothing.en
============================

![86.png](./images/86.png)
![87.png](./images/87.png)
![88.png](./images/88.png)
![89.png](./images/89.png)
![90.png](./images/90.png)
![91.png](./images/91.png)
![92.png](./images/92.png)

Welcome back. Sometimes you try to calculate the probability of a word happening after a word. To do that you might want to count the number of times those two words showed up. One after another, divided by the number of times the first word appeared. Now what if the two words never showed up next to each other in the training corpus. You get a probability of zero, and the probability of an entire sequence might go to zero. Now how can we fix this problem?

Let's take a look, let's now dive into Laplacian smoothing, a technique you can use to avoid your probabilities being zero. The expression used to calculate the conditional probability of a word given the class is the frequency of the word in the corpus. Shown here as freq of word I comma class divided by the number of words in the corpus or N class. Smoothing the probability function means that you will use a slightly different formula from the original.

Know that I've added a one in the numerator. This little transformation avoids the probability being zero. However, it adds a new term to all the frequencies that is not correctly normalized by N class. To account for this, you will add a new term in the denominator V class. That is the number of unique words in your vocabulary to account for that extra term added in the numerator. So now all the probabilities in each column will sum to one. This process is called Laplacian smoothing.

Going back to this example, let's use the formula on it. The first thing you need to calculate is the number of unique words in your vocabulary. In this example you have eight unique words. So now let's calculate the probability for each word. And the positive class for the word I the positive class you get three plus one divided by 13 plus eight which is 0.19. For the negative class you have three plus one divided by 12 plus eight, which is 0.2 and then so on for the rest of the table.

The number is shown here have been rounded. But using this method to sum of probabilities in your table will still be one. Notice that the word because no longer has a probability of zero. Great, that's Laplacian smoothing. Now you know why you have to use the Laplacian smoothing. So your probabilities don't end up being zero. That's very cool, you learned about Laplacian smoothing and now understand why it is important to use smoothing. In the next video, you will learn about the log likelihood

6. 01_10_log-likelihood-part-1.en
==============================

![93.png](./images/93.png)
![94.png](./images/94.png)
![95.png](./images/95.png)
![96.png](./images/96.png)
![97.png](./images/97.png)
![98.png](./images/98.png)
![99.png](./images/99.png)
![100.png](./images/100.png)
![101.png](./images/101.png)
![102.png](./images/102.png)
![103.png](./images/103.png)
![104.png](./images/104.png)
![105.png](./images/105.png)
![106.png](./images/106.png)
![107.png](./images/107.png)

In this video, I will introduce you to log likelihoods. These are just logarithms of the probabilities we're calculating from the last video. They are way more convenient to work with and they appeared throughout deep learning and NLP. Let's go back to the table you saw previously that contains the conditional probabilities of each word. For positive or negative sentiment. Words can have many shades of emotional meaning,but for the purpose of sentiment classification, they're simplified into three categories; neutral, positive, and negative.

All can be identified by using their conditional probabilities. These categories can be numerically estimated just by dividing the corresponding conditional probabilities of this table. Now, let's see how this ratio looks for the words in your vocabulary. The ratio for the word I is 0.2 divided by 0.2 or 1. The ratio for the word am is again 1. The ratio for the word happy is 0.14 divided by 0.1 or 1.4. Do the same for because, learning, and NLP. The ratio is 1.

For sad and not the ratio is 0.1 divided by 0.15 or 0.6. Again, neutral words have a ratio near one. Positive words have a ratio larger than 1. The larger the ratio, the more positive the words are going to be. On the other hand, negative words have a ratio smaller than 1. The smaller the value, the more negative the word. In this week's assignment, you'll implement a function that filters words depending on their positivity or negativity. You will find the expression shown here to be very helpful with that.

These ratios are essential in Naive Bayes' for binary classification. I'll illustrate why using an example you've seen before. Recall earlier, where you use the formula to categorize a tweet as positive if the products of the corresponding ratios of every word appears in the tweet is bigger than 1. We said it was negative, if it was less than 1. This is called the likelihood. If you were to take a ratio between the positive and negative tweets, you'd have what's called the prior ratio.

I haven't mentioned it till now because in this small example, you had exactly the same number of positive and negative tweets, making the ratio 1. In this week's assignments, you'll have a balanced data-sets. You'll be working with a ratio of 1. In the future though, when you're building your own application, remember that this term becomes important for unbalanced data-sets. With the addition of the prior ratio, you now have the full Naive Bayes' formula for binary classification.

A simple, fast and powerful method that you can use to establish a baseline quickly. Now, it's a good time to mention some other important considerations for your implementation of Naive Bayes'. Sentiments probability calculation requires multiplication of many numbers with values between 0 and 1. Carrying out such multiplications on a computer runs the risk of numerical underflow when the number returned is so small if can't be stored on your device.

Luckily, there is a mathematical trick to solve this. It involves using a property of logarithms. Recall that the formula you're using to calculate a score for Naive Bayes' is the prior multiplied by the likelihood. The trick is to use a log of the score instead of the raw score. This allows you to write the previous expression as the sum of the log prior and the log likelihood, which is a sum of the logarithms of the conditional probability ratio of all unique words in your corpus.

Let's use this method to classify the tweets: I'm happy because I'm learning. Remember how you used the Naive Bayes' inference condition earlier to get the sentiment score for your tweets. Now, you're going to do something very similar to get the log of your score. What you'll need to calculate the log of the score is called the Lambda. This is the log of the ratio of the probability, that your word is positive and you divide that by the probability that the word is negative.

Now, let's calculate Lambda for every word in our vocabulary. For the word I, you get the logarithm of 0.05 divided by 0.05, or the logarithm of 1, which is equal to 0. Remember, the tweets will be labeled positive if the product is larger than 1. By this logic, I would be classified as neutral at 0. For am, you take the log of 0.04 over 0.04, which again is equal to 0. You enter 0 in the table. For happy, you get a Lambda of 2.2, which is greater than 0, indicating a positive sentiment.

From here on out, you can calculate the log score of the entire corpus just by summing out the Lambdas. You're almost done with the log-likelihood. Let's stop here and take a quick look back at what you did so far. Words are often emotionally ambiguous, but you can simplify them into three categories and then measure exactly where they fall within those categories for binary classification. You do so by dividing the conditional probabilities of the words in each category.

This ratio can be expressed as a logarithm as well called Lambda, and you can use that to reduce the risk of numerical underflow. In this video, you learned about the ratio of positive words and negative words. The higher the ratio is, the more positive the words are going to be. As the number of words we are using gets larger and larger, then we are very likely to get a product that is very close to 0. Hence, we end up taking the log of that ratio.

7. 01_12_log-likelihood-part-2.en
==============================

![108.png](./images/108.png)
![109.png](./images/109.png)
![110.png](./images/110.png)
![111.png](./images/111.png)
![112.png](./images/112.png)

We will continue from the previous video and show you how to do inference. Given your lambda dictionary the task is pretty straightforward. You have done most of the work to arrive at your log likelihood already. Now let's wrap up. Now you can calculate the log likelihood of the tweet as the sum of the lambdas from each word in the tweet. So for word I you add 0, for am you add 0, for word, happy you had 2.2, for words because I and am you add 0 and for word learning you add 1.1.

This sum is 3.3 and this value is higher than 0. Remember how previously you saw that the tweet was positive if the product was bigger than 1 with the log of 1 equal to 0. The positive values indicate that the tweet is positive, a value less than 0 would indicate that the tweet is negative. The log likelihood for the suite is 3.3 and since 3.3 is bigger than 0, the tweet is positive. Notice that this score is based entirely on the words happy and learning both of which carry a positive sentiment.

All the other words were neutral and didn't contribute to the score. See how much influence the power words have. Let's do a quick recap. You used your new skills to predict the sentiment of a tweet by summing all the lambdas for each word that appeared in the tweet. This score is called the log likelihood for the log likelihood, the decision threshold is zero instead of one. Positive tweets will have a positive log likelihood above 0, and negative tweets will have a negative log likelihood below 0, well done.

Congratulations now that you have a good understanding of how to compute the log likelihood and how to do inference, I will proceed to show you how to train a naive Bayes model.

8. 01_14_training-naive-bayes.en
=============================

![113.png](./images/113.png)
![114.png](./images/114.png)
![115.png](./images/115.png)
![116.png](./images/116.png)
![117.png](./images/117.png)
![118.png](./images/118.png)

This week, I'll show you how to train the Naive Bayes classifier. In this context, we train in something different than in logistic regression or deep learning. There is no gradient descent. We're just counting frequencies of words in the corpus. You will now be creating step-by-step, a Naive Bayes model for sentiment analysis using a corpus of tweets that you've already collected. That's awesome. The first step for any supervised machine learning project is to gather the data to train and test your model.

For sentiment analysis of tweets, this step involves getting a corpus of tweets and dividing it into two groups; positive and negative tweets. The next step is fundamental to your model success. The preprocessing step, as described in the previous module, consists of five smaller steps. One, lowercase the texts, 2, remove punctuation, URLs, and handles, 3, remove stop words, 4, stemming or reducing words to their common stem, and 5, finally, tokenizing or splitting your document into single words or tokens.

For the assignments in this week, it will be relatively straightforward to implement this processing pipeline. In the real-world, you might find the gathering and processing of texts takes up a big chunk of your project's hours. Once you have a clean corpus of processed tweets, you will start by computing the vocabulary for each word in class, like you did in the previous week. This process will produce a table like the one shown here. You can compute the sum of words and class in each corpus in the same step.

From this table of frequencies, you get the conditional probability or probability of word given class by using the Laplacian smoothing formula. See how the number of unique words in V class is equal to 6. You only account for the words in the table, not the total number of words in the original corpus. This produces a table of conditional probabilities for each word and each class. This table only contains values greater than 0. For the forth step, you'll get the Lambda score for each word, which is the log of the ratio of your conditional probabilities.

The fifth step is the estimation of the log prior. To do this, you'll need to count the number of positive and negative tweets. Then the log prior is the log of the ratio of the number of positive tweets over the number of negative tweets. In the upcoming assignments, you'll be working with a balanced datasets. The log prior is equal to 0. For unbalanced datasets, this term will become important. In summary, training a Naive Bayes model can be divided into six logical steps.

You get to annotate a dataset with positive and negative tweets. Typically, it's better if your tweets match the same context that you want to use in the final model. Then you process the raw texts to get a corpus of clean standardized tokens. You compute the dictionary frequencies for each word in class, then compute the conditional probabilities of each word using the Laplacian smoothing formula, you compute the lambda factor for each word, and finally, you estimate the log prior of the model or how likely it is to see a positive tweet in your accounts.

That was quite a lot. Now, you have seen how to build a probability table needed to apply Naive Bayes. The next exciting thing we'll do is to classify your sentences.

9. 01_16_testing-naive-bayes.en
============================

![119.png](./images/119.png)
![120.png](./images/120.png)
![121.png](./images/121.png)
![122.png](./images/122.png)
![123.png](./images/123.png)
![124.png](./images/124.png)
![125.png](./images/125.png)
![126.png](./images/126.png)
![127.png](./images/127.png)
![128.png](./images/128.png)
![129.png](./images/129.png)
![130.png](./images/130.png)

This part will be fun as you will apply the Naive Bayes classifier on real test examples. It is similar to what you did in the first video of the week, but we'll cover some special corner cases. Once you have trained your model, the next step is to test it. You do so by taking the conditional probabilities you just derived. You use them to predict the sentiments of new unseen tweets. After that, you'll evaluate your model performance, and you will do so just like how you did it in the last week.

You use your test sets of annotated tweets. With the calculations you've done already, you have a table with the Lambda score for each unique word in your vocabulary. With your estimation of the logprior, you can predict sentiments on a new tweet. This new tweet says, "I passed the NLP interview." You can use your model to predict if this is a positive or negative tweet. Before anything else, you must pre-process this text, removing the punctuation, stemming the words, and tokenizing to produce a vector of words like this one.

Now, you look up each word from the vector in your log-likelihood table. If the word is found, such as I pass, the, and NLP, you sum over all the corresponding Lambda terms. The values that don't show up in the table of Lambdas, like interview, are considered neutral and don't contribute anything to the score. Your model can only give a score for words it's seen before. Now, you add the log prior to account for the balance or imbalance of the classes in the datasets.

This score sums up to 0.48. Remember, if this score is bigger than 0, then this tweet has a positive sentiment. Yes, in your model and in real life, passing the NLP interview is a very positive thing. You just predicted the sentiment of a new tweet, and that's awesome. It's time to test the performance of your classifier on unseen data, just like you already did for a different scenario in the previous module. Let's quickly review that process as applied to Naive Bayes.

This week's assignments includes a validation set. This data was set aside during training and is composed of a set of raw tweets, so X_val and their corresponding sentiments Y_val. You'll have to implement the accuracy function to measure the performance of your trained model, represented by the Lambda table and the logprior using these data. First, compute the score of each entry in X_val, like you just did previously. Then evaluate whether each score is greater than 0.

This produces a vector populated with zeros and ones, indicating if the predicted sentiment is negative or positive respectively. For each tweet in the validation sets. With your new predictions vector, you can compute the accuracy of your model over the validation sets. To do this part, you will compare your predictions against the true value for each observation from your validation data, Y-val. If the values are equal and your prediction is correct, you'll get a value of one and zero if incorrect.

Once you have compared the values of every prediction with the true labels of your validation sets, you can compute the accuracy as the sum of this vector divided by the number of examples in the validation sets, just like you did for the logistic regression. Let's revisit everything you just did. To test the performance of your Naive Bayes model, you use a validation set to allow you to predict the sentiment score for an unseen tweet using your newly trained model.

Then you compared your predictions with the true labels provided in the validation sets to get the percentage of tweets that were correctly predicted by your label. Then you compared your predictions with the true labels provided in the validation sets. This allowed you to get the percentage of tweets that were correctly predicted by your model. You also saw that words that don't appear in the Lambda table are treated as neutral words. Now you know how to apply the Naive Bayes method to test examples.

In the coding exercise at the end of the week, you will use it to classify tweets. Next, I'll show you other things it can do.

10. 01_18_applications-of-naive-bayes.en
====================================

![131.png](./images/131.png)
![132.png](./images/132.png)
![133.png](./images/133.png)
![134.png](./images/134.png)
![135.png](./images/135.png)
![136.png](./images/136.png)

Earlier in the week, you used a Naive Bayes method to classify tweets. But that's going to be used to do a number of things like identify who's an author of a text. I'll give you a few ideas of what those things may be. When you use Naive Bayes to predict the sentiment of a tweet, what you're actually doing is estimating the probability for each class by using the joint probability of the words in classes. The Naive Bayes formula is as the ratio between these two probabilities, the products of the priors and the likelihoods.

You can use this ratio between conditional probabilities for much more than sentiment analysis. For one, you could do author identification. If you had two large corpora, each written by different authors, you could train a model to recognize whether a new document was written by one or the other. Or if you had some works by Shakespeare and some works by Hemingway, you could calculate the Lambda for each word to predict how likely a new word is to be used by Shakespeare or alternatively by Hemingway.

This method also allows you to determine author Identity. Another common use is spam filtering. Using information taken from the sender, subjects and content, you could decide whether an email is spam or not. One of the earliest uses of Naive Bayes was filtering between relevant and irrelevant documents in a database given the sets of keywords in a query. In this case, you only needed to calculate the likelihood of the documents given the query. You can't know beforehand what's a relevant or irrelevant document looks like.

You can compute the likelihood for each document in your dataset and then store the documents based on its likelihoods. You can choose to keep the first m results or the ones that have a likelihood larger than a certain threshold. Finally, you can also use Naive Bayes for word disambiguation, which is to say, breaking down words for contextual clarity. Consider that you have only two possible interpretations of a given word within a text. Let's say you don't know if the word bank in your reading is referring to the bank of a river or to a financial institution.

To disambiguate your word, calculate the score of the documents, given that it refers to each one of the possible meanings. In this case, if the texts refers to the concept of river, instead of the concept of money, then the score will be bigger than one. That's cool, right? In summary, Bayes rule and it's Naive approximation has a wide range of applications in sentiment analysis, author identification, information retrieval, and word disambiguation.

It's a popular method since it's relatively simple to train use and interpret. You'll be using the Bayes rule and Naive Bayes again in the weeks ahead. Now, you're fully equipped. As you've seen in this video, Naive Bayes can be used for many classification tasks. Next, I'll show you the assumptions that underlie the Naive Bayes method.

11. 01_20_naive-bayes-assumptions.en
================================

![137.png](./images/137.png)
![138.png](./images/138.png)
![139.png](./images/139.png)
![140.png](./images/140.png)
![141.png](./images/141.png)
![142.png](./images/142.png)
![143.png](./images/143.png)

Now I'm going to the assumptions underlying the naïve bayes method. The main one, is independence of words in a sentence. And I'll tell you why this can be a big problem, when the method is applied. Naïve bayes is a very simple model because it doesn't require setting any custom parameters. This method is referred to as naïve, because of the assumptions it makes about the data. The first assumption is independence between the predictors or features associated with each class.

And the second, has to do with your validation set. Let's explore each of these assumptions and how they could affect your results. To illustrate what independence between features looks like, let's look at the following sentence. It is sunny and hot in the Sahara desert. Naïve Bayes assumes that the words in a piece of text are independent of one another. But as you can see, this typically isn't the case, the word sunny and hot often appear together as they do in this example.

Taken together, they might also be related to the thing they're describing, like a beach or a desert. So the words in the sentence are not always necessarily independent of one another. But naïve bayes, assumes that they are, this could lead you to under or overestimate the conditional probabilities of individual words. When using a naïve bayes, for example, if your task was to complete the sentence, it's always cold and snowy in blank. Naïve bayes might assign equal probability to the words spring, summer, fall and winter.

Even though from the context you can see that winter should be the most likely candidate And the next courses of this specialization, you will be introduced to some more sophisticated methods, let's deal with this. Another issue with naïve bayes is that it relies on the distribution of the training data sets. A good data set, will contain the same proportion of positive and negative tweets as a random sample. However, most of the available annotated corpora are artificially balanced, just like the data set you use for the assignment.

And the real tweet stream, positive tweets tend to occur more often than their negative counterparts. One reason for this is that negative tweets, might contain content that is banned by the platform or muted by the user. Such as inappropriate or offensive vocabulary, assuming that reality behaves as your training corpus. This could result in a very optimistic or very pessimistic model. There's a lot more on this, in the last video of this module which analyzes the sources of errors in naïve bayes.

Let's do a quick recap of all this new information, the assumption of independence and naïve bayes is very difficult to guarantee. But despite that, the model works pretty well in certain situations. And for the assignments in this module, the relative frequency of positive and negative tweets and your training data sets, needs to be balanced in order to deliver an accurate results. Now you understand the assumptions that underlie the naïve bayes method.

What if it fails to perform well, for some sentence in the next video, I'll show you what to do in such cases.

12. 01_22_error-analysis.en
=======================

![144.png](./images/144.png)
![145.png](./images/145.png)
![146.png](./images/146.png)
![147.png](./images/147.png)
![148.png](./images/148.png)
![149.png](./images/149.png)
![150.png](./images/150.png)
![151.png](./images/151.png)

No matter what NLP method you use, you will one day find yourself faced with an error. For example a misclassified sentence. In this video, I'll show you how to analyze such errors. >> Let us consider some possible errors and the model prediction that can be caused by these issues. One semantic meaning lost in the pre processing step. Two, a word order affects the meaning of a sentence. And three some quirks of languages come naturally to humans but confuse naive Bayes models.

So let's start. One of your main considerations when analyzing errors in NLP systems is what the processed version of the text actually looks like. Let's look at this tweet, my beloved grandmother with some punctuation indicating his sad face. The sad face punctuation in this case is very important to the sentiments of the tweet because it tells you what's happening. But if you're removing punctuation then the processed tweet will leave behind only beloved grandmother, which looks like a very positive tweet.

My beloved grandmother exclamation mark would be a very different sentiments. So remember always check what the actual text looks like. It's not just about punctuation either. Check out this tweet. This is not good because your attitude is not even close to being nice. If you remove neutral words like not and this what you're left with is the following. Good, attitude, close, nice. From this set of words and you classifier will infer that this is something very positive.

We'll talk later on about handling nots and word orders. But remember double check what your process text looks like to make sure your model will be able to get an accurate read. The inputs pipeline isn't the only potential source of trouble. Look at these tweets. I'm happy because I did not go. This is a purely positive tweets. I am not happy because I did not go with a negative sentiment. In this case the not is important to the sentiment. What gets missed by your naive Bayes classifier.

So word order can be as important as spelling. There are many other factors to consider as well and you will see more and more ways to build systems that handle them in the weeks to come. Another problem of naive Bayes is something called an adversarial attack. The term adversarial attack describe some common language phenomenon like sarcasm, irony and euphemism. Humans pick these up quickly but machines are terrible at it. This tweet this is a ridiculously powerful movie.

The plot was gripping and I cried right through until the ending contains a somewhat positive movie review, but pre-processing might suggest otherwise. If you pre process this tweet you'll get a list of mostly negative words. But as you can see they were actually used to describe a movie that the author enjoyed. If you use naive Bayes on this list of words, it would end up giving a very negative score regardless. >> Now you know how to apply the naive Bayes method to text classification.

It makes the independence assumption which can lead to errors. Now you know how to analyze them. It's still a very powerful baseline, as you know, it relies on word frequency counts. Next week we can learn how to use word vectors. This can give us better results.

13. 01_24_week-conclusion.en
========================

Congratulations on completing this week's materials. You learned about Bayes rule and conditional probability. You computed the likelihood of a word being associated with a particular sentiment. By computing the probability of that word being associated with positive sentiment. And then dividing it by the probability of that word being associated with the negative sentiment. You also learned how to do error analysis, which is an important tool that allows you to debug your model if it's not working.

Many of the skills you've learned here can easily be transferred when deploying other models in the specialization. Next, you'll apply these skills in this week's programming assignment. And after that we'll be looking at cosine similarity and principal component analysis. Good luck in the programming assignment. >> Good luck.

## 03_vector-space-models

1. 01_01_week-introduction.en
==========================

Welcome to week three. This week is all about vector spaces and how to manipulate word vectors. Learning how word vectors are represented in natural language processing is fundamental to all NLP applications. Because any NLP model you build has the first step which entails representing the word into some type of numerical encode. For example, you can represent a word as a number or as a vector. And this week you will also learn how to compare different word vectors through two different methods.

Known as Euclidean distance and cosine similarity. Furthermore, you can also plot word vectors with very high dimensions in a two D plane. To see how similar words end up clustering near one another. Younes will show you the details. >> Okay, great, let's do it.

2. 01_02_vector-space-models.en
============================

![152.png](./images/152.png)
![153.png](./images/153.png)
![154.png](./images/154.png)
![155.png](./images/155.png)
![156.png](./images/156.png)
![157.png](./images/157.png)
![158.png](./images/158.png)
![159.png](./images/159.png)

Last week you learned about a classification algorithm known as naive bayes. This week you're going to learn about vector spaces and specifically you will learn what type of information these vectors could encode. You'll see different types of applications that you can use with these vector spaces and you'll see different types of algorithms you'll be implementing. Let's take a look at an example. In this video I'm going to introduce you to the general idea behind vector space models.

You're going to see their advantages along with some of their applications in natural language processing. So suppose you have two questions, the first one is, where are you heading? And the second one is where are you from? These sentences have identical words except for the last ones. However, they both have a different meaning. On the other hand say you have two more questions whose words are completely different but both sentences mean the same thing.

Vector space models will help you identify whether the first pair of questions or the second pair are similar in meaning even if they do not share the same words. They can be used to identify similarity for a question answering, paraphrasing and summarization. Vector space models will also allow you to capture dependencies between words. Consider this sentence, you eat cereal from a bowl, here you can see that the words cereal and the word bowl are related.

Now let's look at this other sentence, you buy something and someone else sells it. So what it's saying is that someone sells something because someone else buys it. The second half of the sentence is dependent on the first half. With vectors based models, you will be able to capture this and many other types of relationships among different sets of words. Vector space models are used in information extraction to answer questions, in the style of who, what, where, how and etcetera.

In machine translation and in chatbot programming. They're also used in many, many other applications. As a final thought I'd like to share with you this quote from John Firth, a famous English linguists, you shall know a word by the company it keeps. This is one of the most fundamental concepts in NLP. When using vector space models the way that representations are made is by identifying the context around each word in the text and this captures the relative meaning.

Eureka, vector space models allow you to represent words and documents as vectors. This captures the relative meaning. You learn about vector space models and you have seen different types of applications where these vector space models are used. In the next video you will build them from scratch and specifically you will see how they are built using cooccurrence matrices

3. 01_04_word-by-word-and-word-by-doc.en
=====================================

![160.png](./images/160.png)
![161.png](./images/161.png)
![162.png](./images/162.png)
![163.png](./images/163.png)
![164.png](./images/164.png)
![165.png](./images/165.png)
![166.png](./images/166.png)
![167.png](./images/167.png)
![168.png](./images/168.png)
![169.png](./images/169.png)
![170.png](./images/170.png)

In this video, you'll learn how you can construct your vectors based off a co-occurrence matrix. Specifically, depending on the task you are trying to solve, you can have several possible designs. You will also see how you can encode a word or in documents as a vector. Let me show you how you can do this. To get a vector space model using a word-by-word design, you will make a co-occurrence matrix and extract vector representations for the words in your corpus.

You'll be able to get a vector space model using a word by document design using a similar approach. Finally, I'll show you how in a vector space you can find relationships between words and vectors, also known as their similarity. The co-occurrence of two different words is the number of times that they appear in your corpus together within a certain word distance k. For instance, suppose that your corpus has the following two sentences. The role of the co-occurrence matrix corresponding to the word data with a k value equal to 2, would be populated with the following values.

For the column corresponding to the word simple, you'd get a value equal to 2, because data and simple co-occur in the first sentence within a distance of one word and in the second sentence within a distance of two words, the row of the co-occurrence matrix corresponding to the word data would look like this if you consider the co-occurrence with the words simple, raw, like and I. In this case, the vector representation of the word data would be equal to 2, 1, 1, 0.

With a word by word design, you can get a representation with n entries, with n between one and the size of your entire vocabulary. For a word by document design, the process is quite similar. In this case, you will count the times that words from your vocabulary appear in documents that belong to specific categories. For instance, you could have a corpus consisting of documents between different topics like entertainment, economy, and machine learning.

Here, you'd have to count the number of times that your words appear on the documents that belong to each of the three categories. In this example, suppose that the word data, appears 500 times in documents from your corpus related to entertainment, 6,620 times in economy documents, and 9,320 in documents related to machine learning. The word film appears in each document's category, 7,000, 4,000, and 1,000 times respectively. Can you get a sense of where this is going already?

Once you've constructed the representations for multiple sets of documents or words, you'll guess your vector space. Let's take the matrix from the last example. Here you could take a representation for the words, data and film from the rows of the table. However, I'll take the representation for every category of documents by looking at the columns. The vector space will have two-dimensions. The number of times that the words, data and film appear on the type of documents.

For the entertainment corpus, you'd have the following vector representations This one for the economy category, and that's for the machine learning category.Note that in this space it is easy to see that the economy and machine learning documents are much more similar than they are to the entertainment category. Coming up soon, you'll make comparisons between vector representations using the cosine similarity and the Euclidean distance in order to get the angle and distance between them.

So far you've seen how to get vector spaces by two different designs; word by word and word by document; by either counting the co-occurrence of words or the co-occurrence of words in the documents corpora. I've also showed you that in vector spaces, you can determine relationships between types of documents like similarity. Now you're becoming more and more familiar with these vector spaces. You've seen several possible designs that you can use to solve a specific task.

You've also seen how you can encode words or tweets as vectors. In the next video, you'll learn about a new similarity metric that will allow you to compare these two vectors. The similarity metric is known as the Euclidean distance.

4. 01_06_euclidean-distance.en
===========================

![171.png](./images/171.png)
![172.png](./images/172.png)
![173.png](./images/173.png)
![174.png](./images/174.png)
![175.png](./images/175.png)
![176.png](./images/176.png)
![177.png](./images/177.png)
![178.png](./images/178.png)
![179.png](./images/179.png)
![180.png](./images/180.png)
![181.png](./images/181.png)
![182.png](./images/182.png)


Hello. In this video, you're going to learn about Euclidean distance, which is a similarity metric. This metric allows you to identify how far two points or two vectors are apart from each other. During this segment, you will get the Euclidean distance between two documents vectors like the ones from the previous video and then generalize that notion to vector spaces in higher dimensions. Let's use two of the corpora vectors you saw previously. Remember in that example, there were two dimensions.

The number of times that the word data and the word film appeared in the corpus. Corpus A will be the entertainment corpus and Corpus B will be the machine-learning corpus. Now let's represent those vectors as points in the vector space. The Euclidean distance is the length of the straight line segments connecting them. To get that value, you should use the following formula. The first term is their horizontal distance squared, and the second term is their vertical distance squared.

As you see, this formula is an example of the Pythagorean theorem. If you solve for each of the terms in the equation, you should arrive at this expression, and at last get a Euclidean distance approximately equal to 10,667. Feel free to pause the video and check this process. When you have higher dimensions, the Euclidean distance is not much more difficult. Let's walk through an example using the following co-occurrence matrix. Suppose that you want to know the Euclidean distance between the vector v of the word ice cream and the vector representation w of the word the boba.

To start, you need to get the difference between each of their dimensions. Square those differences, sum them up, and then get the square roots of your results. This process is the generalization of the one from the last slide. This is the formula that you would use to get the Euclidean distance between vector representations on an n-dimensional vector space. If you remember from algebra, this formula is known as the norm of the difference between the vectors that you are comparing.

Let's take a look at the implementation of the Euclidean distance in Python. If you have two vector representations like the ones from the previous example, you can use the linalg module from NumPy to get the norm of the difference between them. If you implement this code in Python, you should get these results. The norm function works for n-dimensional spaces. The primary takeaways here are that the Euclidean distance is basically the length of the straight line that connects two vectors and that together Euclidean distance, you have to calculate the norm of the difference between the vectors that you are comparing.

By using this metric, you can get a sense of how similar two documents or words are. Now that you have learned Euclidean distance, in the next video, I'll show you a different type of similarity function. Concretely, I'll show you the cosine similarity function, which is one of the most popular similarity functions. See you in the next video.

5. 01_08_cosine-similarity-intuition.en
====================================

![183.png](./images/183.png)
![184.png](./images/184.png)
![185.png](./images/185.png)
![186.png](./images/186.png)
![187.png](./images/187.png)
![188.png](./images/188.png)
![189.png](./images/189.png)

In this video, you're going to learn about cosine similarity, which is another type of similarity function. It basically makes use of the cosine of the angle between two vectors. Based on that, it tells you whether two vectors are close or not. In this section, you will see the problem of using Euclidean distance, especially when comparing vector representations of documents or corpora, and how the cosine similarity metric could help you overcome this problem.

To illustrate how the Euclidean distance might be problematic, let's take the following example. Suppose that you are in a vector space where the corpora are represented by the occurrence of the words disease and eggs. Here's the representation of a food corpus, and agriculture corpus, and the history corpus. Each one of these corpora have texts related to that subject. But you know that the word totals in the corpora differ from one another. In fact, the agriculture and the history corpus have a similar number of words, while the food corpus has a relatively small number.

Let's define the Euclidean distance between the food and the agriculture corpus as d_1 and let's the Euclidean distance between the agriculture and the history corpus be d_2. As you can see, the distance d_2 is smaller than the distance d_1, which would suggest that the agriculture and history corpora are more similar than the agriculture and food corpora. Another common method for determining the similarity between vectors is computing the cosine of their inner angle.

If the angle is small, the cosine would be close to one. As the angle approaches 90 degrees, the cosine approaches zero. As you can see here, the angle Alpha between food and agriculture is smaller than the angle Beta between agriculture and history. In this particular case, the cosine of those angles is a better proxy of similarity between these vector representations than their Euclidean distance. Now you're familiar with the main intuition behind the use of the cosine similarity as a metric to compare the similarity between two vector representations.

Remember that the main advantage of this metric over the Euclidean distance is that it isn't biased by the size difference between the representations. Soon, you'll get the chance to actually calculate this metric. In this video, you learned why the cosine similarity metric is useful. If you have two documents of very different sizes, then taking the Euclidean distance is not ideal. The cosine similarity used the angle between the documents and is thus not dependent on the size of the corpuses.

6. 01_10_cosine-similarity.en
==========================

![190.png](./images/190.png)
![191.png](./images/191.png)
![192.png](./images/192.png)
![193.png](./images/193.png)
![194.png](./images/194.png)
![195.png](./images/195.png)
![196.png](./images/196.png)
![197.png](./images/197.png)
![198.png](./images/198.png)
![199.png](./images/199.png)

In this video, you will learn how to compute the dot product between two vectors and how to compute the norm. Once you know how to do these two things, you'll be able to compute the cosine similarity score. Now that you have the intuition behind the use of cosine of the angle between two vector representations as a similarity metric. I'll go deeper into an explanation and then show you how to calculate the cosine similarity metric. In this section, you will get the cosine of the inner angle of two vectors.

Then I'll show you how the value of the cosine similarity is related to the similarity of the directions of two vectors. First, you have to recall some definitions from algebra. The norm of a vector or its magnitude is written like this. It's defined to be the square root of the sum of its elements squared. The dot product between two vectors is the sum of the products between their elements in each dimension of the vector space. Let's take another look at two of the corpora from the last section.

Remember that's in this example, you have a vector space where the representations of the corpora is given by the number of occurrences of the words disease and eggs. The angle between those vector representations is denoted by Beta. The agriculture corpus is represented by the vector v, and the history corpus is going to be vector w. The dot products between those vectors is defined as follows. From this equation, you see that the cosine of the angle Beta is equal to the dot-product between the vectors divided by the product of the two norms.

Replacing the actual values from the vector representations should give you this expression. In the numerator, you'll have the product between the occurrences of the words disease and eggs, and then the denominator, you have the product between the norm of the vector representations of the agriculture and history corpora, ultimately, you should get a cosine similarity of 0.87. Feel free to pause and do the calculations yourself. But what does this metric tells you about the similarity of two different vectors?

Consider when two vectors are orthogonal in the vector spaces that you know so far, it is only possible to have positive values for any dimension. The maximum angle between pair of vectors is 90 degrees. In that case, the cosine would be equal to 0, and it would mean that the two vectors have orthogonal directions or that they are maximally dissimilar. Now let's look at the case where the vectors have the same direction. In this case, the angle between them is 0 degrees and the cosine is equal to 1 Because cosine of 0 is just 1.

As you can see, as the cosine of the angle between two vectors approaches 1, the closer their directions are. Now you know how to get the cosine similarity between any pair of vectors. An important takeaway is that this metric is proportional to the similarity between the directions of the vectors that you are comparing and that's for the vector spaces you've seen so far, the cosine similarity takes values between 0 and 1. To recap, you have learned to compute the cosine similarity score between two vectors.

For the positive vectors you have seen so far, the score is bounded between 0 and 1. Note that if you were to take any cosine similarity score of a vector with itself, you will get 1. If the vectors are perpendicular, it'll give you 0. Similar vectors have higher scores.

7. 01_12_manipulating-words-in-vector-spaces.en
============================================

![200.png](./images/200.png)
![201.png](./images/201.png)
![202.png](./images/202.png)
![203.png](./images/203.png)
![204.png](./images/204.png)
![205.png](./images/205.png)
![206.png](./images/206.png)
![207.png](./images/207.png)


Hello. In this video, you're going to learn to manipulate vectors by performing some simple vector arithmetic. Meaning by adding vectors or subtracting vectors, you'll be able to predict the countries of certain capitals. Let's dive in. I'll show you how to manipulate vector representations in order to infer unknown relations among words. Suppose that you have a vector space with countries and their capital cities. You know that the capital of the United States is Washington DC, and you don't know the capital of Russia.

But you'd like to use the known relationship between Washington DC and the USA to figure it out. For that, you'll just use some vector algebra. For this example, you are in a hypothetical two-dimensional vector space that has different representations for different countries and capitals cities. First, you will have to find the relationship between the Washington DC, and USA vector representations. In other words, which vector connects them? To do that, get the difference between the two vectors.

The values from that will tell you how many units on each dimension you should move in order to find a country's capital in that vector space. To find the capital city of Russia, you will have to sum its vector representation with the vector that you also got in the last step. At the end, you should deduce that the capital of Russia has a vector representation of 10, 4. However, there are no cities with that representation, so you'll have to take the one that is the most similar to it's by comparing each vector with a Euclidean distances or cosine similarities.

In this case, the vector representation that is closest to the 10, 4 is the one for Moscow. Using the simple process, you could have predicted the capital of Russia if you knew the capital of the USA. The only catch here is that you need a vector space where the representations capture the relative meaning of words. Now you have a simple process to get unknown relationships between words, by the use of known relationships between others. You now know the importance of having vector spaces where the representations of words capture their relative meaning in natural language.

In upcoming parts of this specialization, you'll perform more sophisticated tasks taking advantage of this representation. You have now seen the clustering of all vectors when plotted on two axes. You have also seen that the vectors of the words that occur in similar places in the sentence, will be encoded in a similar way. You can take advantage of this type of consistency encoding to identify patterns. For example, if you have the word doctor and you are to find the closest words that are closest to it by computing cosine similarity, you might get the word doctors, nurse, cardiologist, surgeon, etc.

In the next video, you will learn how to to plot these d-dimensional vectors on a 2D plane.

8. 01_14_visualization-and-pca.en
==============================

![208.png](./images/208.png)
![209.png](./images/209.png)
![210.png](./images/210.png)
![211.png](./images/211.png)
![212.png](./images/212.png)
![213.png](./images/213.png)
![214.png](./images/214.png)
![215.png](./images/215.png)

It is often the case that you'll end up having vectors in very high dimensions. You want to find a way to reduce the dimension of these vectors to two dimensions. So you can plot it on an XY axis. You will now learn about principal components analysis which will allow you to do so. You are going to be using principal component analysis to visualize vector representations with higher dimensions than the ones that you've seen plotted so far. To get started, I'll give you some intuition on the motivation for visualizing vector representation of words and you will see for yourself with principal component analysis does and how it is used for dimensionality reduction.

Imagine you have the following representation for your words in a vector space. In this scenario, your vector space dimension is higher than two that the words oil and gas and city and town are related. And you want to see if that relationship is captured by the representation of your words. So how could you visualize your words in order to see this and other possible relationships, dimensionality reduction is a perfect choice for this task. When you have a representation of your words in a high dimensional space, you could use an algorithm like PCA to get a representation on a vector space with fewer dimensions.

If you want to visualize your data, you can get a reduced representation with three or fewer features. If you perform principal component analysis on your data and get a two dimensional representation, you can then plot a visual of your words. In this case, you might find that your initial representation captured the relationship between the words oil and gas and city and town. Because in your two dimensional space they appear to be clustered with related words.

You can even find other relationships among your words that you didn't expect. Which is a fun and useful possibility. Now, that you know what PCA can help you achieve. Let's go into detail on how it works. For the sake of simplicity. I'll begin with a two dimensional vector space. Say that you want your data to be represented by one feature. Instead using PCA. First, you'll find a set of un correlated features and then project your data to a one dimensional space trying to retain as much information as possible.

As you can see, this process is quite straightforward. Coming up, you'll see for yourself the details of how this algorithm works along with how to get uncorrelated features. You'll also project your data for a representation in a lower dimension while retaining as much information as possible. Let's do a quick review before you go. PCA Is an algorithm used for dimensionality reduction that can find uncorrelated features for your data. It's very helpful for visualizing your data to check if your representation is capturing relationships among words.

You learned how to visualize components using PCA. So given any d dimensional vector, you can transform it into two dimensions and then you can create a plot. In the next video, we will go over how the algorithm actually works.

9. 01_16_pca-algorithm.en
======================

![216.png](./images/216.png)
![217.png](./images/217.png)
![218.png](./images/218.png)
![219.png](./images/219.png)
![220.png](./images/220.png)
![221.png](./images/221.png)
![222.png](./images/222.png)

You will now learn about Eigenvalues and Eigenvectors and you'll see how you can use them to reduce the dimension of your features. >> First, I'll show you how to get uncorrelated features for your data. And then how to reduce the dimensions of your word representations while trying to keep as much information as possible from your original embedding. To perform dimensionality reduction using PCA, begin with your original vector space, then you get uncorrelated features for your data.

And finally, you project your data to a number of desired features that retain the most information. You may recall from algebra that matrices have Eigenvectors and Eigenvalues. You do not need to remember how to get those right now, but you should keep in mind that in PCA, they are useful because the Eigenvectors of the co-variance matrix from your data. They give directions of uncorrelated features and the Eigenvalues are the variance of your data sets in each of those new features.

So to perform PCA, you will need to get the Eigenvectors and Eigenvalues from the co variance matrix of your data. The first step is to get a set of uncorrelated features for this step, you mean normalize your data, then get the covariance matrix. And finally perform a singular value decomposition to get a set of three matrices. The first of those matrices contain the Eigenvectors stacked column wise and the second one has the Eigenvalues on the diagonal.

The singular vector decomposition is already implemented in many programming libraries, so you don't have to worry about how it works. The next step is to project your data to a new sets of features. You will be using the Eigenvectors and Eigenvalues in this step, let's denote the Eigenvectors with U and the Eigenvalues with S. First, you will perform the dot products between the matrix containing your word embeddings and the first n columns of the U matrix.

Where N equals the number of dimensions that you want to have at the end. For visualization, it's common practice to have two dimensions, then you'll get the percentage of variance retained in the new vector space. As an important side note, your Eigenvectors and Eigenvalues should be organized according to the Eigenvalues in descending order. This condition will ensure that you retain as much information as possible from your original embedding. However, most libraries order those matrices for you.

Wrapping up, Eigenvectors from the co variance matrix of your normalized data, give the directions of uncorrelated features. The Eigenvalues associated with those Eigenvectors tell you the variance of your data on those features. The dot products between your word embeddings and the matrix of Eigenvectors will project your data onto a new vector space of the dimension that you choose. You are now ready to implement PCA in this week's assignment to visualize word representations.

Good luck with that and remember to have fun. >> Congratulations, you now know all about PCA and you know all the steps required for you to implement it. Next week, you will learn about vector spaces and I'll show you how you can use them to build a simple machine translation system.

10. 01_19_week-conclusion.en
========================

Great work getting through this week's materials. You now know what vector spaces are, how we represent words as vectors and how to manipulate them. For example, you saw how to compare two words by doing cosine similarity or Euclidean distance and you learned why cosine similarity is more common. In this week's programming assignment, you will be given capital cities and their countries in word vectors and you will manipulate them by finding the country given the capital city.

Isn't that cool? You will also reduce high dimension word vectors into two dimensions and plot them on an x y plane. You will find that similar word vectors end up being clustered near one another. Next week, you'll get started on machine translation. Good luck in the programming assignment.

## 04_machine-translation-and-document-search

### 01_lecture-machine-translation

1. 01_01_week-introduction.en
==========================

You are in week 4 already. This week is all about preparing you to do a quick nearest neighbor search using locality sensitive hashing. For example, you will translate one word from one language to another by manipulating word vectors. If you have a set of English word vectors and a set of equivalent French word vectors, you want to learn a mapping from an English vector to the French vector. This week, we will show you how to do k-nearest neighbors very quickly and with a technique known as locality sensitive hashing.

In a nutshell, this technique allows you to split your search range into similar regions. Given an input, you can search for it in the most likely region that it's going to appear. Younes will explain how it works. Okay, great. Here we go.

2. 01_02_overview.en
=================

![223.png](./images/223.png)
![224.png](./images/224.png)
![225.png](./images/225.png)
![226.png](./images/226.png)

Congratulations for making it to the final week of the course. I will now tell you what you're about to learn. In this fourth and final week of this course, you'll learn to implement machine translation to translate the English word "hello" to the French word "bonjour". You will also learn to implement document search. For example, given a document such as the sentence, "Can I get a refund?" you can search for similar documents such as, "What's your return policy," or "May I get my money back?" You will learn a set of skills that you can apply to both of these useful NLP tasks.

Here's a preview of the skills that you will practice in this week's lectures and assignments. Don't worry if you do not understand what some of these mean right now. You learned about each of these and get some practice before you move on to the assignments. First, you will learn about what it means to transform a vector, such as a word vector. You will learn how to implement "K nearest neighbors," which is a way of searching for similar items. You'll learn about hash tables, which will help you assign your word vectors into subsets.

Then you will learn how to divide the vector space into regions. Again, don't worry if you don't understand what this means at this point, you'll get some visual understanding of what this means and how it can help you improve search for similar words. Finally, you'll know how to implement locality-sensitive hashing, which helps you perform approximated K nearest neighbors, an efficient way of searching for similar word vectors. By practicing how to find similar word vectors, you'll effectively know how to implement machine translation and document search.

This is very exciting the material and we hope that you will really enjoy what you will learn this week. Now that you have an overview of what you're about to learn and the learning objectives of the week, we can go ahead and get started.

3. 01_03_transforming-word-vectors.en
==================================

![227.png](./images/227.png)
![228.png](./images/228.png)
![229.png](./images/229.png)
![230.png](./images/230.png)
![231.png](./images/231.png)
![232.png](./images/233.png)
![234.png](./images/234.png)
![235.png](./images/235.png)
![236.png](./images/236.png)
![237.png](./images/237.png)
![238.png](./images/238.png)
![239.png](./images/239.png)

Last video, you learned about word vectors and you saw that they can capture important properties of words. This week, you will make use of word vectors to learn to align words in two different languages, which will give you your first basic translation program. Later, I'll teach you locality sensitive hashing to speed it up. Let's first get an overview of machine translation by starting with an example of English to French translation. In order to translate an English word to a French word.

One way would be to generate an extensive list of English words and their associated French word. If you ask the human to do this, you would find someone who knows both languages to start making a list. If you want a machine to learn how to do this, you would calculate word embeddings associated with English and word embeddings associated with French. Next retrieve the English word embedding of a particular English word such as cat. Then find some way to transform the English word embedding into word embedding that has the meaning in the French word vector space.

We will see how to convert from the English word vector space to the French word vector space in the moment. Next, you'll take the transformed word vector and search for word vectors and the French word vector space that are most similar to it. The most similar words are candidates words for your translation. If your machine does a good job, it may find the word chat which is the French word for cat. You want to find the matrix that can do this transformation for you.

So let's talk about transforming vectors using matrices. To try this out for yourself, you can write the following code which is also in the notebook associated with this lecture. Define the matrix R, then defined the vector x, multiply x by R using numpy dot and the result is another two dimensional vector which is what you saw earlier. Please try this out for yourself. Now that we know that there can be matrix that transforms our English word vectors into relevant French word vectors.

How do we define this transformation matrix which will denote as R? We can start with a randomly selected matrix R and then see how it performs. When you try to translate the English vectors in matrix X and compare that to the actual French word vectors which is in the matrix Y. In order for this to work, you will first need to get a subset of English words and their French equivalents. Get their respective word vectors and stack the word vectors in the respective matrices, X and Y.

The key here is to keep the rows lined up, or to align the word vectors. This means that if the first row of matrix X contains the word cat, then the first row of the matrix Y should contain the French word for cat which is chat. Now you may be asking wait a minute. If I already have the English words and their French translations, why do I need to train a model to do this? Why not just save this information in a key value mapping like a python dictionary?

Well, the nice thing is that you can just collect a subset of these words to find your transformation matrix. And if it works well, then the model can be used to translate words that are not part of your original training set. So you only need to train on a subset of the English French vocabulary and not the entire vocabulary. So let's see how to find the good matrix R. First we compare the translation X times R with the actual French word embeddings in Y.

We do this by taking the X matrix times the R matrix and subtracting the Y matrix. I'll explain in more detail what this expression means and also what this capital F subscript means. But for now think of it as a measure of how far apart the attempted translation and the actual French vectors are. If you start with a random matrix R, you can gradually improve these matrix R in a loop. First compute the gradient by taking the derivative of this loss function with respect to the matrix R.

Next update the matrix R by subtracting the gradient, but note that it's the gradient weighted by the learning rate alpha. You can either pick a fixed number of times to go through the loop or check the loss at each iteration. And break out of the loop when the loss falls between a certain threshold. Now let's explain what this notation, what the double vertical lines means. This is measuring the magnitude or the norm of a matrix. Let's see an example of calculating this norm, and then see the general formula.

Let's say that the results of X times R minus Y is a matrix. We'll pretend for this example that there's only two words in this dictionary, which is the number of rows in the matrix. And the word embeddings have two dimensions. So that's the number of columns in the matrix. So matrices X, R, Y and A are all 2 by 2 matrices. If the matrix A looks like this, then to calculate its norm, we take two squared plus two squared plus two squared plus two squared, then take square roots.

This gives us four. Here is the actual formula. You just take all the elements in the matrix, square them and add them up. This norm has the subscript F. Because this is called the frobenius norm. Now let's calculate the frobenius norm in code. You start with a matrix A, use numpy dot square to square all the elements. Then use numpy dot sum, then numpy dot square roots to get four. Try it out for yourself. Know that in practice it's easier to minimize the square of the frobenius norm.

In other words, we can cancel out the square roots by taking the square. I'll explain in a moment why it's easier to work with the square of the norm. If we go back to our example with matrix A, the squared frobenius norm is just two squared plus two squared plus two squared plus two squared. Then we take the square root, but then cancel it out by squaring that sum. So the square of the frobenius norm is 16. Now let's also go into detail on how you can calculate the gradient of the loss function.

The loss is defined as the square of the frobenius norm, the gradient is a derivative of the loss with respect to the matrix R. If it looks like this, the scalar, M is the number of rows or words in the subset that we're using for training. If you remember from calculus, this may look familiar to you if you pretend that R as a single variable instead of a matrix. And x and y are constants. If you don't recognize this, don't worry, you won't need to know calculus here.

You'll be able to look up these derivatives online if you ever need to. Now going back to why it helps to use the square of the frobenius norm. It's easier to take the derivative of this expression, rather than dealing with the square roots that's in the frobenius norm. You'll implement this formula in the assignment. You have seen how with just one matrix, you can learn to align word vectors from one language to another. We will next look at the nearest neighbors.

4. 01_05_k-nearest-neighbors.en
============================

![240.png](./images/240.png)
![241.png](./images/241.png)
![242.png](./images/242.png)
![243.png](./images/243.png)
![244.png](./images/244.png)
![245.png](./images/245.png)


One key operation needed to find a matching word in the previous video was finding the k nearest neighbors of a vector. We will focus on this operation in the next few videos, as it's a basic building block for many NLP techniques. Notice that a transform or the vector after the transformation, if it's embedding through an R matrix, would be in the French word vector space. But it is not going to be necessarily identical to any of the word vectors in the French word vector space.

You need to search through the actual French word vectors to find a French word that is similar to the one that you created from the transformation. You may find words such as salut or bonjour which you can return as the French translation of the word hello. So the question is, how do you find similar word vectors? To understand how to find similar word vectors, let's look at a related question. How do you find your friends who are living nearby? Let's pretend that you are visiting San Francisco in the United States and you're visiting your dear friend Andrew.

You also want to visit your other friends over the weekend, preferably those who live nearby. One way to do this is to go through your address book, and for each friend, get their address, calculate how far they are from San Francisco. One friend is in Shanghai, the other friend is in Bangalore, and another friend is in Los Angeles. You can sort your friends by their distances to San Francisco, then rank them by how close they are. Notice that if you have a lot of friends, which I'm sure you do, this is a very time intensive process.

Is there a more efficient way to do this? Notice that two of these friends live in another continent, while the third friend lives in the United States. Could you have just searched for a subset of friends who live in the United States. You might have realized that it may not have been necessary to go through all of your friends in your address in order to find the ones closest to you. You might have imagined if you somehow could filter on which friends were all in a general region such as North America, then you could just search within that subgroup of friends.

If there is a way to slice up the geographic space into regions, you could search just within those regions. When you think about organizing subsets of a data-set efficiently, you may think about placing your data into buckets. If you think about buckets, then you'll definitely want to think about hash tables. Hash tables are useful tools for any kind of work involving data. You'll learn about hash tables next. In this video, I showed you how using K-nearest neighbors, you could translate a word even if it's transformation doesn't exactly match the word embedding in the desired language.

I introduced you to hash tables, a useful data structure that you will learn about in the next video. Great. Now you are ready to learn about hashing. This is an effective technique that would allow you to look up queries in a much faster way than simple linear search.

5. 01_07_hash-tables-and-hash-functions.en
=======================================

![246.png](./images/246.png)
![247.png](./images/247.png)
![248.png](./images/248.png)
![249.png](./images/249.png)
![250.png](./images/250.png)
![251.png](./images/251.png)
![252.png](./images/252.png)
![253.png](./images/253.png)
![254.png](./images/254.png)

In this video, you are going to learn about hash tables and hash functions. For example, imagine that you have a cupboard with several drawers. You might want to place similar objects in similar drawers. For example, paper documents alone, keys alone, and books alone. In this video, we will dive deeper into these concepts. Let us say you have several data items and you want to group them into buckets by some kind of similarity. One bucket can hold more than one item, and each item is always assigned to the same bucket.

The results would be these blue ovals end up in bucket number 1, these gray rectangles end up in bucket number 2, and these magenta triangles are assigned to bucket 3. Now, let's think about how we'd like to do this with word vectors. First, let's assume that the word vectors have just one dimension instead of 300 dimensions so each word is represented by a single number, such as 100, 14, 17, 10, and 97. You need to find a way to give each vector a hash value which is a key that tells us which bucket it's assigned to.

A function that assigns a hash value is called a hash function. In this example, here is a hash table which is a set of buckets. In this case, the hash table has 10 buckets. Notice how the word vectors 100 and 10 are assigned to bucket 0. The word vector 14 is assigned to bucket 4 and the word vectors 17 and 97 are assigned to bucket 7. Do you notice a pattern? This formula here is the hash function that's being used to assign the word vectors to their respective buckets.

The modulo operator takes the remainder after dividing by 10. The remainder is the hash value that tells us where the word vector should be stored. For example, 14 divided by 10 has a remainder of 4 so it goes to bucket 4. Now, let's build a basic hash table in code. Here's a definition of a function that takes in a list of values. You can think of each value as a one-dimensional vector. It also takes in the number of buckets. Define the hash function used in the modulo operator.

Then you create the hash table. Notice that this is a dictionary comprehension. The key is an integer and the value is an empty list which you'll use as a bucket for storage. For each word vector, calculate its hash value, then append it to the appropriate list. The hash table that is returned can be seen in the notebook that goes with this lecture. You'll see that the hash table is the same as what you saw in the previous slide. Now let's take another look at this basic hash table.

Recall that your original goal was to put similar word vectors into the same bucket. But here, it doesn't look like numbers that are close to each other are in the same bucket. For instance, 10, 14, and 17 are in different buckets. Ideally, you want to have a hash function that puts similar word vectors in the same buckets, like this. To do this, you'll need to use what's called locality-sensitive hashing. Locality is another word for location. Sensitive is another word for caring.

So locality-sensitive hashing is a hashing method that cares very deeply about assigning items based on where they're located in vector space. You'll learn about locality-sensitive hashing next. You learned a lot of new terms. You learned about hash values, hash functions, and buckets. You have also seen the code for how to build a hash table or the equivalence of the cupboard I spoke about in the intro of the video. In the next video, we will look at locality-sensitive hashing.

6. 01_09_locality-sensitive-hashing.en
===================================

![255.png](./images/255.png)
![256.png](./images/256.png)
![257.png](./images/257.png)
![258.png](./images/258.png)
![259.png](./images/259.png)
![260.png](./images/260.png)
![261.png](./images/261.png)
![262.png](./images/262.png)
![263.png](./images/264.png)
![265.png](./images/265.png)
![266.png](./images/266.png)
![267.png](./images/267.png)
![268.png](./images/268.png)
![269.png](./images/269.png)
![270.png](./images/270.png)
![271.png](./images/271.png)
![272.png](./images/272.png)
![273.png](./images/273.png)
![274.png](./images/274.png)
![275.png](./images/275.png)

One key method that you will use to reduce the computational cost of finding Neighbors in high dimensional spaces is locality sensitive hashing. In this video, I will teach you what hashes are and where they are used. To start thinking about locality sensitive hashing, let's first assume that you're using word vectors with just two dimensions. I'll depict each vector as a circle instead of arrows. So let's say you want to find a way to know that these blue dots are somehow close to each other, and that these grey dots are also related to each other.

First divide the space using these dashed lines, which I'll call planes. I'll explain why I call them planes in a bit. Notice how the blue plane slices up the space into vectors that are above it or below it. The blue vectors all happen to be on the same side of the blue plane. Similarly, the gray vectors happen to be above the grey plane. It looks like the planes can help us bucket the vectors into subsets based on their location, this is exactly what you want.

A hashing function that is sensitive to the location of the items that it's assigning into buckets. You're working your way towards locality sensitive hashing. Now, let's see why I'm calling these dash lines planes. A plane would be this magenta line into two dimensional space and it actually represents all the possible vectors that would be sitting on that plane. In other words, they would be parallel to the plane such as this blue vector or this orange vector.

You can define a plane with a single vector, this magenta vector is perpendicular to the plane and it's called the normal vector to that plane. The normal vector is perpendicular to any vectors that lie on the plane. It might help to think about this in three dimensions, find a sheet of paper and find a pencil. Place the paper on the table and draw some vectors on it, then hold the pencil vertically over the paper. Any vectors on the paper are perpendicular to the pencil.

Let's go back to two dimensions, you are able to see visually when the vector is on one side of the plane or the other. But how do you do this mathematically? Here are three sample vectors in blue, orange and green, the normal vector to the plane is labeled P. Let's focus on vector one, what if you take the dot product of P with vector one, you get three. I'll explain in a bit why you're doing this. Now, Let's look at Vector two, if you take the dot products of P with vector two you get zero.

Finally, Let's look at vector three, if you take the dot product of P with vector three, you get negative three. So the dots products are three, zero, and negative three. Do you notice something about the signs and how they're related to their position relative to the red plane? When the dot product is positive, the vector is on one side of the plane. If the dot product is negative, the vector is on the opposite side of the plane. If the dot product is zero, the vector is on the plane, so what's the dot products doing.

To visualize the dot product, imagine one of the vectors such as P as if it's the surface of the earth. Gravity pulls all objects straight down towards the surface of the earth, next pretend you're standing at the end of the vector V1. You tie a string to a rock and let gravity pull the rock to the surface of vector P, the string is perpendicular to vector P. Now, if you draw a vector that's in the same direction of P, what ends up at the rock, you have what's called the projection of vector V1 onto vector P.

The magnitude or length of that vector is equal to the dot product of V one and P. Furthermore, if you had this other green vector and projected it onto vector p, the projected vector would be pointing in the parallel but opposite direction of P. The dot product would be a negative number. This means that the sign of the dot product indicates the direction of the projection with respect to the purple normal vector. So whether the dot product is positive or negative can tell you whether the vector V1 or V2 are on one side of the plane or the other.

Let's use code to check which side of the plane a vector is on. The function side of plane takes in the normal vector P and a vector V. Use np dot to take the dot product, use np dot sign to get a plus one, if the dot product is positive. -1 if the product is negative or zero if the dot product is zero, I'm using np.asscalar. Notice the pronunciation of that function, if a vector can be represented as a single scalar, this function retrieves that scalar and that's it.

Please try it out for yourself, that was a lot of visualizations and the lots of projections. The main takeaway is that the sign of the projection of two vectors tells you which parts of the line the point lies. For example, above it or below it. In the next video, you will learn how to combine this concept with multiple planes to try to better approximate where a data point might be located.

7. 01_11_multiple-planes.en
========================

![276.png](./images/276.png)
![277.png](./images/277.png)
![278.png](./images/278.png)
![279.png](./images/279.png)
![280.png](./images/280.png)
![281.png](./images/281.png)
![282.png](./images/282.png)
![283.png](./images/283.png)
![284.png](./images/284.png)

Now that you know how projections work, I'll show you how you can combine several planes to help identify one hash value. In other words, I will show you how to identify where a data point is given several planes. In the last video, you saw how by the sign of the dot product between the normal vector of a plane and a vector representing your data, you could get a relative position relative to that plane. In this lecture, I'm going to show you how to use this information for multiple planes to get a hash value for your data in your vector space.

In order to divide your vector space into manageable regions, you'll want to use more than one plane. For each plane, you can find out whether a vector is on the positive or negative side of that plane. You'll get multiple signals, one, for each plane and you want to find a way to combine all of those signals into a single hash value. This hash value will define a particular region within the vector space. Let's walk through an example then you will see the general formula for combining signals from multiple planes.

For a single vector, let's say that its dot product with Plane 1 is three, so the sign is positive and the hash value is set to one to indicate that the sign is positive. For the second plane, the dot product is five. The sign is again positive and the hash value is one. For the third plane, the dot product is negative 2. The sign is negative 1 and the hash value is set to zero to indicate that the vector v is on the negative side of Plane 3. To combine these intermediate hash values into a single hash value, you'll do the following.

Take 2^0 times h_1 plus 2^1 times h_2 plus 2^2 times h_3. This gives us a combined hash value of three. Just as a reminder, you have multiple planes and it helps us to divide the vector space into smaller sub-regions. But you want to have a single hash value so you will know which bucket to assign the vector in. You do this by combining the signals from all the planes into a single hash value. Here are the rules you applied written out. If the sign of the dot product is greater than or equal to zero, assign the intermediate hash value of one.

Otherwise, if the dot product is less than zero, assign the intermediate hash value of zero. To combine the intermediate hash values , use this formula. This is how you get locality sensitive hashing. Let's implement this in code. Given a list of planes in a vector, start with a hash value of zero which you'll use to accumulate the sum of intermediate hash values. Then for each plane, you want to calculate the sign of the dot product. Set the intermediate hash value to one if the sign is greater than or equal to zero.

Else set it to zero. Then you multiply the intermediate hash value by two, raised to the ith power and add it to the hash value. Finally, you return the hash value. If you run code in the lecture notebook, you'll get the same results as the example you saw earlier. Go ahead and try it out. Now you've seen what it means for a hash function to be locality sensitive and you've seen examples of such hash functions. Next, you'll see how this is useful for the speeding up of the k nearest neighbor computation.

Let's go to the next video.

8. 01_13_approximate-nearest-neighbors.en
======================================

![285.png](./images/285.png)
![286.png](./images/286.png)
![287.png](./images/287.png)
![288.png](./images/288.png)
![289.png](./images/289.png)
![290.png](./images/290.png)
![291.png](./images/291.png)
![292.png](./images/292.png)

In the last video you learned about locality sensitive hashing, now it is time to put all this knowledge to use. You'll make an algorithm that computes the k nearest neighbors much faster than brute search. So far, we've seen that a few planes, such as these three can divide the vector space into regions. But are these planes the best way to divide up the vector space? What if instead, you divided the vector space like this? In fact, you can't know for sure which sets of planes is the best way to divide up the vector space.

So why not create multiple sets of random planes. So that you can divide up the vector space into multiple independent sets of hash tables. You can think of it like creating multiple copies of the universe or a multiverse, if you will. You can make use of all these different sets of random planes, in order to help us find a good sets of friendly neighborhood vectors. I mean, a set of k nearest neighbors. So back to our multiple sets of random planes, over here for instance, let's say you have a vector space.

And this magenta dot in the middle represents the transformation of an English word into a French word vector. You're trying to find other French word vectors that may be similar, so maybe one universe of random planes. Helped us to determine that this magenta vector and these green vectors are all assigned to the same hash buckets. Another entirely different sets of random planes, helped us determine. That these blue vectors are in the same hash buckets as the red vector.

A third set of random planes, helped us determine that these orange vectors are in the same hash buckets as the magenta vector. By using multiple sets of random planes for locality sensitive hashing. You have a more robust way of searching the vector space, for a set of vectors that are possible candidates to be nearest neighbors. This is called approximate nearest neighbors, because you're not searching the entire vector space but just a subset of it.

So it's not the absolute k nearest neighbors but it's approximately the k nearest neighbors. You sacrifice some precision in order to gain efficiency in your search, so let's see how to make a set of random planes in code. Assuming that your word vectors have two dimensions and you want to generate three random planes. You'll use np.random.normal to generate a matrix of three rows and two columns. As you see here, you'll create a vector v and for each random plane, see which side of the plane the vector is on.

So you'll find out whether the vector v is on the positive or negative side of each of these three planes. Notice that instead of using a for loop to work on one plane at a time, you can use np dot, to do this in one step. Let's call the function. The result is that vector v is on the positive side of each of the three random planes. You've already seen how to combine these intermediate hash values, into a single hash value. But please do check out the lecture notebook, to see all the code and to practice this last step.

As you see, locality sensitive hashing, allows you to compute k nearest neighbors, much faster than naive search. This powerful tool can be used for many tasks related to vectors and I will show you how it can be applied to search in the next video.

9. 01_15_searching-documents.en
============================

![293.png](./images/293.png)
![294.png](./images/294.png)
![295.png](./images/295.png)
![296.png](./images/296.png)

I will finish this week by showing you how you can use fast k-nearest neighbor to search for pieces of text related to a query in a large collection of documents. You simply create vectors for both and find the nearest neighbors. >> To get ready to perform document search, first, think about how to represent documents as vectors instead of just words as vectors. Let's say you have these documents composed of three words. I love learning. How can you represent this entire document as a vector?

Well, you can find the word vectors for each individual word. I love learning then just add them together. So the sum of all these word vectors becomes a document vector with the same dimension as the word vectors. In this case, three dimensions. You can then apply document search by using k-nearest neighbors. Let's code this up, create a mini dictionary for word embeddings. Here is the list of words contained in the document. You're going to initialize the document embedding as an array of zeros.

Now for each word in a document, you'll get the word vector if the word exists in the dictionary else zero, you add this all up and return the documents embedding. Please try it out. >> You learned in this video an example of a very general method that text can be embedded into vector spaces so that nearest neighbors refer to text with similar meaning. Well, you'll learn more advanced ways to embed text. This basic structure will reappear again and again and again as it's used throughout modern NLP.

10. 01_17_week-conclusion.en
========================

Great work in getting through this week's materials, you now know how locality sensitive hashing works and how you use it when approximating the nearest neighbors. In practice, the more regions you have, the higher accuracy will be, but the slower your search gets, there is always a trade off. In this week's programming assignment you'll be learning the transformation matrix R. That allows you to find the mapping between words in different languages.

You will then implement locality sensitive hashing and see how you can use it to hash different inputs into regions that tend to have similar content. In this course, you have learned a lot so far, you learned about logistic regression and naive Bayes for sentiment analysis, vector space models, PCA and locality sensitive hashing. Good luck with the programming assignment and we'll see you in the next course. >> Good luck.

### 07_heroes-of-nlp-kathleen-mckeown

1. 07_01_andrew-ng-with-kathleen-mckeown.en
========================================

I am delighted to have with me here today, Kathy McKeown, who is the Henry and Gertrude Rothschild Professor of Computer Science at Columbia University. Where she is also the founding director of the Institute for Data Sciences and Engineering. She is also an Amazon Scholar and is well known for the work that she's done over many years on text summarization and many other topics in NLP. Welcome, Kathy, and thanks for joining me. >> Thanks Andrew, and thanks for having me.

>> So today you lead a large group doing NLP research, but your journey to becoming an AI researcher and an NLP researcher has been an unusual one. If I remember correctly, you actually majored in comparative literature when you were in undergrad, even though you're also very mathematically oriented at the time. So tell us your story of how you became an NLP researcher. >> Yeah, so when I started out at Brown I didn't know what I wanted to major in. So I took courses both in math and comparative literature.

And as I went on, I became more interested in comparative literature. Probably in part because of the teachers who I had who really influenced me. It was only as I came near the end of my time at Brown that and when I graduated, I took a job as a programmer, which I found actually very boring. And I thought if I was going to have to be working 40 hours a week, I wanted to be doing something that I enjoyed. And it was then that a friend of mine who was a linguistics major at Brown told me about computational linguistics.

And so I spent a lot of the year in the library reading about AI and natural language processing. And when I applied for Graduate School the following year I I knew that was what I wanted to do. Because it gave me a way to bring together my interest in language and in math. >> So that's fascinating, so as a comparative literature major, you spent a lot of time in the Brown University Library reading about computational linguistics and NLP. Today, with a lot of learners, maybe some watching this video that may not yet be a NLP researcher or AI engineer wanting to break into the field.

So I'd love to hear more about what your experience was like reading so much. Were you doing it by yourself? Did you have a study group or what was that like? >> I was doing it entirely by myself. I really had no guidance in terms of what to look at. I guess this friend that I had made a few suggestions. And then I traced references when I first began reading. I would follow up on references to go further. Yeah, and when I first entered Graduate School, and I had essentially switched fields, I found it very frightening.

I was sure that I was an impostor, that I didn't know enough. And before long they would find out that I really shouldn't be there after all. Yeah, but that's something you overcome with time and you learn that it's not the case and people value your input. >> That's really inspiring. Thank you for sharing that. Would you have any advice for someone maybe today that is trying to do this themselves and wondering if they know enough, or are good enough, or should be in the field?

It sounds like you got through that and you've been incredibly successful. But what would you say to someone today maybe looking to follow in your footsteps and wondering if this is right for them or if they'll make it? >> So I I guess I have a couple pieces of advice. I do think reaching out to people and talking to people is useful. Until I got to Graduate School I wasn't in an environment where I had people to talk to. So I do think it's really helpful, especially to talk to your peers about what they're doing and what they're interested in.

When you pick problems to work on. And I guess, especially in today's world of deep learning and neural nets, I would advise choosing problems that are different from what everybody else works on. Sort of strike out in a different direction, choose something new, a new task, and take off from there. >> And I think I would love to come back to the different problems topic in a minute. And when I speak with learners from around the world, I do hear from some that they feel lonely or isolated.

They're kind of out somewhere or maybe not living in the major tech hub, and they sometimes feel like they're doing this by themselves. So I find it actually really inspiring that you were able to do that by yourself in a library in Brown University. I don't know if you have any other thoughts to offer learners that may feel like they're somewhere in a company or in a city just trying to do this by themselves. >> I'm not sure I do have a lot more to say about it.

I guess read what you enjoy about, if you can be part of a reading group, an online reading group, that would be helpful. There are a lot of reading groups now, and that's a good way to get sort of insights. There are online videos and course experiences, like yours. And I think that's a way to find out what's going on and get in touch with what people are doing. So I think today, the online environment can help people get connected and hear what's going on.

I was lucky, I mean, I was really lucky, [LAUGH] I applied to Penn. I didn't know that at the time it was the best place in natural language processing, and that was totally luck. So I don't know that I would recommend doing it blind again today, I think getting advice is great. >> Everyone that's been successful has had many elements of luck. But the preparation makes you ready to take advantage of when good luck falls into your lap. >> Yeah. >> Thank you for sharing that, that was really inspiring to hear about your early days as a developing researcher.

And today you lead a large group at Columbia University doing very interdisciplinary work and doing a lot of work on summarization and other topics. So tell us a bit more about your current work and what are you excited about. >> So I mean, summarization has really been the bulk of my work over the most recent years. We've done work on summarization of all kinds of different genres, from personal narratives to emails. One thread of research in summarization that I'm particularly excited about is work that I've done with researchers at Amazon and which was published at ACL.

And this is work on summarization of novel chapters. And it's very new, no one has been working on this task, it's very challenging, very different from news summarization. So the chapters are much longer than the news articles on which most current work in summarization today is done. And that is a challenge for current neural models. And a big problem is that there is an extreme amount of paraphrasing between the input, which is 19th century novels, and the output, which is a summary written in today's language.

None of the current models can handle the kind of paraphrasing that we see there. And that, in general, is a topic that I'm really interested in is a sort of very abstractive summarization. Where the sentences use different words than the input document, where the syntactic structure is different. And that is very different from the vast Majority of work today which is done on summarization of news. And it's done on summarization of news because that's where the data is.

So some of the other areas that I'm looking at are summarization of personal narratives that you find online where the personal narratives are very informal language and the summary is more formal. Summarization of debates. In past work, we've also done summarization of email. Which has some of those same characteristics. >> Why did you choose to work on the novel summarization task? >> Well, so we had done work on novels even earlier. I would say in 2010, when one of my students who was very interested in creative writing, and I really thought he should do a PhD.

And so to convince him to stay, we came to a topic that he would be happy with, which was analysis and generation of creative language. And I felt then that my work came full circle, that we collaborated then with a professor in comparative literature. So I came back to my roots in comparative literature and that was a lot of fun. So, when I first went to Amazon, I knew because of Kindle and online on Amazon, they have a lot of novels. And I thought, what would be more fun than being able to summarize novels?

>> Sounds like a fun project, I read a lot on my Kindle, so maybe your work will be a feature on Kindle some day. One aspect of your work that stood out as well is that you're known for doing highly interdisciplinary work. So rather than focusing narrowly on NLP research, your work spans AI, and the media where I know the Columbia University is a great journalism school. So wonderful journalists you work with there or the application of NLP to social networks.

I think you work with medical problems. So tell us a bit about how you think about interdisciplinary work because you've done more of it I think than most NLP researchers have. >> Yeah, I really enjoy interdisciplinary work. I think it's my most favorite kind of research to do. And in part we get a really different perspective on research in the world when we talk to people in other fields. It takes us out of our sort of technical, narrow field. >> And so earlier, you alluded to picking research topics that are novel and I think your research portfolio has certainly touched on a lot of problems that very few others are working on.

So can you say more about that? So how do you pick research projects you work on and how do you advise others to pick topics to work on? >> I think it's important to pick a task that matters. So that for me is one thing to look at. For example, most of the work in text summarization today is done on summarization of what's called single document summarization of news. So take one news article in and generate a summary of that news article. And the reason for that is because that's where the data is.

There's a huge amount of data that has been pulled together from first the CNN Daily Mail Corpus, and later New York Times, and there are a number of other corpora as well. The problem is that's not really a task that we need. We've known for a long time that the lead of the news article can help people pretty well in serving as a summary of the document. And in fact, for years it was hard to beat. The lead people just worked on, that wasn't a problem that people worked on in the early years of summarization.

>> The lead being the first sentence or the first- >> The first couple of sentences in the news article. So, Yeah, I mean, people work on a problem like that because that's where the data is. We have leaderboards. People are competitive. They like to be The leaderboard, but I would question does that one or even half a point in ROUGE, which is the automated metric used to score them, really make a difference? If you look at the output you can see that actually the summaries are quite similar and either one of them might be fine.

So I prefer to go in directions that people haven't gone in before and to choose a task where if you solve it, it's going to help people. It's going to be a useful application that you've developed. So this is why I have done things like summarization of personal narrative, which we did in the course of a disaster. So that we could summarize, think of having a browsing view of summaries of what people have experienced after they've lived through a disaster.

Or the current work on summarization of novels where it'd be helpful to have a summary of an input chapter. I'd like to go in a different direction, in part because I want to solve the task that matters. But I also like to go in a different direction because in this day in age of deep learning where results come so fast, everybody works on the same problem trying to beat the previous state of the art. It can be hard to be the first one to get there, and if you go in a different direction, nobody else is working on, you are going to be the first one to come to solution.

And that's what I like to do in my research. Overtime I like to be first on a problem. I see, cool yeah. And I feel like, for myself, I have a lot of respect for people that could push that extra half points of performance on the leaderboard because hopefully that advances the whole field. And this all shifts. I also have a lot of respect for people with your creativity and the insight to chart a new problem that no one else has thought of, and advances the whole field in a different direction.

I think the field of AI NLP is broad enough. I think it's actually not a bad thing if we have lots of people working on lots of different things, including standardized benchmarks. And a bunch of new things. >> Yeah, sure, I feel that there are not as many people who want to go in that new direction and it does take some sort of guts to do it. Because the first thing that happens when you submit a paper is there is no benchmark. There is no baseline of prior work and reviewers have a very hard time dealing with that.

How can they judge whether it's really a good step forward. Whereas if you can show on a leaderboard that you've improved by a certain amount and you stay within the traditional trajectory, it's easier to judge. >> Yeah, I'm with you on that. Actually, I was recently chatting with one of my friends Sharon Zhou who mentioned that sometimes the way benchmarks and metrics are established is that some researcher publishing a paper publishes something using some metric.

Maybe a good one, maybe an okay one. But to make sure that subsequent papers can compare to earlier work, then everyone, and more and more people end up using the same metric. More for historical reasons and it makes things comparable rather than because it is actually the most useful metric. It's funny how metrics get established in academia. >> Yeah, I mean that has happened in the summarization field. And I think also in machine translation where you want an automated metric because it's easier to develop a system to train over and over again.

And yet everybody knows that the automated metrics that we currently have are really flawed. And but everyone keeps using them, because that's what we've always done. One of my most stark memories was I remember going to a the Information Retrieval Conference and attending a workshop in text summarization. And I remember being fascinated, but struck that about half of that workshop was on text summarization algorithms and the other half of that workshop was on how to develop metrics to evaluate.

Text summarization especially, the development of automated metrics has been challenging. >> Yeah. >> Hey, so in terms of choosing. topics to work on. One of the pieces of work that you've been doing that I thought was fascinating, was you were taking texts from the black community from Harlem, near I guess where you teach at Columbia University and analyzing that as well. Tell us about that. >> This is where I'm moving with my work with a researcher from social work.

And we're also beginning to involve a linguist who works on African American vernacular. And what we're doing is we're looking at what people say, what kind of emotions they express in reaction to major events that are going on today. So, for example, in reaction to Black Lives Matter and in reaction to COVID-19. So this is work that we're just beginning. We've begun with developing an interface where people can post about their experiences with these events and how they're feeling.

And I guess what we're hoping to do with that in part, so we have two directions to go. One on the natural language side is to be able to understand how people express different kinds of language. Sorry, different kinds of emotion in African American vernacular. And how that differs from how people express it in standard American English. And look at the difference in language and probably even the difference in content in terms of what's expressed.

And this can help us in developing algorithms that are not biased as we move forward. Most of the work in natural language, all of the systems have been trained on language that comes from news like the Wall Street Journal. >> Yeah, that's great. If this type of work can help fight bias or build bridges between communities or just play some role in understanding and helping to advance the Black Lives Matter movement, that seems to be a wonderful thing to me.

>> Yeah, I mean, we also want in that work to look at the impact of trauma. So it's a different kind of trauma and sometimes it's not your personal trauma, but the trauma of seeing what has happened to other people who are like you. So yeah, we want to look at how that is expressed in the different kinds of emotions, the intensity of emotion, and so forth. >> I find it really wonderful that NLP researchers, AI researchers can play an active role in some of these most important societal questions and issues of our time.

It feels like the work we do as AI researchers, it could matter in these really important times. >> Yeah, I mean I think so. And I've sort of been trying to do that for a while. I think it really attract students to work with you, and often different kinds of students into the field to work with you. On our first work on with analyzing social media posts of gang involved youth, we didn't have funding. We did that entirely with undergraduates who were just totally amazing.

In earlier work we were looking at being able to automatically generate updates about disaster as it unfolded. We did that after Hurricane Sandy hit New York. And again it was something that students came to me and they had seen this happen and they have seen their neighborhoods hurt. Or they lived through the uncertainty of it and they wanted to help. They wanted to know what can we do and that was at that point in time, this was all pre-neural net we began developing systems that could automatically generate updates as an event unfolded.

>> I think that you don't need a PhD, don't need a long publication record, but in undergrad spotting an opportunity with a desire to help. Can step in and start to work on systems that they can make a difference. >> Yes, they're really passionate about it and There are really good, the work that came out of that was really excellent. >> Yeah, thank you, so Kathy, this is great stuff. And switching tracks a bit, you've been working in NLP and associated areas for a long time.

In fact, I saw that even way back in 1985 you written an early book on text generation before the modern neural text generation techniques were around. So you've been a leader in the field for a long time and seen a lot of things change. I'd love to hear your thoughts on how the field of NLP has evolved over these many years. >> Sure, so when I started, which I got my PhD in 82. so I spent those earlier years at Penn. And there were some characteristics of the field that were salient.

So one of them is that there was a lot of interdisciplinary work. There was in developing NLP systems, we drew a lot on work from linguistics, from philosophy, from psychology, from cognitive science. And so when I was at Penn I interacted a lot with faculty from linguistics. Ellen Prince was one of the people or faculty from philosophy. We spent time in these interdisciplinary meetings. And I can remember walking across campus with my advisor to go from the computer science department to the psychology department, for example.

I was influenced a lot and I have to mention this, although it's not exactly what you asked, I was influenced a lot by senior women at the time. If I look back to who was most influential in how I progressed in my early research. My advisor, of course, who was a male, Aravind Joshi. But then also Bonnie Webber, who was there in computer science, Eva Hajičová from Charles University at Prague who was a linguist. Barbara Grosz, who was at Stanford at that time in the CSLI Institute.

And Karen Spärck Jones was very influential to me. She was from the field of information retrieval. And she and I spent a lot of time talking about summarization. So interdisciplinary is one main feature of that time. A second was drawing on theories from these other areas, so we drew on theories from linguistics. One main kind of theory that we looked at was the focus of attention and how that changed over the course of a discourse. And how that influenced how you made choices and how you realized text in language.

So for example, did you use a pronoun or did you use a full noun phrase? What kind of syntactic structure did you use? You might use different syntactic structures to make a concept more prominent in the discourse. We also drew on work from philosophy. So we drew on work from theories from Searle about intention, and work from Grice about conversational implicature. And so we looked at these theories and we looked at how we could embody them in our natural language approaches.

>> It's great to hear about some of your early sources of inspiration. Much as I think today you will be a source of inspiration to many others. So you've seen a lot and see a lot in NLP, which continues to be a rapidly evolving field. So I'm actually curious, Kathy, what do you find most exciting in terms of emerging or exciting NLP technologies? >> For me, personally, some of the work that I've already talked about today on truly abstractive summarization that uses extreme paraphrasing.

Work on analyzing the language from diverse community. So we've been looking at the black community, but I think there are other communities we could look at as well. I'm interested in looking at how you deal with bias and data. And another very important topic is being able to arrive at what I would call para linguistic meaning. So this pragmatics information about emotion, about intention, would be another important direction to go. And I also think more work on events, being able to understand what events have happened, and to be able to follow them.

I also think about often if I look back. Is it okay, if I talk about this now. I look back? >> Okay. If I look back on my favorite technologies and papers, I can think of papers from three points in time. The first would be older, and this was very early work in language generation, on how we pick the words in our sentence. And we thought then that it was a hard problem that constraints came from many different sources. And we wrote a paper called Floating Constraints on Lexical Choice.

Where we looked at how information from different parts of language, from the discourse, from the lexicon, from syntax, from semantics, will influence what we chose. And we worked in two different domains. One was basketball and one with stock markets. And I give it the example of the floating constraint, where we want to express both the time at which something happened and the manner. In the first example we expressed time in the verb, and the manner in the adverb.

So Wall Street indexes open strongly, open is the time. And in the second we express manner in the verb and time in the prepositional phrase. So stock index surged at the start of the trading day. And so we wanted to look at how we could control that choice. And I think control is something that's missing in language generation and summarization. Today using deep learning methods, how do we control what the output is and make sure it's true to what our intention is?

In more recent work, my favorite is work on Newsblaster. That's still about 15 years ago, but it feels recent to me. And that was where we took a real world problem. We did do some collaboration with journalists, and we've developed a testbed, where we could identify the events that happened during the day, and produce summary on each event. And then we also looked at how we could track that overtime. And this platform gave us a common sort of application, in which my students could address really hard research questions.

And so that was where we looked at, did some of our first work on abstractive summarization. Looking at how we might compress sentences, how we could fuse phrases together, how we might reference, edit references, so that the summary was more coherent. And we also did work on multi lingual summarization. Yeah. >> Cool, Thank you. Lots of exciting, very distinct projects over the years. Do you have any wrap up? Did you have any last thoughts? You can just say, do you have any final thoughts?

>> Well, I guess I would just say that natural language is a really exciting field today. There's been a huge amount of progress with deep learning. We've seen dramatic increases in accuracy, but we still have a lot of directions to go. And I guess I would like to see more of the interdisciplinary work being brought back in. I'd like to see people looking at the data more and at their output more, rather than just numbers. But I think there are many exciting directions for people to work in, and I hope we'll see many people joining the field.

>> Thank you, that was great. Yeah, I also hope that we'll have a lot more people join NLP and contribute to all of this exciting work. So thanks Kathy, it was cool >> Thanks so much for asking me, it was fun. >> For more interviews with NLP thought leaders, check out the DeepLearning.AI YouTube channel, or enroll in the NLP specialization on Coursera.


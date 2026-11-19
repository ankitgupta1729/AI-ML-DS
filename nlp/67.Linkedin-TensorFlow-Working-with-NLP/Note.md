## 1. Introduction

1. 001. Why TensorFlow.en
======================

![1.png](./images/1.png)
![2.png](./images/2.png)
![3.png](./images/3.png)
![4.png](./images/4.png)
![5.png](./images/5.png)
![6.png](./images/6.png)
![7.png](./images/7.png)
![8.png](./images/8.png)
![9.png](./images/9.png)
![10.png](./images/10.png)
![11.png](./images/11.png)
![12.png](./images/12.png)

- [Jonathan] TensorFlow is one of the most popular deep learning frameworks out there, and what makes it particularly appealing is its ecosystem. You can develop and train models using Python amongst several other languages, and then easily deploy them in the cloud or on-prem in the browser or on mobile devices no matter what language you use. Transformers have taken the natural language processing world by storm. Hi, I'm Jonathan Fernandes and I work with machine learning and AI models every day.

Join me as we learn about transformers in natural language processing. In the process, we look at components of a transformer with a special focus on BERT, one of the encoder models developed by Google. We'll also cover topics like self-attention and see examples of bias in BERT and GPT-2.

2. 002. What you should know.en
============================

![13.png](./images/13.png)
![14.png](./images/14.png)

- [Narrator] This course follows on from two other TensorFlow courses, TensorFlow: Neural Networks and Working with Tabular Data and TensorFlow: Working with Images, which are both available in the LinkedIn Library. So if you haven't worked your way through these courses, you probably want to do that first. If you know the basics of Python and you have some understanding of machine learning and have worked with TensorFlow before, you should be just fine.

I'll also be using Google Colab. Now, if you haven't used this before, you'll need a Gmail account which you can sign up for in a couple of minutes. Alternatively, you can just follow along.

3. 003. What is TensorFlow.en
==========================

![15.png](./images/15.png)
![16.png](./images/16.png)
![17.png](./images/17.png)
![18.png](./images/18.png)
![19.png](./images/19.png)
![20.png](./images/20.png)
![21.png](./images/21.png)
![22.png](./images/22.png)

- [Instructor] TensorFlow is a powerful library that we can use for machine learning. Now, it was developed by the Google Brain team and it powers many of Google's services, such as Google Search, and it was open sourced in November 2015, now, you can use it for all sorts of machine learning tasks, such as image classification, all the way to natural language processing. At its core, it's very similar to NumPy, but with GPU support so it supports distributed computing, that means it works across multiple devices and servers.

And it also includes a just-in-time compiler that allows it to optimize computations. It does this by extracting the computation graph from a Python function, and then running independent operations in parallel. These computation graphs can be exported to a portable format, this means that we can train a TensorFlow model in one environment, like I'm doing now using Python on my Windows machine and then run it on my Android phone using Java. Most of the time we'll use high-level APIs, such as Keras, but when you need more flexibility, you'll use the lower level Python API handling tensors directly.

TensorFlow runs not only on Windows, Linux and the Mac OS but also on mobile devices using TensorFlow Lite, including both the iOS and Android. Now, if you don't want to use the Python API, then there's C++, Java, Go and Swift APIs. Now, one of the biggest attractions to TensorFlow is the ecosystem that's available. We've already seen that you can build and deploy models with Python, but there's even a JavaScript implementation called TensorFlow.js, which means you can run your models directly in your browser.

You then also have TensorFlow Lite, which is using an iOS or Android, but there's more, there's TensorFlow Extended, which is a set of libraries built by Google to productionize TensorFlow projects. So, this includes tools for data validation, pre-processing, model analysis, and you can serve these models with a rest API using TensorFlow Serving. Now, TensorFlow Serving's really important because it's easy to create ML solutions that have one or two users, but what happens when you have to scale that out to hundreds of thousands of users?

Then, there's TensorBoard, which is great for visualization because it helps you when training your models. And, finally, TensorFlow Hub provides a way to easily download and reuse pre-trained models. So, these are models that have been known to perform well on certain tasks. This means you aren't starting from scratch, but using the work of other experts.

## 2. NLP and Transformers

4. 004. What is NLP.en
===================

![23.png](./images/23.png)
![24.png](./images/24.png)
![25.png](./images/25.png)
![26.png](./images/26.png)

- Natural Language Processing or NLP is an area of research and computer science focusing on processing natural languages, such as English and German and so on. Now, what do we mean by processing? Well, we're taking these languages and converting them into numbers that a computer understands. Computers then perform several tasks, such as text classification or text generation, or answering questions to demonstrate this understanding. I like this comment from Andras Kornai's book, "Mathematical Linguistics".

"NLP is hard from the standpoint of the child who must spend many years acquiring a language. It's hard for the adult language learner. It's hard for the scientist who attempts to model the relevant phenomena and it's hard for the engineer who attempts to build systems that deal with natural language input or output. These tasks are so hard that Turing could rightly make fluent conversation in natural language, the centerpiece of his test for intelligence." And finally, let's see what computer science researcher Yoav Goldberg has to say.

"Human language is highly ambiguous. It's also ever-changing and evolving. People are great at producing language and understanding language and are capable of expressing, perceiving and interpreting very elaborate and nuanced meanings. At the same time, while we humans are great users of language, we're also very poor at formally understanding and describing the rules that govern language." So we can safely conclude that NLP is a challenging and important area of research.

Now let's look at some of the tasks involved in natural language processing. In sentence classification, we're interested in classifying whole sentences. An example might be sentiment analysis, where we provide a review and want to determine if the review is positive or negative. We might provide two sentences and want to know if they're logically related. In named entity recognition, we might want to classify each word in a sentence as either a person, location or organization.

Financial institutions are often interested in this application for new customers. If a company wants to set up a new account, there are several checks that must be made. If a company trades in only low risk countries and its main business activity is considered low risk. Their onboarding process can be fast-tracked by determining what parts are names, locations, and organizations, financial institutions can then go ahead and perform further searches and downstream tasks on them.

Other interesting NLP tasks are auto generating text, which as the name suggests, is generating text, for example, in English, that is grammatically correct. You can also translate texts between two languages or summarize text. And finally, given a question and some texts, we can answer the question based on the information provided in the text.

5. 005. Transformers for NLP.en
============================

![27.png](./images/27.png)
![28.png](./images/28.png)
![29.png](./images/29.png)
![30.png](./images/30.png)
![31.png](./images/31.png)
![32.png](./images/32.png)

- [Instructor] Let's take a look at where transformers are used in production. The Google search engine now uses transformers, in particular, BERT. In the past, if you did a search on Google for, can you get medicine for someone pharmacy, it wouldn't have picked up on the fact that for someone was a really important part of the query because you're looking for another person to pick up the medicine. Google would've returned results about generally getting a prescription filled, which isn't relevant.

Now with BERT, it captures the nuance of the importance that another person picks up the medicine and returns results about having a friend or family member pick up a prescription. Let me give you another example of Google search using BERT. When I enter the search, what are the rules for The Hundred? The answer back from Google doesn't just give me the most relevant page, but the answer to my question in bold. This is an application of question answering that we saw earlier, using BERT.

In June, 2018, GPT or generative pre-training model, which was developed by OpenAI, was the first pre-trained transformer model and was used for fine tuning on various NLP tasks and obtained state of the art results. Later that year in October, 2018, researchers at Google came up with BERT or bi-directional encoder representations from transformers. In February, 2019, OpenAI released a bigger and better version of GPT called the GPT-2. This was in the news a lot because the OpenAI team didn't want to release the details of the model because of ethical concerns.

Later that year in October, 2019, Facebook's AI research team released BART, or bi-directional and auto regressive transformer and Google released T5. Both of these models are larger pre-trained models using the same architecture as the original transformer. In the same month, the team at Hugging Face bucked the trend. Everyone was moving to bigger models. The Hugging Face team released DistilBERT, which is a smaller, faster and lighter version of BERT and has 95% of BERT performance on the GLUE language understanding benchmark.

And you can see that over the years, the trend is to have bigger model sizes.

6. 006. Transformers, their use, and history.en
============================================

![33.png](./images/33.png)
![34.png](./images/34.png)
![35.png](./images/35.png)
![36.png](./images/36.png)
![37.png](./images/37.png)
![38.png](./images/38.png)
![39.png](./images/39.png)
![40.png](./images/40.png)
![41.png](./images/41.png)
![42.png](./images/42.png)
![43.png](./images/43.png)
![44.png](./images/44.png)
![45.png](./images/45.png)
![46.png](./images/46.png)
![47.png](./images/47.png)

- [Narrator] Transformers form the underlying architecture for many of the popular NLP models you might've heard about such as BERT and GPT. They were proposed by a team of researchers from Google in 2017 in the paper, "Attention Is All You Need." Now, before getting into the details of the transformer architecture, let's take a look at how well they perform on some of the NLP tasks we mentioned earlier. So I'm going to head over to the notebook. Now you can go ahead and select run time and run all the cells.

I'm not going to do that as it takes about two minutes to download some of the models. So for this notebook, I've gone with a theme of Singapore Airlines as this is my favorite airline. So when classifying whole sentences, I have used an actual review. The model needs to determine if the sentiment of the review is positive or negative. So the text is, "The flights were on time both in Sydney, "and the connecting flight in Singapore, "the organization to cope with the COVID-19 restrictions "while in transit was well-planned "and directions easy to follow, "the plane was comfortable with a reasonable "selection of in-flight entertainment, "crew was pleasant and helpful." And this sentence is correctly classified with a positive sentiment.

Now let's take a look at classifying each word in a sentence. The sentence is Singapore Airlines was the first airline to fly the A380, Chew Choon Seng was Singapore Airlines' CEO at the time, Singapore Airlines flies to New York daily. Now when classifying each word in a sentence, you can see that the model has been able to pick up that Chew Choon Seng, is one entity, and so is Singapore Airlines and New York. It's not surprising that the A380 has been classified as miscellaneous, as it's not either a person, place, or organization, but an Airbus aircraft model.

Now let's head over to answering a question. So given the text Singapore Airlines was founded in 1947 and was originally known as Malayan Airways, it is the national airline of Singapore and is based at Singapore Changi Airport, from this hub, the airline flies to more than 60 destinations with flights to Seoul, Tokyo, and Melbourne and so on. The question is, how many aircrafts does Singapore Airlines have? Now you'll see that the answer is in this line here, there are more than 100 planes in the Singapore Airlines fleet.

Now notice that the question that I've asked is not how many planes, but how many aircraft's. And so what we're going to be testing is whether the model is able to understand nuances in the English language. And you can see that the model correctly answers, more than 100. With text summarization, we're able to summarize this lengthy text into three sentences. So if I provide the sentence, it is the national blank of Singapore, the model responds with the answers, anthem, capital, pride and so on.

And if I change the context to, Singapore Airlines is the national blank of Singapore, the model changes this correctly to predicting airline as the top response. The other sentences that are provided are less likely in order of decreasing probability. And you can see finally that the model has no problems with translating from English to German.

7. 007. Challenge NLP model size.en
================================

![48.png](./images/48.png)
![49.png](./images/49.png)

(cheerful music) - [Instructor] The purpose of this challenge is to give you an idea of the scale involved in the NLP models and the infrastructure required. So the first question is, how many parameters does the BERT base uncased model have? You can use the get_model_size function below to help you. And secondly, if you know the number of parameters for a model, how might you be able to determine how much memory is required when running a model inference?

So this would be the amount of space that's required on RAM. And then thirdly, if you wanted to run a GPT-3 175 billion inference, how much RAM would your infrastructure require? This challenge should take you between five and 10 minutes.

8. 008. Solution NLP model size.en
===============================

![50.png](./images/50.png)
![51.png](./images/51.png)
![52.png](./images/52.png)
![53.png](./images/53.png)
![54.png](./images/54.png)

(upbeat music) - [Instructor] Now you can go ahead and select Runtime and run all the cells. I've just done this. So I'm not going to do that again. So the question is how many parameters does the BERT base uncased model have? And we can use the get model size function below to help us. So if I head over to the get model size function, you can see that if I provide bert-base-uncased as my parameter, that the BERT base uncased model has over 109 million parameters.

Now, if you know what the number of parameters for a model, how might you be able to determine how much memory is required when running a model inference? Now, because each of these parameters are represented as single precision floating point numbers, this means they require four bytes. So four times the number of parameters will give us an approximate value for the size of the model. So if I was to take the BERT base uncased model, I have 109 million parameters times four.

This means I would require 436 megabytes of RAM, which is about half a gig of RAM. Now, if we apply that same logic, if we wanted to run a GPT-3 175 billion inference, how much RAM would our infrastructure require? And you can see that we would need 175 million times four, and you can see that we would require a whopping 700 gigabytes of RAM if you wanted to run an inference of the GPT-3 175 billion parameter model.

## 3. BERT and Transfer Learning

9. 009. Bias in BERT and GPT.en
============================

![55.png](./images/55.png)
![56.png](./images/56.png)
![57.png](./images/57.png)
![58.png](./images/58.png)
![59.png](./images/59.png)
![60.png](./images/60.png)
![61.png](./images/61.png)
![62.png](./images/62.png)
![63.png](./images/63.png)
![64.png](./images/64.png)
![65.png](./images/65.png)
![66.png](./images/66.png)
![67.png](./images/67.png)
![68.png](./images/68.png)
![69.png](./images/69.png)

- [Instructor] Now, before you think BERT and GPT-2 should be put into production immediately, let's look at some problems with the models. As always, you can go ahead and select Runtime and run all the cells. I've run this notebook before, so I'm not going to run and download the models again. Now, let's start off with the BERT model and see how it performs with a fill-in-the-blank type task. The examples that are shown are the top five options. So for example, we have this man works as a blank, and the options provided seem reasonable.

This man works as a carpenter, a lawyer, a farmer, a businessman, and a doctor. If we go ahead and say this white man works as a blank, we get some strange results. This white man works as a carpenter. This white man works as a slave. And then if we say this black man works as a, again, we get some reasonable options. So this black man works as a carpenter. This black man works as a lawyer, barber, doctor, and teacher. Now, if we provide a typical white male name, like Thomas, we get reasonable results.

And if we provide a typical black male name, such as Jamal, again, we get some reasonable entries. Now, if we do the same for Amy, a typical white woman's name, and Aaliya, a typical black woman's name, again, we seem to get some reasonable results with Amy works as a waitress, Amy works as a nurse, Amy works as a teacher, model, and lawyer. And we have similar sort of results for Aaliya. Now, what is very strange is that if we input this woman works as a, the results we get back are nurse, so this woman works as a nurse, this woman works as a maid, a teacher, waitress, and prostitute.

I've also found occasional examples of bias against gay people with the BERT model. Now, if you do some more study, you might also find bias, like the jobs for men might be for a doctor, but the job for a woman might be a nurse and not a doctor. I haven't done an in-depth study on the bias in models, but this is an active area of NLP research. Now, with GPT-2, in this case, each time you run the model, you'll get a different auto-generated text. So I start off with the text the black man was known for, and then the text is auto-generated, saying for being a tough guy.

He would grab a fight or beat a guy up, and so on. And then similarly, the woman was known for, and you can see the woman was known for saying that a woman who doesn't understand how men become the first to go to the altar, and so on. Now, if I do the same thing with the man was known for, I say this man was known for his well-heeled work ethic and long and steady nights. He would stay home on Sundays, and so on. Now, I didn't find any significant bias against men, women, white, or black.

However, again, I found examples of bias against gay people in GPT-2. And additionally, I found many examples of racism and bias against people from the Middle East. So auto-generated text had references to antisemitism, Islam, and terrorism. To sum up, bias is an active area of research, and there's a lot of work to be done. I've seen examples of bias against women, gay people, and different races. You don't want to be putting GPT-2 and BERT into production with text generation and masked modeling without some strict boundaries and having a human in the loop to check the output that is created.

So where does this bias come from? And that's what we'll look at next.

10. 010. How was BERT trained.en
============================

![70.png](./images/70.png)
![71.png](./images/71.png)
![72.png](./images/72.png)
![73.png](./images/73.png)
![74.png](./images/74.png)
![75.png](./images/75.png)
![76.png](./images/76.png)

- [Instructor] So what was BERT and GPT-2 trained on? Any bias and prejudice in these data sources will make their way to the models. BERT was trained on the English Wikipedia, which has around two and a half billion words, and something known as the BookCorpus, which is around 800 million words. The BooksCorpus are 11,000 books written by yet unpublished authors. GPT-2 was trained on WebText Corpus. The researchers at OpenAI created the WebText Corpus by scraping all outbound links from Reddit, which is a social media platform, which received at least three Karma points.

They did this because this was an indicator for whether the other users found the link interesting, educational or just funny. So the WebText Corpus contains the text subset of these 45 million links and doesn't include links created after December, 2017. Now, if you read the BERT paper, the two key contributions of BERT are these two tasks, Masked Language Modeling and Next Sentence Prediction. Let's take a couple of sentences from the BERT paper as an example.

So BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on 11 natural language processing tasks, and so on. The MLM, or Masked Language Modeling task, requires BERT to predict the masked out word. So BERT is conceptually something and empirically powerful. The next sentence prediction task asks the question, does the second sentence follow immediately after the first? So does the sentence, it obtains new state of the art results, logically follow from, BERT is conceptually simple and empirically powerful?

Now, when would you ever need either of these tasks and why are either of these tasks helpful? These tasks forced BERT to get a good understanding of language. And secondly, and importantly, we don't need any label data, we can train with raw text. Just so you know, training on this dataset would have been hundreds of thousands of dollars in compute time on Tensor processing units or TPUs.

11. 011. Transfer learning.en
=========================

![77.png](./images/77.png)
![78.png](./images/78.png)
![79.png](./images/79.png)
![80.png](./images/80.png)
![81.png](./images/81.png)
![82.png](./images/82.png)
![83.png](./images/83.png)
![84.png](./images/84.png)

- [Instructor] Transfer learning is made up of two components, pre-training and fine-tuning. So what does pre-training involve? Well, we're training a model from scratch. This means the model's weights are randomly initialized. The model is of no use at this point. The model is then trained on large amounts of data and then becomes useful. Now, let's compare the pre-training for some of the larger models. So BERT was released in 2018. The number of parameters was 109 million.

It took Google 12 days to train BERT, and I've put an asterisk by the 8 times V100s because BERT wasn't trained on GPUs, but rather, Google's equivalent, TPUs or tensor processing units. So the size of the dataset used for training was 16 gigabytes, and the training tokens were 250 billion. And the data sources that was used to train BERT were Wikipedia and the BookCorpus. RoBERTa was developed by Facebook in 2019. The number of parameters was 125 million.

And quite amazingly, Facebook managed to train this in a single day, and that's because they used a whopping 1024 V100 GPUs. The size of the dataset was significantly larger than BERT's, so it was 160 gigabytes with 2,000 billion tokens. The data sources were Wikipedia and BookCorpus as used with BERT, but also the Common Crawl news dataset, OpenWebText, and the Common Crawl stories. And finally, GPT-3 was released in 2020 by OpenAI. The number of parameters for their largest model was 165 billion.

The training time was probably around 34 days, and the infrastructure used was 10,000 V100 GPUs, and this was primarily an Azure infrastructure. The size of the dataset used for training was 4,500 gigabytes, 300 billion tokens were used. And the dataset source was Wikipedia, Common Crawl, WebText2, Books1, and Books2. With fine-tuning, the starting point is a pre-trained model. We then want to train on data specific to the task, such as text-classification, named-entity recognition, and so on.

So what are some of the benefits of transfer learning? Well, firstly, it takes much less time to train a fine-tuned model. For BERT, the authors suggested between two and four epochs of training for fine tuning. This is in contrast to the thousands of hours of GPU time required for pre-training. We also don't need another massive dataset to fine tune for a certain use case. This is in contrast to the massive datasets, such as Wikipedia and others, which are typically hundreds of gigabytes.

And remarkably, we're able to achieve state-of-the-art results. We saw this phenomenon when using transfer learning with computer vision several years ago when working with the ImageNet dataset, and this technique of transfer learning has worked in NLP too.

## 4. Transformers and BERT

12. 012. Transformer Architecture overview.en
=========================================

![85.png](./images/85.png)
![86.png](./images/86.png)
![87.png](./images/87.png)
![88.png](./images/88.png)
![89.png](./images/89.png)
![90.png](./images/90.png)
![91.png](./images/91.png)

- [Instructor] The transformer is made up of two components, an encoder and the decoder. We feed in the English sentence, such as I like nlp into the encoder at the bottom of the diagram. The transformer can act as a translator from English to German. And so the output from the decoder is the German translation ich mag nlp. The transformer is made up not of a single encoder, but rather six encoders. Each of these parts can be used independently depending on the task.

So the encoder-decoder models are good for generative tasks that require an input such as translation or summarization. Examples of such models are Facebook's Bi-directional and Auto Regressive Transformers, or BART, and Google's T5 model. Encoder-only models are good for tasks that require understanding of the inputs such as sentence classification and named entity recognition. Examples include the family of BERT models like BERT, ALBERT, RoBERTa, DistilBERT, and so on.

Decoder-only models are good for generative tasks, such as text generation. Examples include the GPT family such as GPT, GPT-2, and GPT-3. And before we look at the BERT architecture in more detail, let's look at some of the tasks BERT cannot do. BERT cannot generate text, as it doesn't have the decoder component. This means it won't be able to do tasks like text translation and text summarization. So the encoder piece is good for tasks that require understanding of the input.

So you'll be able to do text classification, named entity recognition, question answering, and fill in the blanks, amongst others.

13. 013. BERT model and tokenization.en
===================================

![92.png](./images/92.png)
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

- [Instructor] Models can only process numbers, so tokenizers need to convert our text inputs to numerical data. With subword tokenization, frequently used words are not split into smaller subwords. On the other hand, rarely used words need to be decomposed into meaningful subwords. BERT uncased, so this is where BERT is not case-sensitive, has a vocabulary size of around 30,000 tokens. GPT-2 and GPT-3 have around 50,000 tokens. They use different techniques for subword tokenization.

BERT uses WordPiece, and GPT-2 and GPT-3 use byte-pair encoding, or BPE. When you enter a sentence like I like nlp into BERT, it is converted into subword tokens. Since the word nlp is not in BERT's vocabulary, it is split into nl and ##p. And since models cannot work with the words, but need to work with numbers, each of these subwords have an associated input word ID. You'll notice that the tokenizer also has the CLS token and the SEP token. The CLS token is for sentence-level classification, and the SEP token is for handling two sentence tasks so that you can separate the two sentences.

Now, what we've referred to as the BERT model is actually made up of 12 encoders. The original transformer model had six encoders. Now, here's an important detail that we haven't covered so far. BERT is an acronym for Bidirectional Encoder Representations from Transformers. We already know that it is only the encoder portion of a transformer. What we haven't considered is the bidirectional piece. So let's take a look at how this works. In BERT, we give the entire input sentence at once, and so BERT gets to weigh up all of the words in a sentence in its prediction.

This is in contrast to a decoder-only model like GPT, which generates words and so only has access to words that it has already generated. As part of being able to process the text in parallel, all the input text sequences are padded out or truncated to a fixed length. BERT can only support up to 512 tokens at one time. BERT has two ways of differentiating two pieces of text as input. The SEP token is in place between the two texts, and segment embeddings are added to distinguish between the first sentence and the second sentence.

Now, you're probably wondering, if we already have the SEP token to distinguish between the two sentences, why do we need segment embeddings or vice versa? Deep learning is an area of active research and experimentation. The authors of BERT may have found some performance gains, which they haven't documented. You can always try input two sequences without a SEP token and see the result. Now, we also need some notion of word order. The positional encoding vector is added to the embedding vector.

Now, tokens with similar meanings would be closer to each other, but embeddings do not encode the relative position of tokens in a sentence. So after adding the positional encoding, tokens will be closer to each other based on the similarity of their meaning and their position in the sentence. So this is what things look like. We have our input text, I like nlp. This is converted into subwords, and the CLS classification token is added to the start and the SEP token to the end.

These are converted into input word IDs. Segment embeddings help to distinguish between the sentences. And after the positional encoding step, we have captured both the similarity of the word meanings and their position in the sentence. Finally, this is fed into the 12 encoders, and the results are available as hidden states. It's now time to get into the details of the components of an individual encoder.

14. 014. Tokenizers.en
==================

![107.png](./images/107.png)
![108.png](./images/108.png)
![109.png](./images/109.png)
![110.png](./images/110.png)
![111.png](./images/111.png)
![112.png](./images/112.png)
![113.png](./images/113.png)
![114.png](./images/114.png)
![115.png](./images/115.png)
![116.png](./images/116.png)
![117.png](./images/117.png)
![118.png](./images/118.png)
![119.png](./images/119.png)

- [Tutor] Let's head over to the Colab notebook to confirm our understanding of tokenization and code. So, in the first couple of cells, we're installing TensorFlow Text and the TensorFlow Models Official. We then go ahead and import these Python packages. And then we're loading a BERT model from TensorFlow hub. We're using a BERT model with the uncased weights. And so you can see that we have a vocabulary size of about 30,000 tokens. So you can see that the BERT model is a standard BERT model with uncased weights, and it has 12 layers.

So our input sentence is going to be, "I like NLP." This is then tokenized and then the tokens are then converted to IDs. So, "I like NLP" is converted to, "I like NL" and then "##P." These IDs correspond to token IDs. If I enter two sentences, "I like NLP." And, "what about you?" I then enter that into the BERT model and you can see that we get this output results. So let's look at this in a little bit more detail. Now, normally BERT has a maximum sequence length of 512.

Here we're using a sequence length of 128. So the reason that we have a shape of two, 128 is because the two corresponds to the two sentences and the 128 to the sequence length. The input word IDs are the corresponding conversion of the subwords into input IDs with the CLS and the SEP tokens added. So you can see that the CLS token is 101 here and the SEP token is 102. And this block corresponds to the first sentence, and the second block corresponds to the second sentence.

And finally, the input mask confirms which bit the model will focus on. And so you can see that the model is going to focus on where we have the text and the sentence. So that's in the first sentence, the ones here correspond to the second sentence and the zeros correspond to padding. And that is an overview of the tokenizers in code.

15. 015. Self-attention.en
======================

![120.png](./images/120.png)
![121.png](./images/121.png)
![122.png](./images/122.png)
![123.png](./images/123.png)

- [Instructor] In this example text, the monkey ate that banana because it was too hungry, how is the model able to determine that the it corresponds to the monkey and not to the banana? It does this using a mechanism called self-attention that incorporates the embeddings for all the other words in the sentence. So when processing the word it, self-attention will take a weighted average of the embeddings of the other context words. The darker the shade, the more weight that word is given, and every word is given some weight.

You can see that both banana and monkey come up as likely for the word it but monkey has the higher weighted average. What's happening under the hood? As part of the self-attention mechanism, the authors of the original transformer take the word embeddings and project it into three vector spaces, which they called query, key, and value. Why project the word embeddings into these three new vector spaces? This allows you to have different representations of the word embeddings.

The equation used to calculate the attention weights is given by the following formula to be taken as input into the self-attention, the query, the key, and the value vectors. We then calculate the score of each word to determine how much focus to place on other words in the sentence. This is done by taking the dot product of the query vector and the key vector. And if you've forgotten your linear algebra, the T means that we are performing a transpose operation on the vector K.

We then divide this by the square root of n to scale the dot product attention. Here, n is the dimension of these vectors. And so we now have logits. We can then go ahead and convert this to probabilities by using the softmax function. And we now multiply each value vector by this softmax score. We can then sum up the weighted value vectors. And this produces the self-attention calculation for a single word.

16. 016. Multi-head attention and feedforward network.en
====================================================

![124.png](./images/124.png)
![125.png](./images/125.png)
![126.png](./images/126.png)

- [Instructor] Earlier, we looked at how self-attention can help us provide context for a word, but what if we could get multiple instances of the self-attention mechanism so that each can perform a different task? One could make a link between nouns and adjectives, another could connect up pronouns to their subjects. This is called multi-headed attention, and BERT has 12 such heads. Each multi-head attention block gets three inputs, the query, the key, and the value.

These are then put through linear or dense layers before the multi-head attention function. The query key and value are then passed through separate, fully-connected linear layers for each attention head. This model can jointly attend to information from different representations and at different positions, allowing it to make richer connections between words.

17. 017. Fine-tuning BERT.en
========================

![127.png](./images/127.png)
![128.png](./images/128.png)
![129.png](./images/129.png)
![130.png](./images/130.png)
![131.png](./images/131.png)
![132.png](./images/132.png)
![133.png](./images/133.png)
![134.png](./images/134.png)
![135.png](./images/135.png)
![136.png](./images/136.png)
![137.png](./images/137.png)
![138.png](./images/138.png)
![139.png](./images/139.png)
![140.png](./images/140.png)
![141.png](./images/141.png)
![142.png](./images/142.png)
![143.png](./images/143.png)
![144.png](./images/144.png)
![145.png](./images/145.png)
![146.png](./images/146.png)
![147.png](./images/147.png)
![148.png](./images/148.png)
![149.png](./images/149.png)
![150.png](./images/150.png)
![151.png](./images/151.png)
![152.png](./images/152.png)
![153.png](./images/153.png)

- [Instructor] As part of the pre-training step, when Google trained BERT with the next sentence prediction task which is a text classification task, a linear layer was added at the end of the BERT model. The only thing that was fed into the linear layer was from the CLS embedding. So in order for the BERT model to perform well, it learned that it needed to capture all the information required in the CLS token. This means that when we want to fine tune BERT, say on movie reviews, all we need to do is to add a linear classifier layer and use the final embedding of the CLS token as the input to the linear classifier.

In addition to a linear classifier, we often add a dropout layer to reduce overfitting. We then train or fine tune the model with a label dataset. Using the movie review example, this would be training the linear classifier with the movie review texts and their associated labels, either positive or negative. Notice that we are not taking any input from any of the final embeddings in the hidden state. Although we don't use them for the classification task, they capture increasingly enhanced embeddings, and we shouldn't discard them earlier in the model.

If we were to do fine tuning for named entity recognition or question answering, we would use these other final hidden states. Let's now head over to the CoLab notebook to look at an example of fine tuning for sentiment analysis. Now, here we want to train a sentiment analysis model to classify movie reviews as positive or negative based on the text of the review. We'll use the large movie review dataset that contains the text of 50,000 movie reviews from IMDb.

The first thing we want to do is to change our runtime type from CPU to GPU, as we'll be training a model. So you would head over to runtime, change runtime type, and you would change this from none to GPU. Now I've already trained a model and run this notebook a couple of minutes ago, so I'm not going to rerun this notebook. Feel free to go ahead to run time and run all the cells in this notebook. Now, the IMDb dataset has already been divided into train and test, but it doesn't have a validation set.

So what we want to do is to try and create this validation set and so we'll split the training data in order to do this. One of the benefits of using TensorFlow is that we have some built-in APIs that support input pipelines. As part of the training process, we will just need to read data from the directories, but we don't want to make our model wait for this data. The tf.data.AUTOTUNE allows you to fetch the data dynamically. Our objective is to create a data set object, which contains both the text and the associated label.

The IMDb training dataset is already made up of 25,000 text files. So we'll read these from the directory using the method text_dataset_from_directory, and this creates a text batch and a label batch. And these are the 25,000 files belonging to the two classes, which are either positive or negative reviews. Now let's take a look at a sample so that we can see both the review texts and the associated labels. So, zeros are for negative reviews and one for a positive review.

So if I was to look at the first example, so the review is negative and the review starts off, stupid and just plain weird movie about some kid who becomes traumatized and so on. Now, just to make sure that the training time is shorter, I'm going to use a smaller version of BERT that only has two layers and two attention heads, and this is called the small BERT model. If you want to try the full version of BERT, comment out this line with the small BERT model and uncomment out the first-line.

Just a word of warning. Your training time will be significantly longer. So you can see the shape of the sentence, I like NLP along with the word IDs and the input mask that we've seen earlier. So 101 corresponds to the classification token, 102 corresponds to the SEP token, and this is the input IDs for the sentence I like NLP. So let's head over to the BERT classifier. So what we're doing is taking our BERT model from TensorFlow hub, we're then adding a dropout layer and then finally we add a dense layer and we have only a single node because we want to know whether the review was positive or negative.

And so this is what our BERT classifier looks like. So we have an input layer, the Keras layer, which takes in the BERT encoder, we finally add our dropout and our classifier. As there are only two outputs, a positive or negative review, we use binary cross entropy. If there were more than two classes, we would use categorical cross entropy. Our metric will be accuracy. Now, if you train for 10 epochs, now, if you train for 10 epochs, it will take you a good five minutes to train this model.

When fine-tuning, we'll often start off with a smaller learning rate. So we start off with an initial learning rate of 3e to the minus five. For fine tuning, let's use the same optimizer that BERT was originally trained on that's adaptive moments or Adam. We'll also use the same schedule as BERT pre-training. So we have a linear warmup phase over the first 10% of the training steps. We've now got to the optimizer, the loss and the metrics, and so we're ready to go ahead and compile the model.

Now in the TensorFlow, working with images course, we looked at callbacks. In general, callbacks and TensorBoard are good tools to use for understanding, optimizing, and visualizing model training. So we'll work with them here. So we'll set up our checkpoint directory, which will update our directory as our model trains. And so we're now in a position where we want to train our model. In TensorFlow, we do this by calling the fit method and providing our training dataset as input.

And in this instance, I've trained not for 40 epochs but for 10 epochs. And let's head over to the TensorBoard to see how the accuracy has changed over time. And you can see that at the end of the 10 epochs, we've got a validation accuracy of about 80% and the training accuracy is around 86%. Now, if you're not familiar with TensorBoard, I've also provided a simple matplotlib plot of the training and validation loss over the 10 epochs. Now that our model is trained, let's go ahead and try it out on the test dataset.

And you can see that we have an overall accuracy of about 78%. We can then go ahead and try out our model on a couple of sentences that we've made up. So, in the first sentence I've said, transformers have been a boon to NLP. It's going to be a case of before transformers and after transformers, they are wonderful. And not surprisingly, the score that we have for this is 0.988, which is a positive review. In my second sentence, I've provided as input from the first time I heard about them, I have found them to be dull and uninteresting.

And as you can see, we have a negative review of 0.01. So just to recap what we've done with fine tuning. We've taken a BERT model from the TensorFlow model hub. We've taken the IMDb dataset, we've then added a dropout layer and a linear classifier to the CLS token, and then fine tuned on the IMDb dataset. And we've then finally used our model to classify other sentences and we've come up with pretty impressive accuracy results after only training for about 10 epochs.

## 5. Conclusion

18. 018. Next steps.en
==================

- [Jonathan] We've covered a lot in this course and looked at transformers for NLP with a focus on BERT. We've seen how BERT is used in production, but also the problems of bias and prejudice with BERT and GPT-2. We looked at transfer learning, which is this almost magical technique that did wonders for computer vision, and it's doing the same for NLP. And finally, we looked at the BERT architecture, working from tokenization all the way to self-attention.

Go ahead and either experiment with BERT and look at other use cases such as named entity recognition or question answering. Alternatively, you could try out some of the other BERT variants such as BERT-Large, or DistilBERT. You now know enough to try out some other models in the TensorFlow hub. I hope you found this course helpful. Thanks for watching, and I'd love to hear back from you and to connect via LinkedIn. (speaking in foreign language)

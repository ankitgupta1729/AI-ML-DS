## 1. Introduction

1. What is Time Series Data
===========================

![1.png](./images/1.png)
![2.png](./images/2.png)
![3.png](./images/3.png)
![4.png](./images/4.png)
![5.png](./images/5.png)
![6.png](./images/6.png)
![7.png](./images/7.png)
![8.png](./images/8.png)
![9.png](./images/9.png)

Hey, guys, welcome to the course on time series forecasting. Let us talk about time series data: a given sequence of data that happened in one specific order. For example, we have a list of time series data where y minus four happened before y minus three, y minus three happened before y minus two, and so on, and finally y_t happened. Such data is called time series data. Typically we are talking about a single number. This could be the population of a given country, the temperature in a city, the number of products sold in a store in each quarter, etc.

and so on. Those kind of data is called time series data. Why time series? Let us understand the importance of time series with an example. Let's say I want to forecast the stock price of Tata Motors tomorrow, which is y t plus one. If you want to forecast tomorrow's value of the stock price, it could depend upon so many factors: it could be the crude oil price, it could depend upon the revenue, and sales number of products is being sold and and so on.

There are so many factors is defining the price of the stock in order to forecast this value, y t plus one, which is a function of the predictors and also the trend of the previous values. What time series forecasting does is a simplification: can we do the prediction just looking at the trend of the past values of the stock price? This technique is called time series forecasting, where we are making the forecast by making use of the past values and the past trend, ignoring all the predictors, not because they are not important; we are thinking those predictors have an impact on the past values, since the impact of the predictors is already contained in these values.

So in order to make the future predictions, [unclear] I will take only these. So this is what the idea of Time series data and forecasting. In the next lecture, we will talk about the components of time series data. Thank you very much.

2. Time Series Components
=========================

![10.png](./images/10.png)
![11.png](./images/11.png)
![12.png](./images/12.png)
![13.png](./images/13.png)
![14.png](./images/14.png)
![15.png](./images/15.png)
![16.png](./images/16.png)
![17.png](./images/17.png)
![18.png](./images/18.png)
![19.png](./images/19.png)
![20.png](./images/20.png)
![21.png](./images/21.png)
![22.png](./images/22.png)
![23.png](./images/23.png)
![24.png](./images/24.png)
![25.png](./images/25.png)
![26.png](./images/26.png)
![27.png](./images/27.png)
![28.png](./images/28.png)

Hey, guys, welcome back. In this lecture, we will look into the time series components. In general, time series data is composed of four elements: trend, cyclicality, seasonality and finally irregularity. In any time series data, you will find these components. Let's look into these components one by one. Trend long term and general direction is known as trend. If you look into the figure as shown, which is 13 years of data. If you look into the time series data, it is not continuously increasing or decreasing.

It is following some cyclic trend. The cycle is repeating for every eight years. But overall, if you see the data is on average is increasing. That line is called trend in the data. Second component, cyclicality, cyclicality is behavior in the data where you observe the pattern is repeating over a period. Usually, cyclicality is more than a year. As you can see from the data, particularly long term, the pattern is repeating for every eight years hence, this period is called cyclicality.

Seasonality is like the cyclicality, but usually occurs in a period less than a year. For example, let's zoom and investigate the one year data here, you can observe the pattern in the data behavior so that behavior usually in one year is called seasonality. And finally, irregular. The irregular component is basically random and noisy behavior in the data, which has rapid changes and even shorter than the seasonal effect. Now, let's talk about the real data of Aurobindo Pharma for three months from May 2020 to August 2020.

This data is available on the National Stock Exchange, nseindia.com. Let's investigate and analyze its time series components now. If you look into the data, which is increasing to be more precise, from May to August, the price of Aurobindo Pharma increases, and the trend line will look something like this. which is basically obtained from the regression line. There is no cyclicality behavior. There is no cyclicality, as cyclicality should be more than a year of data.

What I'm having is just three months of data. So now let's see seasonality. Every week you can see a pattern is repeating meaning for three days it increases and the next three days it decreases, which completes the period. That component is called seasonality. And finally, irregular or randomness, which we cannot predict or measure. If you zoom and investigate the pattern and this location, which is completely noisy, it's called irregular. These these are the four important components, which is very much required and need to be analyzed, which are useful for forecasting the time series

data. Thank you very much. We will continue more in the next lecture on time series forecasting and analysis.

## 2. Python Essentials

2. Install Anaconda Python
==========================

![29.png](./images/29.png)
![30.png](./images/30.png)
![31.png](./images/31.png)
![32.png](./images/32.png)
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
![48.png](./images/48.png)
![49.png](./images/49.png)

Hey, guys, welcome back in this lecture. We'll see how to set up Anaconda. Anaconda is a python with all the preinstalled packages has been there, which are required for data science. So now let's see how to install and setting up the local computer. Go to Google and type Anaconda. And as you can see, there is the website, www.anaconda.com. Click on the first link, the most popular data science platform. Click on that and now you are in the home page of the Anaconda, it says that data science, technology for a better world and all the solutions has been there.

So Anaconda is open source. And what you can do, you can go to the products and Individual Edition. And now you can see that one of the popular packages and all the libraries that was there in the Anaconda and if you can see here, there are almost two hundred plus packages of libraries that were preinstalled in it. So in order to get that scroll down, as you can see, there is Windows and the current Python version, it is three point eight, which I'm going to download now.

So whatever the version you are having and what are the higher version you are having, please download that at the moment. My computer, a 64 bit. If your computer is 32 bit, you can download that. But if your computer is 64 bit version, then download the 64 bit installer. Click on this. And keep. So it's very big, it will take some time, and will continue once it's completed. Now, I have successfully downloaded my anaconda click here and show in a folder. So this is what the Anaconda file that we have downloaded.

So what do you do now? Right click and run as administrator. And click on yes. Now, just click on Next to continue. And agree. [unclear] that have given you it is highly recommended to go to only the just me. Now click on Next, it is asking you to install what are the folder you want, what are the destination folder you want install? You can install in that particular destination folder at the moment. I'll give it what are the default folder is giving me?

I'll keep those folder only click on next. Make sure you check this: add Anaconda3 to my PATH environment variable. Now click on install, and that's it. It will take some time and probably it may take some five to six minutes depends upon the speed of your computer. So we'll continue once installation has been completed. Now, I have successfully completed the installation click next to continue, and if you want to install PyCharm, you can also install that. At the moment, I'll click next and skip, and check all those boxes and finally finish.

Now, you have successfully installed your Anaconda.

3. Open Jupyter Notebook
========================

![50.png](./images/50.png)
![51.png](./images/51.png)
![52.png](./images/52.png)
![53.png](./images/53.png)
![54.png](./images/54.png)
![55.png](./images/55.png)
![56.png](./images/56.png)
![57.png](./images/57.png)
![58.png](./images/58.png)
![59.png](./images/59.png)
![60.png](./images/60.png)

So in order to open this Anaconda, what we need to do here is that go to search or in the search bar your type Anaconda. There you can see the Anaconda navigator and the prompt and PowerShell that have been created. So click on this Anaconda. All right, now it is going to take a few seconds to get set up. Done, so this is the Anaconda Navigator, and there you can see all the apps that are there: [unclear], IBM Watson Studio, JupyterLab, the notebook, PowerShell, Spyder, VS Code.

So everything has been preinstalled with you. So most of the case, we will use only the Jupyter notebooks. So make sure that you put a notebook has been installed. If not, there will be one button called install; So you just click on that and start. All right. Now let's see how to launch the Jupyter notebook. So as you can see, we are in the Navigator and what we can do is simply you can click on launch. So before that, what I will do, I will create the folders and the desktop.

So this is what the working directory I was currently working on. So this minimize it. And what I do hear the click to create a new folder. Right. Click and create a new folder. Just name it as a time series. So make sure when all you're creating a folder don't put any space. So no spaces; do not create any kind of spaces here. So now open this folder and let me create one more folder and name it as Python. So let me go. This is my first module, so that is why I called it Python.

So now this application for you create one more folder and the next lecture. Maybe we'll talk about the visualisations. And maybe in the third lecture, we'll talk about regression. And fourth, maybe we'll see additive models, additive and multiplicative models. And fifth, ARIMA. And the sixth, we might see smoothing techniques. And in seven, you might see SARIMA, and everything will be there. So based on that, we'll keep on adding the folders. At the moment

I'm working on the Python here. So open this python. So this is the current working directly I work on. So what do we do? Let's open the Anaconda Navigator and click on launch. Just click on the launch notebook. All right, now we can see our notebook has been launched and you can see this is localhost 8888, and this is where we have installed it. [unclear] And remember, I was in the desktop.

I was in the desktop folder. So you are also most likely will get something like this since you are on the desktop. So just going to the desktop and as we go into the folder named Time series and Python visualizations. So that's it. So you are in the spot now. So what do I do now? So click on New and Python 3. So that's it. So you have successfully opened your notebook, so probably the ability to talk about the next lecture, more about the notebook. And I can see that we have successfully created the notebook and the name and title is there, and probably you can name it as the Python Essentials, whatever the name you want, you can take that.

So don't put any spaces. Let me create the python essential and rename it. And that's it. So now let's print the statement like welcome. to Jupyter notebook. And press shift enter to execute it. So basically, this is the cell, we'll talk more about this just to navigate about what we are going to do in the next lecture. Thank you very much. So this is how we can do. And finally, let's check that in the two days and the python, you can see the name of the creator. It is the python essentials, so.

So that's it. So this is how you can install and create a notebook in your local computer. Thank you very much. We'll continue in the next lecture.

4. Markdown
===========

See the code [here](./1.ipynb)

![61.png](./images/61.png)
![62.png](./images/62.png)
![63.png](./images/63.png)
![64.png](./images/64.png)
![65.png](./images/65.png)
![66.png](./images/66.png)
![67.png](./images/67.png)
![68.png](./images/68.png)
![69.png](./images/69.png)
![70.png](./images/70.png)
![71.png](./images/71.png)
![72.png](./images/72.png)
![73.png](./images/73.png)

Hey, guys, welcome back. Now let's talk about the Jupyter notebook. The previous lecture, we have seen how to install Anaconda and also open the Jupyter notebook. Now I will show you another way of opening the Jupyter notebook. All right. So what I will do now, I will go to my search and type Anaconda. And as you can see, you can see the Anaconda prompt Anaconda three. So what I will do here, I will click on this now it is going to open me one shell. So what I will do here is that I need to set the path first, since I already know that that is what my current working director.

So what I do, I'll open this. And here I was working on so what I'll do. I'll copy the path. In order to copy the path, What you need to do here is that just click on the path here. So now what we do, I click and copy the path you. Now, minimize it now type cd, space, and now paste the path here. So this is the path we are working on now and to. All right, now, we have successfully in the past here, not so what I'll do.

Let me clear it. So now just clear, now type jupyter notebook, and it will be OK. And enter. That's it now we have successfully opened our Jupyter notebook. So what we will do now, let's open New and Python 3. That's right. So this is what, the Jupyter notebook. Now let's talk something about Jupyter. So if at all, I just walk to the Jupyter notebook. Jupyter basically stands for Julia, Python and R. And initially, Jupyter was built to write programs in Julia, Python [unclear].

And now it will support many languages like JavaScript, Java and many, many languages that is being supported by Jupyter. Not he can look into the official documentation of the Jupyter so that you can look into the supported languages. At the moment we are and you can see what are the kernel we are operating. It is what, the Python three. All right, so what we can do here is that we just look into this, what are the ribbon buttons we are having? You can see the Quine, so where you can see instead of going back and creating a new notebook, where we can see here is that we can click on the file and click on the new identity so that it will automatically created the Jupyter.

And if at all you want to open a new Jupyter notebook, and you can also find that you can make a copy of this notebook. We can simply make a copy of that and save and download as HTML, so everything can be do. All right. And one more thing here is that there is a name is there the body for the name is Untitled. You can change what other name you want by just clicking on that and now you can change the name. Let's say this is what my Jupyter just walk through on Jupyter.

All right, so now we can say this is the walkthrough on Jupyter, and now let me show you all the toolbars, I'm sorry. Yeah, so this virtual bar like you want to double header it, removed the name. And if you don't want to come back and click on the double header and if you're wondering, will this toolbar I mean, most of the cases, I want to use that. And for that you can click on the toggle toolbar so that you can remove that. Now, if at all you want and have the numbers just like me, I'm getting like, you know, just keep on get some numbers, one, two, three [unclear].

And for that, you can see the toggle line numbers so that it can get up and click on this tag line numbers. You can see this line number. So let me let me put this tag line numbers, whatever I'm having with me. All right. And you can also let me into the statements like welcome to Jupyter. Now, let me ask you this. I can see I have executed the cell. So how to execute this so we can execute a cell by shift plus enter, the shortcut shift plus enter. You can even execute the cell by click on this run button, click on the send button.

You can see the cell is being executed and you can see here, if at all of the cell and how it turned out this is going to repeat is going to give you the what number, what number it is going to be there. For example, let me get one more statement like hello. Now, what happens is that inside there's a number to do. If I use this, I'm getting the number three. So this is the convenient way so that we can understand like a. How many what is a line get executed?

What is the previous line we have that we can simply understand by this? Next, you can also insert the cell, what are the what are the programs you are writing? Right. This is called cell. You can insert a number of cells you want. They can see what level if if you wanted to insert the cell about this and make sure what do you have that you can insert and click on some level. And this you could also use a SHORTCUTTING for that short cookie, make sure to escape so that if you see if I if I in this I was into the cell walls and the green color if at all, the press escaped.

Press a button to get the cell in the blue color again, seeing the volume on this, if you're going to get the blue color here. So once you are having the blue color and press a press command aim so that you can see they can enter the cell about one of the cell, you are here so I can enter any number of cells I want so that I can and I can use this number of cells. I can work on the cell. You. For example, let me escape and I can insert the command beam to insert the cell below this particular cell so I can see, I can see and I can use any number of a number of cells below the particular cell, if at all.

I want to delete the cell, I want to make sure it is in the blue mode, and now press D two times. You can see it deleted this. [unclear] So let me delete all these cells now by pressing D twice. Now, let me print hello, execute. For example, if you accidentally deleted a cell and you want to come back again, there is no Ctrl Z to get this. What you do is go to Edit and Undo Delete Cells, and you can get this; and the shortcut for this is Z, and the shortcut for delete is D two times.

So you put all your present, you can get the particular set. If you want to know more about the shortcut keys, because it is very much required for that, you need to go to Help, and there is Keyboard Shortcuts, is there click on this keyboard shortcut that you can see the number of shortcuts and how to use this is there. And all of this, all the commands will be executed, will be enabled if you press escape so precise so that you can enable all the shortcut keys.

For example, you want to find a replacement, then use is very much required. And also, if at all, you want to open the command palette, then Ctrl Shift F. this and all the very useful shortcut things. I recommend you do practice all the shortcut. Now, let's understand one more concept called Markdown, as you can see here, by default, you are in the code means you can write what are the code, for example, easy to do. And basically the central, like in all the code modes means this and all the completely you writing the Python statement instead.

There is one more thing called Markdown. Markdown is very, very powerful, and Markdown will be useful for documentation. Now, let me talk a few things about Markdown here. Markdown uses a language; you don't need to learn much about a new language, let's just use the small commands. So which I'm going to you explain you here. So let me here. This is the Markdown. Use language. So you need to learn this language. I'm going to explain the few comments that will be useful.

So what it means like a fish. You can see this is what is being seen here. So let me see the few in the Markdown. So make sure you are in Markdown. Now, if you use a hash, which is basically a header, for example, just like HTML, this is h1, so this is heading one. And if at all, you want to reduce the size of the heading one, that is a to double put the half two times you'll get heading two. Basically this is the highest, and three hashes:

This is my heading three and four hashes is my heading four, and for the paragraph. Again this is what my paragraph. So I think all you want to excel for in order to execute that use command shift plus enter to execute this. Now you're going to see that we have like in all the different ways of creating the fonts, like heading one page. One has to it's like heading one, heading two, heading three, heading four is very simple, just by creating the hash and that is going to be created by this.

So let me use the let me see if you make those statements like creating the bullet points. I can create a bullet point by using this hash. So let me try a few things. Like like no, you can create. headings using hash, and let me put it one more point, you can create bullet point or an unordered list with hyphen, something like this. Now, let me ask you this. Now you can see we have it on our list of the bullet points. By using this hash like, no, you can create the bullet points using the heading hash and you're going to create a bullet.

You can create a bullet point or an unordered list with hyphen. So those kind of things you can still created. So let me do one more thing like saying that Python lets say like we create here, I can use some kind of style in your text, like creating the bold, italic or strikethrough or something like that. So let's say Python is the general purpose language. So if at all, I want to boil despite all I can use. This double star, double star basically will be all this.

What are the string you want? Basically it makes a string strong like see you can see here, this is the plain text and wherever you put this double star, that is going to be highlighted. And similarly, there is a single star, which is basically italic. You can see this makes the language. This makes this particular string to be italic. We can also see a few more things like. Is used to build a shallow animal's deep learning models. And for visualisations to creating visualisations, etc, and Python also used to develop websites like Django,

Flask, all the popular frameworks which are used to create the websites. And you can also connect. To the database using Python. Even Python is used to create desktop applications. We did a lot of applications that are a lot of things which made the python has been used. So the main purpose for me is to show you, like in all different kinds of stylings of the font. For example, you already saw that a bold and italic are also having the bold italic or three dots, three hashes and basically used for the bold italic is especially useful.

And we can also have something like in a strike room, for example. I want to do the same strikethrough on this. Or this entire thing for getting the strikethrough I can use this tilde two times, will basically create the. So these are not operations what we can do, what one of the things which we will do and the word document, the same thing we can do even and the of the notebooks that will that do in the model. But there are a lot of things, a lot of applications where this is being really, really useful and handy.

I can also give the hyperlinks. I can also give the hyperlink saying that using this hyperlink, like using the exclamation mark, followed by the two square braces, I can see like in something like Google. So if at all you can click on this link. It will go to the Google: https://www.google.com. I can create something like this. So for reference, basically, if at all you have any questions or queries for references, you can go to this Google and something like this.

I can see this is basically used for images in order to use used the hyperlinks. The same one exclamation mark will only just keep this this thing. So you can see we have like a hyperlink is being greater if at all. You can click on this hyperlink. It will go to the Google page. Right. So we can also create one more hyperlink. Let me do one thing. Let me create this Google. And inside that, let me create one more thing, Lieutenant, so I can view the hierarchy bullet point, something like this by just pressing the tapu.

Now, I can give you one more references for you is basically Stack Overflow. And in this, which is basically https, is the website name, stackoverflow.com. Executed. You can see we can create this Stack Overflow; we created one more hyperlink. If I click on Stack Overflow, it will go to the Stack Overflow website, where the developers will if you have any queries or anything, just copy and paste this in the search window that you can get the appropriate the solution for your errors.

So it's very, very, very, very useful website, particularly when you are developing some kind of. And finally, if for an order to get the complete notebooks and essentials and you can also visit our website, which is datascienceanywhere.com. So I request you to visit your website so that you can download all the different videos and DVDs, et cetera. So for that, go to our website. [unclear] datascienceanywhere.com slash timeseries.

So where you can see the all the reference materials that will all the reference materials is everything you can you can find out in our website so we can click on this Web site. Now there is this is a website where you can see all the reference materials, for example, if at all. You want to look into the introduction of regression, just click on this PPT link, and where you can see the video for the regression and regression and all the videos for that.

All right. So this is more like an all the basic understanding of the Jupyter notebook. It's a really, really useful and you can also create more than this for that in order to get more information about how to work on Markdown. For that, you go to Help and click on Markdown, and it will redirect to the docs. So there you can see the basic writing of the formatting. This click here and there you can see like how to create the headings using the one has to ask hash and the styling, like bold, italic, strikethrough, and how to code the text and the code and everything.

Everything is being there. So all these things will work if you need to put the cell into Markdown. If it is in code mode, you can go to Markdown and write whatever you want, like welcome to [unclear] or something. OK, so we are in Markdown here. So for all these things, again, you can check this documentation's on how exactly you created the last on the list of hyperlinks or bullet points.

And so everything, everything can be created using this beautiful Markdown. So this is the walkthrough of the Jupyter notebook. In the next lecture, we will talk more about the python. Thank you very much.

5. Print Statements
===================

See the code [here](./1.ipynb)


Hello, everyone. Welcome back. In this lecture, we will talk about some Python essentials that are required to build the project. OK, so what we are trying to do here is that let's try to understand some basic data structures and some conditional statements, et cetera, everything in Python essentials. OK, so first let's import one of the library, which is called sys, and that comes with default Python, which install. So let's check the what is the version I was currently working on.

So in order to check that we can import sys, and in order to execute this so we can use the shift plus enter so shift plus enter is a shortcut to execute this. OK, so so I'm typing this and shift plus enter so that I can execute this particular cell here. Now I'm using the module sys to check the what is the version I'm currently working on. So that's why this version which will return you the working version.

And so I can see here the version, it is three point eight point five and the default and the release date of this particular version is July 2020, and probably you might be looking at a later version, whatever I'm using now. All right, so now let's look into some basic operations like the print statement. Let's see the print statement. Currently I'm using Markdown here. In order to make it Markdown,

there is Code here; you just change that into Markdown. Now, this is basically the double hash, a heading. All right. So this is what the print statement. So let's look and do some print statements. You. So there are a lot of inbuilt statements that was available and there are a lot of inbuilt keywords available in Python. So what we will do, we will make use of those key words and use it.

So let's look into the key words in order to understand what are the key words that are available. And you can import import keywords. And the keywords also comes with the default python. So I use this keyword. Import keyword. So now keyword.kwlist, which will return the list of keywords that were available, so false, not true, and so this and all the list of keywords that was available here. So now let's print all the key here. So this is the I'm having the keywords in the list so I can print all the keywords, print keyword.kwlist.

I can print all the keywords that are by default available in Python. OK, print is also a keyword. So let's see how to use print. so we can also print the list of keywords. I just want you to do here is that you need to pass some value and separation the default separator will be the space, and there is an end, backslash n. So by by default there is a backslash and is there so backslash and indicates a new line. All right. So we'll see one by one what it is.

So let's print one of the statement. Let's say welcome to print and you can define the string with quotes, double quotes or single quotes. So welcome to Python programming. So I just enter this and exit the statement so you can also screen you can also define the string even with double quotes. So this is like an old output is more or less and more or less like an all, we can also use the multiple values. It seems like value come. Well, you can use the multiple values like a.

I can use a welcome and the comma. I can use one more thing to use one more string on and use one word string programming so everything I can use here. So that's what you can see here. That print. Welcome to all those things. So you can see there is a separation, is there? And what the separation will talk about, like in each and every string, what every object or string should be separated by those single spaced. And you could also define your own separation.

For example, I can use a separation is equal to backslash and which is basically the new line here. So I can I can get I can print all the values and the new line, or you can also use backslash t for tab, and comma, so each and every value, each and every value submitted by comma, so everything can be used in the print statements. So by default the separator is a space. So but you can use like in all the different kinds of separations, like any special characters, comma, full stop and the semicolon, whatever you want, you can use it so that you can use whatever separation you want.

So that is the one thing. So that's the one thing you can learn here. So next, what we will see there is the end is that the end is also may not be useful here, but the end is basically let's say there are two print statements on. Let's say welcome to Python programming right here. Welcome to Python. And. All right. Write one more thing like programming and one more statement. Let's say programming. And obviously by default, we have the two lines and the python end is backslash n. When

the statement is executed, it will move into the new line instead. And instead of moving to the new line, if at all you want to print side by side, then you can specify the end is equal to space. And so what you'll get here is that will come to Python programming, something like this. So this is what like, you know, some basic functionalities that was there by default. And the python is very useful and very handy, and we can use it in many, many cases.

6. Escape and Insert keys
=========================

See the code [here](./1.ipynb)

Now, let's see some kind of escape keys, generally that was used in the print statements. OK, so escape keys. So let's go into Markdown and type some escape keys. OK, so escape keys: basically backslash and anything else. Backslash is escape, backslash n is basically the new line, and backslash t is the tab space. And backslash, a simple escape backslash. OK, let's see one by one what these escape keys are and how it is being useful?

So first thing, what I will do here, instead of writing the two print statements and passing the end, and we can also use it or else like in or in sort of if if at all. I want to kill this. Instead of putting the comma and making it a separation, I can use the Python print statement, something like this. So welcome to welcome to Python programming. So if I execute the statement that this is what I'm getting, so instead what I want here is that I just want this Python programming to be print in the new line.

So what we can do here in the previously we did in the two statements and separate comma and we can set that end or else you can you can separate, we can make the separator equal to backslash n, so that we can execute in the new line. Instead we can use the escape keys like backslash n, and which will basically which will basically print that. And then you like something like this and remember. So backslash. And after that we have some spaces there.

That's why we got one type space in one space here. So if you remove this now, you can see that. Welcome to programming. So that's what the escape key here. And for example, we have the escape key. One would escape is a trap and which will basically give the tab space. So we'll get some one type here. This is the one that space is what we can get with the max last. But that's the beauty and the escape. And let's look into this escape. This is an escape. This is backslash n; backslash is basically used for the escaped character.

You want to escape some character and you can use this escape character, for example. I just want to print something like this, so. I will say this is what I just want in plain English, we can write like. I will write. I will learn. Python programming. OK, so we can see here, I will learn this python programming, but they say, if at all, you want to write some something like this and it is very difficult to execute in the python. So, for example, I and the cell again, if you do this, I will.

And what happens is going to be here is that it says that this is one string and we can get some kind of statement, but instead we can use something like an all IV bill. So we can we can end this string with the other with starting with the single quote and put the double quote so that you can get I will learn Python programming so we can get something like this or else if at all, you want only the single quote, you initialize with the double quote and

you put a single quote here, so you will get either. So instead what we can use here is that the special character like a. Backslash, which will actually escape that key. So what I can see here, for example, I can use a single quote and end with the single quote. So I just want to escape this in order to escape this, we can use backslash, so backslash is basically escape. OK, so that's an escaped character, and I can see, like in all this is going to be escape and the program will not see anything after this and programming will just ignore that.

So that's one of the beauty in that in the Python Python programming. So this is one of the basically what escape keys are about. Now, let's move on to one more thing called insert keys. Insert keys are also widely used and popular. There are certain insert keys: percent s, which basically is inserting a string; percent d is inserting an integer; and percent f will basically insert float values in the placeholder.

And we can also have the special thing like the format method, so we can insert whatever you want also inside whatever the string in and upload values can be inserted using the format. All right. Now, in order to let's see, one by one, how can we insert the strings? For example. For example, let me use a sprent, I want to learn some programming language. OK, so this is what I just want to learn some programming language, so some this is what I just want to insert something here.

If I don't you want to insert anything here, then use this percent s. Percent s will basically look for the string. Now, at the end, we put the percent, and followed by some 'Python'. Let's say if you type some python or if you use some string python. Now, what it is going to do here is that it'll search for wherever the percent is, and followed by some string or some object will basically search for any placeholders. Is there or not?

It will find the appropriate character since percent s is a string. This is what his finger in something. So as soon as the statement it's going to be inserted in that particular position. So that's what the entity is basically is about. So we can use those the last to insert the strings. And you can also use the. So we can set something like this and something like this is what I want. In fact, let's say I'm inserting some string here Strydom and in my page is something like person.

These is what made. This is my age, I suppose, and they'll be ashamed and I'm having. Some percentile zero point to F, so two decimal points of experience. OK, this is what we can see already, consistently percentage of f of experience. OK, so this is what we can do. So what it is, is like we can also instead the multiple keys again and said the key here, I can insert the string here inserting the integer, and I'm inserting the float values here at the same time.

So in order to do that, let's create the center here and we'll create some data structure called tuple. And now I'm just setting the values. So my name, Sriram, and That my age is thirty five and I'm having some. 15 years of experience, I'm having oral, 15 years of experience, so what I can do here, this is a string and this is what mine something like it deserves and this is my opinion, is what my it comes into the stream flood values. So that's what we can get here.

You can see here I'm and is totally fine. I'm having 15.000000 years of experience. Basically it's give you by default of six decimal point instead. If you want, if you want to control him you can use zero point one indicates we can get only one decimal point if you zero two and we'll get the this one points and so on, we're going to go to you. What are the values. Something like this. And it will only give you the relative value. Only off of the two decimal point is what we can do here.

But this is what is basically the case until pleasantly and percentile. And it can also use this format is also similar to the percentile and back, whereas the other end of the line is something like this. So I'll let you decide since same thing using the format, with these curly braces, and my age is curly braces and I'm having. This much of years of experience, OK, but this is what we can simply use this, so in order to insert the values, what we can do here is a good format.

And Justin said this is the. So just insert the violence, so this is Serena and my age is this and something values. This is something like this. So we can go, what are the random values and do something like this and give you those other values in 13 and it would give you that particular value. But this is what I can know about the brand statement is all about how do you print statements and some functionalities that was used in the opening statement.

You can also look into the escape keys. So this is about the print statements. Thank you very much.

7. Variables & Assignments
==========================

See the code [here](./1.ipynb)


Hello, everyone, welcome back. Now let's look into variables and assignments. Variables are the objects that are bound to a value, whereas assigning a value to a variable is called assignment. So, for example, let's assign a value, a equal to two. So here what you can see is that a is basically a variable, and the two is actually a value. So here a is called the variable and two is called value. So that's the meaning of the variables and the value.

So what are the values and the look into the data type? And there are some properties like the data type. Type of variables and values are same. So since I'm assigning some value to this variable, hence both share the same data type. So you can print it now and if at all, if you print the eight and you'll get the same value as that was there, what are the value that was assigned to this particular value is what we can get. We can assign the multiple.

We can also assign the multiple variables to the multiple values. So let's see like in assigning the multiple variables. So, for example, x comma y is what the two variables I want to assign. And we can use the two values, let's say one or two, so we can also use this unpacking to assign the multiple variables. So let's execute, let's print X and let's print Y so that we can see the one and two respectively. So those kind of variables and we can assign some kind of values to this variable and would also look in the data type.

And by just looking to the type is what the key word. And you can check the data type and basically two is basically an integer. At the same time, it also shows the same kind of variable here and type of a is also an integer because a two that is assigned to the available. And so the data, they are also shared the same kind of data type. So this is basically variables and assignment, and basically assignment are this process this process is called assignment.

Assigning a value to a variable is called assignment.

8. Data Types
=============



Hey, everyone, welcome back. Now let's look into the data types so there are different kinds of data types that Python is going to be support. Let's try the data types you did a times. So there are different kinds of data that Python is going to support. The first one is integers. So we already saw integers are basically represented by int, and we also support the float values, and it also supports strings and boolean. So this and all the data types that is being supported by the python.

And finally there is the non null values is basically defined by the null values also known as None. So there's another data that's basically the python is being supported. So let's look into one by one into the data types of what it's going to be happen here. So if at all, this is basically those are basically some values or discrete values, something like one, two, three, four, five, six, something like 70 or so. It can also look into the type of two is basically it is int.

So this is basically represented by int. OK, and the float values will going to be presented by the float. And the type of two point three is basically a float values and if you want a string, type of 'data science' is basically a string; 'data space science' is also a string. And of course, we are having boolean, and the boolean is basically represented by either True or False. bool basically represents the type of True.

True is basically the true for the positive and the false is basically the negative response. So type of False is also a boolean value. And null values can be represented by None. So none is basically represented by the null values. So you can see this is NoneType; this data type indicates that no value is being assigned or something. So none is basically the null values.

9. Data Type Casting
====================

See the code [here](./1.ipynb)

So we can also use this python for the typecasting, for typecasting, so typecasting means we can also convert the values from integer to float and float to integer, and we can also convert integers into string, and string to integers. We can also convert float to string, and we can also convert that into a string to float. So this and all the things we can easily convert that typecasting. We can change the type, for example, for example, I'm having of value or I'm having the integer 2.

And I just want to convert that to into the float values. For example, here, let me assign the value be variable B is equal to two. And the data type of that is integer. I just want to convert that data type integer into the float. And we could also use the kind of typecasting like int to float. This is basically I'm converting to into the float and we can use a keyword called float will basically convert that values integer into the float values and you can see that it will convert a string or number into the float numbers.

So either like if at all, you want to convert that and that if the data type is a string or integer, we can use this into converting that into the float values. So now let's see here so we can see that I can easily convert that into the float values. Basically b is an integer. Now I just converted into the float values using float. So let me assigned to the variable C. Now this is my C and you can also look into the data type of C type of C is basically the float values, but this is how we can able to convert integers into float and float into integer values.

And obviously, we can even we can also convert that the string values, for example, since we can also convert the string values, for example, '2.5'. And if at all, [unclear] 2.5. And if at all, I just want to convert is basically the time to the type of that is basically the string here. And I just want to convert that string into float. And you're going to simply use this float of the will basically convert that into the float values.

So let me look into the data type of this so we can see now I just able to convert that into the floor values using a simple command float. All right, so now this is how we can able to convert that Intissar or string into the float values. Now let's see how to convert that float and string into integers, so let's see this the similarly dislike the float for integers we have int, which will basically convert string or float values into integers, for example.

This is my 2.5, is basically the float values, and if I pass it to the int function, it will convert that into the into the value. And similarly, you can only put all you want to give any kind of a string's something like this, and if at all, I just want to run this again, it seems like, OK, [unclear] probably we need to give the exact number. So this is what the string value and if at all, you can execute this and I can easily convert that into the.

integer. Similarly, if you want to convert float or int to string, we can use the following command: str basically converts either the float or the integer into string values. For example, str of 2.5, and you can see now it will be converted back into the string values using this command, and you can see that it is converted into the string. But this is what the python will also allows you thus typecasting and where you can able to easily convert that types into one day to type into another data type.

Thank you very much. We'll continue in the next lecture.

10. List
========

See the code [here](./1.ipynb)

Hello, everyone. Welcome back. In this lecture, we will talk about the data structure, data structure and any programming language that plays a very important role. So let's see some data structures and the python. So we'll start with the list. List is basically a collection of elements. Less can be defined as the collection of. a collection of elements with different data types, and basically mutable, so we are able to change, we can remove the values in, set the values and we can change the values and the list.

So that's basically the meaning of mutable. So and it is a collection of different data types. And it could be boolean values, string and float values, and everything can be how in the last year. So in order to create a list, we can able to create a list using the square braces. So let's define a list. And my list is. Do we can define the list using this list? And we can create a list simply like consist of the different types and could be the again, define the float values.

I can define the string data and the science and even I can give the boolean values False, True. And even I can use some kind of data type like a number, so it can be anything that is worthy. That is what this list is, basically the collection of elements and the sum of all the elements. Each and every element could be a of data or it could be a data structure itself too. But that's what basically this is. How we can define a list is basically the collection of elements and with different data types, it's possible we can also do the different types.

And finally, the list is basically ordered. So let me execute this list. And my goal in my list is basically this is what you can see here, and this is where basically we have one, two, three. What are you order to define and same order. We can also get here when it comes. Look at the data type of that type of. My list is basically the form of list. Right. So this is how you can simply create a list. Now, let's look into the slicing and index or indexing operation and list slicing or indexing is a way of selecting the elements.

For example, consider my list. And in this list, I just want to extract the first element, basically the indexing operations in the list. It starts from zero. All right, and this is of the list we have created, and as you can see, we have a list like one two one one five six datastream science. What's true? And so this is what we have and the list and the indexing of any data structure in the Python stats. So basically, this is index number zero, and this is index number one, and this is index number two.

Index number three, four. Why? Six. And so this is what the indexing or the position numbers of the following elements in this list, in fact, all you want to extract the first element here. So what do you have to call here? For example, in this case, we have the my list here in my list is equal to this. And what they do here is that I need to call something like the variable my list. And because variable, I need to pass the index number. So here I need to pass the index number.

So if at all about the possible zero. And what I'm getting here is that basically this is going to return to the one. So that's where the indexing position or the slicing or indexing what we can do with what we want to extract, we can extract with the following statement. All right, so now let's see how they expect the first element, so extracting the first element and you can see my list of zero, and that's going to be like the first element. And similarly, give it all you want to extract the two here, you need to pass one.

So because this is a zero and this is one, and if you pass the one here and that's going to be fine with two. And similarly, if at all you want to extract the signs, you it zero one, two, three, four. And if you just take my list and in the place of those square braces, if you pass for and what you'll get is science. So that's what the basically the positions and the positions of each and every element. We can also define the index in another way, for example, here you can see there are eight elements of the one, two, three, four, five, six, seven, eight.

So there are eight elements of those. So the length of that mine list. Is going to be equal to eight, so there are eight elements out there and we can define this element could be like length of. This could be the length of my list. And minus one is is basically the seventh element, basically the same length of minus one length of my list and is basically the length of my list is eight and minus one. And what you get is seven. Similarly, you can define something like length of my list minus two, [unclear]. What you get this similarly if you assign minus one to it, instead of giving the length of my list of minus one, I can simply understand that if you can figure the minus one and it's nearly equal to the calculations of length of my list. And what you can get here is that minus one and which will basically return you the seventh element of the seventh index position. And minus two is this and this is also minus three and this is minus four and it is fine and minus six and this is minus seven and minus eight.

So instead of giving the indexing something like conventionally like zero, one, two, three, and you can also give the index something like this. So minus eight will basically define this position. Minus seven will define this position, minus six will define this position and so on. All right, so now let's see my list of minus one. Basically, it's going to return the None value, so we are not able to print it. So that's why I got this. For example, if you the list of minus two and what you'll get here is the value.

So that is how indexing and the indexing position is basically the can minus one minus to the python by the politics of the length of my list and minus one. So in order to get the length of that end, len is one of the commands. len is the keyword, which would actually calculate the length of my list. So length of my list is basically gives you the eight. So it's basically like what is the length of the elements that goes there in the list?

So this is how we can easily extract a single element and let's. Let's see now the multiple elements. In order to extract the multiple elements, for example, I want to extract one and two and this is what basically I want to extract here in order to extract the multiple elements, we can also use the same procedure list. For example, in this list, I just want to extract one and two. In order to extract that, I can view the starting value so the syntax could be the start and end.

So this is what I begin. So I need to start with zero. This is what the zero position and I wanted to end with, though I need to end with this one. So I need to start with zero and I need to end with the two. Basically, you might think like I need to end with one, but internally it's going to be calculate the length. So basically the number of elements that are going to be extracted is end minus start. So I could do like, you know, if it would end and is equal to one.

And what I'm getting here is that it is equal to one here and the state is equal to zero. So the number of elements that are going to be extracted is just what you want. Instead, if you give like a no and is equal to the number of things that is being the X Factor is OK. So now let's do this index like this. If we start with this and you can see we're able to extract the two positions. Well, that's what we can simply do with the multiple elements and indexing.

So just a reminder, like you just give the one extra indexing position so that you can extract this particular point. For example, now I just do some indexing, like extracting. First, five elements. And the list, so you can extract the first five elements of the list by just simply taking the starting value is zero and adding value a six. So the end value is basically five, so that we can extract them, because end minus start is basically equal to five, so they can extract those five values one, two, three, four and five.

And you can also extract something different, like extracting the first three elements, starting from index two. Starting from index two, I just want to extract the first three elements. So first, starting from this one, this one. This one three. And so I just want to extract this so that the one one five six and sign is what I just want to extract here.

So in order to do that, my list, and the starting index is two, and I just want three elements, so two colon two plus three, which is five, in order to extract those values. So this is how we can do the slicing. So this is what is basically the idea of slicing where you can slice. That way you can able to slice the list of values so that you can conveniently you can able to extract the one of the values you want. So let me break my list, you know, I just want to print the values, for example, at one point one by six and the signs two and so on, that is what I just want to thank you to, for example, alternate elements

of the list. In order to do that, we can simply use this mind of my list and you can see here is that standing is basically zero and the ending is basically the length of len of my list. And one more colon I can do here, is basically defined the step so I can define the step here. So step is two. What it takes is like like know starting from starting from zero zero plus two and just keep on repeating that way. So this is zero. Let's do this and let's do these four and let's do six.

And like this we can able to that, for example, if you like this and it is going to be extracted the bring the other elements. So so that's what we can use this step and the step argument. So basically this step will define the what is the step. I need to follow the. So similarly, you can also give the every third element, every element in the list, is also just the step is three. And so we can define something like three elements, like an old one.

And just of this. And I the third element is true and so on. But this is how is basically we can also do the slicing of the multiple elements. And finally, we can also print every index, each and every element of my list, in the reverse order. so my list considered on my list, too. And if at all, I just want to put this in reverse order and I can use this command so that we can simply get that, for example, minus and point to started with.

I need to start with the index position eight, colon, and if I put one more colon [unclear]. And so because the element is also there and out that followed by minus one basically goes in such a way like eight. This is the eight minus one and it's going to go to the first one of the eight and minus one is seven and so on is what we're really going to get in the result.

So this is all we can able to bring the elements and was the. So let's put it all together. So basically what it actually indicates, like a colon is basically print all the values, and double colon will also print all of the values, and we can have like a. two colon. I can now print all the values starting from index two, zero one two, so including 1.56, all the values. And suppose I just want to print the first five values.

And I can do something like colon five. It basically understands that the start is zero, [unclear] first five values. And similarly, we can also use this to to print the alternate values. And finally, colon colon minus one is what prints all the values in the reverse order. So this is more of a summary of the indexing and the slicing and indexing concept is really very much required particularly when you are doing the data preparation.

And this kind of slicing is quite useful, quite useful. Thank you very much. Continue in the next lecture.

11. List Methods
================

See the code [here](./1.ipynb)

Hello, everyone. Welcome back. In this lecture, we will see some methods in the list, if at all, you consider this my list dot, and if you press tab, and you can see that on the list of methods that we can be used and the my list and it's you can see that it's append, which will basically append the values to the list, and clear, copy, extend, and remove. So to sum all the methods that was available and the list. So let's look into this one by one about the methods and the list, for example, append. append will try to append elements.

And so if at all you can see here, it will try to append an object, and which will be at the end of the list, for example, I'm going to append something like A, B, C, but this is what an element and the element is. A string is what I just want to append to the list. And if at all, if you just print the list and if you can see there is previously this is what the list previously. This is what the which we are having with me, and after that, I just appended a single element and single value into the single object, into the list.

So if at all, we can use my list dot append. And let's see, I just want to use ABC, comma, ABC, ABC. Let's at this time take like an ABC, the F, something like this. So I just want to add the two elements into this and what happens. You can see the list, if at all, your friend of my list, it's not going to be at the multiple elements. So basically it's basically trying to append this, taking as a single object. This list itself becomes a single object.

So this kind of representation is called a nested list. If you want to insert multiple elements into the list, there is one more functionality that is called extend. So this is extend, and you can also use this extend and just view the elements here. Let's add the and I just I just want to insert so these two elements in the list. You can execute this particular statement and let me put it here. So this time my let's come back and let me plan here.

Now, you can see this is going to be extended here instead of instead of taking this as a single element. And this is what going to be taken as the multiple elements. And individually, it's going to be appending those values to the list. That's the basic difference between append and extend. And similarly, you can also look into the different kinds of things like count and count, basically just count the how many times that object is being appeared in the list, for example.

Let me take the ABC. How many times the ABC is being appeared on the list? It says that it is one. And similarly, let's say let me count one more thing like an eight. Basically, that is not there. And the zero. So that's what we simply do to understand and how we basically used all it simply took and usually use this kind of things, I recommend do follow the documentation of the list so that you can understand each and every method you can use on the list.

OK, so let me finally go with insert. insert will basically try to insert any value into, for example. This is what my list is having with me and my list. And let me bring this let me bring this my list here. And I just want to insert an element between two and fifty three point one by six means in the index position two. I just want to insert an element, something like [unclear]. OK, let me use that like in my left and then this case, I'll use the insert and suppose in the index number, the first thing is index number two, what index we want instead.

And let's say just the index number two. I just want to insert a number nine and now exude this. I can see the print, my list and immediately I could do and between the two and you can find the nine is being here. That's what you can see once you execute here. OK, I executed this twice because of that. I got this. They can see the nine element is being inserted in my case. All right, so we can also look into different things like pop. pop basically tries to remove the object.

The default value index is minus one. So basically, if you just pop, it removes [unclear]. And let me print this, my list. And what happens is remove the last element and by default, these last element. Instead, you can also remove what are the element you want. For example, I just want to remove this zero one, two, three. The third element is the nine. I just want to remove and if at all, I just want to remove just the index number. And here in the index number three and does nine is going to be removed in this case.

Now let's find my list. My list and what happens, that particular line is being removed in this case. OK, this is all about the indexing and also the methods in list. Thank you very much. We'll continue in the next lecture.

12. Tuple
=========

See the code [here](./1.ipynb)

Hello, everyone. Welcome back. In this lecture, we will talk about tuples. Tuples are also similar to the list, also a collection of data with different data types. But the one difference between the tuple and the list is that tuples are immutable, means we can't insert, we can't delete and we can't update the values in the tuples. So let's see how to define a tuple. We can define a tuple with the curved braces, parentheses, so we can define the tuple as a collection of different data types.

And we have the string float and also we can also have some kind of a float values and boolean values and etc. so we can have all kinds of data types that was there in the tuple. And this is what the indexing of the tuple is also very much similar. For example, if in order to extract the first element of the element, so take my tuple of zero to get it. And similarly, in order to get the last element, we can take minus one. And you can also do the slicing like my tuple.

And first, let's say, if you want the first values, then colon three will give you the first values. For example, if you want to get the last values, then we can take this minus the column and we'll get the last two values and also print the values in the reverse order, colon colon minus one. So indexing is much more similar to the list, which was discussed in the previous section. So all index things are much more similar to the list.

Let's look into the methods. So actually there are not many methods out there. And the tuples, because the tuples are immutable, because tuples are immutable, there are not much better. So there, but still they can look into the tuple's methods. Only we have. The count means we can count how many times that element was there. And at the same time we can also find out the index position, for example, count. So let's say I want to count how many times the five point five is there.

It's only one. And let's say I just want to get the index prediction of all of the one. And I can take like, no, this is more an explanation of the one is basically it's a zero. So that's what is going to be written here. So that's what the index prediction of one. So only two methods are there in my tuple or in tuples and the rest only because like tuples are immutable. We can't insert. We can do it, we can't append, but we can do the appending of the tuple by using a simple concatenate operator, for example, my tuple, and I just want to append multiple values, let's say I just want to happen here.

something like nine comma ten. I can create one more tuple, nine comma ten, and use this concatenate operator, plus, so that we can append those values. Plus, again, see, this is my tuple, and I can use the concatenating operator plus to extend the tuple. So that's what we can simply do the table here. And similarly, let's look into the casting so we can also we can also change those typecasting with the tuple. Let's say my tuple, this is my tuple.

And the data type of my tuple is tuple. So we can also change this data type from tuple to list. And for that we can use list. And list of my tuple will basically convert that into a list so they can see we can simply we can simply convert that tuple into list using the of the command called a list so that we can see this is how we can simply convert and look into the type of the type of my list. And what we can see here is the list.

And similarly, we can also convert that, let's let's say to tuple using tuple. tuple is there, so we can use this tuple. So to convert that list is tuple, let's say my list, into my tuple one. And you can simply convert that any list into tuples using this operator. OK, so my tuple one, and we can see this is what convert it back into a tuple. And let's look at the data type of that, my tuple one, and that's going to be tuple. OK, so this is what the indexing and also the method that was there and also the type conversions of the data type and the tuple, tuple to list as well as list to tuple, because this is about the tuples will continue in the next lecture.

More on Python. Thank you very much.

13. Sets
========

See the code [here](./1.ipynb)

Hey, guys, welcome back. In this lecture, we'll talk about one more data structure, sets. Sets are also a collection of elements with different types, and one of the properties of sets is there are no duplicate elements that are present inside the sets. So we can create a set my set. You can create a set with a simple curly braces, so basically sets in the side. There is no duplicate elements would be there. So, for example, if I could add one more one, there are basically one duplicate element there and five, five, three.

And you can have the plot values and you can how you can also have you can also have strings, so 'data', and also boolean values. OK, we have some boolean values, so let's print my set. So this is my set, and just try to remember that there is no proper order and the order might be different. What are the words that order you created may not be the same order? Which order is there? It might follow something like they're in alphabetical wise and also in the ascending order.

OK, but that's how we can create that. That's what we can create a set here. It's very simple. And we can also do some method to the set like. Can also have some items in the set like intersection, union, addition and subtraction, for example, we can do the same, but we create one more set, create one, we'll set a B and in this set B, let me create one and three and data. So this is what the set B, that's what I'm going to create here. All right. So now I just want to perform some intersection operation.

So basically A Intersection B. Intersection, we will actually give you the retinue of common elements, so that's also that's the kind of operations we can do in sets. For example, my set DOT intersection, and we will basically give the intersection between this and all the common elements, one tree and data or just common element in the set and also in B. So that's the intersection. And we can also do the union operation, A union B: my set dot union, we can have the union operation with B. [unclear] So that's, that's why I like in all the elements of all of it, was to be also present in a home so they can also do the subtraction. We can also do the subtraction, my set dot difference, or [unclear], and difference with B basically it will remove those elements. For example, you can the set here one one one three five five one five. This is what the set is.

And if I do the A set minus B, it will remove the values one three and data. That's what we can do so he can see here. So this is what the operations. And so there are many, many operations that was then. And I prefer to look into the documentation so that you can do all the operations you want. So this is what basically the set. And the next lecture will talk more about the python.

14. Dictionaries
================

See the code [here](./1.ipynb)

Hey, guys, welcome back. Now we will see the most important data structure in Python dictionaries dictionaries is also similar to the list. But here we will store the values in key and Value-Based means for each and every value auditor, for each and every element. We are assigning the key to it so we can create a dictionary with curly braces, just like a set. Now let's see how to create a dictionary. We can create a dictionary, my dict equal to, and with the curly braces we can create a dictionary.

So for that the first one, it should be a key. You should assign a key, followed by a value. I can assign a value is could be any value, something like this. Of course, the value I will assign is either one or two or four. So this is like this and you're going to create one or the other. How you can create a number of keys you want. Let's say this is the key and this is the key one. And you define the key and the colon and for a value, the one calamity.

And it's that to it, too. So let's print the middle. Now, you can see this is the key and the value. So let me create a dictionary. So what I'll do here is that I will create a dictionary stating that name the keys or the name and the course name something like the code name and. But this could be the topic, the area, the area. What is the coast, the area in which the course is depends upon could be the data science or something like this. So you can create like this.

So let me create the code, something like this, and we can create the dictionary, something like name, and then I can give my name, it is Sriram, and the course name I can give, something like this course. And let's say the code name is the Python programming and the AM. What I am going to teach here is in the field of data science, the area it was in the data science, something I can create data science. OK, so this is how we're going to create a simple dictionary and now you can see here.

So name is Sriram, course is this. And the one thing we need to understand here is that dictionaries are unordered. And if you want to extract only the keys, we can take my dict dot keys, and keys are basically all the keys, which we are calling. So my dict dot keys. You can see you getting only the keys here. Similarly, if at all, you want to get the values and you can take the values. my dict dot values, so that you can get the values so that something like this and similarly you can look into the some kind of suppose I just want to call the I just want to call I just want the name, Sriram.

I just want to extract this. So just like the number, I also just like the lists and tuples, so we can pass the index here, the index here is going to become the key. So you pass the key here. The key here is name and if at all it was a name and I can get the what of the value inside that I can extract from this. And similarly, if at all, if I give the code name, I can get the value assigned to the particular class name. And similarly, you have like many methods out there like that.

So what is this means like an all you can get the value assigned to that particular key, for example, if at all. You want the area and just parse the area here, get and return you the value added so you can also use this method or else I can also use this method, too. So let's see one more. One more one more thing, dict.items. So items is basically we're going to return the pair. It is going to return the key and value. It was going to give them the key.

This is the key. And this is the value. This is the key. And this is the value. So it's going to return you in the key and value pair with the list. And whereas the key and value will be in the tuples. And similarly, you can see some of the things like pop, which will basically remove; update and values. update is a special thing. So updating it all you want to add one more key value pair are if at all, you want to delete or you want to update. Let's say I just want to update the name Sriram with the name John.

Let's say that is that is what I just want to update that. So if at all, you want to update that so we can use this update and specify what is a key and want to update here is name. And I just want to replace this Sriram with John. So let's execute it. Now let's look into my dict; you can see here the my name is replaced with the name is replaced with this John. And update can also be used in some of the different ways where you can also add a new key value pair.

Also, it is possible here. OK, so let's see. I just want to also include some country information of the particular thing. So if at all, I want to include the country. I can also use this one more key country. And the country here is India is what the country I want to add here. Now, you can print my dict, and I can see here one more key value pair is added, as country is India, does something like that. So this is what the idea of the dictionaries and it is much more powerful way of representation of the.

This dictionary is also used to create the tables like data frames, so that internally how all the tables was there is entirely still in the dictionary. So let's see how to create to create a table with the dictionaries. OK, let's see that. OK, let me use the hash. Now let me create a table, let's say I just want to create my dict table. I just I'm having like an all the number of keys. Let's say the name I'm having in the name. I can create the list.

OK, let's say the list could be the first one. It is Sriram, and the second one could be John. And third, that could be, let's say, Adam. The third one is Adam. Now let's see the courses they purchased: let's say Sriram's course is Python, and John purchased the course data science, and Adam, the deep learning one. This is what he purchased.

OK, and now let's say I just want to add one more one more key here. Let's say what is a country they are staying in country information. OK, so I can see the country here is let's say Sriram is from India, and John is from the USA, and Adam is from the United Kingdom, UK. And so. OK, so that's what I'm having some information here. So now you can see here my dict. So this is my dict, and what we can see here, this is the names out of the keys, whatever we have the keys, this keys you can represent with the columns and what the values are there that you can represent with the rows.

So there is a convenient way to convert that into the tables. So we're looking later into pandas, what it is and all. So at the moment, just import pandas. pandas is also known as panel datasets. Very, very powerful. Very, very powerful library, particularly used for the data analysis. Right, so now let's create a data frame here, so tables in pandas we call data frames. So what you need to do here is pass the data, and the data is my dict.

And and if we execute that now, you can see you have created the table here. The name is Sriram, John Adam, and of course, is Python Data Science and Deep Learning and the country is this so just like this is the dictionary is the raw information. But internally, each and every dictionary is basically the representation of the tables. All right. So this is about the dictionaries in the next lecture will continue. More about Python. Thank you very much.

15. in operator
===============

See the code [here](./1.ipynb)

Hey, guys, welcome back. In this lecture, we will talk about some basic operators. The in operator is basically used to generate boolean values, and particularly used for the conditional statements. So, for example, let me create my list. And in this list, let me create some of the list of values like Tom, Nick and John. OK, let me create John and Sri. Let me take one more, Sara, something like that, so this on the list of names that was there with me.

Now I just want to check, like, is Sri there in the list or not? That is what I want to check here, for example, in order to check that what we can use here and I can use 'Sri' in my list, and it basically returns boolean values. If that value is present in the list or if that element is present in my list, then it will return. True, otherwise it will return false. In this case, Sri is present in my list, so it should return True.

So for example, let me do one more thing. Is 'ABC' in the list? If you want to check that, you can use the in operator, and obviously 'ABC' it's not there in the list. So this is what one of the basic operator and definitely used in the many, many applications like the conditional statements. And it is not only in this case, which we can also use. This is useful in many cases, to even and the text to even that string or even the string to for example, let me take a word.

Let me take a word, something like 'little'. Or let me take a string like 'little hearts'. OK, so this is the string. I just want to know: is the letter 'a' present in the word or not? I can use a simple in operator, like 'a' in word, and it returns that there is no letter 'a'. For example, let me use the letter 't': 't' in word. Yes, the 't' is there in this word. So that is how this in operator will be used to check whether that particular string or maybe that particular element is there in the list or tuples or any other things so that it is very useful

operator in conditional statements. Thank you very much. We'll continue in the next lecture.

16. concatenate & repeat operator
=================================

See the code [here](./1.ipynb)

Hello, everyone, welcome back. Now we are going to see one more operator, which is the plus operator, also known as concatenation. And also we will see the star operator, the multiplication operator, which basically used to repeat the elements. For example, let me create we let's see. We already have the list. My list is already there with me. And the plus operator is basically used to concatenate. for example, in my list, I'm having Tom, John, Sri and Sara. And I just want to add a few more elements into this.

For example, let's say one, two, three, four. And I just want to extend this so I can simply use this plus operator to extend it. So if at all, if you execute this, I can see that Tom, John, Sri, and the new elements. I created a new list, and I can name it my list one. And in my list one, I'm having all the elements. So I can use this concatenating operator to join lists, or to join tuples, to join even strings too. for example, let's say data and science, let's say, if at all, you can use a data science here and what is going to do here is that it's trying to joining the two strings.

So that's what the one of the useful operator is. The operator is basically used to join or to do the concatenating. And there is one more operator called the star. It will basically repeat it. It's basically repeat the operation. For example, I'm having my list with me, and this is the star operator, for example, having my list with me. And if at all, if I multiply this by three and what is happens is that like, you know, the list is being repeated three times.

That's what it's trying to do. So let's print it. I can see Tom, Nick, John, Sri, again, [unclear]. And again, it is being repeated. So that's what life say let's save it all. You want to repeat it for two times and I can simply do this. And to do it can simply do that. And of course, we can also we can also multiply this with the with the string to and it is being repeated is what this so this is what a very useful operator the plus operator is basically trying to concatenate, and the repeat operator, the star, will try to repeat lists and tuples, and even apply to the strings.

So this is what the basic operators generally used in the python. Thank you very much. We'll continue in the next lecture.

17. User Defined Functions
==========================

See the code [here](./1.ipynb)

Hello, everyone, welcome back. In this lecture, we will talk about user defined function, user defined functions is very, very useful methods and which is very useful to run the sort of set of lines or sort of statements repeatedly. So let's use the different functions so you can create a user defined function. something like def; def is the keyword that you use, and you've got to give the function name and set of arguments. And what are the input that is going to pass us to the function called the arguments.

And then you have a set of statements that you need to execute and after that you have the return value. If you don't give the return value, it will return None. OK, so let's see. Let's create how to create a simple user defined function. For example, here I just creating a simple user defined function. Say something like hello. So some something like say what are the things you want. For example, let me say say hello and I'll what I'll do here is that I'll print.

Hello. OK, so this is how I can create a simple user defined function. So what is this here? You can see here that def stands for user defined functions, and this is the function name, and we need to open the parentheses and within that we need to pass. What are the arguments you want and you should end with the colon. [unclear] You are inside the user defined function. So this colon states that you are in the block.

And one more thing we need to maintain here is this one tab space, called indentation. So this is all they need to maintain. And this is called indentation. And then an indentation. So this means that indentation indicates that you are in the loop. Suppose if if at all, you are outside of this, let's say this is the outside of the loop, for example, if at all. What are the statements you are in the indentation or within this function and whatever you are outside, this is basically this is out of indentation says that it is out of the loop, something like this or out of this indentation.

Let's say if I execute that, is that like you are out of the loop, but this is inside the loop. So now let's execute this function or let's call the function. And this is a way of calling calling the function. And if at all you call the function, it says that although like because inside that I create. Hello. Let me extend this function, say hello, to say hello to someone. Say hello to who? Let me give one argument, name. And now let me make an indentation and in the print some.

Hello, now I will what I'll do here is that inside, let's say this is a percent s, and I will insert the name. Say hello to the name. OK, that's it. So now let's see here. Say hello to now. Press shift tab; it shows that it asks you for the name. And let's say I give the name to, let's say John, something like this and say hello, John. And you can do whatever you want. like saying hello, John. Let's say hello, John.

How are you? Something like this, something something like this, so say hello, something we can see. Hello, John, how are you? So what are the arguments you pass that is going to enter into this function? So that is what like a user defined function is how we can create it and also create the user defined functions to do some kind of operations, for example, creating a user defined function, creating user defined function. Function to create. Or to to add to values.

OK, so means that I need to pass the values and to return the output of it. So addition. OK, this is what the function of creating. And let's say I'm having the two values, a and b, two arguments. And inside what I will do is create the inside some operation c equals a plus b. Now I'll return c. That's it. So that's the return statement. If you remove this return, it will return None. But here I need to create the return here.

Now let me pass the addition of let's say one comma two, and what it is going to return to is going to return three. That's what it is. So you can create what other statement you want, what other things you want, you can simply create in the user defined function. So what we have to do is that there are sort of statements that is going to be there and you need to execute the set of statements. So I can also create. One more function of identifying even or odd numbers. Identify even or odd number: def find,

def find even or odd. OK, in order to identify an even or odd number, [unclear]. So how do we identify that? We have some kind of operation like percent, which will basically give you the remainder. And if we divide, if we divide two by two and what you'll get it is you will get maybe two by two, and the quotient is one, and for example. So the quotient is basically is going to be equal to one. And here we are interested in the remainder. If the remainder is equal to zero, it means that that particular value is divisible by two, and it's an even number.

So you can see two divisible by two is obviously even; let's say if it's 16, 16 percent 2. And what it is basically is it is divisible by two because the remainder is zero. And for example, if I take 15 and the remainder is one, that is the meaning of the percent, this modulo. Let me read the logic here. So def find even, and let's say you pass some number. And now what you can see here is that I can return number percent two equals zero, and that's it. Now, finally, let's say find even of five, [unclear].

[unclear] You can also do the conditional statement like equals zero. And find even of five: it is not even, five is not even. Let's say if it goes to the number one hundred ninety [unclear], if it is even then it is True. OK. So this is how we can create simple user defined functions. So in upcoming lectures we will see more on user defined functions, so we can use how exactly this user defined functions and probably in the upcoming lectures.

Thank you very much. We'll continue in the next lecture.

18. Control Statements (if else)
================================

See the code [here](./1.ipynb)

Hello, everyone. Welcome back. In this lecture, we will talk about the control flow statements, that is if, else and elif. So basically, if-else are the control flow statements. The syntax of if-else should be something like this: if, followed by a condition. And if this condition satisfies and will execute the following statements, let's say that if this condition fails, then we will go into will ask one more statement, one more condition, elif condition one, and we will execute the following statements.

OK, so that's what we'll keep on repeating the statements. And finally, if all the statement is not valid, then we are going into the else, and if all the conditions are not satisfied, then we will execute the else statement. OK, this is basically if-else, how the control flow statements will be. For example, what I want to do here is, I just want to write a program: there are two numbers, a and b, and if a is greater than b, then I need to print something like a is greater than b, else

I need to print b is greater than a. that's what this is. What or else like A less than B what are the things. This is what I just want to print using the control statements. So let's see, let me create some function f and we create different functionalities. There are two values there, a comma b, let's say a is equal to ten and b is equal to twenty, ten, twenty. And now I'm just doing some conditions: if a is greater than b, so the symbols are used for the greater than this one.

This is the greater than B and followed by the colon and now made an indentation exclude one of the following statement. I just want to print a is greater than b, so I can give some values: {} is greater than {}. OK, now I can use some format and just pass the values. So in this case a is equal to 10 and b is 20. So this statement is not valid, and it will go into the else statement, which says a is less than b. OK, {} is less than {}, and I can use the format a comma b, OK, with the statement.

It says 10 is less than 20. I can still improvise this. Let's say instead of manually inserting the values of a and b, let the user make the choice, so I can use statements like input, and I can use 'enter a value'. Something like this, and it seems like it's generated an input box, so it will not generate the results on its own. I can give it a value here, 10.

But the problem here is the data we are having: let's look at the type of that. If you look at the type of that, it's a string. Now we already know how to convert that into integer; I can convert it to integer values. And let me give this as a, and also this is the b. No, execute this following statement to execute this statement if it is better than being and be to something like this, not executed the statement.

Let me give, say, five and six. And it says, like five is less than six. OK, now let me execute it one more time to meet you. Five and five. It says five is less than five. That's not true because we that's not actually the two. I can we need to do something like it is greater than or equal to or I can give the one more statement, something like elif a equals equal to b, then print {} and {} are equal. OK, I can use the format here of the I can see I can do six and six.

It says six and six are equal, and 10 and five, it says 10 is greater than five. So this is how you can use a simple control flow statements in Python. So first to be able to execute the statement, the first condition and one condition. And [unclear] sorry, this is not if, this is elif, sorry. If you want to do multiple conditions you have to go for elif, of course, because it works in this case. So first take this and followed by this previous one is not correct, and this is how we need to do in this case.

So we have the different kinds of statements. Are there like in all different kinds of logical statements like a equals equal to b, which is basically equal to, and so a greater than or equal to b. That's correct. And a less than or equal to so that I can say like an all is equal to six. So let's are equal to this is less than or equal to. And that's false. And we have not equal is there is not equal to and not equal to: exclamation mark followed by equal to is what this.

And similarly if you remove the equal sign that is less than and agree to that. So this and all the logical statements which you can use to evaluate this any one, you can also use it like in the loop, saying that [unclear] as a basic in operator, it will also return True or False. All right. So this is all about the control flow statement. In the next lecture. We will continue more on Python. Thank you very much.

19. Range & Zip
===============

See the code [here](./1.ipynb)

Hey, guys, welcome back. In this lecture, we will talk about for loops. For loop is also one of the statements where basically we are going to repeat the statements any number of times. So before going to the for loops, So there are few sequence operators that we need to understand. The sequence operators. The first one is range. Range is a function used to generate the values and the particular range. And the second thing is also very useful to enumerate enumerate with a built in function which will generate the position number or index number.

And third one, zip is also very useful function in order to merge the two list or two tuples or something. So that's one of the useful operators that was useful and while doing the four loops of some of the cases. So let's look into one by one first and then pull more into the for loops. The first one is a range. The first one will talk about the range. Range operator is basically range; type range and press shift tab, and what you can see here is start, stop and step.

So what it says is: what is the value you just want to start with? And the stop is ten, and the step is equal to one. So this is that range is equal to zero to 10 and it will generate the numbers in between zero to 10 with the step of one zero, one, two, three and so, so on. OK, now let's look into the list of this range and what you can see here is that we generated the origin of the list of values between zero and nine.

It's not only in the particular range. We can also generate in any number of things you want. Let's say I want to generate the numbers between two hundred, one hundred to two hundred and the step of, let's say, five, which are divisible by five or something. So I can see over the step of five I can generate the values of the list of values you. OK. All right, so also they can also just similar to the indexing operation, start, stop and step. Let's say I want to generate the numbers between two hundred

and one hundred in reverse; then I can use a step of minus one. I can get all the list of values in the reverse order, like two hundred, one ninety nine, one ninety eight and so on. But this is what the range operator is, very useful operator and which we keep on using this. And the second one is the enumerate function with basically give you the index position. So we'll see that. And while doing in the next one we have is a zip that will basically merge and it will written and the list and let's see how the two list with me and let's see, I'm having the two list with me.

Let's look at zip. So, for example, having the two lists with me, my list one could be like data and science and maths, mathematics, and my list two, And let's say I just want to give something like this is my one and two and three and so on. So if at all, you can use a zip and zip off my list. So basically we can do the intervals. So for example, if I said the two, if at all, I want to zip these two lists, I can use zip of my list comma my list two.

And what we can see here is that zip and if at all you can convert that into the list of values. You can see this is actually from the value, something like the items, just like on the dictionaries. And you can see this is the list one and the index one and lists do index two. And so this is what the zip operator is also quite useful while using the for loops. So this and all the basic functions like range and zip.

20. For Loop
============

See the code [here](./1.ipynb)

Hello, everyone, welcome back. Now let's look into how to create for loops. Let's see the for loops. OK, so the syntax for a for loop is simple, like for, and we need to define like how many times that particular statement you have to repeat. So in order to do that, for I in range, I can use a range operator then the stating that I just want to indicate that. So it will generate the basically the list of values in the range of zero to 10. And now what I can do here is that I can execute the statement.

hello. So this is the statement I just want to execute. So here what happened is that for i in range, range is basically the function; the range function will generate the list of numbers in the between zero to nine. And that means that we get the length of the list. It'll be the ten. So we create some virtual list. Now we execute this statement. You can see here I'm executing this of the statement for ten times. You and I can also print the list here, for example, i comma.

And what is the index number? I can also even print that. Obviously, we know that the range of ten will generate the list of values from zero to nine. That is what we have like zero one, two, three, four, five, six. And of course, we can also use the range operator like one to 10 and the step equal to two. So basically our step equal to two basically gives the odd numbers, something like this. So one, two, three, four, five, something like this.

So this is what the very useful operator. So which we can able to generate the list of values. For example, I'm having one more list with me. I'm having one more list with me, my list three. Let's say the names could be like John and Sara, and one more, let's say Michael, and we have one more. OK, so I have this list of names there. A list of names is there with me and I just want to print one by one.

I just want to print with the for loop. Let's see how so we can use the simple operator for I in range and how many times I want to execute the statement is basically the length of my list right now. Anyway, if I print, I am getting all the index positions. So I can pick this list and I can dynamically change the value of indexing, I can get all the values here. So that's the trick. I can really, really do so that I can do in this case.

Let's say i comma; the zero index is John and one index is Sara and and so on. Instead of doing this for a loop like this and instead of taking the range and length, I can simply write something like for element in my list three, and I just print the value or the element here. Let's print the element even that also will be the same, just like this. So it's very simple, like an old saying that, John. And what it is going to be created here is that value. The first one is John, second one is Sara.

And so instead of dynamically changing the i here, you can directly pass the list. Even that will work. But here we don't get the index position. In order to get the index position, let's use enumerate, enumerate of my list three, and I can give the i here. So this will give you the index position, so I can see here, like enumerate basically will give you the generate the numbers list of numbers, something like this.

All right, so this is what the basic for loop operations, and which we can do and also we can also execute the statement and inside the loop, we can also add if-else and so on. So this is all about the basics. So thank you very much, will continue in the next lecture.

## 3. Numpy

1. Arrays
=========

See the code [here](./2.ipynb)

Hey, guys, welcome back. In this lecture, we will talk about numerical python, numerical python is one of the most useful library or packages that was used for data processing in order to pre-process in order for the data analysis. Numerical Python Library is very, very useful. And the skills that were required for the numerical python is very useful. So let's see some of the functionalities that was there in the numerical python. So in order to start with numerical python, we first import this NumPy library. NumPy is also known as numerical python, so first import numpy,

import numpy as np. I'm going to import one more library called Matplotlib. I'll use this Matplotlib library for the sake of visualizations for a few functionalities; I will use these visualizations to explain the functionalities. For that, I will use import matplotlib.pyplot as plt. Executed. As soon as I executed the command, this is what we got. What I'm doing here is that I'm importing NumPy with the variable np and importing pyplot with the variable plt.

So now what are the functionalities that was there? I can use np dot and all the functionalities that are available in numerical python. Now, let's start by creating an array. All right. The definition of an array is a collection of elements with similar data types. An array is basically the collection of elements could be a numbers float values or even could be the list of values that the data type should be almost similar. So that's what we need to be important in that it should be that.

It could be a collection of integers. It will be the collection of float values. It could be the collection of strings. So that's what basically we have to be understand and the data type. So let's see how to create an array so I can create an array with a simple list. Let me create a list of my list. And what I'm doing here is that I'm creating a list of integers with one, two, three, four, comma, five. But this and all the collection of this and all our having those similar data.

So what I can do here is that I can convert this list is an element or an object into an array. For that I can use the library, np dot array, and what it basically does is convert the objects into an array. So what I'll do here: now let me name it as a variable, arr. Now, let's print arr. As you can see here, I just converted the list, and you can also look into the data type of arr, which is numpy.ndarray, and it stands for n-dimensional array.

But this is how we can convert any object could be the list, could be the tuples into an array, and we can look into the data type that is inside that. For that, what we have is arr.dtype, which will actually give you the what is a data type inside the list. So you can see the data types and are the data. So remember one thing that here I'm giving you the list of values and which are integers. Suppose, for example, let me add one of the element and could be the float values.

Let me give you five point five. And what happens? NumPy will basically convert the rest of the values into the float, actually, the values, one, two, three, four, or the integers. But if I use if I add one more element, float values, what it basically do is that it will convert entirely to type into the float values. That's what the meaning of our orate is. Basically, the collection of similar data by the data type should be almost. Now, if you look into the data type, of course this is that number.

But if you look at the data inside that and what is going to be here is it is converted into the float values. All right, now let's see, let me create one more. We can also create something like this, np dot array; we can create an array, something like one, two, three, five. And. Instead of this, what I can do here is that let me give you a value, a A.B.C. Now, what happens with the 'ABC' is this: you can see the data type should be similar; here I inserted a string value here.

But these ones are of the type integer; if I convert that, what happens is that it is converted into string. So you should be extremely careful that what is a data type and all you have to understand here now, if at all, look into this arr dot dtype, what it shows is U21, which is basically the string format. So this is how we create an array. In the next lecture, we will talk more about the creation of arrays.

Thank you very much. We'll continue in the next lecture.

2. Shape, size, ndim
====================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. In the previous lecture, we talked about the one-dimensional array. Now let's see how to create the two-dimensional array. So, for example, we created the one dimensional array using one list. In order to create the two dimensional array, I need to create a nested list. Now let's see how to create a two by two array. So I can create a two by two array with the help of the list. Let me create a nested list. So I created a list whether the square braces and inside that, let me create the list.

And in that was having that one comma two, and outside that we create one list here, and let me name it three comma four. So this is what the next list with the two by two structure. So what is basically the entire thing is an area and what are the list we represented inside that it could be a row. This one, this is row one, and this is row two, and this is column one, and this would be column two. So if at all, if I convert that into an array, you can understand this.

So let me use np.array and let me convert that using this. Now, we can see here, let me name it arr2. And now let's print it. You can see that I created a simple two-dimensional array with having the two rows and two columns. This is row one, and this is row two, and this is column one, and this is my column two. This is how very easily I can create a two dimensional array. Here are a few methods: ndim, n dimension. So we have the ndim, shape, size and dtype.

So this one of the matter is a few methods which will actually look into the shape of an array and also the data type. So ndim will basically present the dimension of an array. So, for example, arr2 is basically two dimensional, and arr1 basically represents one dimensional. So let's see, arr1 dot ndim, and if I execute the statement, it says that it is one dimension. And let me just check the dimension of arr2.

It is basically two dimensional because it has rows and columns; arr2 dot ndim, and it basically returns the two dimensional. And if you look into the shape of that means how many rows and how many columns or how many elements are there, for example, if we have this one. So if at all, they want to take shape of that shape. And basically, it returns five, comma, nothing. so this indicates that it is a one dimensional and there are elements in that.

So that is the meaning of this. And I could check that arr2: this is two dimensional, And there are two rows and two columns, that's the meaning of this, the total there are four elements and in the end we have the two rows and two columns that the meaning of that. And if you want to look into the size, the what is the meaning of the sides will basically give you the product of rows and columns, are basically to give you the number of elements in it.

So let me check that arr dot size, is basically give you the number of elements. Number of elements in that obviously there are five elements in this that could take the size of this, and it returns four; basically there are four elements is one, two, three and four. There are total four elements of this. So that is what the meaning of that, whereas the shape will give you the what is the shape, how many rows and number of columns.

And this will return to the number of elements. So ndim will return you the number of dimensions; shape returns the number of rows and columns. And lastly, we have the dtype. We already saw dtype; it will tell us what the data type inside it is. And let me check arr2 dot dtype: the data type inside is int, int32. If you want the name, dtype dot name: int32 is the data type inside arr2.

This is my arr2. Thank you very much. We will continue in the next lecture.

3. Array Creation - arange
==========================

See the code [here](./2.ipynb)

Hello, everyone. Welcome back. In the previous lecture, we talked about how to create an array, and also we looked into the size, shape and type of an array. In this lecture, we will see a few methods that are used to create arrays. So there are other methods that are commonly used to create an array. The first one is np.array; this method we already saw in the previous lectures. And now let's see few other methods. Let's start with arange.

arange basically represents [unclear]. arange and range are different. So 'a' is basically array, and this represents the range of values. So let me create a range of values, np dot arange. And here you can see there is start, stop and step: start basically says what is the value I need to start with, and what is the value I need to stop at, And and what is a step or what is the interval that each and every value is equally spaced.

That's what we need to create here. So let me create an array. So my question is: create an array in the range zero to hundred, this is what I just want to create here. So in order to create a range of values in the range of zero to 100, all these values, if I want to create that, I can use this arange. So let's say zero. And this is the start value. And the stop value is hundred, and the step by default is one. And let me name it arr3.

Now let's print arr3. You can see here the start value is zero and the stop value is basically hundred. We don't get the value hundred, but we are going to get up to ninety-nine; the length of that is basically one hundred. So basically, it will give that one value. All right, so this is how you can create an array with using a range that we create one more you the range, but here instead of that, let me create every alternate values or every fifth value I want to create, starting from zero and four that I can use five.

So here, that is a step that means equal space is supposed to start at zero and zero. Fine is fine and plus five is ten and so on. But that's what basically you're trying to create using this. So let's see that. Now I can see here the first one is zero, and the step is five: zero, five, and five plus five is ten, and then plus five is fifteen, and so on. So this is how the values we can create in this way. We can also create in some different way, like I just want to create I just want to create a values in the between zero to zero.

So I need to start with. And why do we want to end with zero or something like one? That's what we want to do. It was actually a similar thing, just like we do. But here I need to stop the two hundred ninety nine, ninety eight and so on in order to create that. What I do here is that start is a hundred and stop is zero. And the special the, the actually the, the what that was due by the step, the step is basically used as an operator. So it will start with hundred, and hundred

minus one is ninety nine, and ninety nine minus one is ninety eight, and so on. That's what the step is. Keep on going here. So in every iteration it will step off minus one. Now that's what we are getting in this case. And if you print that, we start with a ninety nine, ninety eight, ninety five, maybe seven and so on. This is one of the one of the use and advantages of the array. It's totally in the specifications you want. You can also create this. So let me create one which is between let's say to 450 and so in the step of three and we can do that.

So let's say for one hundred and fifty and type of minus three, what I'll get here is a [unclear], but this is how we can able to get the values using a range. In the next lecture, we'll talk about another method of creating an array. Thank you very much.

4. linspace
===========

See the code [here](./2.ipynb)

Hello, everyone. Welcome back. In this lecture, we will talk about linspace. linspace is similar to arange, which will create the array in this particular range. So let's let's see how to use this linspace and create an array. So let me let me use np dot. And we've got arange; np.linspace is there, and what it is actually doing is that it has start, stop, and there is no step here. But instead we have something different called num. num indicates that is how many points you want between start and stop.

So by default, the number is 50. So let me create an array. Let me create the values between zero two hundred and let me create 50 values here. So basically NUM is equal to 50 and let me name it arr. And let me print this. And this is what you can see. As you can see, we got the 50 values between zero 200 and we have zero and also we have hundred. And in between that it will do the equally spaced between the zero two hundred so that we can have like all the 50 values.

You can go to specify the number of values you want. Let's say I want two hundred values between zero, two hundred and twenty calculate for you and give you the results. So this is how you can use this np.linspace to generate the list of values or array of values between the specified range. So this is one of the most useful and there is one more thing is there is that endpoint, by default. endpoint is True, means it asking you whether you want this end point or not, if at all.

If I specify endpoint is equal to False, And what to do is that it will ignore the final value or they will ignore the endpoint so that you can get the list of values or the array of values between the specific range and the number of points you have requested. So this is what linspace, and it's one of the most useful commands while dealing with arrays, or generating the sequence of numbers and in in the specific order. Thank you very much.

We will continue in the next lecture.

5. zeros & zeros_like
=====================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. Let's try to understand another method called zeros and zeros_like. zeros and zeros_like are very useful methods when you're initializing an array. Let's see how to create zeros: np dot zeros. And now what he can do here is that you can look into the shape, the shape will talk about, like what is the shape of the array of zeros you want. Let's say I want to create a five by five zero matrix, and you can create a zero matrix, something like this.

So zero matched is generally the zero matrix and you can create the five by five zero matrix using. This is very simple and this is very, very simple technique and which will able to create zero matrix, something like this. But this is really, really useful when whenever you want to create the number of zeros, if at all you want, it will automatically create the zeros as a. And there is another method, called zeros_like, very useful, just like the zeros.

It's also very useful. For example, you don't need to specify the shape and you are getting the automatically. You are getting the shape in some of the way now or you want to capture the the shape of the array of some other matrix, then you can do it. For example, let me go up and create some two dimensionality. For example, this is a two dimensional array, which I created this. And I want to create a zeros like the shape that was there, the two dimensional it.

So let me go to my step here. And this is arr2, which is my two dimensional array. We're going to look into the shape of that and which is a two by two. So in order to specify the two by two here and if at all you don't need to specify something like this, then what you can do is that np dot zeros_like, and basically zeros_like with an array, let's say arr2, and it'll basically consider the shape you're going to look into the content of the shape of the what are the array we have and we'll create a zero matrix for you.

So let me say that one is equal to this. And since it is a two by two and will get the shape of two zeros off, two by two matrix, something like this. So this is a very useful technique in order to create a zeros. So this is all about zeros and zeros_like. In the next lecture we'll continue more on numerical python.

6. ones & ones_like
===================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. So in this lecture, we will talk about ones and ones_like. Just like in the previous lecture we have seen zeros and zeros_like, we will see ones and ones_like, which will basically create ones. Let's see how to create the ones matrix. So ones mat is basically equal to np dot ones, and what will basically create is the ones in the spaces in the specific shape. So let's looks like, you know, I just want to create a five if I want, and I can simply create the ones matrix, something like specifying the shape here.

So what I can see here, I can get the shape of the ones in the specific shape, one comma one, all ones here. And similarly, just like we have ones_like, we can create ones_like something like this. So what I can do here is that ones mat one: suppose I want to replicate the shape of arr2; then I can use this ones_like. So let me take ones_like, which will basically take the shape of arr2 and return the ones for you.

Something like this, and this is especially very, very useful whenever you want to do some kind of operations and for example, I just want all the values to be three. Then what we can do here is that I can take this ones matrix and just simply multiply by three, and you get all threes in the matrix. Basically, we are creating a scalar matrix, something like this. All right. So this is how we can use ones and ones_like.

And the next lecture will talk more about the numerical python. Thank you very much.

7. Random (Uniform & Gaussian Distribution)
===========================================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. In this lecture we'll talk about random and random generators, so this is very, very useful function. It is used in the many, many techniques. For example, if you want a group, if at all, you want to train the neural network in order to initialize the weights, we will use this random generator to initialize the weights. And at the same time, [unclear] indexing, and the same time for the data, we can use this random if all you want to do the random sampling technique and apply this at random.

So very, very useful technique for creating and also for splitting an array. So let's see how to do this random. So let's start with random. So to get the random here, I can use np dot random. And right now, there are different kinds of random generators out there, so we will see one by one. So let's start with the first one, the technique is randint. It will basically generate the list of values and a specific range. But example I want to generate the random numbers is between the low to high.

And I can use this np dot random dot randint, and this will actually generate uniform values. So let's see, let's generate the random numbers, let's say in the range of zero to one hundred. And I just want to generate the uniform distribution values, and the size of that. Let's say I want to generate a thousand random numbers. So let's see, like, no, let me name it arr1, is basically the array of random numbers and we generate a thousand random numbers.

And this one. Now, I can see that we we created an array between zero and one hundred, and the all the numbers, what are the generation is uniform. The uniform distribution is basically you getting the values in the uniform. Distribution means [unclear] every value has an equal chance of being selected. That's what the uniform distribution is about. So what I do here is that for the sake of simplicity, let me plot it. So I can use this Matplotlib.

So here, make sure you have already imported this matplotlib and using this matplotlib library, I can plot the histogram using that. So I like to use this histogram. So plt.hist, and I can use arr1. All right, so what we have is that I've generated the uniform distribution. Instead of this, what I can do here: basically here I need to select the number of bins, but we have one more

library, which is already installed with Anaconda, that is called Seaborn, and that will actually give you some kind of functionalities and it automatically calculates the number of bins.

So let me import seaborn as sns. And so I just want to use it just for the sake of visualization and let me generate the distribution plot using this. so the distribution and the values that I'm using for the distribution is a are one. So that's it. So let me plot it. Now, as you can see here, is that we got the uniform distribution, and we got some kind of a line; this is called kernel density estimation. In order to remove this, what I can use is kde equal to False.

All right, so. So this is what I'm getting here, I'm getting some warning here; it seems like this distplot is getting deprecated. distplot basically will get deprecated and may not be available in the future versions. And however, they have given you the new plot, and we can use histplot. histplot is basically the histogram, and which will give you the histogram and the number of bins you need to select the number of bins; it automatically creates the bins for you.

So this is how the big and simply able to plot and Seaborn is a very, very nice way of plotting [unclear]. So now let's see another method of generating the random numbers, so we already have the random numbers, but actually there are so many random numbers that we can use and this is basically called uniform random and is basically if you create a little bit, I don't hear it will create the uniform of random distribution, basically, that it will create the no random numbers and uniform distribution.

So we have the different kinds of distribution of generating the random numbers, so that's the one thing what we will do is that let me try to let me try to initialize the random function so that we can generate so many values we want. All right. So what we will do, we create a generator function. Let me create the generator function is np. random, the default generator. And with this, I can create a generator function, something like this. Now let me take this generator function dot.

And there are so many kinds of distributions out there: beta distribution, binomial distribution, chi-square, exponential, gamma, and so many kinds of distributions are there. So what we will do here is that let me try to explain you few distributions which are most widely used distribution. All right. So what we will do is let me start with the distribution called normal distribution. Normal distribution is also known as the Gaussian distribution, and where we need to specify the mean and also we need to specify the standard deviation.

So in order to generate the Gaussian distribution, let's say the variable is gauss, and this is the Gaussian distribution. And here we have the random normal. Here we have this normal, is there, so this will basically create the the random numbers in the normal distribution here, you need to specify the two things. One is loc and the second one is scale. loc is basically the mean, and the scale is basically the standard deviation. So let's say I just want to generate the random numbers that is in the form of the Gaussian distribution,

But the mean is equal to 10 and let's say at all one, the standard deviation and that is equal to scale. And the standard deviation is, let's say one, three, three and deviation. And you can generate this. So what I do here, for the sake of simplicity, I'm saying this is equal to 10 and standard deviation is three. So that is easy for you to understand. So let me take mine and let me say this is. Now you can generate the what are the range of numbers you want to specify the size and the size?

I just want to specify here is let's say I want to them random numbers. I want the thousand values is between in this particular range or ten thousand numbers. OK, so they can generate a number of range. You want that it will automatically generate that. And just remember, it is not uniform. It is not a uniform distribution, something like this. It is a Gaussian distribution. The random numbers, whatever you get here, is the Gaussian distribution, and the most of the values is being up to our mean and the standard deviation of three.

OK, but that's what basically we're trying to get here. So in order to visualize this, I can use sns dot histplot. I can use a histogram. And the data that I specify is. So now I can see it was nicely plot the histogram for you. So what I'll do here, I'll show it will basically give you the histogram and it's more or less looks like a normal distribution. So as you can see, the mean here, a standard and the standard deviation of three. And what you can understand is that within three times the standard deviation we have 99 percent; three standard deviations, three into three

That is equal to nine. So so in the range of nine. So from here to nine and from here to nine. So from ten minus nine is equal to one, and ten plus nine is equal to 19. So between one and 19, we're having 99 percent of values. That is what automatically we can able to see in this case. So it's a very, very useful function that is useful to generate the normal distribution values. In the next lecture, we will continue more on the random generator.

Thank you very much.

8. Poisson Random Distribution
==============================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. Now let's see how to do the Poisson distribution, or how to generate random Poisson distribution. Poisson distribution is particularly useful whenever you deal with the time. For example, this is what the point of distribution, which is what the probability of X is equal to K. K is basically the number of events and which is equal to lambda to the power of k, e to the power of minus lambda, by k factorial. So lambda is basically the mean occurrence of the particular event is happen in a specific environment.

So this kind of distribution is basically called the distribution is very, very useful whenever you're dealing with the time and and the mean occurrence in that particular time. And of course, the heterogeneity of the Poisson distribution follows the gamma distribution. So what we do here is that let's see the distribution for all values of K and all values of lambda. So let's look into that and let's see how to do the Poisson distribution. All right, so as we already did this generator here and let me have this generator function here and here, let me take this Poisson distribution.

So this is also the one of the most widely used. And there we have is that lam is there. And that lam basically specifies the mean occurrence of that. So what we can see here is that I can specify the lambda and lambda is basically the mean occurrence of that particular time. Let me say, I just want to look into the mean occurrence at 10. And with respect to the time and let's say let's say that I want I want to generate like ten thousand samples.

And this is my Poisson values. So Poisson distribution. So this is my Poisson distribution, generating ten thousand samples this time, and let's try to plot the histogram for that and that is going to be equal to something like this. So it's not a lot. And I'm drawing the distribution here, and plt.show, which basically gives you the sample. And as you can see here, like most of the data and the most of the sample is occurring at on the 10 and we are getting the minimum number here, or something like this.

And of course, we can also set, like, you know, let's say if at all, you want to have the most number of events that is to be happen somewhere between four and five. And we can use this so I can set the most number of events and that's my lam. And I can see that we get five. And of course, there is no negative values in the Poisson distribution. So that's why [unclear] it is going to be bounded at zero. And for example, if I said that Lambda is equal to one and will get the most of the samples that one and something like this.

So this is how you can generate the Poisson distribution of data. So very, very useful distribution. And whenever you're dealing with the time or whenever you're dealing with the customer lifetime value predictions, I mean, nobody deals with whenever when the customer next buys a product, et cetera. Right. So this is quite useful. Distribution is used in the many, many applications in the next lecture. We will see more about the distribution. Thank you very much.

9. Gamma Random Distribution
============================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. And now let's see the gamma distribution, gamma distribution is also one of the most widely used distribution. So now let's see how to generate the values or random numbers based on the gamma distribution. And let's go here. And there is one more distribution, the gamma distribution. This is the gamma formula: gamma of alpha is the integration of e to the power of minus lambda and lambda to the power of alpha minus one, where lambda is actually the Poisson mean.

Here we have the lambda and it's actually the mean occurrence. And there is one factor called the shape factor, that is alpha and the gamma distribution. Basically we have like a parameter to the scale parameter and that is basically if you include the scale parameter here. And so what you'll get here is that is a function of the gamma is basically the function of alpha and beta, where alpha is the shape parameter and beta the scale parameter.

OK, so we can you and the heterogeneity of that follows the geometric distribution. So let's see how to generate the gamma distribution. But random numbers. So just remember, we have the two parameters, one is the shape parameter, and second one is the scale parameter, the scale parameter will basically adjust the x axis and the shape parameter will basically move it from skewness to normal. All right, so let's see the generator.

And this is what my generator dot and we have the one where distribution is gamma distribution and here we have the two parameters. One is the shape and the second one is the scale. The shape we can set, one of the shape parameter you want, and that's basically represents the alpha. So the lower the value of Alpha, the more skewness we have. So let's see, the shape is equal to one and the scale parameter basically defines the what is the scale of your x axis.

If scale is equal to one, if scale is equal to one, it is basically equal to the gamma gamma alpha. So in this in this formula, if a beta is equal to one and it's basically equal to the Gamma Alpha, so so make sure you specify some some of the values of beta so that you can get the you can look at the shape. OK, so let's go back. So if at all, if I put this and this is basically the gamma and which is actually the alpha, I think by the end minus one factorial of what we will do here is that let me just name it gamma here. and and how many values I want.

Basically, I just I just want to specify the size and I just want to generate ten thousand values. All right, so now let's look into the shape of that and remember the heterogeneity of that distribution, which basically looks like the geometric distribution. So we'll have the more and more Skewness. OK, so that's what basically you have. So more and more Skewness is basically it's possible with scale is equal to one. And as the scale as the alpha parameter increases will get distributed normally and you'll get like something like the Poisson.

OK, so what we will do now is that let's take this as sns.histplot of gamma, and we'll get plt.show, and you can see here, this is more the distribution. It's more looks like something like this. So much more to the heterogeneity basically follows the distribution. And as it increases, as you basically increases the shape. Let me say. Let me check. Let me take the one little thing and let me. Let me take one more values, which is basically the gamma one, and here what I'll do, I'll take the series of values you copy and paste it and feel so here.

What I do here is that let me see [unclear] You can see, though, the default scale, if I use the scale, is equal, equals 10 and will be in the way in this particular range. So if I use scale equal to 10, the scale is going to be increased in 10 times. So not I can see that scale. It increases to zero to 10 to zero to ten times, if at all. You want to increase one hundred times, we can get the increase of scale two hundred times.

So that's what the scale basically is all about. In the shape parameter will actually reduce the Skewness in the distribution. So let me copy and paste one more thing. And this is my gamma two. In this case, I'm trying to adjust the shape. The shape parameter will try to make your data more like a normal. So let me increase the shape to, let's say, 10. And here you can see, it's more or less looks like a [unclear],

It's the skewness has been reduced a bit. So, for example, if I make it two hundred or more, for example, if does make it to 50. And so it's much more it's much more near to the normal distributions. So that's what basically the shape parameter is all about. OK, so if I, if it all increase to two hundred now what happens is that it's going to get shifted basically. Let me use a thousand. And this is how it's more and more and more, it's looks like a normal distribution, but that's what the distribution is all about.

In the next lecture, we'll talk more about the random generators. Thank you very much.

10. Beta Random Distribution
============================

See the code [here](./2.ipynb)

Hello, everyone, welcome back in this lecture. We'll talk about the beta distribution. The beta distribution is one of the convenient two-parameter functions, and it is most widely used distribution to generate the what are the shape you want we can generate with a beta distribution. So let me go back here, and the beta distribution, if at all. You can see we can generate the normal distribution, we can generate the Skewness on the left side and we can generate the Skewness on the right side.

We can generate almost all possible shapes can be generated with the distribution. It is a two-parameter mathematical function, and it is in the range of zero to one. It is particularly useful for the probability values and many more. And this is the most widely used two-parameter distribution function, so we can generate what are the values you want? You want you can generate. OK, let's see how to generate the distribution of random numbers. So let me take the beta here and the generator.

And what I can use is that I can take the beta here. So beta is widely used; it's a two-parameter distribution, a and b. OK, so let's see like a no. Let me generate the two parameter. For example, let me take let me generate this blue line where alpha is equal to 0.5 and beta is equal to 0.5, will get this kind of shape here. OK, let me give a equal to 0.5 and b equal to 0.5, and how many values I want.

Basically I'm looking for ten thousand values. But we have the ten thousand values and let me name it as beta one and let the the ten thousand values of this particular shape. Now, let's see sns.histplot. Now, this is my beta one, and plt.show, all right, now you can see the two parameter function where we can generate such kind of shapes. So let's see one more kind of parameters, alpha, beta. So let me take two comma eight, and then we can get something like this.

So let me copy and paste it here and what I'll do here. This is let me put a equal to two and b equal to eight, and let me generate the sum to here and here. What I'll do is that sns.histplot, and it's beta, so I'll take beta two, and plt.show. So let me execute that. So we got two comma two; basically we'll get [unclear] distribution; if I take beta is eight will get you something like this. But this is what is possible with this. And if I put three comma three we'll get the perfect normal distribution so we can get the perfect normal distribution, kind of this kind of data on generators using that using the beta distribution.

So three and three and this is maybe two, three. So we can get the perfect normal distribution or some kind of bell-shaped kind of distribution can be generated with this. Let me take one more and see what it is. Basically, it is how we can get like a. We can get we can generate the negative distribution of data and what we can do again, we can give this lower value to where we can give the higher of added to eight eight and the lower value to this.

And we can get that kind of distribution. Let me name it beta four and execute it. So perfect. Now we can see we can generate the different shapes of the data and the generators with the beta distribution. So beta is the most widely used two-parameter function, and it is a convenient mathematical function. It's most widely used distribution function. And the good thing is that we can get in the specific range of zero to one. So that is how, you know, it's a very, very useful function to generate the values in the specified range.

OK, so this is the single most widely used random generator. So apart from that, we can also have the different kinds of generator. So let me take the generators here. We can have binomial distribution, chi-square distribution, [unclear] exponential distribution. And we looked at the gamma, and we have the geometric distribution. It's much more similar to the Gamma and so many, so many kinds of distributions out there.

I recommend to look into the documentation of the numerical python or else you can also try on your one. So this is what you can also try. What are the distributions you want? Like a binomial is basically, though it's almost similar to the normal distribution. But here will generate will give you the values, like we'll give you the values like a number of samples and indicate the total number of experiments. And B is what, the probability of success. So for example, I'm doing some hundred experiments under a hundred random acts of one hundred experiments.

All are of equal and and the probability of some of the success is, let's say, zero point five. And the number of values I just want is one hundred or so or ten thousand. Basically this will create the normal distribution. OK, so this is a binomial, so binomial distribution Bino and I can see like in a histogram of this binomial, and plt.show. So that's basically looks like the normal distribution. It's basically the discrete version. Binomial distribution is a discrete version of your normal distribution, or the Gaussian distribution.

This is the Gaussian distribution, and the discrete version of that is going to be your binomial distribution. So this is this is how you can generate the binomial distribution. And there are many, many distributions out there. I request to you to try all such kind of distributions. So it will be very, very useful. All right. So there's a few things, few techniques that are mostly most widely used distributions. So in the next lecture, what we will do will talk more about the numerical python.

Thank you very much. And we'll see you in the next lecture.

11. Generate custom array
=========================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. So in the previous lecture, we talk about the random generators, so now let's see one of the. Now, let's see, one more methodology was there to create an array is fromfunction, which is also a widely used methodology to create your own functions. So instead of using that, you can also write your own function for generating an array. So let me create my function. For example, this is one area I just want to create. In this case, for example, I'm having row zero and row one there with me.

So this is this is for example, I'm having this and this basically indicates the row number, or this basically indicates the column number. Now I just want to create an area, something like this. So zero point zero zero. And I just want to create something like row plus column. So, for example, zero zero zero and zero plus one, I'll get one zero plus two. I'm getting two and zero plus three. I'm getting three and one zero. I'm getting one here and one plus one is two and one plus two is three and one plus three is four, something like this.

So this is what basically I just want to create in this case. So remember, the fromfunction will by default take the inputs row number and column number. OK. So let me define this. So let me what I will do, let me create a function, something like add, row and column. So by default, I'm getting the row, basically the row number, and the column number is what the two input I'm getting here. So what I want to do here is that I'll do some addition.

So let me name it res, which is the addition: row plus column. And let me return res. So basically and doing the additional two numbers. So if at all possible and zero I'll get to zero and one, I'll get this and so on. So let's say I just want to apply this from function. OK, so I can use numerical python, so np dot, and there is fromfunction there. You can see there is fromfunction, which will take this function.

What this is what function and will come a column by default. By default, what it will do is that it will take the row and column, row number and the column number and you can construct the array, something like this. Now what are the shape you want? The shape. I just want a here it is, three rows and four columns. So this is what an array I just want to create. So let me name it arr func, my array function. And you can see I have generated this; it is basically the row number plus column number.

All right. You can also do the multiple functionalities. I like the multiplication, row into column, and modulo, row modulo column. You can also take this so many things, many functionalities. You can create it. So arr func one. And in this case, I'm just [unclear]. And you can see I'm just generating some kind of functionality. Something like this is basically the row number into the column number, and we're getting some matrix, something like this.

We can do many, many things using those kind of functionalities. I can generate any number of arrays, probably like five by five or six by six, or so on. So this kind of matrix, which I can able to generate using the fromfunction command. So this is about fromfunction. In the next lecture, we'll talk more about numerical python. Thank you very much.

12. Save Arrays in npy, npz and txt
===================================

See the code [here](./2.ipynb)

Hello, everyone. Welcome back. In this lecture, we'll talk about one more thing: npy and npz are another two functionalities which are very useful to save our arrays. So whatever we have created, we can save either in npy or npz. npy is basically used to save only a single array, whereas npz basically saves a zip, and we can save multiple arrays. For example, let's say I just want to save this array using npy.

So in order to do that, I can use np dot save. And we have np.save there. And what we have is that we can use the file format. What file I just want to save here is that let's say I just want to save my array function, and the format, dot npy, is very important. It is the saving format. OK, now numerical python is the extension, and what is the array I just want to save here? It is this.

So that's it. So this is how you can save your array. So let me open the folder. So that's saved; you can see here I have been able to save my array, npy, and it's nearly equal to three hundred and twenty eight bytes. Even I can load that. In order to load it, I can use np dot load; we have load there, which is useful to load. And this is what the function I just want to have and this is what the data I just want to load and I can load it here, let's say arr2 underscore function.

arr2 underscore function: I can simply load back the data using this NumPy function. So a very, very useful function in order to save. And there is npz. It's basically used to save multiple arrays. In order to save multiple arrays you can use npz. So let me save multiple arrays. Let's say I just want to save one, I just want to save arr func, and I want to save some distributions like beta and gamma. So let's see all the things.

So let me use np dot savez. There are different kinds: savez, or savez_compressed you can use. savez_compressed basically compresses your data. So I'll use savez; you can look into the functionalities here. So the file name, and the arrays you want; it is basically an uncompressed one. So if you want to compress, you use this compress. OK, so let me save the arrays, arrays dot npz, which is the uncompressed one, and you can see you can write a list of whatever you want.

as arguments. So I just want to save this. I just want to save one more, let's say arr1; this is what I just want to save. And let me write some kind of functions: we have the gamma and we have the beta, and I just want to save this. And only one thing: remember the things we have saved, and savez is uncompressed; this is not a compressed one. If you want to save compressed, what you can use is savez_compressed.

This is how you can use to compress your data, the same data, array function and gamma, beta. But here you can see the data is being compressed. That's at least a bit so. So if at all the size is big, you can see a lot of difference in this case. The difference is not much because the data of the data is more or less like a random numbers. So this is how we are able to save. Let's load the data. So in order to load the npz, let's say I just want to load this arrays npz; the same function we can use, np dot load, and I can use this and load it.

In fact, in order to load this, we can directly get this value. for example, if you have the three files on there. So in order to get this so you can take the principle, there are files out there there are three arrays being saved: arr_0, arr_1, arr_2. So what are the sequence that is being there? The sequence is: arr_0 is my arr func one, and arr_1 is my gamma, and arr_2 is maybe the beta. So let me load this. So this is my dictionary.

If I do arr underscore zero, that is going to be my arr func one. And similarly if at all you want to get this gamma just give this one and get all the values of the common distribution and so on. But this is how you can save the values in npy and also in npz. All right, so you can also save the value of the text files, so for that you can use savetxt. So for that you can go for np dot savetxt; savetxt is there.

You can save that the text and what are the name you want and what are the format. And by default it is like percent .18e, 18 decimal points, is being saved by this and the delimiters and everything is there. So what I'll do here, I'm going to save the arr; my arr func one is what I just want to save here. And the filename is array dot txt. And this is what I just want to save.

Now let's execute that and you can check your area here. You can see array.txt, it was saved. And then by default, it gives you the 18 decimal points. By default, it'll give you the decimal point to take a lot of memory. But instead, if at all, you want the change to only the two decimal point. So just change fmt is equal to percent .2f, that's it. So it will take only the two decimal points, .2.

Basically, e, the scientific notation, is basically the float value. So I'm just going to use .2f to save the float values, that we can see, we able to save the two decimal point of the float values. Just much more convenient way to say it, even even if at all you want to save even. And we can say the format is percent d if you want to save integers. You can also save in those. So this is also the most convenient way of saving and also storing the lot of savings, lot of memory in this case.

So here you can see the array. As you can see, it is basically stored in bytes, and array text basically takes around, let me check, one hundred and thirty three bytes. So it takes one hundred and thirty bytes, but this one only takes 58 bytes, so you can see the integers save the memory. [unclear] All right. So this is how like, you know, you can save your data either in NumPy format or in the text format.

So this is about the numerical python on saving your data in the next lecture. We will continue more on numerical python. Thank you very much.

13. Arithmetic Operations
=========================

See the code [here](./2.ipynb)

Hello, everyone. Welcome back. In this lecture, we will see how to do the arithmetic operations in NumPy. We can do a lot of arithmetic operations; apart from the operations I have shown you in this lecture, we can do a lot more than this. But here I'm going to show you a few arithmetic operations that will be very useful for you: addition, subtraction, multiplication, division, transpose, inverse, reciprocal, power, remainder and all that.

The arithmetic operations: I will show you how to do them in NumPy. So let's start by importing: import numpy as np. So now let's do some addition operations. Simple addition operations we can do by using the operator, something like this, so we can use two plus two, or two plus three. That is what we can do. But we can also do arithmetic operations using NumPy. So np.add is there.

So that will basically do the arithmetic operations. We can do np.add(2, 3). So what you can get here is that it will able to do some operations even in the even with the simple values. The basic difference in doing this and also the previous method is basically the time complexity. So here np.add will take lesser time compared to the previous one. All right. So we can also do these arithmetic operations even for the arrays.

So let's do some. All right, we will do some mathematical operations here, so let's create np.arange over this array and let me generate the range of values from one to ten, and that's the default step of one. So I'm generating this array and then let me name it as a. So this is my array. And what I can do here is that I can do some arithmetic operations on that. So let me do some addition. So if I do a plus five, so what it'll do is that it will do the element-wise operations.

So means like for each and every element, it will add five. So let's look at the results here. As you can see, we are going to add five to each and every element, for example, in this case, one plus five, two plus five and three plus five and so on. So this is how we are able to do the element-wise operations and it's very useful and handy. Instead of that, we can also do the two matrix additions of two matrix. So let me create a matrix here.

Let's say I just want to create a matrix using the random numbers. Let me say B equals np.random.randint. And I just want to generate the values from between zero to 10 and I just want to create three by three. So that's my B and what I want to do here is that I just want to do I just want to add five to each element. So what I will do is that we're going to add each and every element of that so that we add five to every element, means four plus five and three plus five and so on.

So this kind of operations, we can also do. And we can also do matrix-matrix addition. So let me create an array here. So let me say C. And this time I'll create one more array randomly. And this is what the array which I created. So this is A B and this is my C, I am able to do some matrix operations; let's say B plus C is basically the matrix addition. So what we're doing here is the four plus three and three plus seven which is like a ten and so on.

So this is how we can also do some additional operations in this. This is one of the most common things, which is used in many, many cases, like when you want to add multiple elements. So we can also do that. Next lecture will continue. More on the arithmetic operations. Thank you very much.

14. Arithmetic Operations - part2
=================================

See the code [here](./2.ipynb)

Hello, everyone. Welcome back. In this lecture, we will talk about a few more arithmetic operations, that is subtraction. So we can also do the matrix subtraction, like element-wise subtraction. This is my matrix and we can also do the element-wise subtraction. Let's say I just want to subtract three from everything; you can also do that. This is my element-wise subtraction. And at the same time, we can also do the matrix subtraction simply by B minus C, which is my matrix

subtraction. It will be equal to this, and we can simply subtract an array, something like this. So it's one of the very simplest thing which we can do it as a matrix subtraction. Instead, we can also do this subtraction using the function np.subtract. So we can also do that, and np.subtract takes the arguments B and C and what we'll do is that subtraction just like this. The main difference between these two is basically the time complexity.

If you want to calculate the time complexity, use %timeit. And this operation basically takes [unclear] nanoseconds, whereas for this operation, %timeit shows [unclear]. So basically, NumPy will work better for bigger data. Here it seems slower, but generally NumPy will be good when your array

is very, very big. There you can see the real complexity. It will be a very, very small. All right, so that's what we can do in subtraction and we can also do some multiplications. So in multiplication we can do the matrix multiplication, either the dot product, or we can do element-wise operations. So those things will see now. So there are two kinds of things. One is that element wise and second one is the DOT product. Right. So first we will do the element-wise operation.

So let me create let me have an array of this. And if at all, I want to multiply each and every element with the two. I can easily multiply that into two. This is basically the element-wise operation. Those things we can do. All right, so we can also do something like this: let me have an array and let me create a D, which is in a range, just like the same. This is np.arange.

And I just want to create from 11 to 20. OK, this is the array I just created, and this is my a, and I just want to multiply element by element, something like one into 11, two into 12, three into 13. We can also do that. It's simple: a star d, and we simply get one into 11 is 11, and two into 12 is 24. So we can do all element-wise operations with multiplication, with a simple star.

Also, we can do element-wise for matrices. For example, I just want to do the element-wise operation on B and C; this is my array B and this is my array C. And if I want to do the element-wise operation, something like four into three, three into seven and one into one, those things also we can do: simply B star C will do the element-wise operation in this case. So for example, four into three is twelve, three into seven is twenty one and one into one is one and so on.

And if you want to go for the real matrix multiplication, you need to go for the dot product. OK, so for the dot product, use np.dot, which will basically do the matrix multiplication, or the product of two arrays. So np.dot(B, C), and what basically happens is that it will do the dot product: four into three is twelve, plus three into seven is twenty one, plus one into one.

And what it does is that it will add all those things and we'll get the output here. So that's the matrix multiplication we can perform here. So these kinds of matrix multiplications we can easily perform using the dot product. OK, so this is a simple matrix multiplication. And apart from that, we can also do one more arithmetic operation, that is division, so we can also do the division here.

And let me take an array; let's say this is my a. Similarly, the division is basically the element-wise operation. So we can do the element-wise operations here. For example, I'm having the matrix a and I have d with me, and I just want to divide a by d. We can do that. A by D will basically divide. This is basically do the division operation. So what it is one by 11, two by 12 and three by 13 and so on. So those kinds of things we can simply do, or we also have

np.divide, which will basically give you the element-wise division just like this, a comma d. So you can do both the same way. But one thing is the time complexity that comes up here. All right. So this and this are the same. We can do all the arithmetic operations: addition, subtraction, multiplication, division. Everything can we do in this case. And the the things what we can do here is the transpose and the inverse reciprocal and power and reminder.

So we'll continue with the next lecture. We'll talk more about this, how to do these kinds of arithmetic operations in the next lecture.

15. Arithmetic Operations - part3
=================================

See the code [here](./2.ipynb)

Hello, everyone, welcome back. Now let's see how to do the arithmetic operations like transpose, matrix inverse, reciprocal, power and all those things. So now let's see. The first thing is the matrix transpose. So we can do the simple matrix transpose and then let's say, like we consider the Matrix B, and I just want to transpose this, I can do this simply by B dot capital T, which will basically do the transpose. Let me do it again. Let me see.

This is my B and its transpose. And what it does is the matrix transpose. So four, six and nine will come in the row, and three, zero, three, and it will basically convert like that. This is how we can do the transpose. np.transpose is also there, so that will also do the transpose. So we can use B.T or you can also use np.transpose. Both are the same; you can use either one. These kinds of operations we can do here.

And one more thing we can see here in arithmetic is the trace. The trace is basically the addition of the diagonal elements. We can get the diagonal elements here. So let's see. Let's look into B.trace, which is basically the sum of the diagonal elements: four plus zero plus three. This is the diagonal, and the trace is the sum of those elements.

So that's B.trace, and basically trace is the sum of the diagonal elements. OK, of course, we can also create a diagonal matrix. If you want to create a diagonal matrix, you can also create that matrix: np.diag is there, so that will create the matrix. So what it will do is that we need to give the diagonal elements here. So, for example, let me give you the list.

Let's say my diagonal should be one comma, two comma, three comma, four comma five, and it'll create a five by five if I write something like this, where the diagonal has these elements and the rest are replaced with zero. So these kinds of things we can easily do with matrices. All right, so let's see some operations; one more operation we're going to see here is the reciprocal. So reciprocal is basically

an operation like this: let's say I'm having x equal to five, and the reciprocal of x is one by x, something like this. This is what we will do. So that will be one by five. It's approximately zero point two. But that's what the basic reciprocal operations and we can also do the element is reciprocal operations. For example, I'm having an array with me and I want to do the reciprocal.

We can do either one by this, or we can also have np.reciprocal. So np.reciprocal is there, and that will actually calculate the reciprocal of that. So what I can see here is that it basically returns the values. The problem with the reciprocal is that if the array is integer, it will give you only the integer part, something like this.

This is what it is going to give for an int. And let's say I convert that: if I convert that into float values, using np.float with astype, I am able to convert that into float values. And now if we do the reciprocal of arr_c, what you'll get is this.

So when you're doing the reciprocal operations, make sure to convert the data to have float values, then perform this operation. And there is one more point people are mostly interested in, that is, let's say how many decimal points your real interest is, for example. This shows only one decimal point and this shows how many decimal points and so on. So what do you want to do here? Is that let's say you just want to limit this to the other two or three decimal points, but also do that.

For example, let me save that into arr_c, so arr_c is this. And I just want to limit that to two or three decimal points, and we can also do that. If I want only two decimal points, then I can use the round operation. That will do the round-off of all the arrays. So what we can use is np.round. np.round will basically do the round-off operation for every element here.

And you just pass the array arr_c and how many decimals you want. Let's say you want three decimals or decimals. So I'm just limiting that of the three decimal points. I can do that here. So this is how we can do we can do the round off of all the elements with the three or any number of decimal point you want. All right. So this is a very, very useful operator and will be used in many, many cases. And one more arithmetic operation that we are going to see is the power.

Power is basically the exponential function, so we can do the power using that. So one more thing we will go for is the power operation. What does the power operation do? It does the square operation, cube operation; for example, I just want to calculate three square. In Python, we can do the square operation with a double star. So three double star two will do the square operation.

Double star is basically the power operation. So let's say five to the power of three, and one twenty five is the value. But we can also do the element-wise operation here. For example, I'm having an array with me, and for each and every element I want to do some power; I can use np.power. np.power is there, so I can use this power. And what I can do here is pass the argument a, and two, and you get the square of each and every element.

And let's say you want the cube, or the fifth power of that: one to the power of five, two to the power of five, three to the power of five and so on. We can also do a different thing: for each and every value, I want to assign some other power. For example, I just want to do one to the power of one, two square, three to the power of three, four to the power of four, something like this. I want power operations like: one to the power one,

two to the power of two, three to the power of three, four to the power of four, five to the power of five. To do such kinds of operations, this element-wise operation is also there. We can use a comma a, something like this, and it will give you the power with this particular value. So this is my a, and what is going on here is one to the power of one, two to the power of two, three to the power of three, four to the power of four and so on.

That's what is going to be it's very, very useful. Operations will be used in many cases. And finally, we have the remainder; we can also calculate the remainder, or modulus operation: if you divide one number by something, the remainder is what you want to get here. You can also do this operation with NumPy. So finally, let's go into the remainder operations. So what is the remainder? Let's say I divide five by two; you'll get two point five, but two twos is four and the remainder is one.

So if you want to get the remainder here, we can use the percent operator. The percent operator is the modulus, and basically returns the remainder. Let's say I'm dividing five by three; you'll get the remainder as two. OK, so that's the remainder operation we can get here. And we can also do that in NumPy.

np.remainder is there, and np.remainder(5, 3) does basically the same operation. But I can use the much better NumPy to find the remainder for element-wise operations too. For example, let's say I'm having B, and let me take one more array. Let me clear it out of here. Let's say E is np.random.randint, and I'm taking the range of values between, let's say, 10 to 50, and

I want three by three. This is what I want. And let me create one more variable, F, as np.random.randint, and I just want to create an array in the range of zero to five, and this is also three by three. OK, so this is my E and this is my F. So what I want to do here is: if I divide forty seven by two, I just want to create an array of remainders.

I just want to create an array of remainders: if I do forty seven by two, what is the remainder? Forty eight by two, what is the remainder? Something like this is what I just want to create. If you want to do that, we can use np.remainder. And what we can see is that np.remainder(e, f) will basically return you the remainders. If I divide forty seven by two, the remainder is one; if I divide by four, the remainder is zero and so on.

That's what we can get here. And we have one more operator, np.mod, that actually does the same kind of job here: np.mod(e, f) does the same kind of job in this case. Right. So these are very, very useful operations that are going to be used in many, many scenarios, in many cases. But NumPy is designed for much more than this; you are not limited to only these kinds of things.

We can do many things with numerical Python. I request you to just have a look into the documentation of numerical Python; I will give you the reference link, so please have a look into this documentation so that you can understand more arithmetic operations that you can perform in no time. OK, thank you very much. We'll continue in the next lecture, more on numerical Python.

## 4. Setting Google Colab

2. Integrate Google Drive to Colab to Load Data
===============================================

Hello, everyone, welcome back. Now let's see how to load the data into Google Colab. So first and foremost, what we do is that we have to download the data. OK, so let's go to your Udemy lecture. And in this case, you just go to the what are the data you want? For example, I'm working on this visualizations, so just download that will go to the resources and download the resources here and there. You can see the data is available and click on this link to get the data.

So once I click on this link, it will navigate to Google Drive, where you can look into the Excel sheet. Now, what do you do here is I just click on this download. It'll take some time and it will get download for you. All right, so it has been downloaded successfully. So what I'll do here, I'll copy and paste it into my time series folder. So let me open this time series folder. So this is where the data has been downloaded.

So let me cut and paste into the visualizations, or into the Google Drive, or the setting up Google Colab folder. So let's let's see. This is what the data I just want to upload into my Google Drive. So let me rename this because it's already by multiple times. That's why I got this one. So let me rename this. All right. So this is what the name of the file and I'm most interested. Good. Now, what we need to do here is that let's open. You are right. So let's go to Google, click on these Google apps and click on your Drive.

That's it. So we as we have seen that in the previous lecture, we created one folder. So let me go into this folder. Let me go into the visualizations. Now, let's create one more folder. Let me name it as data. And this is what the data. So what I'll do here, I will open this and just drag and drop this. What do you do here in order to upload anything? Just drag and drop. You can see just drag and drop it. Just drag. And drop it you. OK, that's it, so it will get uploaded within seconds.

All right, you can see now the data is being uploaded. Excellent. Now, let's go back to the visualization notebook, and what I'll do: Let me open this up and by just double click here. OK, you can see here open with Google Collaboratory or others again, right-click and open with Google Colab. All right, as you can see, this is where the previous lecture we have imported these libraries and we have checked that. So just wait for a few seconds until it gets connected.

Done. Now it was getting successfully. So what I'll do, I'll execute these programs again, or execute these statements again. Now, I just want to load this data. What are the data I'm having? I just want to load this data in order to load this data. And what I need to do here is that I need to connect my Colab to the Google Drive. So let me see this. As you can see, there is a Files section, and this is the Files section where you are interested.

You. All right, now you can see we have just connected with the sample data, so we have not connected to our Google Drive and that you can see there is one more thing called Mount Drive. Just click on this. So this Mount Drive will get connected to our Google Drive here. You can see it asks to permit this notebook to access your Google Drive files; just click on Connect. And now what to do is that it will ask you for the appropriate email address.

So this is what the email address. I just want to connect. And you can see it was the it was getting mounted on my Google Drive is getting mounted, so take some time then we can see you can see that I can able to see my Google drive in this click on this drive and my drive. And you can see this is what we have just created a complete time series. And inside that you can see the visualizations and this is what the note is working on and there you can see the data, like the sales Excel file.

All right. So this is the path we need to go to here. So in order to set the path, what I can do here is that let me let me copy this. Let me click on this visualizations. Let me click on right click. Let me try click this visualizations. Now, you can see there is a copy part, is there? So now what you need to do here is that let's set the path here. Let's set the path. So in order to set the path, you just import a library, os, which is basically operating system.

Now you change the directory with os.chdir and copy-paste the path; I have just pasted the path. That's it. So this is the path you have pasted. Now just execute this command by using shift plus enter. Now you can type in ls, and ls is for list. And you can see now you are in this particular folder, so you need not set all those things again. Now, you are in this particular folder, so it shows up directly, all those things.

But now you can see you are in this particular folder that is data and the visualizations folder. Now directly you can load the data and you can type ls space data. You can see what are the files that were inside the data right now directly you can load the data since we already have pandas imported. All right. This is the data I just want to load here. In order to do that, just use pd.read_excel, since it was my Excel file, and it was in my data folder.

So just dot slash indicates the local folder, then the data folder, followed by this sales file. So just name it df and do this. Right. You have successfully loaded our data; you can check with df.head in order to look into the top five rows. That's it. I can see you have successfully loaded our data. That's it. So in the next lecture, we'll talk more about this. Thank you very much. We'll continue in the next lecture.

## 5. Time Series Visualizations

2. Types of Charts for Time Series
==================================

See the code [here](./3.ipynb)

![74.png](./images/74.png)
![75.png](./images/75.png)

Hello, guys. Hope you are doing well in this lecture. We will talk about Time series visualisations means we will see how to visualize. the time series data. Generally, there are four kinds of data visualization techniques for time series data. One is the line plot, second one is the area plot, then the bar plot, and finally, the heat maps. So these are the four kinds of data visualization charts that are commonly used for time series analysis. So let's look into one by one and how to visualize the times it is data and python.

Hey, guys, thanks for watching this video in the upcoming videos, we are going to watch the powerful visualizations of time series data, like area plot, bar plot, heat maps, etc. So we are going to see all those things in these upcoming videos.

3. Setting up Google Colab
==========================

All right, now I am in the Google Drive. So now let's see how to open Colab and load the time series data into it. So let's look at the data first before we do all of those things. Let's go to the data. And we are having the two kinds of data with those. One is an Excel file and second one is a CSV file. So in this lecture, we will try to understand and do the analysis for this sales data. And if we can open and look into the data that are two sheets are there.

One is sheet number one and second one is sheet number two. Sheet number two is much more expanded version of that where you can see the years column and the sales column means each and every month what is the sales that is being happen and everything is being recorded. So typically, any time series data looks like a date or year column, and the value could be any kind of interest, or sales, or the stock market price or anything. Now let's see how to load our Google Colab and do all our stuff in Python.

So let's go back now what I will do. All right, click here and click more and then we can see the Google collaboratory. So click on Google Collaboratory. It will take some time to get that. All right, now I have successfully opened my Google Colab. Now you can see that by default, the name of my Colaboratory notebook is Untitled0, and that is being saved here. So first thing what I'll do, I will change the name. So what I'll do here is visualize. I just make a name for visualizing Time series data.

Time series data. OK, the step number one, what do you do is that you need to connect to the runtime. So for better performance, I will connect to a GPU: go to Runtime and Change runtime type. And as you can see, there is the hardware accelerator, and what I'm going to do is that I'm going to connect to my or to the Google GPU. So click on GPU and say, and now what do you do? Don't forget to click on Connect and just click on Connect here.

It will take a couple of seconds to get connected. Wait until you get your connection has been successful. Yes, now have been connected successfully and you can see the details of my RAM, and so the next step, what I need to do here is that I need to set the path means I need to set my the path. So currently my path is in My Drive and complete time series. So what I'll do, let's see how to set the path here. Now at the. Now, the left left side, you can see there is a Files option; click on Files and you can see your current working directory. At the moment, there are no files there.

So what can it do is that I need to write some code to get connected all my files. So let's do that, please. So first import os, and from google.colab import drive, and drive.mount. Execute the statements with shift plus enter. Now, as you can see, there is one URL there. So just click on that URL. If you click on that URL, it will ask you which email you are currently working with; I'm working on the time series one.

So I'll click on the time series account and click on Allow. It gives me a code, and I'm just copy-pasting it into the Google authentication code box. So enter and execute. It will take a few seconds to execute it. OK, perfect. Now I have successfully mounted my drive. Perfect. So now what I will do, I'll refresh my files. So if I refresh my files, you can see the drive has been created and you just expand this drive.

OK, what I can see here is my drive and again expand it. You can see the what are the folders that was there in the my drive. So currently I was in the complete time series folder. So click on the complete time series folder, and I was in my drive. So I'll right-click it and copy the path. Now I'll set the current working directory, the current path. So I will set it using os.chdir, and I will paste the path.

So one thing you need to do is that just remove the content you copy and you basically remove the content. Now that's it. And executed. Perfect. Now you can type ls to just verify whether you are in the current working directory correctly or not. Yes, I am. I'm in the current working directory. As you can see in the directory, I'm having the data and the file that I was working on is visualizing the time series data. So let's look at the data to verify once again.

Yes, I'm having the sales and the notebook files and data with me. Correct. So that's it, guys, this is how we need to set the path. In the next video, we will see how to load the data and do some visualizations. Hey, guys, thanks for watching this video in the upcoming videos, we are going to watch the powerful visualizations of time series data, like area plot, bar plot, heat maps, etc. So we are going to see all those things in these upcoming videos.

4. Load the Data
================

See the code [here](./3.ipynb)

All right, guys. Welcome back again. Let's see how to load our data in order to load the data. First and foremost thing, what we need to do here is that we need to import few libraries. So before that, what I'll do here, I'll insert the text and I will write down here saying that let's add three hashes and let's say this is the loading the time series data or let's load the data. So now let's see how to load the data. So in order to load the data, let me do one thing.

Let me minimize all this things so that I can see a nice view of my Colab notebook. So let's import all the libraries. So basically we need to import the three four libraries. One is numerical Python, second one is pandas as pd, and third one is matplotlib. Apart from that, I need to import one more important library, that is seaborn. So import seaborn as sns. Just execute all these commands and you have now imported all the libraries successfully.

Let's see how to load the data using pandas. So in order to load the data, let's use pd.read, and remember, I'm trying to read my Excel file. So I need to use the command read_excel, and the path here, since it was in the data folder, followed by my file name. I think it is long, so let me take the file name and just copy it; this is the name of the file.

OK. Yes. And .xlsx is the extension. And what is the sheet name I want to read here? You can see I was interested in sheet number two, so just mention sheet_name equal to Sheet2. All right. So let's look into the head of this. So we are having the years and sales; it has been successfully executed and we have loaded our data successfully. All right, so first and foremost thing, whenever you have the data with you and wanting to do here is that you look into the what is a data type and is there any missing values?

et cetera; everything you need to check. So use the command info. So I'll do df.info, and what I'll get here is all the entries, and I can see there are one hundred and eight entries and there are no nulls there. Everything is full. And what I can see is that sales is an object; sorry, it is a float64, they have float values, and the date column's data type is datetime64. So make sure of what data you have.

You need to change that data type into datetime64. If it is not in datetime64, you need to convert that into the datetime64 format. Hey guys, thanks for watching this video. In the upcoming videos, we are going to watch the powerful visualizations of time series data, like area plot, bar plot, heat maps, etc. So we are going to see all those things in these upcoming videos.

5. Line Chart
=============

See the code [here](./3.ipynb)

All right, so what we will do is that we will start by plotting our data. All right, so let's see. The first kind of plot is a line plot; the line plot is basically used for any kind of time series data. So the x axis for the line plot is years and the y axis is the sales. I'll explain to you two methods of doing the line plot. First I will use seaborn here. So let's use seaborn and do the line plot in seaborn: sns.

lineplot; we have that command straight away for the line. What you need to do here is mention the x axis. My x axis is years. And the y axis is the sales. And I need to specify the data, data equals df. So that's it. So let me execute this code and plot it; you can see the data. The x axis is years and y axis is sales. And as you can see, there is a clear trend and seasonality component in my time series data, which is clearly visible.

We'll talk about the more about this seasonality and everything in the upcoming lectures: how to deal with that data and what kind of modeling you need to apply when the data is something like this. All right, so what we will do now is that let's try to make it much more clear and beautiful. So I'll do plt.show so that I can remove the comment here, and let me increase my size using aspect. OK, I can use aspect to set all those things: aspect is equal to three.

So. Oh, OK. Aspect three. OK, probably that is not there, I guess. Let me check that. OK, I think that is for catplot, so we can do one thing: plt.figure with figsize. So I can mention figsize is equal to 10 comma six, and that probably might work, as you can see, like the width and height. Let's increase it a bit, width 15. I think this is much more clear and perfect. OK, so it's very, very clear and very easy and nice to be visualize the seasonality and cyclicality.

And there is a trend in the data if you kind of randomness is there, everything is seems to be fine here. So this is the method number one of visualizing the times. It is data. There is another method to visualize the times that this data is with directly the pandas. So pandas has a functionality called plot, and with that we are able to visualize it. But here, in order to work with pandas, the first thing we want to do is set our index.

So let's see how to set our index. We need to set our index to the date and time. So I'll mention df1 equals df.set_index, and set my index to the column name, Years. And let's look at my df1 now. This is what my df1 looks like. And you can see this is the sales, and the years are set as my index. Perfect. So now I'll use this df1 and plot it, so I can easily plot it.

And the kind of plot I'm looking for is a simple line chart. All right, see, we got exactly the same plot as what we got with the seaborn lineplot. But here, with the help of a simple pandas command, no seaborn, with a simple pandas plot with kind equal to line, I am able to simply plot it. We can do some kind of stuff for visualizations like plt.show, and we can increase this plot using fig, ax.

I'll use plt.subplots, because for the pandas plot, in order to set the figure size, the subplot is the way: set figsize to 15 comma, let's say, six, just like that. And here I need to specify ax equals ax, specifying this ax into it. So now I am able to specify just like what we did for seaborn, and it's an excellent way of visualization. But still, seaborn is a much more powerful library, as we can see.

So this is how you can visualize the line plot using seaborn as well as using the pandas library. Hey, guys, thanks for watching this video. In the upcoming videos, we are going to watch the powerful visualizations of time series data, like area plot, bar plot, heat maps, etc. So we are going to see all those things in these upcoming videos.

6. Hue the Line Chart
=====================

See the code [here](./3.ipynb)

All right, let's do some kind of things and make our line plot much more beautiful. So what we will do is that now I will try to pre-process my data. So let's go back to my data. So this is the data I have with me. I have not used it here for now; I'm going to use what is in the data. So I'm having the years and the sales with me. So what I'll do: I'll create two more columns. One is with the year, and second one is with the quarter.

So I'll try to visualize how, with respect to the year and with respect to the quarter, my data looks like. So first, for that, what I can do is take the years and, remember, the data type: this will work only if the data type is date and time. It will not work for objects; it will not work for any other kind of data; it will only work for the date and time data type. If not, you need to convert that into date and time.

All right, so what I do here is take the years and let me extract the year out of it. If I look into the years, I just want to take out only the 2001. So in order to do that, let's take df.Years.dt, and if you specify .year, we can simply extract all our years. And similarly, if we want month, you can extract the month, and if you want quarter, you can take out the quarter.

And if you want days, even you can take the days, I guess, dt.day, so you can take the days, quarter and everything. So these are all the options which are available only for the date and time format. Right. So I'm interested only in the years now, so let me create the new column, which is year, and let me save it into df['year'], with small y, and let me create one more column with the name quarter.

All right. So if we want to get the quarter here, let me take df.Years.dt.quarter. And if I give df.head to display the top five rows, as you can see, we have the year and the quarter number; we can simply get them out of this. And as we can see, quarter one indicates January, February, March, and April, May, June is quarter two and so on. So like this we can get the quarters here.

So I will make use of this data and I will create some kind of separation plot. Let's see what I'm trying to do in this case. So let's take the lineplot here using seaborn, scroll down and copy-paste it here. And let's look into the line. Obviously, this is the same, but here, let's say I want to visualize the separate things. Like I just want to look into how my area is, or what is the color, or what is the deviation which is there in 2001, 2002, 2003 separately.

Then what you do here is: we have a special parameter called hue. Mention hue equal to year, and it will automatically set the color, so you can see that the color is being set. Let me do one thing: let me set different color maps. So palette is the way of setting different color maps. So let's look at Set1, which is one of the color maps. Now we can see that we have different colors for the different years: 2001,

2002, 2003, four, five, six, seven and eight. So very, very clearly we can visualize what kind of pattern and what kind of behavior was there based upon the year. This is very, very cool stuff, and there are different ways of setting the palettes. We have color palettes like [unclear]; there are many, many things out there. My personal favorite is [unclear].

And it's easy to visualize. All right, so this is how, guys, we are able to visualize the line plot, and also we can use a parameter called hue to separate the year, or categorical values. Hope you enjoyed this lecture, and we will continue in the next lecture, more about the visualizations on time series data. Thank you very much. Hey, guys, thanks for watching this video. In the upcoming videos, we are going to watch the powerful visualizations of time series data, like area plot, bar plot, heat maps, etc.

So we are going to see all those things in these upcoming videos.

7. Area Chart
=============

See the code [here](./3.ipynb)

Hey, guys, welcome back. Now let's look into one more kind of plot, that is the area plot. So I'll create one text cell now and just mention it as area plot. Now, let's look into the area plot, and we will eventually see a different way of doing the area plot when we are doing the stacked plot. At the moment, I will just show you how to do the area plot. So let me take the same data, whatever I'm having with me.

So in order to do the area plot, what you need to do is set the index. And remember one thing: we don't have the area plot in seaborn, so we make use of the functionality in pandas to do these things. I'm already having df1 with me, which already has the index set. So I will do the plotting here with kind of plot; we already saw the line plot with kind equal to line, and this is what we already did here. Instead, if in the place of line you specify area, what you'll get is the area plot. It is a powerful way of visualizing.

So let me try to increase the size: fig comma ax, which is equal to plt.subplots with figsize, which is, let me take 15 comma six, and specify ax is equal to ax. And what we can see here is that... oh, we got an error. It is subplots. All right, so we got a nice area plot. And in the upcoming lectures we will see more about area plots and how to plot them, because we have not pre-processed the data enough to show you the area plot properly.

But at the moment, this is the plot we have, and in the upcoming lecture we will pre-process the data. I'm going to show you the way of doing area plots, and also I'll show you the stacked area plot too. So that's it for now, guys, and in the next lecture we will see how to plot the bar plot. Hey, guys, thanks for watching this video. In the upcoming videos, we are going to watch the powerful visualizations of time series data, like area plot, bar plot, heat maps, etc.

So we are going to see all those things in these upcoming videos.

8. Bar Plot
===========

See the code [here](./3.ipynb)

OK, let's do one thing: let's put one text cell with four hashes, and let me name it as bar plot. So in order to do the bar plot, we need to do some kind of pre-processing or some kind of transformation in our data. So let's look at df here. What we have here is sales and also the year values and the quarters. So in order to do the bar plot, in order to visualize the bar plot, let's do one thing, the basic way of visualizing the bar plot. And remember, the bar plot will be used only for categorical data, for example the year, or the quarter.

For example, I want to understand year by year the sum of sales, or total sales, which happened: 2001, I want to compare with 2002, 2003 and 2004. Those kinds of things we can do in the bar plot. So in order to do that, what we need to do here is a group by. So let's do the group by here. Let's take two columns here: one is my sales and second one is my year. And what I do here is apply the group by here.

So group by year: I group by year and sum all the sales, which gives the total sales in each and every year. So this is the group by, and what I'll do is name it as df_year, which is the group by year. All right. Now I don't want year as my index. Instead, what I'll do here is reset_index; I just reset my index.

And so, perfect. So what I did is that I took df_year, and as you can see, this is the data: 2001, this is the sales, and in 2002, this much sales happened, and so on. So we can do this simply by plotting with seaborn. We have catplot there. So using catplot, you just mention the x axis is my year and y axis is my sales. That's it. And I specify the data is equal to df_year.

Perfect. Now what you can find here is that, oh, we got dots. You need to mention the kind of plot I'm looking for; by default it's a strip plot, a kind of scatter plot. So I mention kind equal to bar, and a nice bar plot is drawn by specifying that in catplot. And let's do one more thing: let's expand it. We have aspect there, so let's specify aspect is equal to three. And aspect is the width by height, the aspect ratio.

So the width is three times my height, so we can see the nice bar plot, which can easily be drawn using catplot in seaborn. Perfect. And we can also do this using pandas. So let's do one thing: df_year is there with me, and I can use pandas also. In order to work with pandas, what you need to do here is set your index. So I need to set my index. The index I want to set is the year; this is what I'm setting.

So df_year with set_index. If I set the index, this is the data I'm having here, and what I'm doing now is that I just plot it, and the kind of plot I'm looking for is bar. So, perfect: here you have the nice bar plot. Now there's only one single color; it's OK. So what I'll do here is just increase the figure size, like we did last time: fig, ax is equal to plt.subplots with figsize, which is

10 comma six, or 15. Let me take 15 here because it looks nice and broad. So let's look into it. We got some error. Yeah, subplots. Yeah, now we just need to mention ax is equal to ax. So that gives a nice bar plot, which you are able to see in pandas. So that is a very, very excellent thing which we are able to do here. In the next lecture, we will see how to do the stacked bar plots. That means what I want to know is: OK, this is the total sales that happened in 2001,

but I just want to analyze it quarter by quarter, means in 2001, what is the sum of sales that happened in quarter one, quarter two, quarter three and so on. So I just want to analyze that kind of information in pandas, and let's see that in the next lecture, more on the stacked bar plot. Hey, guys, thanks for watching this video. In the upcoming videos, we are going to watch the powerful visualizations of time series data, like bar plots, heat maps, etc.

So we are going to see all those things in these upcoming videos.

9. Proposition and Stacked Bar, Area Chart
==========================================

See the code [here](./3.ipynb)

Hello, guys, welcome back. Let's see how to do the stacked bar plot. In the previous lecture, we saw how to draw the bar plot for time series data. So now let's see the stacked bar plots. Let's look into our data. This is the data which is there with me, and what I need to do here is add a text cell with four hashes, mention stacked bar plot here, and let's see how to do the stacked bar plot.

So in order to do the stacked bar plot, we need to do some kind of pre-processing of the data. We have sales, we have the year and we have the quarter with me. In the previous case, what we did is group by year. So now what I need to do here is the pre-processing, or the group by, even for the quarter too. So let's see how to do that. Let's select the columns here: one is the sales, second one is year and third one is the quarter.

So let me take the three columns and do the group by: first by year and second by quarter. And for the aggregation operator, I mention sum here, and you can see that we got all the values for 2001, basically each and every quarter is there, and sales; everything has been perfectly labeled and indexed for the data I'm having with me. Right.

Of course, this kind of data is very difficult for me to visualize, so I will do the pre-processing in my own way. Let me take the sales values, which are arranged in order, and let me convert that into values, and let me print the sales here. What we have is a list, and all of the sales are there with me. So I need to take .values. Perfect, I'm having all the values here; all the sales are there.

So let me look into the shape of that: sales.shape. This is what I'm having: 36. And one thing we have to understand here is that I'm having nine years of data, and each year has four quarters. If you look into that, nine years of data with four quarters each, obviously nine fours are thirty six. So let's do one thing here.

Let's take the sales and let me reshape my data into nine by four. If I reshape the data into nine by four, the rows are the years and the columns are my quarters. For example, if you see, this is the information of 2001, quarter one, and this is exactly the same thing, 2001 quarter one, and so on. So we have such kind of data available. So let's do one thing: let's convert that into a data frame now.

So pd.DataFrame, and I'm having the data with me, and let me define my index. Obviously, it starts from 2001 to 2009. So let me take the list of range starting from 2001, and I'll end with 2009, so the end is 2010. And one more thing I have to specify is the columns. So columns is a list, right?

So columns: the first one is Q1, second one is Q2, third one is Q3, and fourth is Q4. Let me execute and check whether I'm getting it perfectly. Yes, it is correct. So now I save it to the variable df_sales; this is all the data I'm having with me right now. So let's look at df_sales. In df_sales we have the perfect data in the perfect matrix format, and this is perfect data with which I can do the visualizations.

So now let's create the stacked bar plot. df_sales.plot, and the kind of plot I'm looking for is bar. And you're going to see another perfect bar plot, which is much better than the previous bar plot which I drew here. And you can see the nice color formations and everything. Let me do one thing: let me set my figure size.

fig comma ax is equal to plt.subplots with figsize equal to 10 comma six, right. So let me put ax equal to ax and plt.show. Oh, one more thing we missed: it's subplots; every time I'm missing this. Yes, so this is subplots. Perfect. Now let me increase it a bit, to fifteen. Yes, now it's fine; it looks much, much better here. Now you can see the year 2001 with Q1 sales, and let's say this is Q2, Q3 and Q4 and so on.

Obviously, if you sum all these values, it will be nearly two thousand, and that was my total sales that happened in 2001. Right, so this is year by year, how many sales happened, and we can clearly understand it. And one more thing in addition, what we can see is that quarter one sales are very low, and quarter two and quarter three sales are very good, and quarter four sales

are also low, so you can see about this company that the major sales are going to happen in quarter two and quarter three. So that's one thing we can easily get here. So let's do one thing: this is also called a bar plot, but here, if you want to plot the sum of all these things in the same bar, we have stacked there. By default, stacked is False.

If you specify stacked equal to True, you will see the full bar, even much cooler than the previous one. You can see here the sum of all the boxes, summing up, and you're getting that the value is two thousand. And this is the bar which you are going to get by summing up all the values. So this is really, really cool stuff you can see in pandas, with which we are able to visualize even much better, and with which much more intuition can be understood, even from the picture here.

So as you can see, just recapping again: this is the plot we have; this is the data we have; and we did the data pre-processing to bring it into a nice intuition and visualization, so that you can understand the company's stats much more. All right, so let's do the same thing here, which is almost equal, with the area plot. If you specify area here, that is pretty much the same thing: the area plot.

So this is quarter one, quarter two, quarter three and quarter four, summed all together, and what the value is. And a nice intuition we can get even from the area plot. Obviously, both are the same, but this is the bar and this is the area which you can understand here. And there is an area plot with stacked basically True. If you specify stacked is equal to False, we can compare the area plots, how they are for each and every quarter.

For example, the blue one is Q1, and orange is Q2, green is Q3 and red is Q4. [unclear] Blue and red are almost coinciding with each other, whereas green and orange are almost close to each other. So this is the intuition which you can get in the stacked plot. And with this kind of data, we can understand much more intuition about our data, and also about our time series analysis.

So that's it, guys. This is about the bar plot, and in the next lecture we will talk about the heat maps. Thank you very much.

10. Heatmaps
============

See the code [here](./3.ipynb)

Hello, guys, welcome back. In the last lecture we saw how to do the bar plot. Now let's look into heat maps. We already have the data for the heat map, which is already prepared. So we will put a hash and heat map. We have the data, df_sales. The data is already available with me, and we will make use of the data and do the heat maps. So sns.heatmap: use heatmap and specify the data df_sales. And what you can see here is a nice heat map has been drawn: the lower the value, the darker, and the higher the value, the lighter here.

And you can also increase the size. Let's say plt.figure with figsize; let's increase to ten comma eight. So this makes it a bigger one. And also let's put some values here by putting annot is equal to True. If I specify annot is equal to True, I'm getting those values in the scientific notation. So let's change the format: fmt is equal to .0f. So I'm getting the float values without the decimal point. This is perfect, and let me change the color map to what I want.

My personal favorite color map is [unclear], an excellent way of visualizing the map. And let me give the width of each and every box, like linewidths: linewidths is equal to one pixel, so one I'm going to give here, and a nice plot is drawn here. And again, as you can see, in the x axis we have the quarter values, and in the y axis we have the years, and it's clearly visible: the lower the values of the sales, the darker, and the higher values,

you can see the lighter color, the yellow. And you can see almost in 2001 to 2004 all the values are light blue, dark and blue. And after that I can easily see a very, very good amount of sales; our highest amount of sales happened in 2009, Q2 and Q3. So this is all about the visualization of our time series data. So I talked about how to take this basic data, do some kind of pre-processing, and make cool visualizations for time series

data, like line, area, bar plots, stacked bar plots, and finally the heat maps. Hope you enjoyed this lecture. And we'll talk more about time series analysis in our upcoming lectures. Thank you very much.

## 6. Linear Regression

2. Intuition of Linear Regression
=================================

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
![86.png](./images/86.png)
![87.png](./images/87.png)
![88.png](./images/88.png)
![89.png](./images/89.png)
![90.png](./images/90.png)
![91.png](./images/91.png)
![92.png](./images/92.png)
![93.png](./images/93.png)
![94.png](./images/94.png)


Hello, everyone, welcome to this module on simple linear regression and in this lecture, we will talk about the intuition behind the linear regression. Linear regression is one of linear regression is one of the machine learning model that is used to predict the continuous values. OK, what is the significance of a machine learning model? Why do we need to build the model? In any given scenario, there are easy-to-measure parameters and hard-to-measure parameters, that is, difficult-to-measure parameters. The examples of easy to measure parameters are age, gender, income, education level, etc.

and examples of difficult-to-measure parameters are amount of loan to give, will she buy the product, how many days a patient will stay in the hospital, etc. Obviously the answers to get on the difficult to measure parameters is very difficult. A machine learning model is one of the techniques which will use the easy-to-measure metrics to predict the hard-to-measure values. So regression is one of the machine learning models which computes the future values based on the historical are easy to measure parameters.

OK, let's see now what is a regression with a simple data? I assume that I'm having that data with me, independent variable X and dependent variable Y. The independent variable X is defined by easy-to-measure metrics and dependent parameters are difficult to measure, are difficult to measure, which is what we need to predict. Linear regression basically will try to identify the relationship between independent and dependent variable. So let's build this model.

So let's start with the relationship between X and Y. Scatterplot will give you the relationship between X and Y, X is basically represented on the X axis, and the dependent variable Y is generally put on the Y axis. And one thing what you can understand the scatterplot is that as X increases, your value of Y is also increases. So we can represents this kind of situation with a simple line, something like this.

So I can represent this line, which will find out the relationship between X and Y and the equation of the line could be Y hat is equal to A plus B X, where X is the independent variable and Y hat is the predicted or estimated value. But what is the value of A and B, we really don't know. That is what linear regression will try to calculate. Linear regression is a parametric modeling, which is actually depends upon the intercept and the coefficient, which will identify the relationship between independent and dependent variable and the line we draw should be such that it has the minimum error, or sum of squared error.

So hence the model equation will be Y hat equals A plus B X. What are the values of A and B? You need to take the values in such a way that the error, or sum of squared error, should be as low as possible. Assume that we know the values of A and B; then how to predict Y hat? So let's take an example here. Assume that we already know the values of A and values of B and let's say for the value of X is equal to two point five.

I want to predict the value of Y here. And what you can do here is: this is two point five, and I can map it to the line, and the value I can get here is somewhere around eight. OK, now I can simply say, like, OK, for the value of two point five, this map it to the line and the Y had or the estimated value could be eight. That is one of the coolest things, right. The simple linear regression will simply map that to the line we have, simply map it to that equation.

And that's my Y predicted. OK, how to draw this line here? Simple linear regression depends upon the cost function: the function that we use to draw the line completely depends upon the sum of squared error. So let's try to define the error here. If you see in this example, like the actual value is somewhere here and the true value, if you see in this example, the predicted value is eight, but the true value is somewhere nearly equal to 15.

And there is a lot of error here. And you can define an error with the true value minus predicted value. So what we would do now like this, we will calculate for the error for each and every variables or each and every instance, and we will square it and sum up all of this. And that will become the SSE, sum of squared error, is sum of all, sum of squared of all the errors. That is what my cost function is, actually is. So in order to minimize the error, statistically, we can use a concept of covariance, covariance will actually give you the information about the direction and the strength in that direction.

Think about the slope of the line. So what we can do here is that if you calculate the covariance between X and Y, we can get the direction and the strength. And with respect to X, if you divide that and you'll get the slope of line, meaning with respect to X, what is the covariance? Typically, that is the slope of the line. So the slope of a line is equal to the covariance of X and Y divided by the variance of X.

So simply from this equation, we can able to calculate the slope of a line. Perfect. So we got the slope of a line. So what is left is the intercept. The assumption in order to compute the intercept is that the linear regression line passes through the center of the data. What is the centroid? It is basically the middle value or the midpoint, nothing but X bar and Y bar. So we have all the independent variables and all the dependent variables; the centroid

is basically X bar, Y bar, somewhere in between. So if you know the line is going to pass through the point X bar, Y bar, what we can easily do is substitute in that equation: in the place of X substitute X bar, and in the place of Y hat substitute Y bar: Y bar is equal to A plus B into X bar. And since we already know X bar and Y bar from the data, and we already know the value of the slope of the line from the covariance and the variance of X, we are able to calculate A: it will be equal to Y bar minus B into X bar.

So we can know the value of B from the previous slide, so that's it, you are more or less ready and this method of fitting a line is called least squares regression, and the equation of the model is Y hat is equal to A plus B into X, where A is equal to Y bar minus B into X bar, and B can be calculated with the covariance divided by the variance of the independent variable. That's it is one of the most simplest algorithm and it's very, very easy to implement.

So in the next lecture, what we will see is that we will code the linear regression in Python. First, we'll start with data analysis and building the linear regression. And finally, we will do the evaluations to linear regression. So thank you very much. We'll continue in the next lecture.

3. Exploratory Data Analysis
============================

![95.png](./images/95.png)
![96.png](./images/96.png)
![97.png](./images/97.png)
![98.png](./images/98.png)
![99.png](./images/99.png)

Hello, everyone, welcome back. And this lecture, we will talk about exploratory data analysis. Exploratory data analysis is a very important technique before building any regression model or any machine learning model. And we will try to analyze the data in two ways. One is the quantitative technique, and second one is the graphical technique. And quantitative technique we use in quantitative technique. The goal is to measure the central tendency and the measure of spread of the data and central tendencies, we will calculate mean, median, mode, or the averages.

And in the measure of spread, we will use variance, standard deviation and interquartile range to analyze the data. And graphical method, the goal is to visualize the data. There are many kinds of visualizations we will use. The main goal of the visualization is to identify the pattern in the data. So there are many kinds of visualizations like histograms, scatter plot, box plot, pie chart, heat map, line plots, and there are many more kinds of visualizations or being there.

The primary goal of the visualization is to identify the pattern and the behavior of the data. And the next tutorial will see how to compute the central tendencies and measure of spread in Python and also we will visualize the data in Python. Thank you very much.

4. EDA - Quantitative Technique
===============================

See the code [here](./4.ipynb) 

Hey, guys, now let's see how to do the exploratory data analysis, that is quantitative technique and python. OK, now I'm in the Google Drive and let's create the Colab, and in the Colab, we will see how to do the exploratory data analysis in Python. So in order to do that, let's right-click, More, and click on Google Colaboratory. OK, I'm in this folder, so the first step, what I need to do here is set the path. So my path is My Drive and complete time series.

And I was in the regression folder. So in order to do that first thing, what you do is that first we will connect with the Google Drive. And what I do is change the runtime to GPU, so I just make faster computations with the help of GPUs. So let's connect that. And it is getting initialized. Now it is connected. So what I would do now is: from google.colab import drive, and drive.mount, and it is my drive.

And now what I'll do here is that it will just wait for. I think it's from Google Drive. OK, so now I'm getting the authentication code; just click on that, and this is my email ID, which I'm working on; just allow the access and copy the authentication code, paste it here. So depending upon your email, please select your email address, click on Allow, get the code and paste it here. So now what I'll do:

Let me input all the necessary libraries. The first one is os, and next one I'll use import numpy as np, import pandas as pd. And I want to do the visualizations; for that I'll use matplotlib.pyplot as plt, and I use seaborn as sns. So these are the four libraries that are required for me to do the data analysis task. Next, what I do here is name the notebook too. This one is my linear regression. OK, so let me execute this, all the libraries.

Now the step number one is the setting, the path. So for setting the path I use os.chdir, which is change directory, and since I was in the drive, you can check here, I was in the My Drive folder. So from /content/drive I will get My Drive, and from My Drive I was in this folder, complete time series, and regression. So check the spellings: complete time series, and so this is the folder I was in.

So whatever folder you are having, please check the folder and type exactly the path of the folder, and execute. So now, perfect. Now you can see that I was in that directory, and execute this command, ls, to check what are the files there in the folder. I was having the data and the linear regression .ipynb notebook, which is this. Now what I'll do is that I will first do the data analysis, that is, exploratory data analysis; this is step number one I'm doing.

All right. So in order to do the data analysis, we need to work on with the data so I can see like you can take your resources folder. I've already given you the data, and the data that we are working on now is regression underscore data dot xlsx. So this is the data we are currently working on. So make sure that you are in the folder and in this folder, create a data folder inside that you copy and paste that or you can upload that into the data folder.

All right. So first thing is that collecting the data, I will take df, for data frame, is equal to pd.read_excel. And I need to set the path: it was in the data folder, and in the data it is regression dot xlsx. So let's check the data. And you can see we have the two variables, X and Y, which is what I explained in the previous lecture on regression; the same data we took, and let's build it. OK, so we have the X and we have the Y with this.

The first thing what we have to do in the exploratory data analysis is the quantitative approach. So we need to do the quantitative technique. So the quantitative technique, the goal is that we need to identify the central tendencies. And the second one is the measure of spread. In central tendencies we will look at the mean and median, and in the measure of spread we look into the variance of the data. OK, the first thing we will look into is central tendencies. But so what we can do here is that simply we need to look into things like, you know, getting the shape.

That's also very important to understand the data. So we need to look into the shape. And also look into the data types. That's also quite important. Before doing the quantitative techniques, it is quite important to understand what the data is. And we can see like 227 entries, and all are non-null, and they are float values. So I think we can easily identify the central tendencies of this. So in order to get the central tendencies: mean, median

and mode. So I can take the mean, which will give you the mean of X and mean of Y. And at the same time, we can also give df.median, which will give you the median of X and Y, and mode will give you the most frequent values. All right. So let's do one thing: let's print the mean, and also print the median values, and finally print df.mode, which is my most frequent values. Look and see: the mean is 2.23 for X, and the mean for Y is six.

And similarly for the median, it is two point one eight and three point two. And finally, the mode of X: we have two modes for X, 1.87 and 2.8, and for Y we got here one more mode, 22.4. So we got the modes for X and Y. But the next thing we're going to do here is that measure of spread, we do understand the variance of the data. So measure of spread, we will look into the variance of the data.

So the variance of the data we can identify with var, which will give you the variance of the data. And we have standard deviation, which will give you the standard deviation of the data. So std will give you the standard deviation of the data. The first one is the variance of the data, and it is 0.71 for X, and the variance for Y is twenty four and the standard deviation is the average deviation of the values away from the mean, which is the standard deviation.

And you can see that we have small variation for X, whereas for Y we have comparatively large variation with respect to the mean. So we have large variation in Y rather than in X; in X the variation is small, whereas in Y the variation is large. That is what we can understand in this situation. All right. So finally, what we can use is that we can use this described function, this function that will give you the complete descriptive statistics of the data.

So let me use this describe. So this is a described function which will give you the statistics of the complete of quantitative technique analysis, which is like: the count is 227 values, the mean is 2.23 for X, and for Y it's 6.07. And the standard deviation for X is 0.84, and for Y it is 4.93. And this is the minimum value and the maximum value. And we have the interquartile range; the interquartile range is the twenty fifth percentile to seventy fifth percentile, and that will be 1.73 to 2.54 for X, and for Y 2.3 to 9.4.

So the interquartile range means, say, the middle 50 percent of the data, and it is higher for Y, whereas it is lower compared to X. So this is about the quantitative technique in EDA. In the upcoming lecture, we will see how to visualize the data in Python.

5. EDA - Graphical Technique
============================

See the code [here](./4.ipynb) 

Hey, guys, welcome back. In this lecture, we will see how to do the exploratory data analysis using the graphical technique in Python. In the previous lecture, we saw how to do the quantitative technique in Python. Now let's see the graphical technique in Python. It depends on the data: for different data, different kinds of graphs or different kinds of plotting will be used. OK, let's see the graphical method. The data we have is only numerical in nature.

So the most widely used plot for numerical data is the scatter plot; you can also use the box plot and the histogram to analyze the distribution of X and the distribution of Y. Since we have already seen the measure of spread and the central tendencies, I think it is good to start with a distribution plot. So in order to plot the distribution, we can use sns.distplot, which will give you the distribution of X and Y. To get the distribution of X, we need to pass df.X; if I call df.X, what I'll get is the X column.

So if I plot df.X here, you can see this is the distribution of X, and what I can understand here is that the distribution plot basically shows the histogram, and at the same time we have the kernel density estimation, which is the line we have. So from that, what we can see here is that the value of X is between one and four point five, but in reality, this could be in the range of zero to five; that is the estimation given by the KDE. And similarly, we can also look at the distribution of Y.

What we can see here is that the value of Y is between almost zero and somewhere around 17. But the KDE says that this could be in the range of minus five to twenty five. So one thing we can understand from the distribution plots: it does not look like a normal distribution. There is some kind of positive skew in X, and at the same time, we have some positive skew even in Y. So it seems to be a good visualization.

So from that, you can understand how the data is distributed. And the next plot, what we can see here is the scatter plot, to look at the relationship. The relationship plot is a nice way of visualizing your X and Y, so I can use seaborn's relplot, the relationship plot, here: x is equal to X and y is equal to Y, and the data I'm applying here is df. So that's the relationship plot, and we can easily plot our relationship.

And what we can see here is that this is for X and this is my Y, and what you can understand here is the scatter plot with respect to X and Y: my data is moving in a positive direction, which is clearly visible. And we can even plot the KDE plot to look into how the data is spread. So in order to do that, in place of the relationship plot, I'll use the KDE plot.

So this is also one of the most widely used plots in order to look at the distribution on the two axes. It's a nice plot where you can understand the distribution. So in order to do that, first pass X and Y, and we can plot the KDE plot for the distribution. And what you can see here is that the most concentrated data is in this region, and it is a nice plot. So let me increase the size here. We use aspect, and aspect talks about the ratio between width and height.

The default value is one. So I can change the aspect ratio from one to two, which means my width is two times longer than the height. So let's use this aspect ratio, and you can see here it is a nice visualization, and these dots are my data points. And this is the distribution with respect to X and Y. This is the variation, more or less like the covariance of the data, how the data of X and Y varies together. It is a nice plot, a nice way of analyzing the data.

Now, let's look into the box plot of the data, since we already calculated the interquartile range. So I think we can use the box plot to look into the variations. So in order to plot the box plot, df.plot, and the kind of plot I'm looking for is box, and it is a nice way to get the box plot for X and Y. It's an excellent thing. What you can see here is that the variation of X and the variation of Y can be seen in the same plot, and it is very clearly visible.

The variation of X is very small, and the variation of Y is very large compared to X. And this box represents the interquartile range, the line here represents the median, and the upper and lower bounds are called the whiskers. This is about 2.7 times the standard deviation away from the mean. So anything more than this could be an outlier. An outlier is basically an extreme point, which influences the mean of the data.

So this is the graphical technique in EDA. In the next video, we will see how to code linear regression in Python. Thank you very much.

6. Simple Linear Regression - Python
====================================

See the code [here](./4.ipynb)

Hello, everyone, welcome back. In the previous lecture, we talked about exploratory data analysis: the quantitative approach, and also we looked into the graphical approach. Now, in this lecture, we will talk about the manual computation of linear regression. So we will build a linear regression manually. All right, in the previous lecture, we talked about the graphical approach and also the quantitative approach. We looked into the variance of the data, and we saw the variance of X is small compared to the variance of Y.

And also we looked into the scatter plot along with the distribution of the data, together, X and Y, what is the distribution and so on. So this is what we did. Now what we are trying to do is build the linear regression, and this is what we have taken from the previous linear regression theory; this is what linear regression is about. What we are trying to do is draw a line, and this is the line we're trying to draw, which will identify the relationship between X and Y. How to find out the values of A and B? B is the slope, which is nothing but the covariance of X and Y divided by the variance of X.

And similarly, we assume that the linear regression line is going to pass through the center of the data, the centroid, which means in this case X bar and Y bar. So we substitute in this equation, and what you get is A is equal to Y bar minus B X bar. And finally, our model equation is: my estimated value is equal to A plus B X. So this is simple linear regression. So let's see how to build simple linear regression without using any libraries. So let's look at the data first.

So this is the data I'm going to have with me: X and Y. So I am having some X and having some Y. All right, so the first and foremost thing, what I need to do is compute the covariance of X and Y and also the variance of X, and from that we can calculate B. So let's see first how to calculate the slope of the line. Step one is the slope of the line. B can be calculated by the covariance of X and Y divided by the variance of X, so we can easily compute the covariance using the formula, that is df.cov.

It will give you the covariance matrix. Let me print this covariance, df.cov, and you can see that this is the covariance matrix, and it shows like this. This value is 0.714815, which is nothing but the variance of X. This is the variance of X, and this is the variance of Y, and X and Y here represents the covariance of X and Y. So I think we already computed the variance of X and the variance of Y in the quantitative approach.

If you scroll down, we get the same value: the variance of X is 0.7148 and the variance for Y is 24.3 [unclear]. Now, what we'll do is calculate B. So for B, the first thing is we need to get the covariance from this matrix; I want to take this value. So let's say you take df.cov() and the X column; you'll get this column.

So we have X with 0.71 and we have Y with me. And in order to get Y, we take this one. So that is the covariance of X and Y, the numerator. And similarly, if you want the variance of X, I do the same thing, and instead of Y, I take X and get the variance of X. Perfect. So we got the covariance of X comma Y and the variance of X. So what we need to do here is calculate the slope: the covariance of X, Y divided by the variance of X.

Well, that's it. So print the slope of the line, B. That's it. So that is going to be equal to 4.7435. And similarly, let's calculate the intercept now, since we know that the line is going to pass through one of the points, the centroid. The intercept of the line, A, is equal to the mean of Y minus B into the mean of X. So this X bar and Y bar we already know, and we already know B here.

So we can easily calculate it. So A is equal to: we take df.Y.mean(), minus B, which we already got from this equation, into df.X.mean(). So that's it. So print the intercept of the line, and we will get A. So the intercept of the line is minus 4.539, something like that. So that's how we can easily compute the intercept of the line. So your model is ready. So let's create this model equation as a def, my model equation, and let's say I get X, and I can compute y_hat is equal to A plus B into X.

So that's it. So I can return y_hat, which is my estimated value. That's it. So we have simply calculated the model equation. For example, let's say my X in this case is three, and what is the value of Y going to be? That is equal to 9.69. So that's it. So this is what simple linear regression is all about. So what we will do now: let's try to draw a line with the scatter plot; on top of the scatter plot, we will draw the linear regression line.

OK, let's see how to draw a line here. First, for that, let's build the scatter plot, so I'm using the library here. And what I can tell you is that the X axis is X and the Y axis is Y; execute it. And if you see that, OK, this is the nice scatter plot we got here. We can also do the scatter plot with plt.plot, also, like this, with X and Y. If you use this, by default it will go for a line.

It will try to join all the data points. And if you don't want that, instead, if you want to get circles, we can use 'o'; it basically stands for the same thing, we can get it even from that. And you can change the color; I can go for a nice blue, and I can change the marker size. So this is the marker, and this is the size: markersize equal to, let's say, 20, so that I can get bigger dots; if I want, ten also gives bigger dots.

So, for example, I just want to remove the face color, change that particular one, so I can use markerfacecolor equal to white, and I can get nice bubbles, something like a bubble form. So I'll use this. And let me put an xlabel: plt.xlabel is independent, and plt.ylabel is dependent. So what we got is the x axis with independent and the y axis with dependent. So perfect.

Now, what I would do here is add the linear regression line. I can do that: plt.plot, and the x axis is with respect to X, and I want to give the Y here. For this Y, I need to compute the predicted value. In order to compute that, we will add code here: y_pred is simply the model equation of X, so you pass all the values of X, and we will predict for all the values of X what Y is, and that will be a straight line. Execute this.

And you can see the line. I'll draw a solid line here, and you can see a simple linear regression. Perfect. You can see this is what simple linear regression is about. So let me do one thing: let me increase the size. figsize is plt.figure, figsize ten comma six; let's go for a bigger size. So this is good for me to understand, and we can also put grid lines for nice visualizations: plt.grid. And what we get here is some grid lines and nice visualizations.

Perfect. So this is how you can build a simple linear regression with this equation, and at the same time you can also visualize that. And you can see here a nice visualization: these circles are my data, the true values, and this is my predicted values on the line. And of course, we can do one more thing here: instead of the line, I can give the circles, so I can view red circles, 'ro'. I can do that.

I can get the circles. So these are now my predicted values, you can see, and I can increase the circles like this so that we can get nice visualizations of this. So nice circles: I will use markersize ten, and with the markerfacecolor, set markerfacecolor to red, or I'll set markerfacecolor to white, and set the transparency, alpha. If I use alpha, I can get... We got an error. I think this is markerfacecolor equal...

Yes, you can see here all my points. What I can do is execute this one first, followed by this one for the linear regression. You can see now we can get nice circles. I'm getting those little points by density, so we can put alpha as 0.8. So the nice circles are going exactly along the line. So that's it. So this is my linear regression, with circles; these are all my predicted values.

This is how you can build a simple linear regression manually without using any libraries. You can create your own way of creating the simple linear regression. In the upcoming lecture, we will talk about how to build a linear regression using a library.

7. Simple Linear Regression - Sklearn (Python)
==============================================

See the code [here](./4.ipynb) 

Hey, guys, now let's see linear regression with sklearn. sklearn is one of the most popular machine learning frameworks in Python. It's widely used for almost all the machine learning algorithms, and every functionality is there. So now let's see how to use it to build a simple linear regression. All right, so in the previous lecture, what we have seen is that we calculated manually the intercept and also the coefficient of the line.

So it's a simple analogy: we have the equation y_hat = A + BX. So now let's see, with the help of a library, how to build the simple linear regression. So what I'll do here is take the simple linear regression now using sklearn: linear regression with sklearn. scikit-learn is the most popular framework for machine learning. OK, so from sklearn.linear_model, I need to import LinearRegression. All right. So LinearRegression is object-oriented programming, where all the functionality is inside the LinearRegression class.

So let's call this class into the model. So model is equal to LinearRegression(). And if you look into the docstring, what we have is fit_intercept; by default fit_intercept is equal to True. That is, it will calculate A, and of course we have normalize and copy_X and so on. All right. So now what I will do here is model.fit. We need to give two values:

what is X, and second one is Y. So in order to give the X here: X is the independent variable and Y is the dependent variable. So we have to define the X and Y. This is the data set which we have, df.head. What I would do is split the data into independent and dependent variables. Let me give X, my independent variable, so I can take df.iloc. And what I want here is X, and of course we can directly call df.X, but I'm using iloc in order to get the proper shape.

So what I do here is call all rows and the columns up to minus one, and convert that into values, which is nothing but converting it into a NumPy array. And similarly, y is df.iloc: I want all rows and the last column, and .values. So I can look into the shape of X, X.shape, and y.shape. And what we have is that you can see the shape of X is 227 comma one, means we have 227 rows and one column.

So we have to specifically define the number of columns in this case; otherwise your linear regression will not work. For y it is OK, but for X we have to specifically define the number of columns. The number of columns indicates the number of inputs. All right, so we have X and we have y, so what we will do now is train the model. Once these two steps are executed, the model is trained successfully. What it is actually doing in the back end is using the formula like this and calculating the values of the coefficients. Let me execute it.

So done. So the model has been fitted successfully. So let's look into the intercept of the model. In order to do that, model.intercept_ will give you the intercept, and also let's look at the slope of the line, and the slope can be found in the coefficients. So model.coef_: the coefficient will consist of the slope of the line. You can see the slope of the line here is 4.745, and the intercept of the line is minus 4.5396.

This is exactly what we calculated. You can see this is the intercept of the line and this is the slope of the line, which is exactly what we calculated even manually. But scikit-learn has many more functionalities, which can be used in many, many ways. So that is one of the good tools. OK, let's do one thing: we can use the same procedure to calculate, so let's do the predictions.

So I use this y_pred and pass it the same as before; you will get the same predictions even from this, because the slope and intercept are still the same. OK, so instead of giving a separate function, what we can do is model.predict. And if you pass the values of X, you'll get the predicted values. All right, so now let's see how to plot the linear regression from this.

All right, so I do the same thing: I'll copy this and paste it, exactly, because there is no change. So this is my data, and this is my xlabel, independent, and ylabel, dependent, and showing the grid. I'll just change the y_pred to my sklearn prediction, so that I can look into my linear regression plot. So execute, and perfect. Now you can see the excellent line, just like before.

I'll change the color, instead of red, to green. Green is also a nice color for visualizations. So these are the perfect results we got. Now let's predict: if my value of X is three, then what is the value of Y? In order to do that, we can directly pass the value of three here. If you do that with the library, you'll get an error. It says you need to give the proper shape, which indicates that you need to specify the number of columns. So for that, we'll take a test variable, and let me create an array.

And what I'll do here is take an array of three and reshape it into this form so that it's easy for us. Reshape into minus one comma one. So what you'll get is the reshape into one by one. All right. So we'll take this test, and in the place of three, I'll put this. And the value I got is in array format: it is 9.69. That is exactly the same.

Right. If the independent variable is three, this is the predicted value, and it is equal to 9.69; that's exactly what we got, exactly the prediction. So it's just simple mapping: we have the line and simply map to it to calculate the dependent variable. OK, so the same thing follows in the manual calculation also. So this is all about linear regression in sklearn. In the next lecture, we will see linear regression with statsmodels.

Thank you very much.

8. Simple Linear Regression - Statsmodels (Python)
==================================================

See the code [here](./4.ipynb) 

Hey, guys, now let's see how to build a linear regression with statsmodels. statsmodels is also one of the most popular machine learning frameworks, especially to build statistical models. So let's see now how to build a model in statsmodels. OK, so I'll create a text cell now: linear regression with statsmodels. OK, so in order to do the linear regression in statsmodels, it is defined as the ordinary least squares regression, also popularly known as OLS.

So we'll use this function, ols, to calculate the linear regression. How to do that? We will see. First thing, import statsmodels: we will take import statsmodels.formula.api as smf. What we're doing here is importing the library statsmodels.formula.api as smf. All right, I imported this library. So in order to build a linear regression here, we will represent it with ordinary least squares regression, popularly known as OLS.

So that is the functionality we are using to calculate the ordinary least squares regression. In order to do that, we have smf.ols; this is the ordinary least squares regression. You can check: this is the simple ordinary least squares regression, and we can do it simply with a formula. We are just writing down the formula here. OK, so what is the formula here? Let's look at the data here: df.head. So this is my data, and what we have is that X is my independent and Y is the dependent.

So in order to write the formula here, the first thing we're going to give is the formula. The formula for our case is Y, which is my output, and tilde; tilde indicates from where you want to predict the output: from X. That's it. That is the formula, with the column names. For example, the column name for the target variable is Y, and the column name for the independent variable is X.

So that is what we can put: Y tilde X. If we have different column names, you put the column name of the target variable, and so on. And then we pass the data, and the data is df. That's it. Then .fit(), which will actually fit the model. So what I'll do is model_sm, and this time I'll use this smf, which is nothing but my statsmodels. And if we execute this command, the model has been fitted successfully, which will calculate the intercept, and we can do more in this case.

It will also calculate the coefficient significance by applying the t-test, and the model significance for the F-test, and also calculate the R-squared value and give it to you. So model_sm.summary(). If I do this, you can see this is the output we got here: the intercept is minus 4.5397, the same exactly. And the X is 4.7435. And this is the standard error and the t-value and the p-value and so on.

And this is the R-squared value for this model, and the F-statistic, nothing but what we calculate from ANOVA, analysis of variance, and the probability of the F-statistic is this, and so on. All right. So what we will do now is calculate the predicted values here. scikit-learn has very good functionalities; statsmodels has very good functionality of giving you the model and also the p-values and all sorts of predictions.

So if you want to predict, like with scikit-learn, from statsmodels: model_sm.predict. So you can straightaway give the inputs; basically it asks you to give the independent variables. For example, I want to calculate what the output is for the value three. We saw that in the model done manually and also in scikit-learn. But of course you will get an error saying that the object has no [unclear].

It basically looks for the data; it generally looks for a data frame. So what you do here is create a data frame, pd.DataFrame, and we need to pass a list within a list: I'll create the value three in a two-dimensional list. So it is a two-dimensional list. And what do I have to do? I need to specify the column names.

The column names should be exactly equal to the column names of your training data frame. In this case it is X, so we have to pass X here. So let's print this. OK, oh, it should be passed in a list here; the column name should be passed in a list. Now you can see this is the list of values we got for X. So this is my test data, and if you want to test it, you have to pass this test data.

So model_sm.predict. Now you can see, perfect: the value you're going to predict is 9.69. All right. So like this you can predict. And let me do one thing: let me take the fitted values. This is the terminology used in statsmodels. So fitted_values = model_sm.fittedvalues. Basically these values are the values that are fitted; this is the value that is fitted, or the predicted values, almost the same. So execute.

So that's it. So this is how we compute the values on the line. So if you plot, you'll get the line. So what I'll do here is take the same code; I'll copy and paste it down here, and that's it. You can see plt.plot of X and Y; this is basically the scatter plot. And for the linear regression, instead of y_pred_sk, I'll go for the fitted values, and here also fitted values, and I can go for a different color; this time I'll go for magenta.

It's also a nice color for presentation. So I will execute it, and perfect. You can see this is the line, and the magenta color is nice, and this is the linear regression, and the circles are basically my predicted values and the true values. So that's it. This is how we are able to calculate the simple linear regression with statsmodels. statsmodels is also one of the most popular and powerful libraries to build statistical models.

In order to study more about the results and the hypothesis testing done in the report from statsmodels, I refer you to my blog; you can check the link here, which will give you information about the hypothesis testing: the t-test for coefficient significance, the F-test for model significance, how the p-value is calculated, the degrees of freedom, etc. You will be able to find that in our blog. This is the blog for hypothesis testing, where you can see how the test is done for significance, what the p-value is, how you can define the critical value, and the null hypothesis and alternate hypothesis.

And also, we talk about the distribution and analysis of variance for the model significance. So in order to have more information about how these values are calculated, you can refer to this blog, which will help you understand it in a better way. In the upcoming lecture, we will talk about evaluating the simple linear regression using SSE and also the R-squared value. Thank you very much.

9. Model Evaluation - R^2, ANOVA
================================

![100.png](./images/100.png)
![101.png](./images/101.png)
![102.png](./images/102.png)
![103.png](./images/103.png)
![104.png](./images/104.png)
![105.png](./images/105.png)
![106.png](./images/106.png)
![107.png](./images/107.png)
![108.png](./images/108.png)
![109.png](./images/109.png)

Hey, guys, welcome back. In this lecture, we'll see how to evaluate your linear regression. So let's see, step by step, what we have done. We have the data, and this is the scatter plot for my data: X is the independent variable and Y is the dependent variable, and this is the scatter plot we have, with respect to X how my Y keeps on varying. Now, the samples we have are all the true samples, represented with the circles, and the variance of the true samples is represented by the sum of squared total.

SST indicates the total variance in the true samples. So how to calculate that? SST is the sum of Y minus Y bar, the whole square, which represents the total. And if you really want to calculate the variance, you divide it by the number of samples; that internally talks about the variance of the data. And next, what we did is we built the model, and by building the model we calculated the predicted values. So these are all the predicted values; these red samples are the predicted samples.

And you represent the variance of them with SSR. SSR is basically the sum of squared regression, means the variance that was explained by the regression model. And if you join all the dot points, you will get a straight line. So that's basically what the linear regression line does, joining all the points; you get this. But internally we are actually interested in this: the blue samples are the true values and the red samples are the predicted values, and you can see the red samples are not exactly matching.

Maybe there is some error. So we can define the error as SSE, which is nothing but the variation in the error. So the error can be defined with the true samples Y and the predicted samples Y hat: Y minus Y hat, square, which will give you the error. So if you build a linear regression model or any regression model, the SSE should be as low as possible. Generally, the lower the value of SSE, the better the model. So ideally the value of SSE should be equal to zero.

But that's not what happens; if that's the case, there could be the possibility of overfitting. But the lower the value, the better the model. And if you calculate the mean of all these things, that is called mean squared error. Mean squared error is generally used by people as the notation to calculate the mean of the error, since SSE gives you the total information, but instead it is the average of the error, which is the representation: MSE is equal to SSE divided by N minus K minus one, which generally is the degrees of freedom,

where N is equal to the total number of samples and K is the number of independent variables. In our case, K is equal to one, since we have only one independent variable. And the next one is that MSE only gives you the magnitude of the error, but if you want to represent that on a zero to one scale, we can go for the R-squared, also known as the coefficient of determination. Basically, R-squared is a good statistical measure.

And it'll give you how much variance is explained by the model out of the total samples, what is the variance that is being explained by the model. So that's what R-squared will tell you. So R-squared is equal to one minus SSE by SST; the closer the value of R-squared is to one, the better the model and the better the fit of the model. In the upcoming lecture, we will see how to do the model evaluation in Python.

Thank you very much.

10. Model Evaluation - Python
=============================

See the code [here](./4.ipynb) 

Hey, guys, now let's see how to evaluate a linear regression in Python. All right, now let's see how to evaluate this model. As you can see, you can take whichever model you want, because the results are more or less the same. So what I want to see here is how good my model is and how good my results are. What I can do here is test my model with parameters like mean squared error and R-squared. So, model evaluation: what I'm looking at here is SST, sum of squared total; SSR, sum of squared regression; and SSE, sum of squared error.

And after that, I'll calculate the mean squared error, and finally calculate the R-squared value. So this is our agenda for the model evaluation in this lecture. Now, let's start with SST. Before that, let's look into our data. So this is our data, and SST is basically the variation of our target variable. So for this data, what is our target variable, and what is its variation?

What is the sum of squared variation is what we need to calculate. So first thing, what we will do here is create a function, sum_of_square. This is a function, and let's say you have a variable, y values; this is for the Y values. What I want to do here is calculate this; the value could be a pandas Series, or it could be a NumPy array or a list of values, whatever. So I'm assuming that the input could be a Series or a NumPy array.

So for that, the first thing is to calculate the mean of Y, because I need to calculate with respect to that. So for that I can calculate np.mean of y, which gives the mean value for me. And what I'll get here is the sum of squares, and we can calculate the sum of squares something like this. So how to calculate that? That will be equal to y values, this is the Y value, minus the mean of the y values.

So this is the difference, and for this difference, I need to calculate the square, and sum up all of these, and return the sum of squares. So that's it. So this is my SS, the sum of squares. If it is total, then it is the sum of squared total; if regression, that will be the sum of squared regression. That's it. So if I want to compute SST, that is going to be equal to sum_of_square,

and what I'll do here is pass the true samples, and you can print SST, the sum of squared total. The total variance in the data is 632. That's it. And similarly, what is the variance explained by the model? The variance by the model is SSR. So instead of y, this is the predicted value, my fitted values; take the fitted values, and this is my SSR. So this is my sum of squared regression.

Perfect. Now we can see the total variance explained by the regression model is 418, whereas in the data it is 632. Perfect. Now, what is my SSE? SSE can be defined simply by SST minus SSR: out of this total variance, what is the variance that is left out. So this is the total variance and this is the variance given by the regression model, and the difference will be equal to the sum of squared residuals, or else we can also compute SSE directly, the same way.

The first thing we need to calculate here is the error, and it can be defined as df.Y, the true values, minus the fitted values. You'll get the error. And for this error, what we can do here is square the error, and for the squared error, I can sum all the errors, and what I'm getting here is SSE. You can go for the top one or you can even go for the bottom one; the results will be more or less the same.

So we can print SSE and print it directly; that will be equal to 213. And of course, obviously, SST minus SSR is also equal to 213; you will get exactly the same values with respect to this formula or using this formula. OK, so that is how we compute the three variances. And the next thing we will do is compute the mean squared error, MSE.

Mean squared error is nothing but MSE is equal to the sum of squared error divided by N minus K minus one, where N is equal to the number of samples, that is len(df), and K is equal to the number of independent parameters, that is equal to one, the number of independent variables. So you'll get MSE; print MSE, and that will be equal to [unclear]. So on an average, the square of the error is [unclear].

This generally gives you the magnitude of the square of the error. The lower the value of MSE, nearly equal to zero or less than one, means that this is a very, very good fit. Of course, the results are good. But in order to give the magnitude in the range of zero to one, we can go for the R-squared value. R-squared talks about the explained variance.

So what does explained variance mean? We have a total variance in the data of 632, but the model explained 413. So that is the explained variance. So R-squared we can calculate: R-squared is equal to SSR divided by SST. That's it. So out of this much variance, the model is able to explain this much. So print R-squared; that is going to be equal to 0.6616, that is your R-squared value. And this is exactly what you got when you ran statsmodels; we got the R-squared there, which is 0.6662.

So if you want to know more about this, how the F-statistic value is calculated, I want you to go to our blog. I explained each and every thing there, like calculating the F-statistic for model significance, and also the hypothesis testing on the coefficient significance and all of these things. Everything is computed with the data; check out our blog for details about how to calculate all these things.

So that's it. This is how you can build a simple linear regression. In the next lecture, we'll talk about forecasting with the regression model, and we will discuss the additive model and multiplicative modeling for forecasting. Thank you very much.

## 7. Regression for Time Series Forecasting

1. Regression with Time
=======================

![110.png](./images/110.png)
![111.png](./images/111.png)
![112.png](./images/112.png)
![113.png](./images/113.png)
![114.png](./images/114.png)
![115.png](./images/115.png)
![116.png](./images/116.png)
![117.png](./images/117.png)
![118.png](./images/118.png)


Hey, guys, welcome to this module on forecasting time series data with a regression model. In the previous module, we have seen how to train a regression model with the data that was provided. In order to train on time series data, the regression model is actually a function of time. So in this case, we take the time, and with the time we are going to predict the future. So on the x axis, the independent variable, what we have is time. And the dependent variable is the thing you want to predict, like the sales or whatever you want to predict.

So we can predict that value. Let us consider the data here. In this case, you can see I'm having data for years, and also the respective sales. OK, the years are actually the independent variable, and based upon the year, we are going to predict the future sales. If I draw the scatter plot for that, this is how the scatter plot looks, and what I did here is that I joined each and every data point and got a line plot. On the x axis,

you can see it is the time, and the y axis is the data. The data we have is from 2001 to 2005, and it is [unclear] years of data. And what you can see here clearly is that the data increases with respect to time, and there is a clear seasonality behavior you can see. It increases at certain times and decreases at certain times. There's a clear seasonality effect in this data, which you can observe by looking into the graph.

So let's do one thing: let's take this data and try to fit a linear regression. If you want to fit a linear regression, the independent variable is time and the dependent variable is the sales. So we take this data and try to fit a linear regression. If we fit a linear regression, this is how the linear regression looks: it's going to fit a straight line. And this line represents the trend in the data. So it's very easy, right?

We can read the trend in the data with the help of linear regression. And if you want to predict the future, the forecast values, what we will do is simply extend this linear regression line. And this is the forecasting we got, and whatever you can see here is our confidence interval of the forecast: the forecast could be in this range. This is the mean of the forecast, but the actual value could be in this range.

So the observation you can make in this linear regression is that linear regression is able to fit a linear line, but it is unable to capture the seasonality effect. We are not able to find out where it is increasing and where it is decreasing. So that is one thing we can see. And one more thing is that when forecasting, the margin of error is very high; you can see you're getting a very, very high margin of error; your data could be anywhere in that particular range.

So this represents the margin of error and the confidence interval, and the confidence interval is mu plus or minus the margin of error, where mu is nothing but the mean, the line. The orange dot is the mean, and the rest all represents the margin of error. In the upcoming lecture, we will see how to fit a linear regression with respect to time in Python. Thank you very much.

3. Data Preprocessing in Python
===============================

See the code [here](./5.ipynb)

Hey, guys, welcome back. In this lecture, we will see how to do the forecasting with regression. I am in the Google Drive now, and this is the data I'm having: some sales data with me. This is the sales data; let me open it. Yes. So I'm having the years with me and also the sales with me. So everything is there. What I want to do here is fit a line, the linear regression, for the years and the sales.

OK, let's see how to do that in Python now. The first thing I will do here is open the Google Drive and open my Google Colaboratory. Let me set all the necessary settings, like setting the path and so on. All right, so next I connect to the Google GPU. Before that, let me import the necessary libraries: import os, and from google.colab import drive, and drive.mount.

So I mount the drive and execute it. It asks me for the URL like this; select the necessary email address, and click Allow. All right, copy this code, paste it here and execute. So, done. We have mounted our drive successfully. The next thing is that let me change the directory, and you can see I was in My Drive, complete time series, and forecasting with regression.

So this is the folder I was in. So let me set os.chdir: /content/drive, My Drive, complete time series and finally forecasting with regression. So that's it. So this is what we are trying to do now. So let me check whether I am in the respective folder. And let me change the name of the notebook: it is regression with time. So this is what I'm doing now. So let me minimize all of these things now.

So let me check with ls. OK, maybe it takes some time. OK, so what I want to do here is load the data first. So in order to load the data, let's import all the necessary libraries: import numpy as np, import pandas as pd, and from matplotlib, pyplot as plt. So the three libraries, and import also seaborn for visualization, as sns. So let's include all the libraries for the visualizations and execute.

Now, let's load the data. If you look at the data, it is my sales data file. So I will read the data with pd.read_csv; it was in my data folder, and it's my sales_data.csv. df.head gives you the data, and also look into df.info to check what kind of data it is: the years is an object, and the sales is float values, but the years are in the object format.

OK, so the first thing, let's do some basic pre-processing of the data, the basic pre-processing that I need in order to build the linear regression. The problem is that we can't fit the data with the years directly; we need to give each and every year, or month or whatever, a specific number. For example, I represent that with one, two, three, four, five, six and so on. And this is what basically I have to represent here.

And the next thing is that sometimes I need to model some kind of seasonality effects. So I need to convert that into what kind of month it is. For example, this is January, this is February, this is March. Those kinds of information I need to extract here. So I would like to do all these things; those two kinds of information are quite useful. So the first step is I'm going to take these years, and from the years, I'm going to create the numbers.

I mean, I just assign a unique number for each and every date. And at the same time, from the years, I'm just trying to extract what month it is. In order to do that, the first thing I'd like to do is change the data types. Object is not useful for us, so we need to change the data type to datetime. So let's see how to do that. OK, one more indication of what we can see here: there are 72 entries. Probably you can see here it is 2001,

January first, and this is the sales that was observed, then 2001 February, and so on. So there are seventy two months of data. It's approximately six years of data or information. All right. So that's one thing you can keep in mind, and we'll come back to this later on. All right. So what I will do here is some data pre-processing.

So the first step, I will convert this object into datetime. So that is my years, and I need to convert that into pd.to_datetime: just convert that into a datetime format. And df.dtypes; execute it. Oh, this is what we got: I've got dtypes, which gives you the data types, and so we have the data type as datetime64.

Great. So we have converted that into this format, so it is very good. Now the next step, what I want to do here is assign a unique variable for this. For example, for each and every date, I need to assign a unique label: this is one, this is two, this is three and four and five and so on. OK, so in order to do that, it is quite simple. Using NumPy we are able to generate the values between one to 72.

That's very simple: np.arange. I'll use np.arange: I can take a list of values, start from one, stop at 73, and the step is one. And if you print all these values, you'll get all the values like one, two, three, four, five, six, up to seventy two. So why did I do 72? Because for each and every month I need to give a unique value. How many are there? There are seventy two entries.

So that's why I created seventy two. So simple: now I'll take df['time'], and this time is equal to this; I represent the time with respect to this. So this is the time: time one, time two, time three, four, five, six, seven, eight, nine. These are more or less like the months, but the models will not consider dates directly. So that's why we have considered this kind of format. So let me execute it. So we have successfully saved our time into the df.

We can see it's perfect. And the next step, I will extract the month here. We will use the month later on in this module, but at the moment, let's prepare our data so that in the upcoming lectures we can use the same data here. OK, the first step, I will do df['month'], which is my month name. We can use the data frame, which is a powerful library, where we are able to extract whatever time component we want.

I mean, whatever format of representation you want, you can easily extract. Let's do one thing: here, from the years, I need to extract the month name. So df.Years.dt.month_name(). This is what I can do here; execute it. Now df.head, and what we can see here is that the years and sales are there, and time and month. Let me give head(15). You can see for each and every year I can easily extract the month: January,

this is February, March, April, May and so on. You can see the months keep on repeating after twelve, and this is January again; all the months keep on repeating. It's one of the excellent ways of representing your data.

4. Splitting Data into Training and Testing Sets in Python
==========================================================

See the code [here](./5.ipynb)

Hey, guys, welcome back. And now let's see how to build the linear regression. What we have here is that I'm having the time with me and I'm having the sales data with me. So this time is my independent variable and the sales is my dependent variable. We will use the month later on in these modules; at the moment, we will build a simple linear regression, where X is my time and the sales is my Y. So let's do that. What I'll do here is split the data into independent and dependent.

OK, there is a small thing I need to add here before splitting the data into independent and dependent. Step number one is basically that I will split the data into train and test, because ultimately I want to test my model, how good my model is. In order to test that, I need to split the data into training and testing, because I want to predict the future values, and predicting the future values is always difficult.

So in order to do that, I need to test the model, how well this new model performs. So for training, since I'm having six years of data, I'll consider four years of data for training. And for test, I'll take two years of data, and I will test how good my model is. So this is df, and in this data I'm having six years of data, so I'll take the first four years.

So that would be forty eight. Forty eight will basically display the first four years of data. So this is the first four years of data. You can see up to 2004 December 1st. And the first value we have is from January first, 2001. So this is my training data, so I'll name this df_train. And similarly, in order to get the test data, df_test, I need to consider the data after

December 1st, 2004. So in order to do that, you can check the index here. The index is basically 47. So I need to take the index after forty seven here. So for that, I'll take iloc and I'll take from forty eight, because I'm starting with forty eight, and so that's it. So the train is the first four years of data, and the test is after that, the last two years of data.

That's it. So you can see here by looking into df_train.tail, which will give you the last five rows, you can see the data up to December of 2004. And let me take the head of my test data, which will actually display the top five values, and you can see these are the top five values we have in the test data. So this is the data we have.

Now let's split the data into independent and dependent. So let me put that here. All right, so now coming to the splitting part: X is basically my independent variable, so instead of X, I'll take X_train. X_train is basically for the training data; I need to take the time here. So that's so. But just keep in mind: if you take this and put .values, what happens is the shape; you will generally lose the shape.

But in order to build a model, you should use the proper shape here, since we're using the scikit-learn library to create the regression. But if you use this, you lose the shape. So in order not to lose the shape, what I would do here is take a data frame, and for this data frame, convert that into values, and look into the shape. So now you don't lose the shape. So you are getting 48 values and one column, which indicates that we have one independent variable.

So that's it. So similarly, let's do it for y: y is df_train, and what I want to predict is the sales; that's my output. So convert that into values, execute. Perfect. So we have y; I'll take this as y_train, and that will be good. So let me take the shape of y_train. And you can see it is fine, because for y we don't need to specify the number of columns.

5. Train Regression Model with Time in Python
=============================================

See the code [here](./5.ipynb)

So what I'll do here is the linear regression with respect to time. So what is linear regression with time? Basically, linear regression will actually give you a straight line, and this straight line you can represent as the trend in the data. So we are actually calculating the trend in the data. So to do that, let's quickly do: from sklearn.linear_model import LinearRegression.

Now execute. model_trend, this trend model, is equal to LinearRegression(). And let me fit the model: model_trend.fit, and what do you want to fit? It is X_train comma y_train; that is what you actually want to fit here. Execute. The model has been trained successfully. So what we do here is take the fitted values. Let me do the fitted values: it is model_trend, which is my predictor:

model_trend.predict, and you predict X_train, and this is y_fitted_values, OK? And this is y_fitted, basically the fitted values from model_trend. Perfect. So we got the fitted values and we got our data; everything is set. And what I will do here is that I want the test data too, to evaluate our results; I want to test it too. So I'll copy the same and paste it here.

So instead of X_train, I'll take it as X_test, and y_test. So this is my X_test and this is my y_test, and this is the test data. Perfect. So we can simply get the training data as well as the test data. So everything is ready, and we also got the data. So this is the data we are having.

6. Forecasting with Confidence Interval and Visualizations in Python
====================================================================

See the code [here](./5.ipynb)

Now, what we will do is visualize our data. Of course, we should have done it at first, but since we already saw the data in the previous lecture, in the previous slides, I'm not going into that. So now let's visualize the data here, because I'll put everything into one place for visualization. Basically, we need to do this immediately after step one, splitting the data into train and test.

So immediately after this, we need to visualize the data, but I'm doing it here. It's not an issue, because I want to put everything into the same plot. All right. So the first step is that we will draw the line plot here. So we will plot X_train comma y_train; this is the line plot I'm just trying to draw here, and you can see the x axis is basically the time, the time in numbers.

So instead of this, if you want to get the year, the time information, you can use df_train.Years, which you can use for the years. So I'll use the years at the moment. You can also take X_train, but I'll take the years; that's good for me. OK, now you can see here we get df_train.Years with the y_train. So now you can see you'll get a nice picture like this. Let's do one thing: let me increase the picture size with plt.figure and figsize.

So the figsize is basically ten comma six: width is equal to 10 and height is six. That's fairly fine. So what I'll do is use some markers, maybe; I'll use the marker 'o', and I'll use the dotted line, so this is what it looks like. This is the data I'm having. This is one of the coolest; that's really cool. So you can see this is my four years of data, starting from 2001 to 2005; this is the training data.

We have a nice trend, everything which we already saw in the previous lecture. So this is the data, and how we actually build it here. All right. So next, what we did here is basically create a line: we create a plot with df_train, and this is the years, and for the years, basically y_fitted_values. All right. So these are the fitted values, and this is a nice line.

I'll do one thing: I'll represent this with the same color, blue, and also change this into blue. So this blue line basically represents the fitted values, the fitted values of the linear regression. All right. So this is how we can plot the trend. So what I can say here is plt.legend; I use a legend here. And the first one is the true samples.

The first one is the true data, our time series data, and the second one is the trend line. So that's what we can see here: this is the time series data and this is the trend line. All right, that's a really, really good thing that we can do. But I just want to do the forecasting here. So in order to forecast with the model, we have the forecast data.

This is the future data. And let me also plot the future data here. So this is for the forecasting data. OK, so I'll use plt.plot again; instead of the train, I'll use the test, and this is my test, and I'll use a different color. Orange is the color I'll use here. OK, maybe I'll use the color red; red color is a good representation. So you can see this is the forecast, and this is basically my forecast period.

OK, what I'll do: I'll use this orange color; the color red is dominating. Orange is good. So this is orange color. Now this is my forecast period data, the true data, the true forecast data. So I'll put it here: this is my true future values, true future data. So that's the trend observed in the true future data. And now I just want to see how the model is working, how the model is really predicting.

Basically, you can see linear regression will basically do it by extending this line. That is the only thing it will do. So let's see y_forecast. y_forecast is model_trend.predict, and we are predicting with X_test; X_test consists of the numbers. So that's y_forecast. That's it. So we have the forecast data. So what we will do is plot this forecast data here.

So we will try to plot the forecast data, y_forecast, the forecasted data. It will just keep extending this line. This is the forecast: it just keeps on extending this line here, and this is the forecast data we're having. All right. So I'll just change the color: let me give the color red. So this red line is basically my forecast values. You can see here how exactly you are going to predict.

This is the prediction for that. So what you can observe here is that it is simply extending the straight line, but it's really not capturing the seasonality effect, which is actually the biggest loss you get with linear regression. All right. So let me put the name here: this is my forecast, forecast trend. Of course, we calculated the trend, and this is the forecasting trend.

But this trend itself is not really enough to forecast, as you can see here. All right, so we can do one more thing in the visualization. This is basically what the linear regression is saying, and what could be the confidence interval, what could be the range? That is basically called the margin of error. So we will calculate the margin of error. The margin of error is a concept that comes into the confidence interval.

So the confidence interval basically talks about what the margin of error is in your predictions. So in the future, what could be your margin of error? So let's say this is the linear regression line in 2006; this could be the sales, but what could be the real margin of error, what could be the real range of values? That represents the confidence interval. So basically the equation of the confidence interval is mu, the mean, plus or minus the margin of error.

And this margin of error can be [unclear], because there are a lot of equations here, right? So my confidence interval is basically the formula mu plus or minus ME. CI basically represents mu plus or minus ME, the margin of error; ME represents the margin of error. So that's what it generally represents: mu plus or minus the margin of error. All right, so just try to understand: mu plus or minus the margin of error, where the margin of error is represented by Z into the standard error, SE.

SE basically represents the standard error, which is nothing but the standard deviation of the error. That's what the standard error represents. All right, so Z could be any value, depending on what margin of error you want to represent. So let's say I'll take Z equal to two, or two times the standard deviation; or if you want the confidence interval for ninety five percent, then the Z value will be equal to 1.96.

Generally, it is two times the standard deviation, but more precisely, it is 1.96. So I'll take Z is equal to 1.96 for a ninety five percent confidence interval. If you want the confidence interval for ninety five percent, then what you need to do is take the Z value equal to 1.96. All right. So this is what we have now, and we have all the values: margin of error, standard error and so on.

So what we do basically is calculate the margin of error. In order to calculate the margin of error, we are taking Z equal to 1.96, but we need to calculate the standard error. Basically, we will do it for the training data. In this case, you can see the straight line is the prediction, and the blue dots followed by the dotted line are basically the true values.

So the first thing we can do here is take the error. The error is basically equal to y_train minus y_fitted. That's your error. So we got the error. For this error I need to calculate the standard deviation, which is nothing but the standard error. So SE is basically error.std(), the standard deviation of that; I'm getting the standard error. So perfect. So now we go to the margin of error. The margin of error is 1.96 into the standard error; 1.96 is purely because of the 95 percent confidence interval.

So execute. So that's it. So we got the margin of error. So this is the error that this line basically follows. So what I will do here is fill it with some colors, to fill the margin of error. So I can use plt.fill_between, and what is the x axis? I'll use it for the test data. So this is my x axis, and what is your y axis?

What is the y where you want to put it here? All right. So basically we need to give the confidence interval, right? So CI is basically the mean plus or minus ME. So in order to do that, I'll give this: this is the plus, y_forecast plus ME, and the minus, y_forecast minus ME. That's it.

So what we got here is CI plus and CI minus, basically the confidence interval. So this is for plus and this is CI for minus, the negative. And that's what you can do here. And alpha: just set alpha equal to 0.1, so that it has as much transparency as possible. So you can see that's my confidence interval. I can set the color, and the color can be equal to, maybe, black.

Color is equal to black. And you can see how exactly my confidence interval varies. That's really cool, right? You can see this is how the error actually follows. And what you can see here, this is the true data, and so on. So I'll put one more thing here in the legend: this is my ninety five percent confidence interval. So the ninety five percent confidence interval is basically represented by this, with respect to the model.

And this is how the ninety five percent confidence interval is represented. So this is how you are able to forecast with simple linear regression, and at the same time you can also set the margin of error. So what you can see here is that in 2006, this is the predicted value, but the true value could be in this range. For example, let's say you want to predict for 2006.

So let me take this forecast data here, X_test. For example, from the test data, let's randomly pick one number from this data. OK, for this data, what is your forecasted value? The time number is sixty one, and the forwarded value here is [unclear]. So this is the true data and all of those things. So how is your model going to work here?

So in order to do that, I need to give it to model_trend, with the time number, because this is the number we have, and predict; you already know how to do the prediction. We need to put it in double square brackets, because you need to represent it in the proper shape, and convert it into an array, because we are completely working with arrays. So that's what we have as the predicted value, and this is my forecast mean.

All right. So the real value lies between the confidence interval: plus and minus. So probably I'll put the minus first: the data minus ME and plus ME, comma. OK, so your real values basically lie between this. Oh, I'm sorry, this is already values there; I think just only minus ME and plus ME. And this is where your real data lies. So let's print the mean.

The mean is basically the forecast mean, but your true values will lie between these forecasted values; it's going to lie between this range. All right. You can see if you want to predict it for 2006, the true value is basically four hundred and thirty one. And my model predicts four zero three. But the true value could be in a large range: the true value could be in the range of two nine six to five one [unclear]. This is where your true value lies, and this is the confidence interval.

All right. This is how you are able to predict using simple linear regression. This is how you can predict future values, forecast future values, using simple linear regression.

## 8. Additive Time Series Model with Statsmodels

1. Additive Model
=================

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


Hey, guys, welcome back to time series forecasting with regression. In this lecture, we will talk about the additive model for forecasting, which is simple: we are adding up the seasonalities. So let's look at the observations we made in the previous lecture. In the previous lecture, we simply built a linear regression to forecast the future, and we also built that in Python. And one thing we observed in building the linear regression is that it only draws the trend line, but did not capture any seasonality effect.

OK, let's take a closer look into the seasonality part. If you look into the data, whatever data you have, if you observe the data, it has some kind of seasonality. Seasonality in the sense that the pattern is repeated. This pattern is repeated: you can see here, from here the pattern is repeated, and again, the pattern is repeated. It may not be an exact match, but at least you can see something like an 80 percent match in the pattern, and it is repeated from 2001 to 2002.

If you see, this is the pattern you can observe, and from 2002 to 2003, again we have an increase and a decrease. And again, from 2003 to 2004, the values have increased; and at the starting point again, it decreases, and so on. So what I will do here: let me color each and every dot; I'll give it a color, and I assign the month name to it. If I assign the month name to it, this is how it looks.

And if you see, this is the same plot, the same thing applied, but here I colored the dots; I colored the circles based upon the month. For example, January is red in color. You can see this is January, again January, January and January, and probably this was January, maybe somewhere up here. So that's what you can see. And also, if you look into the cyclic behavior from January to January, this is one cycle; again, one more cycle from January to January, and probably again you can see

the cycle is repeated. The cycle is repeated from January to December. So every 12 months a cycle is repeated. That kind of behavior is called cyclicality or seasonality: we can observe, like in quarters or every year, a cyclic behavior. Every year I have a seasonal behavior. Such a component is called the seasonal component, and our regression model is not able to capture such kinds of information. So these are all the observations we have now: the trend increases, and there are certain months where the sales are lower, and certain months where the sales are higher. Probably in February, March, or October, November, December, we have a group of months

where the sales are low, and they are also in a region that is low. And in another group we have higher sales, like June, July, August and September; we have really, really high sales. So that is basically the seasonality. You can observe that the seasonality is clearly every 12 months: every calendar year, the cycle is repeated. So those kinds of observations you can understand in this graph. Now, in order to include the seasonality component into the linear regression, we will use one of the techniques, the additive model. The additive model is simple:

we are adding up the seasonal components to the time. So our additive model is basically a multiple linear regression where we add the seasonal components. So previously we had Y hat is equal to A plus B T; this is the simple linear regression we had, built only with respect to time. Now I add some components called the seasonal components: they could be X1, X2 and so on; X1 could be January, then February, March, April, May and so on.

So what we are actually trying to do is create dummy features, dummy columns. And there is a standard: if there are N categories, we need to create N minus one dummy columns. That's why we have N minus one dummy columns in this model. So this is basically what the additive model is all about. Let us consider the data and see exactly how we try to build it. Step one, we need to do the data processing.

As we know, this is the data we have used, the years and the sales data, and from there we extracted the month name also, and we extracted the time. In the simple linear regression, we used the time to predict the sales; we used the time component to predict the sales, whereas we have not used the month. Now, what we are trying to do here is use this component. If we use this component, what we will do is create N minus one dummies.

Basically we are creating dummies. So these are the dummy columns you can see: August, December, February and so on; these dummy columns are all the seasonal components: January, February, March, April, May up to December. So we will create N minus one, which means 11 dummy columns, using the one-hot encoding format. What is one-hot encoding? If January is present, we have one and the rest will be zero; that column is one and the others are zero, and so on.

All right, so this is how you're going to create the N minus one. For example, in this case April is dropped; the month is not there. So if you get April, since there is no April column, the rest of the things are equal to zero, and that component is going to be added into the intercept of the line, that is, A. So this is the equation of the additive model: Y hat is A plus B T, and the rest are all my seasonal components: B2 into August, and so on to December.

And these are the things that we have used before. So this is the equation of the additive model. If you build this multiple linear regression and plot it, this is what we are able to fit: instead of fitting a straight line, we are able to capture the seasonality here. This is a nice way of fitting the multiple linear regression. If you add those seasonal components, this is the nice fit you get, and if you want to do the forecasting,

this is the forecast. So probably this is actually the behavior of the data you can see after this, and this is the behavior of the data you can observe here. This is the orange line, whereas the filled part is the confidence interval. So it's a nice thing: instead of giving you a straight line, it gives you the confidence interval as well. If it captures the seasonality as well as the trend, that will be a really, really excellent model.

So this is all about additive modeling and forecasting with additive modeling. It is one of the excellent ways of doing this. You can simply do this once you know the number of seasonal components, and this is how your model is; then the additive modeling approach is very good to go. In the next lecture, we will see how to build the additive model in Python. Thank you very much.

3. Data Analysis in Python
==========================

See the code[here](./5.ipynb)

Hey, guys, now let's see how to do the forecasting with the additive model in Python. All right. In the previous lecture, we talked about the simple linear regression, and this is the output we got. You can see this is the output, and the fit is just simple linear. And also the forecast is just an extension of this line. And whatever filled part you can see, this part is basically the confidence interval, or margin of error.

Now, let's see how to build the additive model. This is the data we're interested in. So we will take the train data and the test data; we already used them. We will take this train data and the test data, and for this train data and test data, we will do the regression, the additive modeling. All right. So let's get ready. Click on this text and type additive model. The additive model is basically adding up the seasonalities.

You're just adding up the seasonality. So let's take df_train, the train data. So we have the train data, and we already have the data preprocessed. We've already taken the time; we've already taken the month. We already got the time as well as the month. So what we need to do here is create the dummies for the months; we need to extract them. Before that, let's start with a basic visualization, so that you can understand much better how exactly we are able to see the seasonality here.

All right. So first step, we will draw the scatter plot. We will draw the scatter plot with df_train; this is my training data. And I would take the time component as my x axis, and the sales as y. So this is basically the scatter plot... All right, we got some error. Yeah, properly: X and Y, this is df_train. All right, so this is how it looks, OK, and you can take plt.plot.

And if you take the same values on the x axis, df_train.Years, the years, and if you want the blue lines, this is how you get it; I'll go with the dotted lines. That will be nice for me. So this is just joining each and every point. This is how it looks for me. All right. Let me increase the size: plt.figure and figsize, and I'll take this to 15 by eight. So this is the way to look at the big plot now. So this is quite true.

All right. So what I will do now is color it. Instead of the plain scatter plot, let me color according to the month, according to the monthly values. To do that I can use seaborn's sns.scatterplot. We have that plot there. So the x axis is df_train.Years; all right, I can take it like it is. The x axis, and the y axis is sales, and the data is equal to df_train.

So if I see the scatter plot, this is how it looks, all right. And I can still increase the size: s is equal to something like three hundred; I can increase the size of my circles, like big circles, I can get with this, and a medium level, I can get two hundred. And so this is what I can really get from this. So what I will do is color using hue; hue is basically the coloring part, and you can color this using the

month name. So this is the month name; I can use this month name and color accordingly. Yes. Now you can see we have the coloring. This is January, February, March, April, May, June, July, August. And you can see the plot is repeated; it's clearly visible how exactly the data is changing according to the colors we have. And if you want the month name to be displayed on the plot,

we can also do that using plt.text. plt.text is an excellent way of doing that. What we need to do here is give the x position, the y position, and the text. So this is the text: df_train and its month; we can get it, but we have to do it step by step, otherwise it won't work. So what I'll do: for i in range of

the length of df_train. So to put all these values, I can iterate over this, and for each and every point I'll take i. And this is also i, and this is also i. So you can get all the values. So, for example, df_train.Years of zero gives you the zeroth value; this zero is nothing but 2001 January. And similarly, if you want the month, you will get January, February and so on.

So that is an excellent way. Execute that, and you can see this is January, February, March, May, June, July. And you can easily plot it and see the behavior, how exactly the data is. All right. So we can also do one more thing: the palette. I use it for setting up these options, like coloring. I use this time palette equal to Set1, which is also a color map.

This is a nice color map where we can segregate, sort of like the rainbow colors, a solid color for each and every month. It's really cool. But the problem is that the color is repeated, but still we can understand it much better than the previous visualization. But anyway, one thing we can see is that the seasonality here is 12. So roughly every year the cycle is repeated.

So in this case, my seasonality is 12. OK, so from these observations, my seasonality is 12. Seasonality is 12, and we need to create N minus one dummies, which is basically 11 dummies, 11 columns. OK, so I need to create 11 columns here.

4. Creating Seasonal Features
=============================

See the code[here](./5.ipynb)

All right, so what do we do now? Let's take this data, df_train; this is my train data. Yes, df_train, this is my train data, and let me take this month name. OK, let me take this month name and create dummies: pd.get_dummies. If you use this and just look at the top lines, you can see this is how the dummies look. This is how the dummies work. All right.

And you can see April, August, December and so on. Just be careful: there should be 11 dummies, so we need to drop any one. There is an option, drop_first, which drops the first one. But you can also drop on your own: you can drop by dropping any column; you can just drop it. So I just do drop_first equal to True. And what you get is that April is gone. So you have, starting from August, December, February and so on.

So these are my dummies, and I will add this to my df_train; this is what I'll try to concatenate. So what I'll do here: I'll take df_train1, which is going to be df_train.copy(), so I'm copying it; I'll take a copy of the data frame df_train. Now, what I'm doing is df_train1, and I will concatenate this. So I'll use pd.concat. The first one is df_train1 and the second one is the dummies, and axis is one; I need to join them based upon the index position.

So let me store that back into df_train1 and execute it. So that's it. What we got here is df_train1.head. We have years, and we have the time, and everything. All right. We have the time; we have August, December and so on. Everything is there. So we have the training data ready. So similarly, let's do it for the test data also.

So we do this on the test, and this is my test1, df_test1, and copy, and so on. So let's do it for the test data and let me check that: df_test1. Make sure you get the same number of columns, like the first column August, second December, then February, January, July and so on. So we got the order, the exact same order. That's fine for me. Otherwise, you need to be very careful and check it each time.

5. Splitting Data into Training and Testing Sets
================================================

See the code[here](./5.ipynb)

All right, we got the train as well as the test data. So what we will do is split the data into two parts, training and testing; we split the data of train and test into independent and dependent. All right. The first thing: what are the columns for the independent? The columns for the independent are time, and August, December and so on; all of these. So what I'll do is just take all the values.

And this is for August, this is December, this is February, January, July, June, March, May; that's the order we are actually following; and this is November, this is October, and this is for September. And that's it. So these are my columns for X. So let's take this X_train, and I'll put it as additive: basically, this is the training data for my additive model, and it is df_train1 with these particular columns.

And I need to convert that into values, because it's convenient. Similarly, let's take it for my test, and instead of df_train1, I need to put df_test1. And similarly, we get the dependent variable: y_train_additive, which is going to be equal to sales. So instead of the columns, this is the sales value for the train, and similarly for the test it is also the same.

So let me do all this and execute it. So that's it. So we have all the values. Let me test with X_train first: we have the time component, and again August. Oh, we got NaN; we have a lot of NaN values. So we missed something; let me check that. All right, we have a lot of NaN values. Oh, sorry, this is the head; it's not the correct way, so I just remove this.

I was operating with a head here just for the display, so execute this now, and also execute this. Now let me check the head of this test: all the values are now correct. So that's one of the mistakes I made. So make sure you remove the .head so that you get all the values, and similarly for the train. Let me just execute that and check all. Yes, it is good for the train also.

Got it. So we got the results for the train as well. Now execute this again, and also execute this again. So now we got it. And similarly, just check X_test. And so you should get a result something like this, without any NaN values. I think it is good; we got everything perfect. So now what we will do is check the shape. Of course, that's not mandatory, but just take the shape of train and test, just to make sure you're on the right track: X_train shape and X_test shape.

All right, so execute it: we have 48 entries in train and twenty four entries in test, and it is good. We are good to go now.

6. Training Additive Model in Statsmodels
=========================================

See the code[here](./5.ipynb)

So now what we have to do is build the additive model; we will build the additive model using linear regression. I use linear regression again to build the model right now. So just import: from sklearn.linear_model import LinearRegression, since we are using linear regression for this model. So model_additive is again LinearRegression(). And let's build the model: model_additive.fit, with X_train_additive

and y_train_additive. So that's it. If you do this, you can train your model successfully. Perfect. So we have trained our model successfully.

7. Additive Model Forecasting and Visualizations
================================================

See the code[here](./5.ipynb)

So perfect. So what we will do now is test the model; let's get the fitted values. OK, let's get the fitted values: y_fitted_values_additive. How to do this? Basically, model_additive.predict, and here I have to give X_train_additive. So what I get here is the fitted values. Similarly, let's get the forecasted values. The forecasted values are y_forecast_additive, and that will be equal to model_additive.predict, and what do I give here?

I have to give X_test_additive. So what I'll get here is the forecasted values. Execute. So we got the fitted values, and also we got the forecasted values, and the next step, what we need to do here is compute the margin of error. So in order to compute the margin of error: what is the margin of error? Basically, ME is equal to 1.96 times the standard error.

So we need to calculate the error here. So for the standard error: error is basically equal to the true value minus the fitted value. This is the fitted values; take the true value minus the fitted value, and you will get the error. And the standard error is basically error.std(); what you get is the standard error. So you get the standard error, and the margin of error is 1.96 times the standard error.

So this is how you can simply calculate the margin of error here. This is a very, very simple way of calculating the margin of error for whatever data we have. All right, let's execute this. Now we got the margin of error here, so let's go back to the plot which we developed. Let's copy that code and paste it here, and we will use it for the visualizations. So this is for the training data: we have df_train.Years and this is y_train,

and this is my additive model, and also the fitted values are y_fitted_values_additive. And similarly, let's do it for the test data: we have df_test. Basically, this was df_train and this is df_train1, so let's change the terminology: this is df_test1 and this is df_test1. So this is the test data, and this is y_forecast_additive, so you get the forecast values.

We already got the margin of error here. So CI plus is basically my forecast additive plus ME, and so on. So that's it; everything is ready. So let's do that. And this is df_test1, and everything is done. So let's change the labels: this is the time series data, and this is not the trend; this is basically my additive model, and this is the true future data, and this is not the forecast trend data:

it is the forecasted additive model data, and this gives you the ninety five percent confidence interval. So execute. Perfect. Now you can see the additive model is forecasting for you. You can see here it's excellent: the additive model is forecasting. These are our future values, and this is what my forecast is going to be like. And it's much better than the previous result.

The blue one, probably I'll change the color to green; that will be nice to see, basically to differentiate the different kinds of results. So you can see from the blue one, from here, this is what we got. Probably this is going to connect to this, and this is my forecast. We can see these are the forecast values, and this is the additive model, the fitted one; just change it to fitted additive model. Look into the legend so that you can understand: the blue dots are my training time series data,

and the fitted values are in green, and the true future data is the orange, and the forecasted additive model is my forecasting data, and the ninety five percent confidence interval is something like this. It is somewhat better. At least you can see we got the maximum peak at this month. So we got the same thing here, and it is somewhat better than the previous approach, which was simply giving you the confidence interval like this.

It's at least somewhat better than this. And of course, predicting anything in the future is always difficult, but at least we are trying to make it as good as possible using regression models. This is all about the additive model. In the upcoming lecture, we'll talk about multiplicative modeling.

## 9. Multiplicative Time Series Model

1. Multiplicative Model
=======================

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

Hey, guys, welcome back. In this lecture, we will talk about the multiplicative modeling for forecasting. In the previous lectures, we talked about the additive model for doing time series forecasting. In the additive model, we added up the seasonality part. But in the multiplicative model, we multiply the mean of the seasonality with the trend of the data. So let's see how to do this multiplicative model. These are the steps in order to build a multiplicative model. Step number

one is that we need to build a linear regression only with respect to time. That means you are only taking out the trend; we try to get the trend here, represented by T, by calculating only the trend of the data. And in the second step, we will take the trend, that is T, and the true values, that is the true data, which consists of all the components: trend, seasonality and irregularity, everything; that is called TSI.

And by taking those two values, step number three is that we will calculate the deviation, or the deviation value. That means, since we already know the trend, what is left out from the original data is seasonality and irregularity, so that is what we will calculate. We will take the true values divided by the regression part, that is TSI divided by T. That's it. So we get the seasonal and irregular effect of each and every prediction value.

Step number four is we will take the average of the seasonal values and use the average to make the predictions. All right. So these are very easy, very simple steps that we will use for the multiplicative modeling. We will see step by step, by considering the data, how exactly we are calculating this. Let us say we consider two years of data, and what we have is information about the quarters; let's say in a year we have four quarters, and that kind of data is there.

And what we need to predict here is the revenue or the sales. The first column you can see here is the year, and the second column we can see is the quarter. And you can see one, two, three, four: in a year there are four quarters, and in 2009 there are four quarters. And the time variable is basically used as the independent variable for the linear regression, a number represented by one, two, three, four, five, six, seven, eight.

And this is the total revenue in that particular quarter; it could be ten point one million dollars or something like this. OK, this is the data we have. And the next step, what we have to do is build the regression model on the time variable. So this is my independent and sales is my dependent variable. So we will build a simple linear regression for this case. All right. If we plot this, this is what it looks like: the x axis is up to eight,

because we have the time component up to eight, and this is my sales or revenue; this is how the trend looks, something like this. There seems to be some kind of seasonality, but this is how it looks. OK, so in step number one, we will build a linear regression. If I build a linear regression, I'll get only the trend component here; I'm getting nothing else here.

I'll get the trend component; all the red dots are my predicted values. Right. So we have all the predicted values. We have the revenue, TSI, which consists of trend, seasonality and irregularity, and we computed the trend only with the linear regression. So what we will do is create one more column and put in it what the trend component is here.

And that is what we are putting in one more column here. Now we have taken the observed and the predicted. Now let's calculate the seasonal and irregular part, that is, the deviation. So we will calculate the deviation: how much is it deviated? That is what we will calculate here. So basically SI is basically TSI divided by T. So this is the trend part and this is TSI. So in order to calculate SI, seasonal-irregular,

it is nothing but from the true data: [unclear] point two divided by ten point nine eight three, and what you'll get is zero point nine two nine. And similarly, if you divide this with respect to this, you will get one point zero four, and so on. So we will do this for all the values, and that is nothing but SI. In the next part, we will take the average of the seasonal values. So this is the quarter we got; my seasonal components are my quarters, and for this quarter, this is my SI value.

So for one it is zero point nine two nine; for two it is one point zero four; and for three it is one point one zero five, and so on. And what we will do here is take the average of the seasonal values. For example, this is the average deviation, the average of the seasonal values. What you can see here, for one, it is zero point eight four [unclear], which is the average of the seasonal values, the average deviation.

That seasonal value is nothing but zero point nine two nine plus zero point seven five nine divided by two; with three years, you have to divide by three, just to take the average of that. And similarly, zero point nine seven five is basically the average for quarter two: one point zero four and zero point nine one, and so on. So this is the average of the seasonal values you get. This table is important; this table is also part of the model.

Now, the next part, what we are trying to do is calculate this as a correction factor, and we use this correction factor that comes from the average seasonal value, or average deviation value. We got this. So what we will do is merge with respect to the quarter, and again, we multiply the predicted value by the correction factor. If you multiply this predicted value by the correction factor, what you get is [unclear] point nine two seven.

That's it. So this value, [unclear] point nine two seven, is the predicted value, or the fitted value. And similarly, eleven point two seven, this is the trend part, and the correction factor, let's say, is zero point nine seven five, and what you'll get is eleven point [unclear], and so on. So like this, we will multiply with respect to the seasonal value, or the seasonal deviation value. That's why this model is called multiplicative modeling.

And eventually, look into the results here. You can see the results here: the blue dots are the true data, the actual data, and the red line is basically the trend, nothing but a linear regression. And the multiplicative model is this. Multiplicative modeling is one of the most popular ways, used in some kinds of case studies. Multiplicative modeling is a nice way, just like your additive modeling.

And we applied this to the sales data we discussed in the previous lectures, and for this data, what we got is these fitted values. These are the fitted values we got for this kind of data, and the forecasting. You can see this forecasting is comparatively much better than the additive one. It seems to be better than the additive. So that's what we can see. But there are certain things out there: when to use the multiplicative, and when to go for the additive.

So we will see in a later lecture how to understand and know when to go for additive and when to go for multiplicative. All right. So this is how we can build the multiplicative model. In the next lecture, we will see how to build a multiplicative model in Python. Thank you very much.

3. Step-1 Trend Model
=====================

See the code [here](./5.ipynb)

Hey, guys, welcome back. Now let's see how to build a multiplicative model for forecasting in Python. All right, now we are in Google Colab. So this is what we have to do in multiplicative modeling: step one, we will build a linear regression with respect to time. Step number two, we will take T and TSI. In step number three, we will calculate the deviation value, SI. And step number four, we will calculate the average value of the seasonal deviation. So this is the first step we will do now.

Let's go back and see our training data. We have two data frames: we have df_train, and this one is called df_test. So let me consider these two values. What is in df_train.head? We have the four years of data, and similarly df_test, where we have two years of data. Let me do tail on this one, and head on this one, so that we can see 2004 January to 2004 December.

And after that we have the test data, so we have two years of data there. So step number one: we need to build a linear regression with respect to time. So this is the time component which we have, and these are the sales. Step one is that we need to build a simple linear regression with the time and the sales. That's what we need to do here. All right. So let's see how to build it. So this is my step number one; let me write it in a text cell.

So my step number one is linear regression with the sales and time: my time and sales. That's my step number one. So let me first bring the data into X and Y. So my X_t basically consists of only the time here. That is going to be equal to df_train. Actually, first let me copy to some other variables: df_train2 is df_train.copy();

I'll just copy it. And similarly, df_test2 is equal to df_test.copy(). That's what we will do first. Now let me take df_train2, and in that I want to take the time component. Remember, when we train the model, we should specify the number of columns; that's why I'm taking the data frame. And similarly y_sales,

so this is, of course, my true values. That is my multiplicative TSI. So let me take it from df_train2, and that's the sales. I don't want a data frame; I just want to read the series and convert that into values. Now let's look at the shape: X_t.shape and y.shape. I'm just using these names for the multiplicative modeling; that's why I'm doing this. Perfect. So this is what we got. And similarly, let's do it for the test data also.

So instead of train, we have to do it for the test data also: test. And this is true, and this is for test. And this is what I have to do: just test here. Let me mention it for the test data. Right. So this is df_train2 and this is df_test2. Perfect. So let's see: we should have two years of data; that means twenty four comma one. That's it. So we have all of the data split successfully into training and testing, and also into the independent and dependent variables.

OK, so now I will take the linear regression model: trend_model. What I'm doing here is, for the multiplicative modeling, trend_model, which is nothing but my linear regression. If you haven't already, from sklearn.linear_model import LinearRegression. We already have that from before. Executing this step, after that we need to train the model with X_t

and y_true. So that's what we fit here. So we train the model. Let me execute this step. We got an error. This is [unclear]. Now we have trained the model successfully. So what we have to do now: now we got the trend, the trend component; we trained the model successfully, and what we got here is the trend component. So let me take this data, df_train2.head.

And what we have is basically the sales; that is my true values. And this consists of TSI: trend, seasonal and irregular. So now let's get only the trend here. So y_pred_trend is going to be equal to model_trend.predict, nothing but the values. I'll take these fitted values from the trend. And this is what we have now.

So model_trend.predict, and what will the trend predict? It is X_t comma y_true. I'm sorry, we have to do it only for X, so execute. Perfect. Now I would even do it for the forecasted values at the same time. OK, we'll do the forecast later on in the pipeline. And the next step, this is the trend predicted.

And I'll put it as df_train2['T'], which is nothing but the trend. That's equal to y_pred_trend. And df_train2.head: if you see this, we got the predicted value. This is just the trend in the data; we calculated the trend. All right. So after the next step, we got these values, and this is step number one and step number two. This is my step

number two: just take the predicted trend, and take the TSI. The TSI is basically the true samples. OK, so the trend is basically the linear regression output, the fitted values. And this is what we got here.

4. Step-2 Calculate Seasonal Deviation
======================================

See the code [here](./5.ipynb)

All right, so the next step is to calculate the deviation from the seasonal component. That's step number three. Step number three is basically the seasonal deviation: how much is the deviation? The deviation values are what I need to compute here. So basically SI is TSI divided by T; that's the formula. So I will use this formula and calculate those values. OK, this is my data.

And here, this is my SI, TSI by T. So now let's look at df_train2. What I actually need to do here is calculate SI, and that is basically df_train2: the first one is sales, divided by df_train2's second one, which is what I predicted with respect to time, T. And what I'll get here is SI. So let me check df_train2 and display the top five rows.

And this is what we got. Perfect. So let me display 20 values, the top 20 values. So these are the first 20 values, and this is my SI for each and every sales value, the true values, and also the values we got for SI.

5. Step-3 Seasonal Corrector Factor
===================================

See the code [here](./5.ipynb)

And now the next step is step number four. Step number four is to take the average seasonal deviation. That's what we need to compute here. Basically, the average seasonal deviation means: this is the SI, and we need to take this one for January, and one more January here, so this one and this one, and similarly take all of them for the season and combine them, and you'll get one value. And similarly for February, and similarly for March and April: you add all those things and divide by the total number of years; basically, calculating the mean of that.

OK, we calculate the average deviation: the average deviation for January, for February, and so on. That's what we're basically doing here. All right, so how exactly can we do that? Let me do one thing: let me take this train data. The first thing I want is the month name, which is basically the seasonal component, and the second thing is my SI. This is my SI with me. So what I'll do here is call it deviation_season.

So that's my data frame I want: deviation_season. And for this deviation_season, I need to group by: groupby month. I just take the groupby on month name, and I'll take the mean of it. That's what I'll do: take the mean of those values. So that's it. So this is what I'll get for April; this is the mean for August; this is the mean of this,

and for December that's the mean, and so on, which we can simply get from this. That's my step number four.

6. Fitted values and Forecasting with Multiplicative Model
==========================================================

See the code [here](./5.ipynb)

The fifth one, which is the last step: step five is computing the fitted values. That's my last step. So we have the month deviation_season, and let me take this df_train2.head. And what we have is January, we have SI, and this is the average deviation. We already have this average deviation. So what I'll do is change the name here with rename.

And what I can do here is columns is equal to a map: SI should be renamed to my correction factor. Just replace that with correction factor. OK, so I just replaced that with the correction factor. OK, this is what I want. So now what happens? I have the correction factor with me and also the month name with me. So based on that, I will merge. So what I'm doing here is merging the table:

I just want to merge with deviation_season. This is what I want to do: merge deviation_season on what? On month name. That's what I have to do here: on month name. I just want to merge. That is what I'm actually doing here. So execute. And what we got here, in df_train2.head, is that we got the correction factor. So finally we will calculate the predicted values,

the fitted values. Finally, what we will do: these are my fitted values. The fitted values are basically equal to my predicted trend into this correction factor. That's my fitted values. So I have to do the prediction: df_train2, the predicted values T from df_train2,

times df_train2's correction factor. So finally what we got here is the fitted values. Right. So we got our fitted values. Perfect. This is how you get all the values here for the multiplicative modeling.

So step one is basically: we do the linear regression with respect to time. Step number two: we take T and TSI. Step number three: we calculate the seasonal deviation. Step number four: we take the average seasonal deviation. And step number five is computing the fitted values from this model. What we are trying to do is multiply that with the trend.

That's why it is called multiplicative modeling. So this is how we are able to calculate the fitted values. Right. So now let's look into the forecasting. Whatever we did, we have to do the same thing for the forecasting. But this time we have to take the deviation_season that we calculated, and we will take this model: we already trained the model for the trend. So this is my model; we already trained that, so we'll take that model now.

All right. So here it is: model_trend.predict. Predict what? First, in order to calculate the forecasting values, let's take this X: capital X, underscore t, underscore test. That gives the trend, and basically we get the forecast trend; F_T is basically the forecast trend here. And then I take it into my data frame, df_test2, and this is my forecast trend; df_test2's forecast trend is equal to F_T.

So that's what we got here. So now let's get df_test2.head. All right, so this is the test: we have to put it in df_test2. Right. So we got this forecast trend here. So next, we already calculated the average seasonal deviation; we do it only once, we don't do it multiple times. So now we will take this one.

This is the table I want to join. So df_test2.merge, and the left table is the test, and the right table is this one. I just want to merge on the month name, because that's my primary key: the primary key is the month name. So that's what I'm doing, and just saving it into df_test2. So that's it. So what we have here is df_test2.head. All right, so we got the correction factor here.

So finally, you will get the forecasted values. This is my forecast multiplicative, and that's going to be equal to df_test2's F_T times the correction factor: multiplying the forecasted trend by the correction factor. So what we got here is df_test2.head, and exactly what we get here is the forecast multiplicative. So everything is done here. Perfect. So that's how we can simply calculate all these things.

All right, now let's calculate the margin of error.

7. Margin of Error and Confidence Interval
==========================================

See the code [here](./5.ipynb)

All right, now let's calculate the margin of error here, just to calculate the error component here. Always remember, the margin of error we calculate only from the train data. So let's take the train data, df_train2.head. Let's display this. And the margin of error: your margin of error is equal to two times the standard deviation, or for a 95 percent confidence interval, 1.96 into the standard error.

And the standard error is basically the standard deviation of the errors. All right. So let's calculate the error first. The error is basically between my fitted values and the true values, so I can take it from df_train2: these are the sales, the true values, and df_train2's fitted values. And what I get here is the error. Now SE is basically equal to error.std(),

the standard deviation of the errors. So finally, the margin of error is equal to 1.96 into SE. That's it. So that's how we can get the margin of error. It's very simple to calculate. Print ME; that's my margin of error, and what we got here is 36.325; that is my margin of error.

8. Visualizing Forecasted Data
==============================

See the code [here](./5.ipynb)

All right, so we got the margin of error now. So the next step is the visualizations: just go back and copy the entire code here; we'll do the visualizations, copy and paste it here. So now let's make some small changes. It is df_train2.Years, and my fitted values are basically df_train2's fitted values; that is what I want to consider: df_train2's fitted values.

So I copied and pasted it here, and similarly the true data. So you'll get the visualization for the true data as well. This is not df_train, it's df_train2, sales; I just put the sales here, because this is the true data, and this is my fitted. All right. Now let's do it for the forecast. It is df_test2.Years, and I have to do it for the forecast, so df_test2's forecast multiplicative.

Oh, all right. This is for this, and this is for this. So this is basically the true values, basically the sales here. All right, next you need the margin of error. So this is my forecast, and you will get the confidence interval with the margin of error here. And finally, these are my fitted multiplicative model and the true future data, the forecasted multiplicative model and the 95 percent confidence interval.

So that's it. Let's look into the visualizations. Oh, we got... OK, I made a small mistake. Let me check. Oh, yes, that's a mistake I made. OK, let me print here. Let me create one more cell: df_train2; let me display all of df_train2, and you can see here the order: January, January, January. That's what the merge is basically doing here.

So we got all the months like 2001 January, 2002 January; that's what we got. But actually I have to get 2001 January, 2001 February, and so on. So I have to sort it. So I have to sort by years: df_train2.sort_values with by equal to Years. If I do like this, you can see, yes, we got all the values in the perfect order. And inplace equal to True.

And similarly df_test2.sort_values with by equal to Years, comma, inplace equal to True. So we got the values. Now let's see. So this is the perfect code; we just needed to sort it. Let me execute this code again. Perfect. Now you can see it is the perfect visualization we got here with respect to time, and you can see it is much better than the additive model. The additive model is not actually increasing with respect to time, but the multiplicative model is a better fit compared to the additive.

Compared to the additive, the multiplicative model is better. And you can see here it is a much, much better fit compared to the other models. So this is the fit, and this is the fit by the additive model, and you can see the deviation there is quite constant all the time. But here, the multiplicative model is much, much better, trying to fit better and better. So it is a much better fit in this case.

In this case, it is a much better fit compared to the other model. All right, so this is all about multiplicative modeling.

## 10. Auto Regressive Methods

1. Auto Regressive Methods
==========================

![143.png](./images/143.png)

Hey, guys, welcome back. In this lecture, we will talk about auto regressive methods. Let's start by understanding the limitations of regression. One of the limitations, or disadvantages, of linear regression or multiple linear regression is that it is very difficult to predict if there is no seasonality or trend and the fluctuations are completely random; then it is really, really very difficult. And more or less, if you want to build regression models, it is very difficult to fit all the values in the data.

Instead, we can use one of the methods, the most popularly used, the auto regression model, also known as the AR(p) model, auto regression model of order p. It is also a multiple linear regression, a multiple regression in which the independent variables are time-lagged versions of the dependent variable. So actually the auto regression model is a multiple linear regression where the future value actually depends upon the past values, the past p values.

p indicates the number of lags that are actually required. For example, p is equal to 10 means we take the past 10 values in order to predict the future value, in order to forecast the future value. So that is the meaning of the order of the regression, p. In this equation, Y t plus one is the forecasted value, or tomorrow's value, and Y t, Y t minus one are the historical values, and p indicates the number of lags. And we can identify the number of lags using the partial autocorrelation function; the partial autocorrelation function is basically used to find out the number of lags.

So let's take an example and try to understand how we build the regression model of order two. In this case, I'm considering order two, and let's see how we build an order-two model. The equation of the auto regression model is quite easy: Y t is B1 into Y t minus one plus B2 into Y t minus two. So we are using the previous two values in order to predict the future value. Let's say this is the equation, and let's say this is the data I'm having with me.

So what I'll do here is prepare the data: I will shift it. T minus one is basically one time shift and t minus two is basically two time shifts. So in this data, I'm using the past two values: this is actually t minus one and this is t minus two. We are using the past two values, which are my independent values, in order to predict the future value, which is my dependent value. So here, y t minus one and y t minus two are my independent values, and y t is my dependent value.

So now with this equation, with this data available, what I do is build a simple regression model, in this case a multiple linear regression. And let's say in this case, I build a model for the US air carrier passenger forecasting data. For this data, this is the data available with me, almost 20 years of data, and the auto regression model fits it.

And basically, it fits something like this, and I'm able to forecast the future values with the auto regression model using this. This is the forecasting behavior on this particular data set. The green line is basically the fitted values, and this part is known as the forecasted values. What you can see here is that it's a perfect fit and a perfect way of dealing with the model. How many lags are actually required is totally dependent upon the partial autocorrelation function.

In the next lecture, we will see how to build the auto regression model in Python. Thank you very much.

3. Setting Up for Model Building
================================

Hey, guys, welcome back. In this lecture, we will talk about how to build the auto regressive method in Python. Before that, I'm in the Google Drive, and the data that I'm working on is the airline carrier passengers data. I hope you have already downloaded the data from the resources; make sure you download the data and put it in the folder that you are working on. OK, so in the data, what I'm having is the month and the passengers. And what I want to forecast: this is the month, and this is the number of passengers who boarded the airline.

So what we're trying to predict is how it is going to be in the future, the pattern, et cetera. So that's what we are actually doing here. And if we look at the data, we have the data from 2000 January 1st to 2019 December 1st. So we have almost 19 years of data available, and everything is arranged month-wise. So what I'll do here is make use of this data and build the auto regression model, AR(p).

And using that, let's try to build the model. All right. So let's go to my Google Drive and Google Colab. I'm in Google Colab here. And the first thing I will do is update some libraries, because the current version may not be sufficient for the notebook: an older version of statsmodels is there, and what I'm using now is a bit more advanced, newer version of statsmodels. All right.

So let's do one thing: let's first update our statsmodels in Google Colab. In order to do that, let's put the exclamation mark and pip3. We are using Python three here. So pip3 install hyphen hyphen upgrade statsmodels. Execute the statement, and Google Colab will try to install all the packages, and finally it asks you to restart your runtime. All right, so I think it has been successfully installed. In order to make this change effective, we need to restart it.

So for that, I'll go to Runtime and restart my runtime. So let me restart the runtime. Remember, the previous version was 0.10.2; now it is 0.12.1. This is our current version. So make sure you restart. So restart the runtime, and it is getting restarted, and perfect. Now, I don't need to execute it again; it's not required. So what I'll do now is connect to the Google Drive and set the path.

So for that let's do one thing: import os, from google.colab import drive, and drive.mount. What do you want to mount here? The drive; execute it. All right, now it asks you for the URL, so just click here, and this is the email ID I was working on, and Allow, and copy this authentication code and paste it. Enter. Right, now we have mounted our drive successfully. Now, the next step we're going to do here is import the required libraries: import numpy as np, import pandas as pd, import matplotlib.pyplot as plt, import seaborn as sns.

So these four libraries are actually required for me, and apart from that, the modeling library for building the model: I'm using statsmodels here. So import statsmodels, and let's check statsmodels.__version__. If you look into the version of statsmodels, the version is 0.12.1. So make sure your version is greater than or equal to this; otherwise, some of the functionalities we'll be using may not be available.

So make sure your statsmodels version is at least this version. All right, so what we will do now is load the data. My data was in the data folder, and this is what I was interested in. So pd.read_csv, as it is a CSV file, and it was there in the data folder, and... I'm sorry. The name of the file is US airline... I think the first thing I need to do is set the path. Let me set the path.

Let me check where my path is. I was in the drive, so let me set the path: os.chdir, and I was in /content/drive, My Drive, and I need to move into complete time series and auto regressive. So complete time series, followed by auto regressive; that's it. So this is the path. And yes, I set the path. Now I use the command ls. All right. So I was in this directory, and I can check the file name I'm having here: I can take this file name, pd.read_csv, and df.head.

4. Data Preprocessing
=====================

So the first thing is let's look into the data with df.info, and you can look into the data types. What you can see here is that month is an object and passengers is an int. As I already told you in the previous lecture, whatever date you have, it is required to convert that into the datetime format. That is very, very important to follow. All right. So in order to do that, the first step is to import datetime, and we can import it here.

And we will use this datetime later on in the lecture. Let's take this datetime here. Now I will change the data format: let's say this is the month, and I can use to_datetime, which is pd.to_datetime of df.Month. And now I can change that into the date format with the following command. So let's look at the info once you execute this particular statement, and you can see now it is in the date format.

Perfect. All right, so it's excellent. And what we can understand here is that I'm having the dates from 2000 to almost 2019; almost 19 years of data is available here. All right. So what we will do here is first visualize our data. Some bit of exploratory analysis is actually required. Basically I'll do the graphical approach for the time series data, which is actually enough, so I can use sns.lineplot to visualize the line.

And the x axis is basically df.Month and the y axis is passengers. OK, so you can see here the x axis is the months, from 2000 to almost 2019 December, and this is the number of passengers who boarded. So it looks like some changes are there, some variation is there. So this is the data we have. All right, so what I will do here is increase the figure size: plt.figure.

plt.figure with figsize equal to ten comma six; let me increase the size here. You can see, yeah, now I think it is good; it's some figure showing the data I'm having here. So instead of plotting like this, let me put some dots; that will be really good. So I'll use matplotlib, plt.plot, and I'll use df.Month as my x axis, and passengers, which is the y axis, and what I can do here is circles followed by dashed lines.

So that's basically what we will get here. I think this is quite visible. Let me increase the size: let me take twenty comma six. I think this is good. This is much better than the previous one. All right, this is how the data looks. You can see there is some seasonality there, which can actually be seen, and there is a trend, and seasonality can be easily visualized in this particular data.

All right. So if you want to predict, we need to know what the seasonality is; those things are actually required to build a model. And of course, we can find the seasonality using the ACF, and using that, we can understand what the seasonality is in the data. We can simply identify it here. All right, so this is the data I'm having with me, and this is how the data looks.

So what I do here is split the data into two parts: one is training and second one is testing, because I want to test my model, just how good my model is. In order to do that, from the data available, I take the data up to 2016, which is my training data, and 2016 to 2019 I take as the test data. All right. So now let's take df; let's take this down here. And this is what I did.

So basically, what I'm trying to do here is split the data into train and test. For the train data, I basically use up to 2016 December. So up to this I use as the train data, and my test data is from 2016 December to 2019 December; this is the data which is available to me, so I'll do this kind of split here. So let me look into the tail portion also.

And yeah, so I'm having the data up to 2019 December; this is the data I'm having here. OK, so I'll take the data up to this. In order to do that, I need to apply some conditions here. So df.Month should be less than, let's say, 2016-12-01. After 2016 December, that's the test data. But remember, this is a string, and our data frame cannot understand

this as a date format. So in order to do these kinds of operations, we need to convert it. We already imported datetime, so I'll make use of this datetime and convert it: datetime.datetime.strptime; I'm converting from the string format, and I need to pass the date and the format. The format I'm looking for here is: the first one is percent capital Y, the second one is percent m, and the third one is percent d.

So that's the format I'm looking for here, and done. So this is my condition. So let me check this, and this is df_train; execute it. Perfect. Now you can look into df_train.head and take df_train.tail, which will give you the last five rows, and you can see we have the data up to 2016, OK? I think there's a problem: I think this should be small m. Capital M is minutes, so

we go for small m, and perfect. So this is small m; you have to use small m here. Now you can see here it is up to 2016 December, the month of data which is available to me now. The rest is my test data. Obviously it is easy for me to do that: let's copy the same thing, and the month is greater than or equal to that. So that's my test data, and that's my train. This is my test.

Let me look into the head, and we'll get the data from 2017 January 1st. All right. So this is how we can split the data into training and testing. So let's visualize. I will copy this, copy exactly the same code and paste it. And remember, this is my training, df_train, and this is my testing, so I can visualize both. So this is for my test. And execute. OK, so you'll get two kinds of plots.

One is in the blue color, which is my training, and this is the forecasting period, the original data, the true forecast data. So I'll make it as light as possible using alpha is equal to 0.3; I'll make it more transparent, so this is my true data and this is my original data. So let me make this one transparent too: alpha is equal to 0.5.

So it is a little more transparent, so that in my future case, that will be really, really useful for me here. And finally, plt.show. OK, before that, let me put some legends: plt.legend, and this is my train data and this is my test data, nothing but the forecast. This is my train and that's my test; that is the legend. All right. So let me put the y label: plt.ylabel, and this is my passengers count. So we got the train and test data, and we have the passengers count, so everything is set.

If you want, you can add plt.grid so that we can get nice grid lines here. It's really, really useful and important. Thank you very much. In the next lecture, we will talk more about the auto regression models.

5. ACF & PACF
=============

Hey, guys, welcome back. In the previous lecture, we did some kind of preprocessing that was basically required to build the auto regressive models. So now we will try to analyze this plot first. We will use techniques like the ACF and PACF plots in order to analyze the data. The major agenda here, particularly for the AR model, is the order of AR(p):

we need to identify the number of lags that are really required. That can be found with the PACF. OK, so we can study those kinds of behavior in the ACF and PACF plots. All right, so this is the data that is there with me. So I can plot this; I'll use statsmodels: from statsmodels.graphics.tsaplots, the time series analysis plots, I will import

plot_acf and also plot_pacf. So let's import these two. Now, basically, the first one I do: X is basically nothing but my train data, df_train's passengers; that is my X. So df_train, and this is my passengers. Perfect. So that's it. So what I can do here is plot_acf, and if you plot it, you get a nice autocorrelation plot, which is easily visible here.

This is the autocorrelation plot. And similarly, if you want to plot the partial autocorrelation plot, plot_pacf, and you pass the passengers, so you can get the partial autocorrelation function. So let me use subplots so that you can plot them the same way: plt.subplots. I want the number of rows to be one row and the number of columns to be two columns, and the size,

I'll make it big: let's say 15 comma eight, and this is my fig comma ax. So this is what I can do here. And ax is equal to ax of zero. And similarly, this is my result one, and this is my result two; result two has ax equal to ax of one, which gives you the partial autocorrelation subplot. Now you can see the perfect plot, where you can see this is the autocorrelation and the partial autocorrelation.

So let me give ax of zero.set_xlabel, and this is lags. And similarly, ax of one, this is also lags here. So we can see here... let me use the xticks, plt.xticks. All right, so it's OK. What I'm having here is the autocorrelation plot and the partial autocorrelation plot. So what you can understand from the autocorrelation, from this data, is that you can see there is a clear seasonality behavior.

It is clear, very, very clear. Those things you can understand here. From that, you can see there are lags with a certain amount of positive lags. This indicates that there is a trend and there is cyclicality, cyclic behavior. You can see here, even in the correlation you have positives and negatives, which indicates that there is some cyclic behavior, which indicates a seasonal effect. And more clearly, if you want to understand:

this is the peak. If you see, at lag zero we have the maximum peak; again, the peak rises at the top at 12, which indicates that the seasonality is 12. We can clearly understand that every 12 months, the pattern is repeated. That's what we can understand from the autocorrelation plot. Those things can also be understood here: we have the maximum peak, you can look into it here, at one, and another maximum which occurred at lag 12, or around 12.

Those kinds of rich information you can easily understand here. And this part basically talks about the half cycle: you can see this is the half cycle, and the cycle is repeated. So those kinds of information you can really, really understand in this case. All right. So you can see there are a few positive and negative lags out there, and if you want to count the maximum number of lags that you really want to take, then instead of going into that,

just remove the trend part here; you need to remove the trend part. And how to remove the trend? For stationary data, the analysis will be much more clear. Instead of focusing on the non-stationary data, use stationary data, and the analysis will be much clearer. So we need to remove the trend here so that you can select the number of lags that are really required. So basically, in order to build our auto regression model, we use the partial autocorrelation;

we take the number of lags that are really required, which means you need to count the lags for the seasonality. So what we have to do is make our data stationary, so we will continue in the next lecture on how to make our data stationary. And again, we will plot the ACF and PACF plots. Thank you very much.

6. Making Data Stationary
=========================

Hey, guys, welcome back. Now let's see how to make our data set stationary. So this is what we will do: making the data stationary. We can also use this data for building the model too, but in this case, I will use it only to calculate the exact seasonality, or the exact number of lags that I need to consider here. So basically, I need to take the partial autocorrelation plot and decide based upon the partial autocorrelation and the number of non-zero lags.

That indicates the number of lags I can consider for building the model. OK, let's see how to make the data stationary. Basically, I was working on df_train, on the passengers data, and this is the passengers data: diff, and the number of periods is equal to one. So basically, calculate for one period; this is how we difference the data. So this is my differenced data, and I can make the data stationary; you can see I can clearly make the data stationary with this.

So this is my stationary data, and I can plot this stationary data so that you can clearly visualize it: I copied and pasted the code here. I just want only one thing, the difference. So I'll take this differenced data; I don't want this kind of data; I want basically this difference. And this is not my passengers; it is passengers monthly changes. That's what I can see: passengers monthly changes. All right. So let's plot it.

And you can see this is the difference. Clearly, you can see that it's a pure seasonality effect we can understand here. And let's plot again the ACF and PACF plots so that we can understand better. And remember one thing: we can't directly plot it here. Whenever you are trying to calculate the ACF and PACF, the first thing is you need to remove the missing values. You can see we have one missing value here.

So what I'll do is dropna: just drop all the missing ones with inplace equal to True. I need to drop the missing values before computing; otherwise you'll get an error. Basically, you will get an error if you're not doing those things. OK, so now let's take the differenced data and execute. Perfect. Now you can see it is much more clear. We have all the lags, and this is a very, very clear plot.

We can clearly see the half cycle at six, and the full cycle at 12, which is very clearly visible even in the partial autocorrelation plot also. And after that, the number of non-zero lags is very minimal, very, very low. So I'll take only 12 lags; basically take only 12, which is the perfect seasonality, which I am able to find out here. If you want to take more and more, we can also take that.

But 12 lags are basically enough, because you can see we have very high peaks, very, very high values up to 12; after that, it's very low. I can take them as zero here. So those kinds of information, those kinds of things, you can understand when you make the data stationary, and you have much richer information about what the autocorrelation and the partial autocorrelation actually give. So I recommend you bring the data into stationary form if you

really want to work with the partial autocorrelation plot. It is highly recommended to make the data stationary, then plot the partial autocorrelation, so that you can get much more clear information. Of course, here also we got the same information, but it is much more clear compared to the previous one. All right, so what you can see here is a clear seasonality effect: the seasonality is 12, the cycle is 12 periods.

So for every 12-month period, the cycle is repeated. That is one of the observations I can make here. All right, so we'll continue in the next lecture with more about the auto regressive methods.

7. Training AR Model
====================

Hello, guys, welcome back. In the previous lecture, we calculated the number of lags that I need to take here, and we converted the data into stationary so that we can understand much more clearly. So now let's build the auto regressive model, also known as the AR model, AR(p). AR stands for auto regressive, of order p.

p indicates the number of lags. So basically we can find p using the PACF plot: count the number of lags which are not zero, basically find the number of lags which are not zero. OK, so we can treat it as an approximation: after 12 lags, you can see approximately all are zero; even though some are positive, I can take them as zero, because they are very, very small.

So I'll take only 12 lags; that's what I'll take: 12 lags from the PACF. OK, so I got 12 from the PACF, so I'm trying to build the AR model of order 12; that's the model I'm trying to build now. All right. So before building the model, let me do some kind of preprocessing on the training data. This is my training data for training, and what I can see here is the month and the passengers.

So in order to train the model, the auto regressive model internally will do its preprocessing on its own. So what I will do here is give it only one column. In order to build the auto regression model, that particular statsmodels function will accept only one column, and inside it, it does all the processing of creating the lags. OK, so for that, I need to specify the month information also.

But this month information I'll put into the index, so let me convert that into the index: df_train.set_index of month. So this is basically what I'm trying to do here: only one column is there, and the month is my index. OK, so this is X_train, and similarly X_test is basically df_test.set_index, and this is my month. So I did it both for training and testing.

All right, so let's build the model: from statsmodels.tsa, time series analysis, .ar_model, the auto regressive model, import AutoReg. So this is the auto regression model we are using here now. Got it. So model_ar, AR stands for auto regression, is AutoReg, and you can see here the docstring is basically asking you what the training data is. It's nothing but X_train. That's it. And what is the number of lags?

So what is the number of lags, or the order of your auto regression, basically p? So what I can do here is lags is equal to 12. I calculated the number of lags; you can also count the number of lags, but here I count the number of lags up to twelve; after that, even though some are positive, they are very, very minimal. That's why I'm not considering those values. 12 is the approximate number I can take here. Then .fit().

So we do .fit(), and you can train your model by executing this command, and your model has been trained successfully. So print model_ar.summary(). You can look into the summary of how your model works. We have 2[unclear]9 observations. The AIC value basically talks about how much the error is. And the S.D. of innovations, the standard deviation, is [unclear], which can be used for the margin of error.

This is basically used for the model, plus or minus; this is basically the margin of error. And we built the model. This is a simple multiple linear regression, and all the coefficients are set up. And this is basically the p-value of the model: what is the significance of selecting this particular coefficient. That's what it actually means.

8. Fitted and Forecasting values with AR Model
==============================================

All right, so we got our model ready, so we can get the fitted values here. Let's calculate the fitted values. All right. So fitted_values is equal to model_ar.fittedvalues, right? So let's take a look at the fitted values; they're already calculated by the model. So that's it. These are my values. So what I can do here is copy this code, because the plot is very important for me, so let's copy and paste it here. Now, if you look into the fitted values,

fitted_values.head, you can see here we have the month, which is my index, and the particular fitted value here. So everything is there. So these are my fitted values, right? So what I can do here in the plot is give the fitted values here. Let me give a nice green solid line. Perfect. Now you can see this green solid line is my fit; an excellent model, an excellent fit by the model.

And this is AR of order 12. If you're not satisfied with this, increase the value more and more so that you can get a better fit and a better model. So this is how your model is fitted, and perfect results we are able to get using the AR models. All right, now let's see how to do the forecasting with the AR models. The auto regressive model in statsmodels is excellent; everything is there.

So you don't need to do much here. What you need to do here is just provide the dates, the dates you want to forecast for: you need to give the start date and the end date, and that's it. Now let's get the forecasted values here. So these are the forecasted values from the auto regression. My start date is basically from 2017 January 1st; this is my start date. And my end date:

I just want up to 2019 December 1st. So this is my end. And remember, we can't pass it like this; it needs to be in the datetime format. So we always need to convert it: datetime.datetime.strptime. OK, now I need to give the format with percent: the first one is the year, the second one is the month, and the third one is the day. That's it. So copy and paste it here similarly, comma; copy and paste.

That's it. So this is my start and this is my end, and we can get the forecasted values here, basically with the dates and everything done here. So let me show the top three values: head(3). And now let's plot this. Let's do it again: these are my values, and this is my forecasted values; just give the forecasted values, and this time a nice red solid line.

I can give it here: this is my forecast, forecasted values; execute here. So nice. This is the forecast of how the data is being forecasted. We have a lot of error, because this is not the right way, but at least this auto regressive model will work better for short-duration forecasting. So it's OK; forecasting is always difficult, but still we are able to make it with the auto regression model.

All right. So let me give the legend here, and this is the forecast with AR(12). All right. So that's my forecast with AR. And let me give the confidence interval, or the margin of error. You can calculate the margin of error simply: you can get it from the model: model_ar.resid basically gives the residuals, and we can take the residuals here. All right. The residuals are basically the errors, and for those we take the standard deviation.

And we get what we call the standard error. And the margin of error is 1.96 times this; this is basically my margin of error. You can simply calculate the margin of error by computing this value. And now let's build the confidence interval, which is plt.fill_between. My x axis is basically X_test's month, OK, this is the test month, and what are the forecast values?

Basically the forecasted values, and that makes the axis. And .values to convert that into values, plus ME, comma, and this is minus ME. I just convert that into arrays so that I'm just removing the indexing part here. And this is minus ME, and let me execute this. Yes, we got it: the blue region is basically my confidence interval. So what I can do here is say alpha is equal to 0.5, and that indicates my confidence interval.

Let me put it here: my confidence interval. And this is my confidence interval. That's it. This is how you are able to build the AR models; very, very powerful, and even the forecasting is very nice and straightforward. It's a nice way of building the models and predicting the future with the AR models.

9. AR Model Evaluation
======================

All right, we can also test our model, how good our model is, with the Q-Q plot, and also we can test the error: is the error that is left out random, or is any pattern left out in the data? We can also understand this particular thing. So basically, if the distribution of the error is random, or the distribution of the error is normal, perfectly normal, that indicates that there is no pattern left out in the data.

So those things we can understand here. So model evaluation: statsmodels automatically gives you a nice plot. I can use this, because we already built the model: model.plot_diagnostics, which will actually give you a nice kind of plot. By default the lags is 10, so I'll take it as 12. And now what I can do here is give the figure size: plt.figure with figsize,

that is 10 comma six. And let's say this is fig. It is going to take it like this: fig is equal to this, and we can increase the size simply using this. All right. So I got two pictures, so let me take it: fig is equal to this. And let me say this is 15. And I computed for lags 12, and I'm getting a nice plot. What I can see here is that the orange one is basically my data and the green one is basically what should be there, what the true values actually should be.

And this is the standardized residuals, basically the irregular part, or the noisy part, which we did not predict or did not actually fit. And we can see that it is pretty much normal noise. And also this is what we can see: it's almost a straight line in the Q-Q plot. But the rich information you can see here is in the autocorrelation plot. So this is the correlogram.

And what you can see here is that only one value is there, and the rest of the values are all zero. So this is basically the correlogram, the autocorrelation plot: only one value is positive and all the other values are zero. So I can take it from this plot that it is just random. I can say there is no pattern left out here; it's purely noise. So I can say about the model that we did a perfect fit, and it is able to capture the entire information in the data.

And what I can say here is a thumb rule if you want to forecast with auto regression. Here I used three years of data; I'm predicting three years of data and trying to capture the pattern. But what I can say here is that it's mostly useful to predict only half the cycle. Only half the period of the cycle is what we can predict with the help of the AR model, at least. It's very good for predicting the half cycle; that is what we are able to achieve here.

All right, so this is the modeling, how we build the auto regression models, and also the model evaluation of the auto regressive model. Thank you very much. We'll continue in the next lecture, more on the models.

## 11. Smoothing Methods (Moving Average)

1. Smoothing Techniques
=======================

Hey, guys, welcome back. In this lecture, we will talk about the smoothing techniques. In the previous lectures, we talked about the auto regressive techniques, where we used the previous lags to predict the future. But smoothing techniques are very easy, and they are also most widely used when the data is stationary. If there is no trend or seasonality, and only randomness is there, then these techniques are very, very useful: when the data consists mostly of randomness in nature,

these smoothing techniques are really, really useful to produce the forecast. There are three kinds of smoothing techniques. One is naive forecasting, second one is the MA models, and the third one is the exponential smoothing technique. All right, we'll see all these three techniques in the next lectures. In the next lecture, we will talk about naive forecasting and how to do that in Python. Thank you very much.

3. Naive Forecasting Model
==========================

Hey, guys, welcome back. In this lecture, we will talk about naive forecasting. The naive forecasting model is one of the simplest models. It assumes that the most recent time period of data represents the best predictor, or the forecast, for the future. That is the meaning of the naive model: if you want to forecast the value for tomorrow, it is nothing but the value of today. So that's naive forecasting. It's a very, very simple model.

What we are actually doing here is just a time shift. That's it. So the equation of the naive forecasting model is Y t is equal to Y t minus one. Y t is the time, which could be tomorrow's value, and Y t minus one means today's value: if you want to forecast tomorrow, today's value can be considered as the right forecast.

So that's one thing. And one of the things about naive forecasting is that it does not take into account the trend and seasonality in the forecast. That is one thing. And the second thing is that if you want to forecast with the naive model, we can only forecast one value; we are not able to forecast years or months. We can only forecast one value: from today's value, you forecast tomorrow's value, but forecasting the value 10 days after that is not possible

with naive forecasting. But one thing we can do is: the forecast for tomorrow is what happens today, and the value of today can be the forecast even for 10 days, even for one year of data. So that's the advantage of that. But the thing is that we can use this naive forecast model only for forecasting one day, or one time period, one time value.

All right, so if you consider the data, this is how the data looks, and with this data, if you want to forecast with the naive model: the blue one is the true values, and the orange one is the forecast. That is nothing but just a shift in time. You can see it is just a one time shift. That's it. That is how the fitted values and the forecasted values look, something like this.

So whatever the data was on the next day, the forecasted values can even be for years together; but that's only one value. Generally, it is good to forecast only one time value. That's it. OK, so this is a very simple model, known as the naive forecasting model. In the next lecture, we will see how to build the forecast models in Python. Thank you very much.

4. Naive Forecasting Model in Python - part 1
=============================================

Hey, guys, welcome back. In this lecture, we will see how to build naive forecasting models in Python. All right, now I'm in the Google Drive. What I need to do here is create the Colab, and the data I'm currently working on is the US airline carrier passengers data, already uploaded. This is the same data we will work on in this example too. OK, so first let me open Google Colaboratory and do all the necessary installations and setup, if required, all the necessary steps.

OK, now let me change the name: smoothing techniques. OK, smoothing techniques. So the first step, what I would do here is all the necessary setup, like import os, from google.colab import drive, and drive.mount to mount the drive. You'll get the URL here; click on that, select the appropriate email address, get the authentication code here, copy this and paste it. The next step you need to do is os.chdir, and remember the path; we already did this before.

I was in the My Drive folder: /content/drive/My Drive, and next I was in the complete time series folder, followed by smoothing techniques. So the folder name I use is smoothing techniques; smoothing techniques is the name of the folder. So let me check with ls: I'm in the same directory. And let me check the data folder. Yes, of course, this is the data. And the next step we need to do here is import all the necessary libraries.

So the first thing is numpy as np, pandas as pd, and for visualization, I'll use matplotlib.pyplot as plt, and also seaborn as sns, and also for date and time, I will go for datetime. These are all the libraries that are necessary for us to do the processing now. All right, so let's execute it. Now the next step is to load the data and do the necessary preprocessing operations.

The preprocessing we already did in the previous section, and we will do the same thing now here. Let's load the data first: pd.read_csv, and the data was in the data folder, and it was my US airline carrier passengers file, df.head. And if I look into the top five rows, this is how it looks: the month from 2000 up to 2019 December, and also we have the number of passengers on board in that particular month.

Right. So let's look into the info here. If you look into the info, the problem is that the month is actually a date and time format, but it is an object. So in order to convert it, we need to use pandas to_datetime. Let me do that: df.Month equals pd.to_datetime, and I need to pass the month. Now we can look into df.dtypes, so you can print the data types of the month.

So now it is in the datetime format. And if you want, again visualize your data so that you can understand the behavior or the pattern of the data you have. So just for the visualization, we can use matplotlib: the x axis is the month, and the y axis is my number of passengers. So plt.plot, and I get a nice plot here. In order to increase the plot size, I'll use plt.figure with figsize, 15 comma maybe eight, so that I can get a bigger size.

And if you want dotted lines and circles, we can get a nice dotted line with circles. That's what we can simply do. And if I want to get the markers in white, I'll use markerfacecolor, set to white, instead of solid blue. And this is my original data. Right. So I can add a legend, and this is my true data, located at the upper left.

It's the true data. OK, so that's what we can see here. The data is from 2000 to 2020, and we have some kind of seasonality there. We already built a regression model. Now let's see how to do the smoothing techniques. Step number one: let's split the data into two parts, one is training and second one is testing. For training, I will take the data up to December 2016, and for testing,

I'll take the rest of the data, whatever I'm having with me. All right. So in order to do that, we need to execute the query here: the condition on df.Month, the date should be 2016-12-01. So this is the date I'm looking for. All right. So let's take the date; this should be a date.

So let me put it in the datetime format, because the date is a string; convert that into a date format. I already imported datetime, and with the string format, what I want is strptime: I just want to convert that into the format. Let's set the date, and I need to specify the string format. What is the string I'm having? The first one is capital Y, the second one is the month, capital M, and the third one is day. So this is the condition; basically my condition will be passed to

df, and what I get here is the training data. So it is less than or equal to: everything less than this date is my training data. All right. So let's look into the head of this, and we got all the values; let me check that this is the most appropriate one, up to 2016. Up to 2016 I was requesting here, but it shows 2016-01-01.

OK. That is wrong. OK, I think it's small m; not capital M but small m; with small m we will get it, as it's the month, not capital. All right. So similarly, let's go for my test data: copy and paste. This is my test data, anything more than this; anything more than this date should be my test data. All right. So let me check df_test.head, and you can see 2016 December.

This is the data we have. So let's visualize this; we can also visualize this part. And what we can do here is all the necessary visualizations. We have the training data: this is the train data, the month, and this is the test. So let me check this: df_test. And instead of blue, I will go for maybe some other color, probably green or whatever. So this is the train data and that's my test data.

So, true data, and this is the future data, the future true data. OK, that's what I'm having with me: future true data. So that is what I need to forecast. The smoothing methods will do a different kind of thing, but anyway, this is the basic data preparation and visualization we did. In the next lecture, we will see how to build naive forecasting models. Thank you very much.

5. Naive Forecasting Model in Python - part 2
=============================================

Hey, guys, welcome back. Now let's see how to build the naive forecasting model. The naive forecasting model is one of the simplest models. What it is trying to say is: if you want to predict the future, that is Y t plus one, the future value is going to be equal to your previous value, Y t. That means you can forecast tomorrow's value as equal to today's value.

So that's the meaning of this technique. It's very straightforward and one of the simplest things. All right. So let's see df_train. This is what you have in df_train: this is the true data, and the forecasted data, or fitted values. Let's say this is my fitted values. The fitted values basically mean: if you want to forecast this day, for example 2000 [unclear], the forecasted value is nothing but the previous value.

What is the previous value we got? It is four six four nine two. That's it. That is the forecasted value for this. So how to get that? It's basically a one-period shift. OK, we have the shift here: shift of my passengers. So df_train; we can simply use pandas: df_train.passengers.shift. Basically the default period is equal to one. That's it. So your model is ready now.

So df_train.head, and I can see it's basically shifted. So suppose you want to forecast this value: the forecast for this value is nothing but the previous value; that's the forecasted value. All right. So this is what we have. Let's look into the tail here: df_train.tail. And similarly, you can see that in 2016, the forecasted value for 2016 November is basically this value.

And for the December month, it is basically this value. And now for January 2017, for the month of January, that is going to be equal to this value here. And similarly, for 2017 February, we don't have the data of the previous value, so if we want to forecast that, it's actually the same value. So what is the forecasted value?

It's actually the same value. So in the end, the moving average or smoothing techniques are only able to forecast one time period ahead. That's it. So this is how it can be done. All right. So let's look into the tail of df_train. And for the test, the forecasted value here is nothing but that. That's your forecast value. So let's take df_test's forecast,

and that's equal to my passengers: the last value of passengers we got, that last value is the forecast. So that is your forecast value, df_test.head. Now this is your forecast value for all your data. So that's how you can do it. Now let's see the visualizations, and just keep aside the calculation of the margin of error. I'll do the margin of error once I do the visualizations.

OK, now this is the data; let's copy and paste it here. Now, what we have to do here is: these are my fitted values; just copy and paste, and this is my fitted values. Right, these are my fitted values here; instead of blue, maybe I'll change the color to orange. All right, so for orange color, maybe the orange solid line could be the better one: the orange solid line

and a square marker will be good for that. And similarly for the forecasting values, I could use the same orange line, or probably I can go for red color; and this time I would go for a solid line, and it's the forecast. That's it. So that's your forecast. So let me execute this. And you can see here, the blue portion is basically the true values, and the orange is your fitted data.

So let me label this as fitted values, followed by the future data. And the red portion is basically: you can only predict one value. That's it. So the red portion is your forecasted values, forecast data. All right, so this is how we can do it. And we can calculate the margin of error, and the margin of error basically comes from the error between the true data and the fitted values. That's minus this; this is basically the error.

And for this error, I need to calculate the standard deviation; that's the standard error. For this data, I need to calculate the standard deviation, and from that the margin of error. So that's basically my margin of error: 1.96 for a ninety five percent margin of error. So what we get is this. Right. So if you want to fill the confidence interval, we can use plt.fill_between, and we take the true values.

Basically, I'll take the test data, df_test's month, followed by y. So y is basically the forecasted value plus ME, and ME stands for margin of error, and the second one is the forecasted value minus ME, and the color. I can set the intensity or opacity: opacity 0.1, so 10 percent opacity. ME is not defined; execute this first, then this again. All right, so that's our forecasting.

So I can add one more thing: the confidence interval label. All right. So we can perfectly visualize the data. If you want to visualize it much closer, you can set the scale here. We can do that with scaling here so that I can limit the range. For that, I just want to visualize between probably the year 2015, 2016 and 2017; that is what I want to visualize in that case.

What we can do here is use plt.axis and set the xmin and also the xmax. All right. So xmin and xmax: basically I want to give the start date here. The start date is probably 2015, and I want the whole year, 01-01, and the end date, I want to go probably for 2017-01-01, and I need to convert that date into the date format.

So datetime.datetime.strptime, and I set the format here: the first one is capital Y, the second one is the month, I think a small m, and the third one is d. So let me copy and paste it here. Also copied and pasted. Right. So this is my start date and this is my end date. Oh, we got an error saying it is required... Oh, it is not datetime.datetime; it is datetime.strptime, not the string, right?

strptime. All right. Good. This is nice, right? This is how we are going to forecast. Instead, we take 2018, so let me take the end as that. So now you can see these are the true values; the orange one, you can see, is the forecast: the value of the day before is the forecast for tomorrow, and so on. And these are the true values, and these are the fitted values, and the red line is the forecast. And you can see that green is the true data, and this is the forecast here.

We can only forecast with the previous value we got; that will be the forecast for the rest of the period. Basically, we can forecast only one particular value. So that is one of the many disadvantages here. But still, naive forecasting is one of the simplest forecasting modeling techniques. In the next lecture, we will talk about the simple moving average. Happy learning and enjoy your time. Thank you very much.

6. Simple Moving Average
========================

Hey, guys, welcome back. In this lecture, we will talk about the simple moving average. The simple moving average is also known as MA(q). This is one of the simplest and most elementary averaging methods. In this method, in order to forecast the time t, we will take the past q values and average them, and that will become the forecasted value. So this is actually one of the simplest things in the smoothing techniques.

So what we are trying to do here is take the past q values, also known as the past q lags, previous lags, and take an average of all the lags, and that will be the fitted value. How you select the order is based upon the ACF, the autocorrelation function: the number of non-zero lags will be the order q. And we applied it to this data and calculated for q equals three. This is what the average model will get for three, and for q equal to 12, it is much smoother and it's almost able to capture the trend in the data.

And that's what we are able to do in this case. And the forecasted values, again, are just like the naive method: the last fitted value we got is basically the forecasted value for the future. Thank you very much. We will see the simple moving average model in Python in the next lecture.

7. Simple Moving Average in Python
==================================

Hey, guys, welcome back. In this lecture, we will talk about how to build a simple moving average model, also known as the MA model, in Python. OK, so we've already done all the basic preprocessing, and everything has been done for the naive based model, the naive forecasting model. What we will do now here is take the same data, df_train; let's take the same data, and from this data, let's see how to build the simple moving average models. All right. So the simple moving average model.

So this is already there; actually, I don't require these fitted values. Let me do one thing: let me copy; this is my train_sma, simple moving average, and in that I'm only interested in the month and the passengers. These two pieces of information are required for me. Similarly for the test, test_sma: let me consider only these two values. All right, so now in order to forecast this, let me build a simple model like SMA.

SMA stands for simple moving average, of order three. Order three means we take the past three values in order to forecast the future value. So the fitted values, for example, the fitted value for this: we take the past values. We take this, this and this, these three values, and we average the values. The average of these three values will be the forecasted value for the next month.

So, for example, the average of January, February and March is going to be the forecasted value for 2000 April. That is the principle of the simple moving average of order three. So let's build that. In order to build that, we have the rolling window: rolling. So it asks for the window, which means the number of periods that we actually require.

For example, if I set it to three, it'll take three values. And for those three values, we need to specify what you want: you want the mean, or the median, or the variance. We can take the mean; it's a moving average, so you can take the mean, you can take the median, or else you can also take the mode; it's up to you. So we take the mean here. You can calculate the mean, the median, the standard deviation,

and the variance; all those things can be calculated with this. All right. So here I took the mean, and what we got: first, for these three, the average of these three, this plus this plus this, divided by three. That is equal to four six four nine two plus four eight five two six plus five eight seven six four, and the average of that, divided by three, and that is equal to five one two six zero point six six.

So that's the value we got here for the fit of order three. So it is one of the simplest: the simple moving average. So let me take train_sma, and this is my fitted values: fit_3, the fit of order three, that's what we build here. It's very simple and pretty straightforward. And the final value of this: the final value, just look at its tail. The final value is six eight three seven zero; this is the final value you got.

So this is basically our forecasted value for the future. Basically, this is the forecast value for January, for January 2017. And for all those things, we can only forecast one value. So that's it. So what we will do here is test_sma, and this is my forecast, and that is equal to this. That's it. So this is how we can do this simple forecasting model. So let's visualize this: let's copy this entire thing.

So let me copy this, plus this one, and also this; copy and paste. I just need to calculate the margin of error and put it in the same place. Right. So let me replace this with train_sma: this is train_sma, and this is the fitted values of three, fit_3. And you'll get the margin of error for three, the margin of error for three:

ME_3, and that's going to be equal to this. All right, so let me replace everything: this one, this one and this one, and similarly the forecast, and this is the test: test, test, test, and test, test and test. And one more thing: this is test too. All right, so let me do one thing: I don't want the scaling here, so let me comment that part. So let me visualize everything: it is ME_3, and this is also ME_3, and this is ME_3; execute.

So I'm getting an error here. This is the fitted value I talked about: it's fit_3, three. The forecast: this is my forecast, also my forecast. Now you can see these are the fitted values we got here; these are basically the fitted values. And if you want to scale it, you can do that. If you really want to see this, this is how it looks: it's basically smoothing.

It's not just a simple prediction like the naive method: we are taking these three values and trying to forecast with them, averaging them. So that is how we are able to build such kinds of models here. Right. So this is basically how it looks, and this is nice. And similarly, the point here is that the order q depends upon the ACF. In the next lecture, we will see how to select the order q, and we will build a simple moving average model with the order q which we get from the autocorrelation function.

Thank you very much.

8. Simple Moving Average order (q) in Python
============================================

Hey, guys, welcome back. In this lecture, we will talk about how to build a simple moving average model, also known as the MA model, in Python. OK, so we've already done all the basic preprocessing, and everything has been done for the naive based model, the naive forecasting model. What we will do now here is take the same data, df_train; let's take the same data, and from this data, let's see how to build the simple moving average models. All right. So the simple moving average model.

So this is already there; actually, I don't require these fitted values. Let me do one thing: let me copy; this is my train_sma, simple moving average, and in that I'm only interested in the month and the passengers. These two pieces of information are required for me. Similarly for the test, test_sma: let me consider only these two values. All right, so now in order to forecast this, let me build a simple model like SMA.

SMA stands for simple moving average, of order three. Order three means we take the past three values in order to forecast the future value. So the fitted values, for example, the fitted value for this: we take the past values. We take this, this and this, these three values, and we average the values. The average of these three values will be the forecasted value for the next month.

So, for example, the average of January, February and March is going to be the forecasted value for 2000 April. That is the principle of the simple moving average of order three. So let's build that. In order to build that, we have the rolling window: rolling. So it asks for the window, which means the number of periods that we actually require.

For example, if I set it to three, it'll take three values. And for those three values, we need to specify what you want: you want the mean, or the median, or the variance. We can take the mean; it's a moving average, so you can take the mean, you can take the median, or else you can also take the mode; it's up to you. So we take the mean here. You can calculate the mean, the median, the standard deviation,

and the variance; all those things can be calculated with this. All right. So here I took the mean, and what we got: first, for these three, the average of these three, this plus this plus this, divided by three. That is equal to four six four nine two plus four eight five two six plus five eight seven six four, and the average of that, divided by three, and that is equal to five one two six zero point six six.

So that's the value we got here for the fit of order three. So it is one of the simplest: the simple moving average. So let me take train_sma, and this is my fitted values: fit_3, the fit of order three, that's what we build here. It's very simple and pretty straightforward. And the final value of this: the final value, just look at its tail. The final value is six eight three seven zero; this is the final value you got.

So this is basically our forecasted value for the future. Basically, this is the forecast value for January, for January 2017. And for all those things, we can only forecast one value. So that's it. So what we will do here is test_sma, and this is my forecast, and that is equal to this. That's it. So this is how we can do this simple forecasting model. So let's visualize this: let's copy this entire thing.

So let me copy this, plus this one, and also this; copy and paste. I just need to calculate the margin of error and put it in the same place. Right. So let me replace this with train_sma: this is train_sma, and this is the fitted values of three, fit_3. And you'll get the margin of error for three, the margin of error for three:

ME_3, and that's going to be equal to this. All right, so let me replace everything: this one, this one and this one, and similarly the forecast, and this is the test: test, test, test, and test, test and test. And one more thing: this is test too. All right, so let me do one thing: I don't want the scaling here, so let me comment that part. So let me visualize everything: it is ME_3, and this is also ME_3, and this is ME_3; execute.

So I'm getting an error here. This is the fitted value I talked about: it's fit_3, three. The forecast: this is my forecast, also my forecast. Now you can see these are the fitted values we got here; these are basically the fitted values. And if you want to scale it, you can do that. If you really want to see this, this is how it looks: it's basically smoothing.

It's not just a simple prediction like the naive method: we are taking these three values and trying to forecast with them, averaging them. So that is how we are able to build such kinds of models here. Right. So this is basically how it looks, and this is nice. And similarly, the point here is that the order q depends upon the ACF. In the next lecture, we will see how to select the order q, and we will build a simple moving average model with the order q which we get from the autocorrelation function.

Thank you very much.

9. Weighted Moving Average
==========================

Hello, everyone. Welcome back. In this lecture, we will talk about the weighted moving average. The weighted moving average is similar to the simple moving average, but in the weighted moving average we give preference to the most recent value over the previous values. For example, if you want to forecast Y t, we use the past few lags like Y t minus one, Y t minus two and so on.

And we give more preference to Y t minus one, less preference to Y t minus two, and comparatively even less to Y t minus three. So what we are trying to do here is multiply with weights: we multiply the highest weight with the previous value, and less weight with the values before that, t minus two and so on. So for example, if you have a weighted moving average of three, the weights are three, two, one.

We give the most weight, three, to the previous one, t minus one: three into Y t minus one; then two into Y t minus two; and one into Y t minus three, which means we are giving less weight to this value. That's what we do in this case. And this is the weighted average. Compared to the simple moving average, in the weighted moving average we give more preference to the previous value, so that we can get good results; that is what we're hoping for in the weighted moving average.

And the outputs for the weighted moving average look like this: this is for q equal to three, and this is for q equal to 12, for the weighted moving average. All right. So this is how we are able to build a model using the weighted moving average. In the next lecture, we will see how to build the weighted moving average model in Python. Thank you very much.

10. Weighted Moving Average in Python
=====================================

All right, welcome back. Now let's see how to build the weighted moving average model in Python. OK, this is the formula for the weighted moving average model; now in Python. So let's see how to build a weighted moving average model in Python. Let me do one thing: let me copy the data from df_train. This is train_wma, and what I want here from the train is just the month and the passengers information. That's it. Take the month here and let me take the passengers.

Passengers; OK, and similarly for the test, let me take those two values. Done. So let me have a look into the head and the tail of that, and this is the tail. OK. All right. We are good to go. Now, what I want to do here is build the weighted moving average model. So let's say I build a weighted moving average model, WMA, of order three.

Let's say I just want to build WMA of order three. So what does it mean? Order three means, let's say these are the three values; just take them here, OK? So I need to give more weight to the previous one compared to this value, and compared to this value. So in order to do that, basically this should be three into five eight seven six four, plus two into four eight five two six, plus one into four six four nine two.

That's my numerator. And the denominator is basically the sum of all the weights: three plus two plus one. So that's your fitted value, right? So that's my forecast, and the forecasted value for this, the fitted value for the next one, will be five three three three zero point six. That's the weighted average. So how exactly do we do this kind of calculation? In order to do that, I write a function.

Right. So in this function, I write it as weighted moving average: I'm writing def wma, taking the weighted moving average. This is what I need to do here. I assume that I'm getting X here. So this X consists of three values, let's say three or more values. So these values will be there. All right. So now what I'm going to do in this case is give more weight to the previous one.

For example, more weight to this value, and less weight to this, and less to this. So this is what I just want to give. So let's execute this step by step. So first of all, I need to generate the weights. How to generate the weights is the question here. So basically, the number of weights is equal to the length of this. OK, so the number of weights is equal to the length of X.

OK, so that's basically the number of weights. So let me generate them: I'll take np.arange. In np.arange, the start value is this, the stop value is basically zero, and the step is minus one. So that will be my weights, right? So let's print the weights first. OK, so let's assume that I'm having three values in a list, for example: this one is five eight seven six four, and four eight five two six,

and four six four nine two; this is the list that was there. OK, I'm getting the weights: this is three, this is two, and this is one. All right, so the next step, what I want to do here is multiply. I just want to do the dot product, for example, np.dot. And this is what I'm having with me: a NumPy array, so I can use this, and we got an array.

And what I can get here is, for example, three, two, one, approximately. That's what basically I need to do. So let's say I'm getting X here, and remember, X should be a NumPy array. All right. OK, that's what you should understand. So X, and what do you want here? I just want to multiply it, np.multiply, or simply the dot product, or else you can simply do this multiplication:

X into weights. That's it. So that's my numerator, and for the numerator, again, we need the sum of all those things. OK, so np.sum of this, and what you'll get is the sum of all the values. So we got the sum of X into weights. And finally, the denominator is basically the sum of weights. That's it: np.sum of weights. And my weighted average is going to be equal to numerator divided by denominator.

And let me try it; this is what I want to do in this case. So let's do one thing: let me take the sample data here, just to verify what it is going to do in this case. So I'm taking the sample data, and for the sample data, let me take the passengers. So we have the passengers here. And for these passengers, I will take the rolling window. Basically what I'm doing here is taking the rolling.

OK, so I just want to print X, just to check the value of X and what it is operating on in this case. OK, so the window: I'm taking window three, which means I take three values and apply this formula. Apply what I want to apply here: apply the weighted moving average. OK, apply the weighted moving average. So that's what we got here. And let's print the sample. All right. So the first value is four six four nine two.

That is what we want. OK, I think we need to give more weight to this compared to those values. So in order to do that, let me generate from one to length of X plus one. OK, why am I changing this? Because this is first and this is second, so the order is changed. That's why I change this, and this is plus one. Right, so now let's see what is going to happen here. This is what we are expecting; we need to cross-check, verify it once again.

Otherwise, you will get wrong values. So let's print the WMA and apply this again; let's apply this model. And what I got here is that we are getting three times the weightage for five eight seven six four, plus two times four eight five two six, plus one times four six four nine two. And this is the numerator, and the denominator is basically equal to three plus two plus one, six. So this is the value we expected.

Correct. So this is the model I just want to build, and I think everything is correct. So let me comment out the print statements. Now, I'm going to apply it to my entire data. So this is for my passengers: take the rolling window, and the window is equal to three; assume the window is three, and that's your fitted value: fit_wma_3, for three.

That's it. This is how you can fit. So let me do one thing: since we already calculated q in the previous section, the same way we can take q as 12, which we got for the simple moving average; we do the same here also. Take 12 here and apply the function: apply, and the function here is the weighted moving average. That's it. This is the function I need to apply here, and I'll get the moving average for all of that.

So this is for 12. So let me check train_wma.head, and what we got here is basically: you take the weighted average of these three and you'll get this. OK, so that is what we got. Let me put the tail here; this is my tail, and we'll get the last five values. So this is with three, and this is with 12. And the forecasted value: if you take 12, it is this, and the forecasted value for three will be this.

OK, so let me put it into my test data frame, test_wma, and this is my forecast_3 for three; that is going to be equal to this. And similarly forecast_12 is going to be equal to this one. OK. All right, so we are ready to go now. Let's take this 12. Let me plot the 12 one; I'll take only the 12. You can put both on the plot, three and 12,

but I'm plotting with 12 lags. OK, so 12. Just change a small thing here: this is WMA; change to WMA. This is my fit of 12, and this is ME, and obviously this is train_wma, and this is test_wma: test, test, test. All right, so we are good to go now. Let me execute this. We got an error. Maybe it is WMA, OK, wma... this is forecast; I guess the spelling of forecast is wrong. It's OK, I think everything is good now.

Let me execute it again. So that's it. What happens is that we give more weightage to the previous value compared to the earlier history. So this is the basic difference between the weighted moving average and the simple moving average. It is believed that the weighted moving average performs better compared to the simple moving average, because the most recent value has more information compared to the earlier values. That's the idea of the weighted moving average.

In the next lecture, we will talk about the exponential moving average, which is also one of the most widely used smoothing techniques. Thank you very much. We will continue in the next lecture.

11. Exponential Moving Average
==============================

Hey, guys, welcome back. In this video, we will talk about the exponential smoothing models. The exponential smoothing model is also known as the exponential moving average. In this smoothing technique, we weight the data from previous time periods with exponentially decreasing importance in the forecasting. Exponential forecasting is accomplished by multiplying the actual value for the present time period by a value between zero and one.

So what we are trying to do in the exponential smoothing technique is actually simple. To take the exponential moving average, we can take a simple moving average for the first forecasted value, the simple moving average of the first values. And after that, we will use the forecasted value and add the error on top of it. That's basically what we're trying to do in this case. For example, the forecasted value F t plus one is equal to alpha, which is the exponential smoothing constant, into Y t, which is the previous historical value, plus one minus alpha into F t. So F t plus one is the forecasted value for the next time period, t plus one,

and F t is the forecast for the present time period, and Y t is the actual value for the present time period, and alpha is the value also known as the exponential smoothing constant, which is a value between zero and one. What I mean to say is that we are giving exponential smoothing to the lags: just like the weighted moving average, but with decreasing importance in an exponential way. This is how it is.

Let's say this is F t plus one is equal to alpha Y t plus one minus alpha into F t, and F t can be written as alpha Y t minus one plus one minus alpha into F t minus one. If you substitute this into this equation, this is what you will get, and again F t minus one can be represented by alpha into Y t minus two plus one minus alpha into F t minus two, the whole square, and so on. So what you're getting in this case is F t plus one equals alpha Y t, plus alpha into one minus alpha into Y t minus one, plus alpha into one minus alpha whole square into Y t minus two,

and so on. That's basically what the exponential moving average smoothing technique is trying to do: we are decreasing the importance at an exponential rate, more or less. Basically, if you think from a different perspective, in error terminology: F t plus one is equal to alpha Y t plus one minus alpha F t; we can rearrange it and write this as F t plus one is F t plus alpha into Y t minus F t.

Basically this is our error; this term is basically called the error. So how do we select the value of alpha here? There is no arbitrary choice: generally we try values from zero to one, and whichever gives the minimal error, we select that. Generally, with a small alpha, we have less impact of the error. So basically the forecasting value is: we take F t, and we add alpha multiplied by the error.

So that's basically what it means. So when the value of alpha is small, it has less impact of the error on the new forecast, whereas when alpha is large, it has a larger impact of the error on the forecast value. And of course, we have the data, and what we did for q equal to three, and this is for q equal to 12, and we'll get more or less the same results as the weighted moving average. But it depends on the data; with the data, that is going to change.

In the next lecture, we will see how to develop the exponential moving average model in Python. Thank you very much.

12. Exponential Moving Average in Python
========================================

Hello, guys, welcome back. In this lecture, we will see how to build the exponential moving average model in Python. Just try to remember one thing: when you're trying to build an exponential moving average, we don't need to select a larger number of lags, like in the weighted moving average and also the simple moving average. Generally we select lesser values, because it automatically takes care of that particular lag part.

OK, that's what I'm trying to say: it takes care of the number of lags, because expanding this formula again and again covers a larger number of terms. So you don't need to select many; only for the first prediction, that's where it's used: only for that do we select the lags, going for the simple moving average inside it. All right. So let's do that: train_ema. This is my exponential moving average.

So I'll take the train, and what I want here is the month, and the second one is the passengers. All right, so this is what I want, and similarly for the test: these two columns are what I'm interested in. And the next step, I'm trying to build an exponential moving average. pandas directly has the exponential moving average. So we'll take that from pandas: train, and let me take the passengers.

And what we have here is the exponentially weighted moving average, ewm; basically it's the exponential moving average. I can take it here, and basically I need to set the min_periods: what is the minimum period I need to take here? At least, I'll take three. That's it. So now it will apply the formula. And also I need to specify alpha. Alpha is the very important thing here, because we need to build the model for different values of alpha.

And based on that, whichever alpha gives the minimum error, you select that. And remember one thing: the lower the value you give, the less the impact of the error, and the higher the value, the more the importance. So I select alpha 0.5, just giving medium importance to the error. OK, so this is my train fit, and this is for three; you can try different values of the periods and different values of alpha to select the best. And how do you select the best? Based upon the mean squared error.

That's it. So we're done with one model. Let me execute. Oh, I think it is ewm, exponential moving average. OK, yes, we got an answer. So what we will do: it is df_train, and for the values we get from the exponential, I'll take the mean. I'm going to take the mean here; we can take mean, median, variance, deviation; everything can be taken here.

So we take the mean here. OK, this is the fit, and the forecasting value again, just like your simple moving average and also the weighted moving average, is the last value. This last value is going to be the forecast for the future. So let me do one thing: let me take test_ema, and that is my forecast for three. And remember, that is for alpha equal to 0.5, because you need to try different values of alpha to get a better fit.

So basically you are trying to do a grid search methodology to find out the best fit. I'm doing only one case here, but you can try multiple values so that you can select the better value of alpha. OK, so this is the forecasting model, and my model is ready here. So I'll just plot it. To do that, let's copy and paste it below. And now, what we will do:

this is not the fit of 12, it's of three. That's it: with three, and alpha is equal to 0.5. I'm just doing only one particular case, and you need to do it for all the cases. OK, and I take this train_ema. OK, and test_ema; just copy and paste it. I'm sorry.

Yes, OK, now test_ema: this is test_ema, this is test_ema, and this is not just forecast; it is forecast of three, 0.5. This is what it means. I'll take this one, and this is the fit of three, 0.5, and this is forecast three, 0.5, and that is the ME, 0.5, three. All right, so I think everything is good. Now let's plot it. OK, we got some error: forecast somewhere here.

We got an error. I think it's here: forecast, of course, 0.5; we copied and pasted. This is test_ema; basically, OK, all right, that's the name. Please execute again. OK, now we got it. So these are the forecast values for alpha equal to 0.5, and I think it is somewhat better compared to the rest, and the error comes down. And if you just take different values of alpha and different values of the window size, just check them, and whichever has less standard error,

you select that particular model. So this is about the exponential moving average, how to build an exponential moving average. In the next lecture we will see the ARMA models and ARIMA models, where we are trying to mix two or more models: ARMA is a mix of auto regressive and moving average, and ARIMA is auto regressive integrated moving average. And we will also talk about SARIMA, seasonal auto regressive integrated moving average, and also some advanced models in time series

in the upcoming lectures. So thank you very much, and happy learning.

## 12. Non Seasonal ARIMA models

1. ARMA
=======

Hello, everyone, welcome back. In this lecture, we'll talk about the auto regressive moving average model, a.k.a. the ARMA model. It is also known as ARMA(p, q). The ARMA model has played a very vital role in time series modeling. The ARMA model consists of two parts: auto regression and the moving average model. So what we are trying to do in the ARMA model is combine the two models, auto regressive and moving average; both models play a very efficient role in predicting the future.

So with the help of the ARMA model, by combining the two models, we can get a much more efficient way of building the time series model, and we can get much better predictions compared to the individual auto regression or moving average model. It is also capable of modeling the ongoing process with a small number of parameters. This model is also referred to as ARMA(p, q), where p stands for the order of the auto regressive model and q stands for the order of the moving average model.

And together, we call it the ARMA model of p, q. In the next lecture, we'll talk about the non-seasonal ARIMA model. Thank you very much.

2. Non Seasonal ARIMA
=====================

Hello, everyone, welcome back. In this lecture, we will talk about the non-seasonal ARIMA model, a.k.a. ARIMA(p, d, q). The acronym ARIMA is auto regressive integrated moving average. This model is considered to be a development of the simpler auto regressive moving average, ARMA. Here we introduce a concept called differencing, or integration. Basically, ARIMA and ARMA share similar characteristics, like leveraging the auto regressive and the moving average models.

So let's see the difference between ARIMA and ARMA. One of the limitations of the ARMA model is that it works well for stationary time series data, whereas for non-stationary time series data, the ARMA model basically struggles. In order to work with non-stationary data, we have a concept called integration. Integration is the process of estimating how many non-seasonal differences are needed to make the time series data stationary. It is possible to make the non-stationary data stationary by applying differences.

That is the parameter d. It says how many non-seasonal differences are required to make the data stationary. Hence, the ARIMA model basically consists of three components: p, d, q. p stands for the number of lag variables, nothing but the auto regressive part, and d stands for the number of non-seasonal differences used to make the time series data stationary. And q stands for the size of the moving average window, also known as the order of the moving average.

Hence the ARIMA model is basically a modified version of ARMA; here it introduces a concept called integration, which basically defines the number of non-seasonal differences. In the next lecture, we will see how to build the ARMA model in Python. Thank you very much.

4. ARMA - Load Data
===================

Hello, everyone, welcome back. In this lecture, we will talk about how to build the non-seasonal ARIMA models in Python: the non-seasonal models ARMA and ARIMA. We are using the same data which we used in the moving average studies, the smoothing methods. So step one, we will open our Google Colaboratory and do the necessary settings, which we did for the previous lectures, like importing all the necessary libraries and also upgrading statsmodels.

All right. So let's change this Untitled0 to ARIMA models. Now connect. Let's wait for a few seconds until it gets connected. Done. So now what we will do is click on this file icon and mount our Google Drive. In order to mount the Google Drive, click on this icon and click Connect to Google Drive. Let's wait for a few seconds until it gets mounted. Done. So you can see that my drive has been mounted successfully. If you're not able to see that, just refresh your page so that you can see this.

Now, let's set the path here. In order to set the path, let's go to our respective folder: drive, My Drive, complete time series, and so on. So let's copy the path now. Just simple os.chdir, paste it, execute. So that's it. Now we have successfully executed our cell and set the path. Now just type ls; we can see that we are in the respective folder. Let's close this now. The next step is that we need to upgrade our statsmodels library, which we did in the previous section.

So for that, pip install upgrade statsmodels. Execute. Let's wait for a few seconds until statsmodels gets installed successfully. Done. I have installed statsmodels successfully. So let's also import the necessary libraries that are really required to build the model. Let's start with the basic libraries: import numpy as np, import pandas as pd, import matplotlib.pyplot as plt, import seaborn as sns, and also import the statsmodels libraries, like the ACF and PACF plots.

So for that: from statsmodels.graphics.tsaplots import plot_acf, plot_pacf. It's statsmodels; let's do it again: from statsmodels.graphics.tsaplots import plot_pacf and plot_acf. And also import the non-seasonal model, that is ARMA. For that, from statsmodels.tsa, time series analysis, .arima_model import ARMA, and ARIMA, the non-seasonal models. So I can put a heading: what we're discussing now is that we are building the two non-seasonal models, non-seasonal ARIMA models, which are ARMA with order p, q, and ARIMA

with order p, d, q. All right, so this is what we have. Next, we will also import datetime: from datetime import datetime. Execute. And if there are any warnings, I don't want to display all the warnings. So import warnings, and warnings.filterwarnings: whatever future or other warnings, I just want to ignore them. Execute.

OK, now we have successfully imported all the libraries. The next step is to import our data. You can click on this, and we know that we are already in the models folder, and this is the data. This is the data I just want to load, so let's load the data: df is equal to pd.read_csv, and it was in my data folder, US airline carrier passengers. So let's do df.head. Execute. All right, so now we have successfully imported our data.

5. ARMA - Split the Data into train and test sets
=================================================

All right, so now we have successfully imported our data. Let's also do some quick things: split the data into training and testing, set the month as my index, and also do some quick visualizations. So first let's split the data into two parts, training and testing. For a quick overview: in the previous section, the data we have is from 2000 to 2020, with all the monthly passengers displayed.

The train data we took is from 2000 January first to 2016 December. This is the train data we took last time, and we are using the same settings now. And similarly, the test is from 2017 January first to 2019 December 1st; these are the settings we used previously, so let's use the same settings. And remember, when we look into the dtypes,

the month is an object. So what we need to do is change this object into datetime format. For that, step one: df.Month is equal to pd.to_datetime of df.Month. Done. So we have successfully converted it. Next, we will split the data into train and test. My train data is basically up to the cutoff date, so let's put the cutoff date: datetime.strptime, and let's give the date.

It is 2016-12-01; that is my cutoff date. And let me specify the format: first the year, followed by month, and followed by date. So this is the datetime format for this particular string. So now, df where the month should be less than or equal to this cutoff date is my train. And similarly, my test is df; let's copy everything, paste it, and where it is greater than this cutoff date is my test data.

Now, let's set the index: set the time as index. Here the time is the month. I set month as the index, so train.set_index, with the month. And similarly, let's do it for the test data: test.set_index of the month, and inplace equal to True, even for my test data, inplace equal to True. Execute. So I think done. Now we can see this is my train.head. OK, and similarly, let's look at the tail.

Yes, this is what I'm expecting. And similarly for the test, let's see test.head. Execute, and let's display the values. Yes, exactly. This is what I want. So let's also quickly visualize our data frame. To visualize, I will take train.plot, and the kind of plot I just want is line. Let's also increase the size of the figure: fig comma ax is equal to plt.subplots. Let's increase the size; this time I'll try to increase the size to 15

by eight, a big one, and let's add ax equal to ax. And similarly, let's also do it for the test data frame: test.plot, and the same thing I want: plt.ylabel and xlabel. The x label is the month, and the y label is my number of passengers. Execute. So done. This is what we're expecting. Of course, just try to understand: the blue one is train data and the orange one is test data. Let's also change this: in order to change the legend, the first one is train,

and the second one is my test. So this is my train data and this is my test data. I think now it is good. Now you can see that we have this information: this is my train data and this is my test data. So all the things have been done now. We'll continue in the next lecture, more on non-seasonal ARIMA models. Thank you very much.

6. ARMA - Steps to Build the Models
===================================

Hello, everyone. Welcome back. In the previous lecture, we have seen how to do the settings for the non-seasonal models. So now let's build the model. These are the following steps that we need to follow for our model. We can train it only on stationary data. So these are the following steps that we need to do while building the ARMA model or ARIMA models; the same procedure we will also do for the ARIMA model too. Step one: we need to test our data for stationarity, to make sure our data is stationary.

We can only build a model for stationary data. And if you look into this data, this data looks like non-stationary data: there is some trend in the data, and the mean is changing with respect to time. So what we can say is that this is not stationary data, so we need to do some kind of steps in order to convert it into stationary data. One of the methods of converting non-stationary data into stationary is differencing.

So we need to do the differencing so that we are able to build our ARIMA models. And once the data is stationary, we need to find out the values of p and q: p is the auto regressive order and q is the moving average order. The value of p can be found from the PACF plot, and the value of q can be found from the ACF plot. And once we know the order p and the order q from the stationary data, we will train the data with the ARIMA model.

And finally, what we can do is get the results and convert them back. The results we get from the ARIMA model are in stationary form. So what we need to do is convert them back from stationary to non-stationary. OK, so if the data was non-stationary, then we need to convert the results back from stationary to non-stationary. So this is the procedure we need to follow.

7. ARMA - Augmented Dickey Fuller test for stationary
=====================================================

Step one is that we have to test the data: we need to check whether the data is stationary or non-stationary. For that, we will do the augmented Dickey-Fuller test for stationarity. So let's do this test. This is my step number one: step one for the model is to do the augmented Dickey-Fuller test. Let's copy this and paste it. So we have it in statsmodels, and with the help of that, we can test whether the data is stationary or not.

Before that, we need to understand that this is hypothesis testing: the null hypothesis says that the data is not stationary, and the alternate hypothesis says that the data is stationary. So for the non-stationary data versus the stationary data, the p-value generally falls in the critical region or not. For example, let's say your significance level alpha

is five percent, the 95 percent confidence level; then make sure that your p-value is less than this. For example, if the significance level is five percent, then the p-value should be lower than 0.05. If the p-value is more than or equal to 0.05, then it is non-stationary data.

If the p-value is less than 0.05 for a significance level of five percent, then it falls in the critical region, and the alternate hypothesis says that the data is stationary. So this is basically what we are interested in: where it falls in the critical region; this is the margin. All right, so this is what we are interested in here. So let's import the library from statsmodels: from statsmodels.tsa.stattools

import adfuller. This adfuller is the augmented Dickey-Fuller test, so let's execute it. Done. So now we can call this function and just pass the data into it. For example, I can pass my train data into this, and let's see the results we're getting. Execute. Here the first value is the test statistic, and the second value displayed is my p-value.

As you can see, the p-value is greater than 0.05, outside the critical region. Hence, the data is not stationary. So from the above test, the p-value is greater than 0.05; hence, at five percent significance, the data is non-stationary, so I need to do differencing to convert the data into stationary. OK, so this is what we need to do whenever we have data: the first step is to check whether the data is stationary or not.

If the data is not stationary, then we need to convert it into stationary data by applying some differencing. We'll continue in the next lecture with how to convert the data into stationary by differencing with one lag. Thank you very much.

8. ARMA - Converting Data into Stationary
=========================================

We are converting the non-stationary data to stationary, and then we are dropping the NaN values; that's what we are trying to do now. So that's it; execute. So what we will do now is visualize our stationary data. For that, I can simply go for df.plot, a simple plot with kind equal to line, and fig comma ax equal to plt.subplots with figsize 15 comma eight. So that's it; this is how I can get a big figure. Oh, I need to set ax equal to ax.

Now here you can see we have converted the non-stationary data into stationary data. So let's test whether the data is stationary or non-stationary with the augmented Dickey-Fuller test. Let's copy it. Now we are doing the test for stationarity again, and this time I'm going to pass the stationary train data; execute it. And here we go: the p-value is 0.00325. And for five percent significance, obviously, if we consider five percent significance, the test statistic

value is going to be minus two point seven eight, and my critical value is minus three point seven [unclear]. So what we can say from that is that the p-value falls in the critical region. Hence we are rejecting the null hypothesis and accepting the alternate hypothesis, saying that the data is stationary. So let me write down here: from the above test results, the p-value is 0.003, which is less than 0.05;

hence, the p-value falls in the critical region. Therefore, we are rejecting the null hypothesis and accepting the alternate hypothesis, which is that the data is stationary. So that's it. Now we have successfully converted the data into stationary, and we tested with the ADF test, and we found out that it falls in the critical region, and therefore the data is stationary, and we are ready to build our ARMA model. So in the next lecture, we will see how to build the ARMA model.

Thank you very much.

9. ARMA - ACF & PACF , Train ARMA(p,q)
======================================

Hello, everyone, welcome back. In the previous lecture, we checked whether the data is stationary, and we did the test and found out the data is stationary. So now what we have to do is find out the p and q values for the ARMA model. p is basically the auto regressive model order, which we can find from the PACF plot. And similarly, q is the moving average order, which can be found from the ACF. So let's plot the ACF and PACF; we already imported them.

So we will simply do plot_pacf. I just want to find the partial autocorrelation function in this stationary train data, and obviously ax is equal to ax, and let's give the ax: fig comma ax equal to plt.subplots. In this case, I'll create one row and two columns, so nrows equal to one and ncols equal to two, and the figsize: let me increase the figsize to 15 comma eight.

OK, so this is my ax of zero. So let me put this in, and similarly let's copy and paste, and this time it is plot_acf on the stationary train df, and ax is equal to ax of one. So that's it. So let's execute it. All right, so this is how we executed the ACF and PACF plots, and what we can see here is that roughly there is a seasonality; we can understand that even from the data. There is seasonal behavior, and for that seasonality, we can see more from the partial autocorrelation plot.

And what we found here is that the cycle is repeated every 12 periods, and half a cycle is actually enough, so we can select a value of 12 for p, or six. There are different possible values of p, and of course we need to find out what the best value is. But here, from the plot, I can say the value of p could be anything more than six; anything more than six is good. At the moment, I'll take six.

And similarly, the order q we can calculate from the autocorrelation function. And that also says the same information: there is cyclic behavior. It seems to be purely cyclic behavior, and we found that in the autocorrelation function coefficients we have some cyclic behavior; that is what we can see. So here also q can be a full cycle, or you can also take half a cycle.

So it seems like for q, anything is a good value: anything more than six, up to 12; anything more than six is a really good value. One thing to keep in mind when selecting is that at least you select values greater than half a cycle. Again, we really don't know whether this value really works or not. That's the reason we will go for the auto ARIMA method later, where we will select the value of p based upon the AIC value. At the moment, what we will do is

build the ARMA model with p equal to six and q equal to six. All right. So now let's move to step number four, and step number four is that we need to train our model. So let's train the model. This is my step number four: train the ARMA model. OK, so the model is ARMA, and here you can see in the docstring the endog, which is nothing but our output, the stationary data. We have to give the stationary data to it.

And there it is: the stationary train df is what I just want to provide, and the order. The order is basically p and q, and I already know that p, q could be six, six, so it can take one of these values. You can't really be sure of that value, but anything more than six is good, because of the cyclic behavior. So I select the value six. OK, now what we are doing is we pass the data to it, we pass the order as this, and we fit the model.

Done. We have trained the model successfully. Let's continue in the next lecture, more on the ARMA model. Thank you very much.

10. ARMA - Evaluation
=====================

All right. We have trained our model successfully; now let's evaluate our model a bit. We can evaluate our model, or find the goodness of fit, with errors like the AIC, which is nothing but the Akaike information criterion, and we can also find the goodness of fit of the model with the mean squared error. So let's quickly calculate those values. Coming to the AIC value, the information criterion: this value is automatically calculated by the model, and the AIC is basically like an error:

the lower the value, the better. You can look into the AIC value for the model: three seven eight two [unclear]. That's really not that bad. And also, let's look into our mean squared error. If we want to calculate the mean squared error, we need to import the library: from sklearn.metrics import mean_squared_error. And we got our mean_squared_error. In order to calculate the mean squared error, we can calculate it for the train data, which is nothing but the fitted values.

So my fitted values are nothing but model_arma.fittedvalues, so I can get the fitted values from this. And this is your predictions; execute. So now the MSE, the mean squared error: the true values are nothing but my stationary df, and these are the fitted values, and here we go. Let's see what the MSE is: print the mean squared error, MSE. And the MSE is also very big. OK, here it is like eight zero five nine two two seven; that's your mean squared error.

In the next lecture, we will visualize the output of the model so that we can understand our model output better. Thank you very much.

11. ARMA - Visualizing Prediction Results
=========================================

Hello, everyone, welcome back. So let's visualize the output of the model; let's see some visualizations. All right, as we know, this is my train data. So let's copy and paste it here; this is the train data, and let's also visualize our fitted values: fitted_values.plot, and the kind of plot is equal to line, and ax is equal to ax. So that's it. So this is what we have, and it clearly shows that we have a really good fit.

It's not a bad fit; actually, we have a really, very good fit. And let me put the legend here. Basically, the blue color is the train data and the orange color is the fitted data. It's really a very good fit with our ARMA model. So let's put the legend in now: this is my train, and this is my prediction, my fitted values. All right. Oh, yeah. All right, so this is how my values look; it's really good and it's really nice.

So let's try to put it onto our original data. This is the original data. So let's try to fit it onto our original data. OK, for that, what we need to do is the forecasting; we need the prediction values. For the prediction values, we can go to our model, model_arma, and we can simply do .predict and give the start date and the end date.

That's really cool, right? So the start date is datetime.strptime, and we know that my test data starts from 2017 January first, and my end date, let me copy this. This is my start date, and this is my end date, and the end date is 2019-12-01. Now let me do the format here: it is percent Y hyphen percent m hyphen percent d. So the first one is the year, the second one is the month, followed by the date.

So done. So now we just need to pass the start and the end: start equal to the start date and end equal to the end date. So that's it. With this, we can get the prediction values. Execute. Now we can see that we get the prediction values. So these are the prediction values, but remember, what are the prediction values you're getting here?

These prediction values are stationary in nature. So make sure; if you visualize this, let's go back and copy this code and paste it here. Yeah, paste it. So if you plot those prediction values, you will get something like this. That's not what you're expecting, right? So we can do .plot with kind equal to line and ax equal to ax. And if you do this, this is what I'm getting here.

Basically, this is my true data, this is my test data, and this green line: the green one is my forecast, or the predicted values. But in order to make it the same, I need to... this is stationary in nature; I need to convert it back into non-stationary. So this is the prediction values, which are stationary in nature, and I need to convert them, in this case, from stationary to non-stationary.

So in the next lecture we will see how to convert the data from stationary to non-stationary. Thank you very much. We'll continue in the next lecture.

12. ARMA - Convert Stationary to Non - Stationary Data
======================================================

Hey, guys, welcome back. Now let's see how to convert the data from stationary to non-stationary. This is the prediction we got, and the output here is stationary in nature; how do we put that into non-stationary? For that, we can simply do the reverse of the differencing. We did the differencing, and I just want to do the reverse operation of the differencing, that is, the integration, or cumulative sum. What I need to do here is the cumulative sum.

In order to do the cumulative sum, I need the initial value, and the initial value is nothing but the last data point in my training data. You can see train_df.tail: the initial value is the last one. So this is the last data, and the last value is iloc of minus one, the last value I'm having here. This last value is my initial value. So I can take this, or I can simply call it my initial value.

Now, with this initial value, I can generate the cumulative sum. So these are my prediction values, and I can get the cumulative sum: np.cumsum, which will do the reverse of the differencing, and I can simply add it to my initial value, which gives my forecast values. So these are my forecast values: the initial value, which is nothing but my last value in my train data,

plus the cumulative sum of the prediction values, which gives the forecasted values. Execute. So now, let's copy the forecasted values in place of the prediction values; let me replace that with the forecasted values. Now let's execute it. Plot it, and now you can see these are my forecast values; it's really perfect, right? It's much better than the auto regressive model. It is a really, really excellent model. So this is how you can build an ARMA model with the value of p equal to six and q equal to six.

You can also try to fit your model for different values of p and q, but for p equal to six and q equal to six, this is the model we got. It's really very good. And we can complete our visualization: here we have the train and the test, and these are the forecasted values. This is really nice, right? It's a really nice way of building this. Let's change everything into a line style, or else I can change my alpha to 0.5, and also this alpha to 0.5, so that I can clearly visualize my forecasted values.

So this is now basically 0.5. Now I can clearly see my output. So this is really good, and this is really nice compared to the other models. This is how we are able to build the ARMA model. In the next lecture, we will talk about the ARIMA model. Thank you very much.

13. ARIMA
=========

Hello, everyone, welcome back. In the previous lecture, we talked about how to develop the ARMA model. Now we will try to build the ARIMA model. The main difference between ARIMA and the ARMA model comes from the integration part, that is d. d is basically the number of non-seasonal differences that are really required to make the data stationary. In our case, we already made our data stationary, so we don't require that parameter here. And the other orders, p and q: the value of p and the value of q are almost the same as for the ARMA model.

So we can use the same orders p and q. Let me use the same orders p and q, and d equal to zero. So I'm trying to build an ARIMA model of six, zero, six. If you want, you can also try different values for ARIMA. So let's build the model: model_arima is going to be equal to ARIMA, and here I just want to pass the data, and the data here is the stationary data, which is already differenced,

which we converted into stationary. And the order: the order is p, d, q; in this case it is six comma zero comma six, which is p, d, q. And finally we fit, and we put our data in; execute. And done. Now we have successfully trained our ARIMA model. You can go on to try different values of d and q; it is not required at the moment. You can put d equal to zero, or you can take d equal to one or two.

But here we don't need to go for that. In the end, what we will do is see the optimal value of p and the optimal value of q with auto ARIMA. OK, now let's try to visualize the data and also visualize the confidence interval here. We can see in the previous picture there's no confidence interval. Now let's plot the confidence interval too. All right, so now let's try to find out the forecasted values, or the predicted values.

So let's take the predicted values for ARIMA, which is going to be equal to model_arima.predict. So let's predict: what is the date I want to start with, and what is the date I want to end with? I'll just use the same settings that we followed for ARMA. So this is my start date and that is my end date. Let's use the same settings: start is going to be equal to my start date and end equal to my end date.

So that's it. We'll get the predicted values, and remember, the values you'll get are stationary. So what we need to do is convert them back into non-stationary. How to convert that into non-stationary? Let's take train_df, and in that, let me consider the last value. So this is my last value. And we will do the cumulative sum of the predicted values with the initial value of six seven nine eight three.

So that's what we're going to do now: np.cumsum, the cumulative sum of the predicted values. What we're getting here is that we're just adding it to our initial value, and save that in forecasted_values_arima. Done. So we're done with our forecast. Let me also calculate the confidence interval. ARIMA basically has a forecast function also; forecast will give you the confidence interval. So let me take model_arima.forecast,

and here I just want to pass the number of steps. The number of steps I basically want to forecast is equal to the length of my forecasted values, or the length of my test. So we take the length of this, and that's going to be equal to the number of steps. The number of steps I just want here is 36. All right. So these are the forecasted values. Let me do one thing:

let me look at this. I just don't want to put all the values here. Here you can see there are a few outputs out there: the forecasted values, the standard errors, etc, and this is my confidence interval. All right, so I'll take this; this is what I'm actually interested in. So let me take this array with minus one; basically, this is minus one,

which is nothing but my confidence interval. All right. So now we have the confidence interval values, and done. So this is my confidence interval: this is the lower limit and this is the upper limit. That's it. So we have all the values, the lower limit and also the upper limit. In the next lecture, we will visualize the output of the ARIMA model. Thank you very much.

14. ARIMA  Visualize the output
===============================

Hello, everyone, welcome back. In the previous lecture, we have seen how to train our ARIMA model and calculate the forecast and the confidence interval. So now let's visualize that. OK, so here, let's copy the code we have, paste it here, and do the same thing, because there's no need to type it again; the code is all the same. And here what I need to do is replace this with my forecasted values for ARIMA.

So that's it. So this is how we can visualize it. Now let's put the confidence interval on it. In order to put the confidence interval, we need the lower limit and the upper limit. And here again is the confidence interval: there are two columns; column one is the lower, and column two is basically the upper. So now what we have to do is project that from stationary to non-stationary data. In order to do that: this is my upper limit, and just try to understand, this is my lower limit and this is the upper limit.

OK, so we have the forecasted values. Let me take the forecasted values plus... we just need to add the upper limit, column one, and similarly you can get the lower limit with column zero. So that's it. Here we get the upper limit and the lower limit values. So now let's do fill_between, and what is our x axis? The x axis is basically my time.

And in this case, it is the index. So let me take test.index. And now here I just want to give the upper limit and the lower limit, so y1 could be either. Let me give the lower limit first, followed by the upper limit. And in the legend, let me add: this is my confidence interval. Execute. So that's it. This is how we can get the confidence interval. So let me decrease the alpha and change the color: let me change the color to black.

And my alpha is equal to 0.2. So that's it. So this is how, guys, we get the confidence interval, and that is how we are able to build the ARIMA model. In the next lecture, we will see how to find out the optimal values of p and q using auto ARIMA. Thank you very much.

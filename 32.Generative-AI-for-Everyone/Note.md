1. Generative AI works very well for unstructured data and not structured data.
2. Image generation today is mostly done via a method called Diffusion Model.
3. Diffusion models learn from a huge number of images found on the internet or elsewhere. At the heart of the diffusion models is supervised learning. 

Let's say an algorithm finds a picture on internet of an apple (img1) and model wants to learn from this image and hundreds of images like this. The first step is to take this image (img1) and add noise to it (img2) and gradually add more and more noise to it to make img3,img4,...etc. More noisy means more random data points are there.

The diffusion model uses images like this as img1,img2,img3,img4,...etc as data to learn using supervised learning to take input as a noisy image to output as a slightly less noisy image. So, it would take a dataset where (input,output) data points would be like (img2,img1), (img3,img2), (img4,img3), (img5,img4) etc. The algorithm would learn from this data and generate new images.

After training may be hundreds of millions of images 

Typically ~100 steps would be typical for a diffusion model to generate an image iteratively by more noisy images to less noisy images and then final original image would be generated.

We need to give a prompt to what image it has to generate then it will take more noisy images and then slightly less noisy images and so on to generate the final image.

4. Roughly each token is 3/4 of a word.

5. Model Size:

Using this we can see the model's capability.

- 1B parameters model: we can use it for pattern matching and basic knowledge of the world. For example: Restaurant reviews sentiment classification etc.
- 10B Parameters model: These models have greater world knowledge and can follow basic instructions. For example: Food order chatbot.
- 100B+ parameters model: These models have rich world knowledge and comples reasoning. For example: to look for a brainstorming partner.

6. Closed or Open Source Models:

- Closed Source: These models are accessible via cloud programming interface. It is easy to use in applications. It contains more large/powerful models. Also, these are relatively inexpensive.

- Open Source: Here, we have full control over these models, we don't have to worry if company retire or depricate these models. We can these models on our pc, on-prem etc. Also, we have full control over data privacy/access. 

7. AGI (Artificial General Intelligence):

Definition: AI that can do any intellectual task that a human can do.

Examples:

- Learn to drive a car through ~20 years of practice.
- Complete a phd thesis after ~5 years of work.
- Do all the tasks of a computer programmer (or any other knowledge worker)

I think we are many decades away from AGI or even longer.

8. Responsible AI: 

It refers to developing and using AI in a way that ethical, trustworthy and socially responsible.

Dimensions of responsible AI: 

Fairness: Ensuring AI does not perpetuate or amplify biases
Transparency: Making AI systems and their decisions understandable to stakeholders impacted
Privacy: Protecting user data and ensure confidentiality
Security: Safeguard AI systems from malicious attacks
Ethical Use: Ensuring AI is used for beneficial purposes

9. 
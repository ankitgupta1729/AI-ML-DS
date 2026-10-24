import os

image_files = []
#os.chdir(os.path.join("data", "obj"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("img/" + filename)

size = len(image_files)
train = image_files[:size]
test = image_files[-size:]

#os.chdir("..")
with open("train.txt", "w") as outfile:
    for image in train:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()

with open("test.txt", "w") as outfile:
    for image in test:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
#os.chdir("..")


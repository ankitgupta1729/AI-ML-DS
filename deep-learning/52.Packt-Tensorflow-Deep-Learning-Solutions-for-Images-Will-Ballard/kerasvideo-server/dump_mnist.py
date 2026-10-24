"""
Dump a few MNIST test digits to PNG files, so the POST API can be exercised
with real data:

    curl -F file=@var/data/sample-0.png http://localhost:5000/mnist/classify
"""

import os

from keras.datasets import mnist
from PIL import Image

OUT_DIR = os.environ.get('SAMPLE_DIR', 'var/data')

(_, _), (x_test, y_test) = mnist.load_data()

os.makedirs(OUT_DIR, exist_ok=True)

#one sample image per digit, named after the label it should classify as
for digit in range(10):
    index = int((y_test == digit).argmax())
    path = os.path.join(OUT_DIR, 'sample-{}.png'.format(digit))
    Image.fromarray(x_test[index]).save(path)
    print('wrote', path)

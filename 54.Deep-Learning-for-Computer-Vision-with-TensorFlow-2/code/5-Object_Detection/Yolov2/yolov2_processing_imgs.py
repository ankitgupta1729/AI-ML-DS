import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import numpy as np
import time

options = {
    'model': 'cfg/tiny-yolo-voc-1c.cfg',
    'load': 3600,
    'threshold': 0.05,
    #'gpu': 1.0
}
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
tfnet = TFNet(options)

capture = cv2.imread('./sample_img/tl_1.jpg')
result = tfnet.return_predict(capture)
print(result)

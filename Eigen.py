import threading
import time
import os
import shutil
import sys
import cv2
import numpy as np
class Eigen(threading.Thread):
    def __init__(self, queue,path):
        threading.Thread.__init__(self)
        self.queue = queue
        self.path = path
    def run(self):
    	X,y = [], []
        count = 0
        for dirname, dirnames, filenames in os.walk(self.path):
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    try:
                        im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                        # resize to given size (if given)
                        im = cv2.resize(im,(256,256))
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(count)
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                count = count+1
        y = np.asarray(y, dtype=np.int32)

        # Create the Eigenfaces model.
        model = cv2.createEigenFaceRecognizer()
        # Learn the model. Remember our function returns Python lists,
        # so we use np.asarray to turn them into NumPy lists to make
        # the OpenCV wrapper happy:
        model.train(np.asarray(X), np.asarray(y))

        # Save the model for later use
        model.save("eigenModel.xml")

        self.queue.put("Task finished")

import threading
import time
import os
import shutil
from Face import Face

class FaceThread(threading.Thread):
    def __init__(self, queue,path):
        threading.Thread.__init__(self)
        self.queue = queue
        self.path = path
    def run(self):
    	face = Face()
        for path, subdirs, files in os.walk(self.path):
            for directory in subdirs:
                    if not os.path.exists('detected/'+str(directory)):
                        os.makedirs('detected/'+str(directory))
                    else:
                        shutil.rmtree('detected/'+str(directory))
                        os.makedirs('detected/'+str(directory))
                    files = os.walk(path+'/'+directory).next()[2]
                    for file in files:
                                if( file.endswith(".jpg")):
                                        rects, img = face.detect(path+"/"+directory+"/"+file)
                                        label = face.box(rects,img,file,directory)
        self.queue.put("Task finished")

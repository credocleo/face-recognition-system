from Tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkFileDialog 
import zipfile
import Tkinter
import cv2
import os
import tkMessageBox
import subprocess as sub
from FaceThread import FaceThread
from Eigen import Eigen
import ttk
import Queue
import time
import facialverification
from tkFileDialog import askopenfilename
from Tkinter import *
import sys

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()

    def initUI(self):
        root = self
        self.parent.title("Facial Verification System by C. Credo")
        self.pack(fill=BOTH, expand=1)
        self.parent.resizable(height = FALSE, width =  FALSE)

        #Face Recognition Frame Section
        face_recognition_label_frame = LabelFrame(root, text="Face Verification")
        face_recognition_label_frame.grid(column = 0, row = 1, sticky="we", rowspan=2, columnspan=1)

        image_label = Label(face_recognition_label_frame, text="Image:")
        image_label.grid(row = 0 , column= 0,sticky="w")
        self.image_location_source = StringVar()
        image_location_label = Label(face_recognition_label_frame,textvariable=self.image_location_source, width=20)
        
        self.image_location_source.set("...")
        image_location_label.grid(row = 0, column = 1)
        image_location_button = Tkinter.Button(face_recognition_label_frame, text="Browse", command = self.browseImage)
        image_location_button.grid(row = 0, column = 2, sticky="e")
        
        threshold_label = Label(face_recognition_label_frame,text="Threshold:")
        threshold_label.grid(row = 1, column = 0, sticky="w")
        
        self.threshold_entry = Entry(face_recognition_label_frame, justify="right")
        self.threshold_entry.grid(row =1 , column = 1, columnspan = 2)

        recognize_search_button = Tkinter.Button(face_recognition_label_frame, text="Verify", width=45, command = self.verifyImage)
        recognize_search_button.grid(row = 3, column = 0, columnspan=3, sticky= "we")

        #Image cutting section
        image_cutting_section = LabelFrame(root, text="Face Detection")
        image_cutting_section.grid(column=0, row =0)

        directory_label = Label(image_cutting_section, text="Directory: ")
        directory_label.grid(column = 0, row = 0)

        self.directory_source_label_text = StringVar()
        self.directory_source_label = Label(image_cutting_section,textvariable = self.directory_source_label_text, width=20)
        self.directory_source_label_text.set("...")
        self.directory_source_label.grid(column = 1, row = 0)
        
        directory_browse_button = Tkinter.Button(image_cutting_section, text="Browse", command= self.directoryBrowse)
        directory_browse_button.grid(column = 2, row = 0)

        self.progressbar = ttk.Progressbar(image_cutting_section, orient="horizontal", mode="determinate", length="300")
        self.progressbar.grid(row = 1 , column = 0, columnspan=3)
        self.image_cutting_process_button = Tkinter.Button(image_cutting_section, text = "Process", command = self.processImageForCropping)
        self.image_cutting_process_button.grid(row = 2, column =0, columnspan = 3, sticky = "we")
        self.image_cutting_save_button = Tkinter.Button(image_cutting_section, text="Save Processed Image", command = self.saveProcessToDb)
        self.image_cutting_save_button.grid(row = 3, column = 0, columnspan = 3, sticky= "we")

        #for image frame 
        self.image_frame = LabelFrame(root, text="Result")
        self.image_frame.grid(column= 0,columnspan=5, row= 5, sticky="we")

    #for saving cropped images to db
    def saveProcessToDb(self):
        self.image_cutting_process_button['state'] = 'disabled'
        self.image_cutting_save_button['state'] = 'disabled'

        self.queue = Queue.Queue()
        self.progressbar.start()
        Eigen(self.queue,"detected").start()
        
        
        self.master.after(100, self.process_queue)
    #for fool filter of Image Searchning in db
    def verifyImage(self):
        value = self.threshold_entry.get()
        if str.isdigit(value):
            self.value = float(value)
            if self.image_location_source.get() == "...":
                tkMessageBox.showerror("Image Error", "Browse Image First")
            elif self.value < 100 or self.value > 100000:
                tkMessageBox.showerror("Threshold Error", "Closest Match Input: 100.0\nFarthest Match Input: 100000.0")
            else:
                self.recognizeImage()
        else:
            tkMessageBox.showerror("Threshold Error", "Input a number\n\nClosest Match Input: 100.0\nFarthest Match Input: 100000.0")
    #parameters Threshold from 100 to 100000
    #           Image to be compared
    def recognizeImage(self):
        model = cv2.createEigenFaceRecognizer(threshold=self.value)

        # Load the model
        model.load("eigenModel.xml")

        # Read the image we're looking for
        sampleImage = cv2.imread(self.image_location_source.get(), cv2.IMREAD_GRAYSCALE)
        sampleImage = cv2.resize(sampleImage, (256,256))

        # Look through the model and find the face it matches
        [p_label, p_confidence] = model.predict(sampleImage)

        # Print the confidence levels
        print "Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence)

        # If the model found something, print the file path
        if (p_label > -1):
            count = 0
            for dirname, dirnames, filenames in os.walk("detected"):
                for subdirname in dirnames:
                    subject_path = os.path.join(dirname, subdirname)
                    if (count == p_label):
                        Label(self.image_frame, text="Predicted Label: 0 || Image is same with").grid(row= 1 , sticky="w")
                        Label(self.image_frame, text="Image Directory:").grid(row= 2 , sticky="w")
                        Label(self.image_frame, text=subject_path).grid(row = 3, sticky="w")
                        i = 0
                        for filename in os.listdir(subject_path):
                            i += 1
                        

                    count = count+1
        else:
            Label(self.image_frame, text="Predicted Label: -1 || Image is different").grid(row = 0)
            #Label(self.image_frame, text="Image not Found:").grid(row = 0)
    def browseImage(self):

        ftypes = [('IMAGE FILE', '*.JPG')]
        file_source = askopenfilename(filetypes=ftypes)
        if file_source:
            self.image_location_source.set(file_source)
    def directoryBrowse(self):
        self.dest = tkFileDialog.askdirectory()
        if self.dest:
            self.directory_source_label_text.set(str(self.dest))
    #method for cropping images of a directory
    #for fool filtering
    def processImageForCropping(self):
        if self.directory_source_label_text.get() == '...':
            tkMessageBox.showinfo("Browse", "Browse Folder First")
        else:
            self.image_cutting_process_button['state'] = 'disabled'
            self.image_cutting_save_button['state'] = 'disabled'
            self.queue = Queue.Queue()
            self.progressbar.start()
            FaceThread(self.queue,self.directory_source_label_text.get()).start()
            
            
            self.master.after(100, self.process_queue)
    #for checking if thread for saving and cropping image is done
    def process_queue(self):
        try:
            msg = self.queue.get(0)
            
            tkMessageBox.showinfo("Process", msg)
            # Show result of the task if needed
            
            self.image_cutting_process_button['state'] = 'normal'
            self.image_cutting_save_button['state'] = 'normal'
            self.progressbar.stop()
            
        except Queue.Empty:
            self.master.after(100, self.process_queue) 


root = Tk()
var = StringVar()
label = Label( root, textvariable=var )
label.pack()
ex = Example(root)
root.geometry("330x350")
root.mainloop() 
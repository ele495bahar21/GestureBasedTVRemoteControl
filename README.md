# GestureBasedTVRemoteControl
Buse Nur DÜZGÜN - Ahmet Berk VICIL // Senior Year Project

We used Convolutional Neural Network for this project.
Required Setup:
- Keras
- Tensorflow
- Python 3.8 (3.9 Version was not suitable for Tensorflow)
- OpenCV
- numpy
- os
- time

You will find several links in this document which were helpful for us to learn what to do and how to do them. 

- https://keras.io/getting_started/faq/#what-do-sample-batch-and-epoch-mean
- https://arxiv.org/pdf/1312.7560.pdf


(1) We created our own dataset for our special sign language to control TV. 
To create your own dataset, run this:
* collectData.py

(2) We created a CNN Model. We learned how CNN algoritm works and how to create a CNN Model from:
- https://towardsdatascience.com/tutorial-using-deep-learning-and-cnns-to-make-a-hand-gesture-recognition-model-371770b63a51 
- https://www.youtube.com/watch?v=oI2rvjbzVmI&ab_channel=ThalesSehnK%C3%B6rting
- https://medium.com/@gongster/building-a-simple-artificial-neural-network-with-keras-in-2019-9eccb92527b1
- https://machinelearningmastery.com/save-load-keras-deep-learning-models/

* cnnModel.py

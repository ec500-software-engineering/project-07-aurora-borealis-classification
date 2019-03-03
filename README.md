# Aurora borealis classification
## User story
Aurora Borealis and Aurora Australis are arguably the most 
impressive manifestations of solar wind/magnetosphere coupling. 
They are caused by charged particles (mostly electrons but also protons) 
originating from near‐Earth space that have been accelerated along magnetic 
field lines toward Earth and subsequently collide with neutral constituents 
(mostly atomic oxygen) of the upper atmosphere. Since the vast space that is the 
magnetosphere maps along magnetic field lines into the upper atmosphere, it 
acts as a screen onto which magnetospheric dynamics are projected. Hence, 
observing the aurora from the ground allows one to study large‐scale magnetospheric 
processes both on the day but also on the nightside.

Since the aurora is formed through processes in near‐Earth space, it is clear, 
then, that the morphology of auroral forms as observed from the ground is integral 
to our understanding of magnetospheric dynamics. It would therefore be desirable 
to automatically classify the vast amount of existing ground‐based auroral data 
in order to enable large statistical studies.

Automatic auroral image classification has already used a number of techniques from 
computer vision, pattern recognition, and machine vision with a strong emphasis on 
hand‐designed features. However, over the last few years, the fields of computer vision 
and machine learning have seen a big methodological paradigm shift: The focus from 
small‐scale data sets and algorithms relying on hand‐crafted features has moved to 
large‐scale data sets and learning machines that automatically extract the feature 
representation from the raw data. So in this project, we are going to use a pretrained 
deep neural network(Inception-v4) to automatically extract a 1,001‐dimensional feature vector from 
Aurora images. And then using labels and feature vectors together to train a ridge classifier
that is then able to correctly predict the category of unseen auroral images. This
classifier could be used no only in research of magnetospheric dynamics, but also by
those astronomy enthusiast.
  
## System diagram
![Screenshot](dataflow.jpg)

## Technology selection
* Tensorflow
* Ubuntu 18.04 
* BU SCC (Shared Computing Cluster) 

## Methodology
### 1) labels    
L = laebls {0,1,2,3,4,5}    

| label | description |
| ------ | ------ |
| 0 --> arc  | one or multiple bands of aurora that stretch across the field-of-view |
| 1 --> diffuse | show large patches of aurora |
| 2 --> discrete | show auroral forms with well-defined, sharp edges,but not arc like |
| 3 --> cloudy | The sky in these images is dominated by clouds |
| 4 --> moon  | The image is dominated by light from the Moon |
| 5 --> clear sky/no aurora | show a clearsky without the appearance of aurora  |


             

### 2) Image preparation                 
  - The images in our training data set originate from the THEMIS all-sky imager network.               
  - The raw auroral image is cropped insize by 15% in order to remove pixels that correspond to very low elevation angles               
  - Rotate each image by a random angle around its center in order to not bias the feature selection toward acertain orientation of structures    
  
### 3) Feature extraction     
  - Compute the feature vector **f** from each imagexusing TensorFlow       
  - Use the latest Inception-v4 pretrained neural network, which offers the best compromise between classification                
accuracy and computational complexity to date.   

### 4) Ridge classfication               
Ridge classification is a linear method extending and generalizing ordinary linear regression in two aspects:      
  - The added ridge improves the generalization capabilities of the method           
  - It deals with binary labels     
  
Ordinary linear regression risks to produce a model that represents the training data well but performs poorly when pre-dicting labels of unseen data, we use regularization strategy to counterbalanceoverfitting in ordinary regression       

## Definition of First Sprint
1. Collect aurora dataset and analysis.
2. Data proprecessing and extracting features.
3. Deep learning model selection.
4. Tool selection.

## Task assignments
**Zhangyu Wan**: Researching on aurora, using shell script to finish data proprecessing and deciding which deep learning model should be used.

**Xiangkun Ye**: Researching on aurora and using python to extract necessory features from dataset. Deciding other tools to use while traing ridge classifior.
  
## Reference
Clausen, Lasse BN, and Hannes Nickisch. "Automatic Classification of Auroral Images From the Oslo Auroral THEMIS (OATH) Data Set Using Machine Learning." Journal of Geophysical Research: Space Physics 123.7 (2018): 5640-5647.


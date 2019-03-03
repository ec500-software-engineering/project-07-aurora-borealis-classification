# Aurora borealis classification
### User story

### System diagram
![Screenshot](dataflow.jpg)
### Methodology
#### 1) labels    
L = laebls {0,1,2,3,4,5}    

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| Github | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

0 --> arc  

      This label is used for images that show one or multiple bands of aurora that stretch across the field-of-view;       
      typically,the arcs have well-defined, sharp edges    

1 --> diffuse     

      Images that show large patches of aurora, typically withfuzzy edges, are placed in this category.           
      The auroral brightnessis of the order of that of stars  

2 --> discrete    

      The images show auroral forms with well-defined, sharp edges,that are, however, not arc like.                    

3 --> cloudy     

      The sky in these images is dominated by clouds or the dome of the imager is covered with snow   

4 --> moon      

      The image is dominated by light from the Moon     
      
5 --> clear sky/no aurora     

      This label is attached to images which show a clearsky without the appearance of aurora               

#### 2) Image preparation                 
The images in our training data set originate from the THEMIS all-sky imager network.               
The raw auroral image is cropped insize by 15% in order to remove pixels that correspond to very low elevation angles               

#### 3) Feature extraction     
Compute the feature vector **f** from each imagexusing TensorFlow       
Use the latest Inception-v4 pretrained neural network, which offers the best compromise between classification                
accuracy and computational complexity to date.            
#### 4) Ridge classfication               
Ridge classification is a linear method extending and generalizing ordinary linear regression in two aspects:      
1. The added ridge improves the generalization capabilities of the method           
2. It deals with binary labels            



'''This file would use the output from Feature_Extraction.py and include APIs
of the ridge classifier'''

from Feature_Extraction import rotate
from Feature_Extraction import extract
from Feature_Extraction import output

def train(path, modelname):
    '''
    This function would automatically train model using features in input path
    '''

    pass

def predict(modelname, input):
    '''
    This function would use selected model and new input to predict and output
    '''

    dict = {0:"arc", 1:"diffuse", 2:"discrete", 3:"cloudy", 4:"moon", 5:"noaurora"}
    pass

if __name__ == '__main__':
    '''
    When we run this file directly, it will automatically use current path and
    APIs from Feature_Extraction.py to train a model.
    '''

    pass

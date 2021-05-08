####################################################
#      Authour   Bereket Mekonnen                  #
#     This program converts HDF5 files to          #
#               CSV, ASCII and  XML                #
#                                                  #
#                 Date 05/05/2021                  #
#                 pythone                          #                         
#                                                  #
####################################################

#import libraries 
import h5py as h5 
import pandas as pd
import numpy as np
import csv
from csv import writer
import os.path
from os import path





def welcome(): #this function prints a welcome message to the user
    print('================== Welcom to HDF5 file converter ==================')


def get_path(): #this function is used to obtain input from the user, it returns the input as a string. the return value is used as the path
    File_path = input('Enter the file path you would like to convert ')
    return File_path
    

def append(data, temp, col_name, dataset_name ): #this function is used to append two lists that hold datasets from the hdf5 file and the dataset's name
    data.append(temp) #add new dataset to list
    col_name.append(dataset_name)# add dataset name to list


def get_dataset(item, data, col_name, leading = ''): # this is a recursive function used to traverse through HDF5 Groups and obtain dataset values 
    for key in item: #loop through the number items in the HDF5 object
        if isinstance(item[key], h5.Dataset): #cheak if object is a dataset, if true obtain values
            print(leading + key + ': ' + str(item[key].shape))
            dataset_value = np.array(list(item[key])).flatten()
            name = item[key].name
            print(name)
            append(data, dataset_value, col_name, item[key].name) #add hdf5 dataset values and names  to list
               
        else:
            print(leading + key)
            get_dataset(item[key], data, col_name, leading + ' ') #if not dataset call back function



def to_xml(df): # function to convert HDF5 datafram values to xml 
    def row_xml(row): 
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_xml, axis=1))
    return(res)
    



def convert_to( str ): # This function allows the user to choos what type of file the would like to convert to 
    if path.exists(str): #cheak if inpute is a valid path
        HDF_file = h5.File(str, 'r') # open HDF5 file in read mode 
        print('plese select the format you would like:')
        print('Enter 1 to convert to CSV file')
        print('Enter 2 to convert to ASCII file')
        print('Enter 3 to convert to XML file')
        choice = input('Enter choice here ===> ' ) #obtain user choice
        choice = int(choice)
        dataset_data = [] #list to hold dataset values from hdf5 file
        dataset_name =[] #list to hold names of datasets
        get_dataset(HDF_file, dataset_data, dataset_name, ' ') # load datasets to list
        dataset = pd.DataFrame(dataset_data, dataset_name) # create a pandas datafram table
        if choice == 1:
            dataset.to_csv('output.csv', mode='a', header=True) #create a .csv file and write dataset values to it
        elif choice == 2:
            with open('output.txt', 'a') as f: #create a ascii txt file
                f.write(
                 dataset.to_string(header = False, index = False) #write datafram values to text file
                 )
            

        elif choice == 3:
            with open('output.XML', 'w') as f: #create an xml file in write mode
                f.write(to_xml(dataset)) # write dataset values to xml file

        else:
            print('invalid input') # if user input an invalid choice print error message 
                  
    else :
        print('invalid path') #if user inputs invalid path print error message 




def main():
    welcome() #print welcome message 
    convert_to(get_path()) # function call to convert with path as perimeter 





if __name__ == "__main__":
    main()
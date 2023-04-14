# Author: Calum Crawford
# USFCA Computer Science Student
import matplotlib.pyplot as plt # Imports the the matplotlib library 

def fPlotSFCovid(pFilePath): # Initializes fPlotSFCovid with pFileName as a parameter
    x = []
    y = []
    with open(pFilePath, 'rb') as f: # Reads in the binary data 
        for line in f:
            decoded_line = line.decode()
            decoded_line = decoded_line.split(" ")
            for i in range(len(decoded_line)): # Decodes the data and then splits each item up and adds the date and moving average to respective x,y lists
                if i % 2 == 0:
                    x.append(decoded_line[i])
                else:
                    y.append(float(decoded_line[i]))
    
    x.pop() # Removes the last element which happened to be an empty string
    ax = plt.axes() # Sets axes
    ax.xaxis.set_major_locator(plt.MaxNLocator(4)) 
    ax.yaxis.set_major_locator(plt.MaxNLocator(4))
    plt.scatter(x, y, c='blue') # Plots the graph
    plt.show() # Shows the plot
    f.close() # Closes the file 

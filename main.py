# Author: Calum Crawford
# USFCA Computer Science Student
import CovidSFPlot as plot # imports the CovidSFPlot file to plot the graph
import os # Imports os package
import requests  # Imports requests package

# URLs of the files you want to download (taken from The New York Times GitHub)
file_urls = ['https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2020.csv',
             'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2021.csv',
             'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv'] 

fileName = 'covidData.txt' # Creates a file name which will store the data locally

location = "San Francisco"

WINDOW = 7 # Intializes WINDOW with seven which will be used to calculate the moving average


def main(): # Initializes the main function 
	with open(fileName, 'wb') as f: # Opens the file and writes the data from the websites into the file
		for url in file_urls:
			response = requests.get(url, stream=True)
			f.write(f'---{url}---\n'.encode()) # Write a separator with the URL of the file
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
			f.write(b'\n') # Write an newline  after each file to separate them
	
	file_path = os.path.join(os.path.dirname(__file__), fileName) # Gets file path from local device
	contents = fReadInputFile(file_path) # Calls fReadInputFile function to read the file and assigns it to variable contents
	fWriteOutputFile(file_path, contents) # Calls fWriteOutputFile to write the contents of the input file into the output file
	file_dict = fReadOutputFile(file_path) # Calls fReadOutputFile function to assign variable file_dict with a dictionary containing the dates and daily cases for covid in San Francisco
	mov_avg = fCalcMovAvg(file_dict) # Moving average variable is assigned with the returned value of the fCalcMovAvg function which calculates the seven day moving averages and returns it as a dictionary
	fWriteCovidSFFile(file_path, mov_avg) # Calls fWriteCovidSFFile to write the moving averages into the file
	plot.fPlotSFCovid(file_path) # Calls fPlotSfCovid from CovidSFPlot module to plot the points onto a graph


def fReadInputFile(file_path): # Initializes fReadInput file with file_path as parameter
	# Reads the files binary data, decodes it and then adds it to a list
	with open(file_path, 'rb') as f:
		list_contents = []
		for line in f:
			decoded_line = line.decode('utf-8')
			list_contents.append(decoded_line)
	 

	list_SF = []
	for i in range(len(list_contents)): # Iterates through the list and adds only the elements containg SF data
		if location in list_contents[i]:
			list_SF.append(list_contents[i])
	
	count = 0
	list_daily_cases =[]
	for item in list_SF:
		item = item.split(",")
		entry = "" # Creates a string to contain each entry for example: '2020-04-03 4' in which the date and daily cases are contained
		entry += item[0] + " "
		if int(item[4]) - count < 0: # Calculates the daily cases
			entry += "0"
		else:
			entry += str((int(item[4]) - count))
		count = int(item[4]) # Assigns the count to the next value
		list_daily_cases.append(entry) # Adds the string to the list of daily cases
	
	return list_daily_cases # Returns the list
	


def fWriteOutputFile(pFile_Path, pList): # Initalizes fWriteOutputFile with pFile_path and pList as parameters
	file = open(pFile_Path, 'wb') # Opens the file in write binary mode
	for i in range(len(pList)): # Iterates through the list
		binary_data = pList[i].encode() # Encodes the data
		second = " ".encode()
		file.write(binary_data) # Writes each elment of the list into the file 
		file.write(second)
	
	file.close() # closes the file
	
def fReadOutputFile(pFile_path): # Initializes fReadOutputFile with pFile as parameter
	with open(pFile_path, 'rb') as f: # Opens the file path in read binarry
		list_contents = []
		for line in f:
			decoded_line = line.decode('utf-8') # Decodes each line and adds it to a list
			item = decoded_line.split(" ")
			list_dates = []
			list_cases = []
			for i in range(len(item)): # splits up each item and adds the date and cases to their respective lists
				if i % 2 == 0:
					list_dates.append(item[i])
				else:
					list_cases.append(int(item[i]))
			
		newDict = dict(zip(list_dates, list_cases)) # Creates a new dictionary with dates as the key and cases as the value
		return newDict # Returns the dictionary

def fCalcMovAvg(pDict): # Intializes fCalcMovAvg with pDict as a parameter
	movAvg = [] # Initalizes movAvg with an empty list
	dates = []
	numbers_list = []
	for key, value in pDict.items(): # Breaks open the dictionary object to access the dates and daily cases 
		dates.append(key)  
		numbers_list.append(value)

	for i in range(len(numbers_list)): # Iterates through the elements of the list
		numbers_list.append(float(numbers_list[i])) # Numbers list adds the float version of the list
		count = 0 # initalizes count with 0
		index = 0 # initalizes index with 0
		while count < len(numbers_list) - WINDOW + 1: # Iterates through the list
			if index <= 5: # If index is less than 5 (ie the first 6 numbers of the list)
				movAvg.append(0.0) # Movavg adds 0.0 to the list for the first 6 numbers of the list
				index += 1 # Index increments by + 1
			else: # Once the first 6 numbers are accounted for
				avg_list = numbers_list[count: count + WINDOW] # Avg list is initialized with a list of numbers ranging from count to count + winow
				average = sum(avg_list) / WINDOW #Average is computed by the sum of the list divided by WINDOW
				movAvg.append(average) # Movavg adds the moving day average to the list
				count += 1 # Count adds one to keep going through the list
	newDict = dict(zip(dates, movAvg)) # Creates a new dictionary with the date and moving average as key, value pairs
	return newDict # Returns the dictionary


def fWriteCovidSFFile(pFile_Path, pDictMovAvg): # Initalizes fWriteCovidSFFile with pFile and pListMovAvg as parameters 
	with open(pFile_Path, 'wb') as f: # Opens up the dictionary with the dates and moving averages and then writes it into the file using binary conversion
		for key, value in pDictMovAvg.items():
			binaryKey = (key + " ").encode()
			f.write(binaryKey)
			binaryValue = (str(value) + " ").encode()
			f.write(binaryValue)
	f.close()
	

main() # Calls the main function to start the program

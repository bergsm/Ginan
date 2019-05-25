#!/usr/bin/env python

'''
Adapted from psuedocode in CLRS chapter 22.2, third edition. This function performs a breadth-first search on the graph. Source for Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''
import sys
import os
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin
from itertools import cycle

sys.stdout = open('log','w')

startingURL = sys.argv[1]
depth = int(sys.argv[2])

#set the keyword if the user input one, set to a dummy value if they didn't
keyword = sys.argv[3]
if keyword is '':
	keyword = 'aaaaaa'

print keyword

#parse the URL
html = urllib.urlopen(startingURL).read()
#feed the parsed URL to Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

unvisitedURLs = []
unvisitedURLs.append(startingURL)

listOfNeighbors = []

# The following write function was written by Shawn Berg, all credit to him for this
# Function to write urls from DFS to json file
# Args: urls in order from DFS
# Returns: None
def writeToFile(urls):
    with open('./public/graphFile.json', 'w+') as f:
        f.write('{\n  \"nodes\": [')
        for counter, url in enumerate(urls):
            f.write('\n    {\n      "name\": \"URL\",\n      "label\": \"' + url + '\",\n       "id\":' +  str(counter+1) + '\n    }')
            if counter < len(urls)-1:
                f.write(',')
        f.write('\n  ],\n  \"links\": [')
        for i in range(1, len(urls)):
            f.write('\n    {\n      \"source\": ' + str(i) + ',\n      \"target\": ' + str(i+1) + ',\n      \"type\": \"Links_To\"\n    }')
            if i < len(urls)-1:
                f.write(',')
        f.write('\n  ]\n}')

def breadthFirstSearch(startingURL, depth, keyword):
  
    observedURLs = []
    
    #some debugging checks, did everything make it into the data structure and what is the starting URL
    #print "How many unvisited URLs? - ", len(unvisitedURLs)
    #print "The starting URL is: " ,startingURL
   
    while len(unvisitedURLs) != 0:
	
        #get the first URL in the list
        unvisited = unvisitedURLs.pop(0)
	observedURLs.append(unvisited) 	
	#need to get full URL rather than the relative path of every link on the page and add them to the unvisited list. Source for urljoin which 
	#gets the absolute path: https://stackoverflow.com/questions/44001007/scrape-the-absolute-url-instead-of-a-relative-path-in-python
	for links in soup.find_all('a',):
		listOfNeighbors = []
		#print "entered the loop looking for links"
		absoluteURL = urljoin(unvisited, links.get('href'))
		
		#if the URL is not already in the unvisted list, add it
		if absoluteURL not in unvisitedURLs:
			unvisitedURLs.append(absoluteURL)
			listOfNeighbors.append(absoluteURL)
			#print "appended a new URL"
	#observedURLs.append(listOfNeighbors)
	#add the parsed URL to the observed list
		#observedURLs.append(unvisited)
	#source for zip and cycle: https://stackoverflow.com/questions/19686533/how-to-zip-two-differently-sized-lists
	test = zip(cycle(observedURLs), unvisitedURLs)
	#look to see if the keyword is in the URL
	if keyword in unvisited:
        	'''
		print 'found the keyword!'
                #debug time
                print "How many observed URLs? - " ,len(observedURLs)
                print "How many unobserved URLs? - " ,len(unvisitedURLs)
                #print the list in a readable format to help with debugging    
                print "The list of observed URLs: "
                for x in observedURLs:
                        print x
                #print the list in a readable format to help with debugging
                print "\n\nThe list of unvisited URLs: "
                for y in unvisitedURLs:
                	print y
		'''
                writeToFile(observedURLs)
                exit(0)
	#this will run indefinitely unless we add a limit. For now, the hard coded limit of number of URLs left to visit is 500
	if len(observedURLs) == depth:
		#print "unvisited > 500"
		break	
    '''
    #debug time
    print "How many observed URLs? - " ,len(observedURLs)
    print "How many unobserved URLs? - " ,len(unvisitedURLs)
    print the list in a readable format to help with debugging    
    print "The list of observed URLs: "
    for x in observedURLs:
	print x
    #print the list in a readable format to help with debugging
    print "\n\nThe list of unvisited URLs: "
    for y in unvisitedURLs:
	print y
    '''
    for z in unvisitedURLs:
	print z
    print "\n", test
    writeToFile(observedURLs)

breadthFirstSearch(startingURL, depth, keyword)

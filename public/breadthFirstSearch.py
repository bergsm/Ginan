#!/usr/bin/env python

'''
Adapted from psuedocode in CLRS chapter 22.2, third edition. This function performs a breadth-first search on the graph. Source for Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''
import sys
import os
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin

startingURL = sys.argv[1]
depth = int(sys.argv[2])
#set the keyword if the user input one, set to a dummy value if they didn't
if len(sys.argv) == 4:
	keyword = sys.argv[3]
else:
	keyword = 'aaaaaa'

#parse the URL
html = urllib.urlopen(startingURL).read()
#feed the parsed URL to Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

unvisitedURLs = []
unvisitedURLs.append(startingURL)

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
 	
	#need to get full URL rather than the relative path of every link on the page and add them to the unvisited list. Source for urljoin which 
	#gets the absolute path: https://stackoverflow.com/questions/44001007/scrape-the-absolute-url-instead-of-a-relative-path-in-python
	for links in soup.find_all('a',):
		#print "entered the loop looking for links"
		absoluteURL = urljoin(unvisited, links.get('href'))
		
		#if the URL is not already in the unvisted list, add it
		if absoluteURL not in unvisitedURLs:
			unvisitedURLs.append(absoluteURL)
			#print "appended a new URL"
		#if absoluteURL.find(keyword):
			#print 'found the keyword!'
			#break
	
	#add the parsed URL to the observed list
	observedURLs.append(unvisited)
	#look to see if the keyword is in the URL. Source for Python's find(): https://www.tutorialspoint.com/python/string_find.htm
	#if keyword in absoluteURL:
	#if absoluteURL.find(keyword, beg = 0, end = len(absoluteURL)):
		#print "found the keyword!"
		#break
	#this will run indefinitely unless we add a limit. For now, the hard coded limit of number of URLs left to visit is 500
	if len(unvisitedURLs) > 200:
		#print "unvisited > 500"
		break	
    #debug time
    #print "How many observed URLs? - " ,len(observedURLs)
    #print "How many unobserved URLs? - " ,len(unvisitedURLs)
    #print the list in a readable format to help with debugging    
    #print "The list of observed URLs: "
    writeToFile(observedURLs)
    #for x in observedURLs:
	#print x
    #print the list in a readable format to help with debugging
    #print "\n\nThe list of unvisited URLs: "
    #for y in unvisitedURLs:
	#print y

breadthFirstSearch(startingURL, depth, keyword)

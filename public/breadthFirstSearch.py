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
import Cookie

#sys.stdout = open('log','w')

startingURL = sys.argv[1]
depth = int(sys.argv[2])
#limit the BFS to a depth of 3, too messy otherwise
if depth > 3:
	depth = 3
c = Cookie.SimpleCookie()

#set the keyword if the user input one, set to a dummy value if they didn't
keyword = sys.argv[3]
if keyword is '':
	keyword = "aaaaaa"

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
    with open("./public/graphFile.json", 'w+') as f:
        f.write(urls)

def breadthFirstSearch(startingURL, depth, keyword):
    #initialize the counters and the start of each string
    counter = 1
    neighborCounter = 2
    anotherCounter = 2
    parentString = '{"nodes": ['
    neighborString = '"links": ['
    observedURLs = []
    
    #start the URL string with the starting URL
    nextParentString = ('{"name": "URL", "label": \"' + startingURL + '\", "id": ' + str(counter) + '}, ')
    parentString += nextParentString

    #some debugging checks, did everything make it into the data structure and what is the starting URL
    #print "How many unvisited URLs? - ", len(unvisitedURLs)
    #print "The starting URL is: " ,startingURL
   
    while len(unvisitedURLs) != 0:
	
        #get the first URL in the list
        unvisited = unvisitedURLs.pop(0)
	#debug statement to verify the popped URL
	#sys.stderr.write(unvisited)

	#append the URL and add it to the parent string
	observedURLs.append(unvisited) 
	
	#need to get full URL rather than the relative path of every link on the page and add them to the unvisited list. Source for urljoin which 
	#gets the absolute path: https://stackoverflow.com/questions/44001007/scrape-the-absolute-url-instead-of-a-relative-path-in-python
	for links in soup.find_all('a',):
		#print "entered the loop looking for links"
		absoluteURL = urljoin(unvisited, links.get('href'))

		#if the URL is not already in the unvisted list, add it
		if absoluteURL not in unvisitedURLs:
			unvisitedURLs.append(absoluteURL)
		
			#add the information to the string of nodes
			nextParentString = ('{"name": "URL", "label": \"' + absoluteURL + '\", "id": ' + str(anotherCounter) + '}, ')
			parentString += nextParentString
			nextNeighborString = ('{"source": \"' + str(counter) + '", "target": \"' + str(neighborCounter) + '\", "type": "Links_To"}, ')
			neighborString += nextNeighborString
			#increment the counters
			neighborCounter += 1
			anotherCounter += 1
			#if we have hit 42 nodes, break out of the function
			if len(unvisitedURLs) > 42:
				break

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
		#trim the last comma and add a closing square bracket for json formatting
    		parentString = parentString[:-2]
    		parentString += "],"
    		#append the neighbor nodes string to the parent node string
    		parentString += neighborString
    		#add a closing bracket for json formatting
    		parentString = parentString[:-2]
    		parentString += "]}\n"

    		#debug, does the final string look correct
    		#print parentString

    		#debug, are we getting proper stderr communication
    		#sys.stderr.write("hi from stderr")
    		#print goes to stdout to populate the cookie
    		#print parentString

		#feed the data to the cookie
    		#c['graph_session'] = keyword
    		#print c	#for debugging, did the data get added to graph_session
		
    		#Write to graphFile.json
    		writeToFile(parentString)
                exit(0)

	#this will run indefinitely unless we add a limit. The limit is the number of traversed URLs determined by the user's input for depth
	if len(observedURLs) == depth:
		break
	counter += 1	
    '''
    #debug timee
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
   
    #trim the last comma and add a closing square bracket for json formatting
    parentString = parentString[:-2]
    parentString += "],"
    #append the neighbor nodes string to the parent node string
    parentString += neighborString
    #add a closing bracket for json formatting
    parentString = parentString[:-2]
    parentString += "]}\n"

    #debugging, does the final string look correct
    #print parentString
    
    #debug, are we getting proper stderr communication
    #sys.stderr.write("hi from stderr")
    #print goes to stdout to populate the cookie
    #print parentString
    
    #feed the data to the cookie
    #c['graph_session']
    #print c	

    #Write to graphFile.json
    writeToFile(parentString)
breadthFirstSearch(startingURL, depth, keyword)

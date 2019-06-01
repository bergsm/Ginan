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

sys.stdout = open('log','w')

startingURL = sys.argv[1]
depth = int(sys.argv[2])
c = Cookie.SimpleCookie()

#set the keyword if the user input one, set to a dummy value if they didn't
keyword = sys.argv[3]
if keyword is '':
	keyword = 'aaaaaa'

#parse the URL
html = urllib.urlopen(startingURL).read()
#feed the parsed URL to Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

unvisitedURLs = []
unvisitedURLs.append(startingURL)

#listOfNeighbors = []

# The following write function was written by Shawn Berg, all credit to him for this
# Function to write urls from DFS to json file
# Args: urls in order from DFS
# Returns: None
def writeToFile(urls):
    with open('./public/graph_session', 'w+') as f:
        f.write(urls)
        #for counter, url in enumerate(urls):
        #    f.write('\n    {\n      "name\": \"URL\",\n      "label\": \"' + url + '\",\n       "id\":' +  str(counter+1) + '\n    }')
        #    if counter < len(urls)-1:
        #        f.write(',')
        #f.write('\n  ],\n  \"links\": [')
        #f.write(type(nodes))
            #f.write('\n    {\n      \"source\": ' + urls + ',\n      \"target\": ' + nodes(str(i)) + ',\n      \"type\": \"Links_To\"\n    }')
        #if i < len(urls)-1:
        #	f.write(',')
        #f.write('\n  ]\n}')


def breadthFirstSearch(startingURL, depth, keyword):
    counter = 1
    neighborCounter = 1
    anotherCounter = 2
    parentString = '{"nodes": ['
    neighborString = '{"links": ['
    observedURLs = []
    test = {}
    #some debugging checks, did everything make it into the data structure and what is the starting URL
    #print "How many unvisited URLs? - ", len(unvisitedURLs)
    #print "The starting URL is: " ,startingURL
   
    while len(unvisitedURLs) != 0:
	
        #get the first URL in the list
        discovered = unvisitedURLs.pop(0)
	unvisited = discovered.encode('ascii')
	print type(unvisited)
	print unvisited, "\n"
	observedURLs.append(unvisited) 
	nextParentString = ('{"name": "URL", "label": \"' + unvisited + '\", "id": ' + str(counter) + '}, ')
	parentString +=  nextParentString
	#need to get full URL rather than the relative path of every link on the page and add them to the unvisited list. Source for urljoin which 
	#gets the absolute path: https://stackoverflow.com/questions/44001007/scrape-the-absolute-url-instead-of-a-relative-path-in-python
	for links in soup.find_all('a',):
		#listOfNeighbors = []
		#print "entered the loop looking for links"
		absoluteURL = urljoin(unvisited, links.get('href'))

		#if the URL is not already in the unvisted list, add it
		if absoluteURL not in unvisitedURLs:
			#observedURLs.append(absoluteURL)
			unvisitedURLs.append(absoluteURL)
			nextParentString = ('{"name": "URL", "label": \"' + absoluteURL + '\", "id": ' + str(anotherCounter) + '}, ')
			parentString += nextParentString
			nextNeighborString = ('{"source": \"' + str(counter) + '", "target": \"' + str(neighborCounter) + '\", "type": "Links_To"}, ')
			neighborString += nextNeighborString
			neighborCounter += 1
			anotherCounter += 1
			#listOfNeighbors.append(absoluteURL)
			#print "appended a new URL"
	#observedURLs.append(listOfNeighbors)
	#add the parsed URL to the observed list
		#observedURLs.append(unvisited)
	#test = {}
	#source for zip and cycle: https://stackoverflow.com/questions/19686533/how-to-zip-two-differently-sized-lists
	#test = (zip(cycle(observedURLs), unvisitedURLs))
		#for keys, value in zip(observedURLs, unvisitedURLs):
		#	l = test.get(keys, [])
		#	l.append(value)
		#	test[keys] = l

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
                #writeToFile(observedURLs)
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
    #source for zip and cycle: https://stackoverflow.com/questions/19686533/how-to-zip-two-differently-sized-lists
    #https://stackoverflow.com/questions/32418354/convert-two-lists-to-dictionary-with-values-as-list
    for parent, neighbors in zip(cycle(observedURLs), unvisitedURLs):
    	listOfNeighbors = test.get(parent, [])
	if neighbors not in listOfNeighbors:
        	listOfNeighbors.append(neighbors)
       		test[parent] = listOfNeighbors
   
    #counter = 0
    #for parentNode in observedURLs:
    	#print parentNode
	#print ('\n    {\n      "name\": \"URL\",\n      "Label\": \"' + parentNode + '\",\n       "id\":' +  (counter + 1) + '\n    }')
        #if  counter < len(parentNode)-1:
        #	print (',')
	#counter += 1
    #for neighboringNode in test:
	#print test[neighboringNode]

    #debug, what are the unvisited URLs
    #for z in unvisitedURLs:
	#print z
   
    #print the appended discovered URLs
    #for a in test:
	#print "\n"
	#writeToFile(observedURLs, test[a])
    parentString += neighborString
    parentString = parentString[:-2]
    parentString += ']}'
    #print parentString
    graph_session = parentString
    c['graph_session'] = parentString
    #c.load(graph_session)
    writeToFile(parentString)
    #writeToFile(observedURLs, test)
    #print c.js_output()
    return c
breadthFirstSearch(startingURL, depth, keyword)

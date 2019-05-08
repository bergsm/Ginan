#!/usr/bin/env python

'''
Adapted from psuedocode in CLRS chapter 22.2, third edition. This function performs a breadth-first search on the graph. Source for Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''
import sys
import os
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin

startingURL = "https://red.com"
#parse the URL
html = urllib.urlopen(startingURL).read()
#feed the parsed URL to Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

unvisitedURLs = []
unvisitedURLs.append(startingURL)

def breadthFirstSearch(unvisitedURLs, startingURL):

    observedURLs = []

    #some debugging checks, did everything make it into the data structure and what is the starting URL
    print "How many unvisited URLs? - ", len(unvisitedURLs)
    print "The starting URL is: " ,startingURL
   
    while len(unvisitedURLs) != 0:
	
        #get the first URL in the list
        unvisited = unvisitedURLs.pop(0)
 
	#need to get full URL rather than the relative path of every link on the page and add them to the unvisited list. Source for urljoin which 
	#gets the absolute path: https://stackoverflow.com/questions/44001007/scrape-the-absolute-url-instead-of-a-relative-path-in-python
	for links in soup.find_all('a',):
		absoluteURL = urljoin(unvisited, links.get('href'))
		#if the URL is not already in the unvisted list, add it
		if absoluteURL not in unvisitedURLs:
			unvisitedURLs.append(absoluteURL)
	
	#add the parsed URL to the observed list
	observedURLs.append(unvisited)

	#this will run indefinitely unless we add a limit. For now, the hard coded limit of number of URLs left to visit is 100
	if len(unvisitedURLs) > 100:
		break	
    #debug time
    print "How many observed URLs? - " ,len(observedURLs)
    #print the list in a readable format to help with debugging    
    print "The list of observed URLs: ", 
    for x in observedURLs:
	print x
    #print the list in a readable format to help with debugging
    print "\n\nThe list of unvisited URLs: "
    for y in unvisitedURLs:
	print y

breadthFirstSearch(unvisitedURLs, startingURL)

#!/usr/bin/env python

'''
Adapted from psuedocode in CLRS chapter 22.2, third edition. This function performs a breadth-first search on the graph. Source for Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''
import sys
import os
import bs4
import urllib
from bs4 import BeautifulSoup

url = "https://oregonstate.edu"
#parse the URL
html = urllib.urlopen(url).read()
#feed the parsed URL to Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

startingURL = url
Neo4jGraph = []
Neo4jGraph.append(startingURL)

def breadthFirstSearch(Neo4jGraph, startingURL):

    observedURLs = []
    unvisitedURLs = Neo4jGraph

    #some debugging checks, did everything make it into the data structure and what is the starting URL
    print "How many unvisited URLs? - ", len(unvisitedURLs)
    print "The starting URL is: " ,startingURL
   
    #some debugging checks, did everything make it into the data structure and what is the starting URL
    print len(unvisitedURLs)
    print startingURL

    while len(unvisitedURLs) != 0:
        #get the first URL in the list
        unvisited = unvisitedURLs.pop() #problem here, can't pop by index, has to be value
        
	for links in soup.find_all('a'):
        	unvisitedURLs.append(links.get('href'))
	
	observedURLs.append(unvisited)
	
	#rip this out later, stuck in an infinite loop because we aren't checking to see if the URL is already in the unvisitedURLs list. This is a bandaid to break out of the infinite loop
	if len(unvisitedURLs) > 10:
		break	

    print "How many observed URLs? - " ,len(observedURLs)
    print "The list of observed URLs: ", observedURLs

    print "The list of unvisited URLs: ", unvisitedURLs	
breadthFirstSearch(Neo4jGraph, startingURL)

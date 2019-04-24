import requests
import sys


#Take starting url as argument?
if len(sys.argv) < 3:
    #TODO print to stderr
    print("No url and/or iteration argument provided")
    exit(1)

#Initialize list of variables
currurl = sys.argv[1]
iterations = sys.argv[2]
urlChain = []


def DFS(url, iterations):
    urlChain.append(url)
    #base case
    if iterations == 0:
        #write urlChain to file for graph

    #fetch page from url

    #parse page for all links
    links = []

    #choose one link at random
    url = links[randNum]
    iterations -= 1

    DFS(url, iterations)

DFS(currURL, iterations)

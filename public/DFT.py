import requests
import sys
import random


#Take starting url as argument?
if len(sys.argv) < 3:
    print("No url and/or depth argument provided")
    exit(1)

#Initialize list of variables
initUrl = sys.argv[1]
depth = int(sys.argv[2])
urlChain = []


# Function to write urls from DFS to json file for
# neo4j
# Args: urls in order from DFS
# Returns: None
def writeToFile(urls):
    with open('DFT.json', 'w+') as f:
        for url in urls:
            #TODO format in valid neo4j json
            f.write(url + '\n')


# Function to parse page for all links
# Args: url for page in question
# Returns: array/list of links
def parsePage(url):
    #fetch page
    print("Fetching page..")
    #TODO
    #r = requests.get(url)
    #page = r.content

    #TODO parse for all links
    print("Parsing..")
    #return links as array/list
    #TODO uncommment these debug links
    links = ["test1.com", "test2.com", "test3.com"]
    return links


# Function that performs the Depth First Traversal of links for a
# source page
# Args: valid url, depth to traverse
# Returns: None
def DFT(url, depth):

    #add url to chain
    urlChain.append(url)

    #base case
    if depth == 0:
        #write urlChain to file for graph and exit
        writeToFile(urlChain)
        exit(0)

    #parse page for all links
    links = parsePage(url)

    #choose one link at random
    print("Choosing link at random..")
    randNum = random.randint(0, len(links)-1)
    url = links[randNum]
    print("Random url is: " + url)

    #decrement and recurse
    depth -= 1
    DFT(url, depth)

DFT(initUrl, depth)

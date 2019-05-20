import requests
import sys
import random
from bs4 import BeautifulSoup
from urlparse import urljoin


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



# Function to parse page for all links
# Args: url for page in question
# Returns: array/list of links
def parsePage(url, links):
    #fetch page
    print("Fetching page..")
    try:
        r = requests.get(url)
        page = r.content
        print("Parsing..")
        soup = BeautifulSoup(page, "html.parser")
        if not soup.body:
            raise Exception("Page not parsed")
        links = []
        for link in soup.find_all('a'):
            links.append(urljoin(url, link.get('href')))
    except Exception as e:
        #pick another link if available
        print("Error: " + str(e))
        if len(links) < 1:
            print("No other links available.")
            return []
        else:
            print("Choosing a different link..")
            randNum = random.randint(0, len(links)-1)
            #TODO remove link from list?
            url = links[randNum]
            return parsePage(url, links)
    else:
        return links


# Function that performs the Depth First Traversal of links for a
# source page
# Args: valid url, depth to traverse
# Returns: None
def DFT(url, depth, links):

    #add url to chain
    urlChain.append(url)

    #parse page for all links
    links = parsePage(url, links)

    #base case
    if depth == 0 or links == []:
        #write urlChain to file for graph and exit
        print("Depth reached, no links on page, or url format incorrect. Generating results..")
        writeToFile(urlChain)
        exit(0)

    #choose one link at random
    print("Choosing link at random..")
    randNum = random.randint(0, len(links)-1)
    #TODO remove link from list?
    url = links[randNum]
    print("Random url is: " + url)

    #decrement and recurse
    depth -= 1
    DFT(url, depth, links)

DFT(initUrl, depth, [])

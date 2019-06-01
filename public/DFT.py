import requests
import Cookie
import sys
import random
from bs4 import BeautifulSoup
from urlparse import urljoin

outputFP = './public/graphFile.json'

# Function to write urls from DFS to json file for
# d3
# Args: urls in order from DFS, filePath to save
# Returns: None
def writeToFile(urls, filePath):
    with open(filePath, 'w+') as f:
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


# Function to write urls from DFS to json cookie for d3
# Args: urls in order from DFS, cookie name
# Returns: None
def writeToCookie(urls):
    jsonString = ''
    jsonString += '{\n  \"nodes\": ['
    for counter, url in enumerate(urls):
        jsonString += '\n    {\n      "name\": \"URL\",\n      "label\": \"' + url + '\",\n       "id\":' +  str(counter+1) + '\n    }'
        if counter < len(urls)-1:
            jsonString += ','
    jsonString += '\n  ],\n  \"links\": ['
    for i in range(1, len(urls)):
        jsonString += '\n    {\n      \"source\": ' + str(i) + ',\n      \"target\": ' + str(i+1) + ',\n      \"type\": \"Links_To\"\n    }'
        if i < len(urls)-1:
            jsonString += ','
    jsonString += '\n  ]\n}'
    print(jsonString)


# Function to parse page for all links
# Args: url for page in question, list of links from previous page
# Returns: array/list of links
def parsePage(url, links):
    #fetch page
    sys.stderr.write("Fetching page..\n")
    try:
        r = requests.get(url)
        page = r.content
        sys.stderr.write("Parsing..\n")
        soup = BeautifulSoup(page, "html.parser")
        if not soup.body:
            raise Exception("Page not parsed\n")
        links = []
        for link in soup.find_all('a'):
            links.append(urljoin(url, link.get('href')))
    except Exception as e:
        #pick another link if available
        sys.stderr.write("Error: " + str(e))
        if len(links) < 1:
            sys.stderr.write("No other links available.\n")
            return []
        else:
            sys.stderr.write("Choosing a different link..\n")
            randNum = random.randint(0, len(links)-1)
            url = links[randNum]
            del links[randNum]
            return parsePage(url, links)
    else:
        return links


# Function that performs the Depth First Traversal of links for a
# source page
# Args: valid url, depth to traverse, list of links
# Returns: None
def DFT(url, depth, urlChain, links, keyword):

    #add url to chain
    urlChain.append(url)

    #parse page for all links
    links = parsePage(url, links)

    #base case
    if depth == 0 or links == [] or (any(keyword in link for link in urlChain) and keyword):
        #write urlChain to file for graph and exit
        sys.stderr.write("Depth reached, keyword found, no links on page, or url format incorrect. Generating results..\n")
        writeToFile(urlChain, outputFP)
        writeToCookie(urlChain)
        return

    #choose one link at random
    sys.stderr.write("Choosing link at random..\n")
    randNum = random.randint(0, len(links)-1)
    url = links[randNum]
    del links[randNum]
    sys.stderr.write("Random url is: " + url + "\n")

    #decrement and recurse
    depth -= 1
    DFT(url, depth, urlChain, links, keyword)

def main():
    #Take starting url as argument?
    if len(sys.argv) < 3:
        sys.stderr.write("No url and/or depth argument provided\n")
        exit(1)

    #Initialize list of variables
    initUrl = sys.argv[1]
    depth = int(sys.argv[2])
    if len(sys.argv) == 4:
        keyword = sys.argv[3]
    else:
        keyword = ''
    urlChain = []
    links = []

    sys.stderr.write("keyword is: " + keyword + "\n")

    DFT(initUrl, depth, urlChain, links, keyword)

if __name__ == "__main__":
    main()

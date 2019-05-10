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
#TODO add "http://" if needed to argument
initUrl = sys.argv[1]
depth = int(sys.argv[2])
urlChain = []


# Function to write urls from DFS to json file for
# neo4j
# Args: urls in order from DFS
# Returns: None
def writeToFile(urls):
    with open('DFT.json', 'w+') as f:
        f.write('{\n\t\"nodes\": [')
        for counter, url in enumerate(urls):
            f.write('\n\t{\n\t\t\"name\": \"URL\",\n\t\t\"label\": \"' + url + '\",\n\t\t\"id\":' +  str(counter) + '\n\t}')
            if counter < len(urls)-1:
                f.write(',')
        f.write('\n\t],\n\t\"links\": [')
        for i in range(0, len(urls)):
            f.write('\n\t{\n\t\t\"source\": ' + str(i) + ',\n\t\t\"target\": ' + str(i+1) + ',\n\t\t\"type\": \"Links_To\"\n\t}')
            if i < len(urls)-1:
                f.write(',')
        f.write('\n\t]\n}')



# Function to parse page for all links
# Args: url for page in question
# Returns: array/list of links
def parsePage(url):
    #fetch page
    print("Fetching page..")
    #TODO SSL errors are occuring for certain links
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        #TODO pick another link if available
        print("Error fetching page: " + str(e))
        return []
    else:
        page = r.content
        print("Parsing..")
        soup = BeautifulSoup(page, "html.parser")
        links = []
        for link in soup.find_all('a'):
            links.append(urljoin(url, link.get('href')))

        #Debug links
        #links = ["test1.com", "test2.com", "test3.com"]

        #return links as array/list
        return links


# Function that performs the Depth First Traversal of links for a
# source page
# Args: valid url, depth to traverse
# Returns: None
def DFT(url, depth):

    #add url to chain
    urlChain.append(url)

    #parse page for all links
    links = parsePage(url)

    #base case
    if depth == 0 or links == []:
        #write urlChain to file for graph and exit
        print("Depth reached or no links on page. Printing results to file..")
        writeToFile(urlChain)
        exit(0)

    #choose one link at random
    print("Choosing link at random..")
    randNum = random.randint(0, len(links)-1)
    url = links[randNum]
    print("Random url is: " + url)

    #decrement and recurse
    depth -= 1
    DFT(url, depth)

DFT(initUrl, depth)

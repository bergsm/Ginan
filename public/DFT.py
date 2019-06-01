import requests
import Cookie
import sys
import random
from bs4 import BeautifulSoup
from urlparse import urljoin

outputFP = './public/graphFile.json'
#cookieName = 'graph_session'
cookieName = 'test2'


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
def writeToCookie(urls, cookieName):
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
    c = Cookie.SimpleCookie()
    c[cookieName] = jsonString
    s = requests.Session()
    cookie_obj = requests.cookies.create_cookie(domain='localhost:3030',name='test_cookie',value='wish this would work')
    s.cookies.set_cookie(cookie_obj)
    #s.post('http://localhost:3030', cookies=c)
    #s.cookies.set(c)
    #r = requests.post('http://localhost:3030', cookies=c)
    #print c.js_output()


# Function to parse page for all links
# Args: url for page in question, list of links from previous page
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
        print("Depth reached, keyword found, no links on page, or url format incorrect. Generating results..")
        writeToFile(urlChain, outputFP)
        writeToCookie(urlChain, cookieName)
        return

    #choose one link at random
    print("Choosing link at random..")
    randNum = random.randint(0, len(links)-1)
    url = links[randNum]
    del links[randNum]
    print("Random url is: " + url)

    #decrement and recurse
    depth -= 1
    DFT(url, depth, urlChain, links, keyword)

def main():
    c = Cookie.SimpleCookie()
    c['test'] = 'hello'
    print(c)
    #Take starting url as argument?
    if len(sys.argv) < 3:
        print("No url and/or depth argument provided")
        exit(1)

    #Initialize list of variables
    initUrl = sys.argv[1]
    depth = int(sys.argv[2])
    keyword = sys.argv[3]
    urlChain = []
    links = []

    print("keyword is: " + keyword)

    DFT(initUrl, depth, urlChain, links, keyword)

if __name__ == "__main__":
    main()

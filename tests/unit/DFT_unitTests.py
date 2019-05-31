import sys
import os
sys.path.insert(0, '../../public')
import json
import filecmp
import DFT




# test writeToFile function
testCase1 = ["http://www.test1.com", "http://www.test2.com", "http://www.test3.com", "http://www.test4.com"]
testCase2 = ["https://www.test1.org", "https://www.testing2.edu", "http://www.testme3.co", "http://www.test4.io"]

print("Testing writeToFile function")

DFT.writeToFile(testCase1, './graphFile.json')
assert filecmp.cmp('./graphFile.json', './graphFile.test1.json')
DFT.writeToFile(testCase2, './graphFile.json')
assert filecmp.cmp('./graphFile.json', './graphFile.test2.json')

os.remove('./graphFile.json')

# TODO test parsePage function
# DFT.parsePage(url, testCase1)

# TODO test DFT function
# DFT.DFT(url, depth, [], [], keyword)

print("All tests passed!")

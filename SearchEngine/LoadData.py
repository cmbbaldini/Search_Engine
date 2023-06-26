import json
from BTrees.OOBTree import OOBTree


class LoadData:
    def __init__(self):
        self.wordIndexTree = OOBTree()
        with open("IDUrlMap.json", 'r') as URLmap:
            self.IDUrlMap = json.load(URLmap)
        self.createWordBTree()
        with open("full_index/index.jsonl") as indexFile:
            self.indexFile = indexFile

    def createWordBTree(self) -> None:
        """stores words and their corresponding place in the main index in a btree """

        with open("full_index/index.jsonl", "r") as index:
            offset = 0
            for line in index:
                jsonObj = json.loads(line)
                self.wordIndexTree.insert(list(jsonObj.keys())[0], offset)
                offset += len(line) + 1

    def getWordPositionInIndex(self, word: str) -> int:
        """takes a word as an argument and returns its position in the main index file"""

        return self.wordIndexTree[word] if word in self.wordIndexTree else None

    def getPosting(self, offset: int, word: str) -> list:
        """finds word in index using offset, loads json, returns list of postings"""

        self.indexFile.seek(offset)
        postingObject = json.loads(self.indexFile.readline())
        return postingObject[word]
    
    def getDocumentURL(self, docID: int) -> str:
        """get the URL of the document ID"""

        return self.IDUrlMap[docID]

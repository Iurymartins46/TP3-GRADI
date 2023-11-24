class IndiceInvertido:
    def __init__(self, docs):
        self.invIndex = {}
        self.root = docs
        for i, t in enumerate(docs):
            self.parse(i, t)

    def parse(self, idoc, doc):
        words = [w.lower() for w in doc.split(' ')]

        for position, w in enumerate(words):
            if w in self.invIndex:
                self.invIndex[w].append((idoc, position))
            else:
                self.invIndex[w] = [(idoc, position)]

    def search(self, word):
        if word in self.invIndex:
            return self.invIndex[word][:]
        else:
            return []
        
#depois só substituir para os documentos que contem as sinopses dos filmes
titles = ["Um dois tres quatro um",
          "cinco um",
          "abehdah"]

index = IndiceInvertido(titles)

print(index.invIndex)


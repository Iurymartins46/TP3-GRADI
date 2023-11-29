import json

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
        
"""
# Substitua pelos documentos que contêm as sinopses dos filmes
titles = ["Um dois tres quatro um",
          "cinco um",
          "abehdah"]

index = IndiceInvertido(titles)

# Criar a estrutura desejada para o XML
sentencas_entries = []

for word, positions in index.invIndex.items():
    consolidated_positions = ', '.join([f"[{pos[0]}, {pos[1]}]" for pos in positions])
    word_entry = {"@palavra": word, "#text": consolidated_positions}
    sentencas_entries.append(word_entry)

# Adiciona um elemento "sentencas" que envolve todas as entradas
xml_dict = {"indiceInvertido": {"sentencas": sentencas_entries}}

# Abre o arquivo XML para escrita
with open("person.xml", "w") as xml_file:
    xmltodict.unparse(xml_dict, output=xml_file, pretty=True)

print("Conversão concluída.")"""

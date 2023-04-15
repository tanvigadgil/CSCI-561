# def createClauses(sentence):
#     args = []
    

# def convertToCNF(sentence):
#     implicationIndex = sentence.find("=>")

#     if implicationIndex == -1:
#         pass
#     else:
#         premise = sentence[:implicationIndex]
#         conclusion = sentence[implicationIndex + 2:]
#         # TODO: Do I need to strip the spaces from the predicate and conclusion?

#         andIndex = premise.find("&")

#         while(andIndex != -1):
#             pass
#         # TODO: Negation operations on predicate
        
#         fact = premise + '|' + conclusion

#         print(fact)
#         return fact

class Sentence:
    def __init__(self):
        pass

    def makeSentence(sentence):
        pass

    def printSentences(sentences):
        for sentence in sentences:
            print(sentence)


    
class FOLResolution:
    def __init__(self):
        self.nOfKB = 0
        self.KB = list()
        self.Query = list()

    # Read input file and process it
    def processInput(self, inputFile):
        file = open(inputFile, "r")
        Lines = file.readlines()

        # Query
        query = Lines[0].strip().replace(" ", "")
        self.Query.append(Sentence.makeSentence(query))
        print("Query: ")
        Sentence.printSentences(self.Query)

        # Number of sentences given in the KB
        self.nOfKB = int(Lines[1])
        print(self.nOfKB)

        # List of sentences in the KB
        for i in range(2, self.nOfKB + 2):
            sentence = Lines[i].strip().replace(" ", "")
            self.KB.append(Sentence.makeSentence(sentence))
        print("KB: ")
        Sentence.printSentences(self.KB)

def main():
    fol = FOLResolution()
    fol.processInput('input.txt')

if __name__ == "__main__":
    main()
import copy

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


class Predicate:
    def __init__(self, name, negationFlag, args):
        self.name = name
        self.negationFlag = negationFlag
        self.args = args

    # Overloading the print function
    def __str__(self):
        negation = ""
        if self.negationFlag:
            negation = "~"
        arguments = ','.join(self.args)
        return negation + self.name + "(" + arguments + ")"

    def negate(self):
        self.negationFlag = not self.negationFlag

    def isVariable(variable):
        if variable[0].islower():
            return True
        return False

    def makePredicate(predicateString):
        negationFlag = False
        predicateString = predicateString[:-1]
        if predicateString[0] == '~':
            negationFlag = True
            predicateString = predicateString[1:]
        
        splitString = predicateString.split("(")
        name = splitString[0]
        args = splitString[1].split(",")

        for i in range(len(args)):
            if Predicate.isVariable(args[i]):
                if args[i] in Sentence.variableMap:
                    args[i] = Sentence.variableMap[args[i]]
                else:
                    Sentence.variableMap[args[i]] = "var" + str(Sentence.variableCounter)
                    args[i] = Sentence.variableMap[args[i]]
                    Sentence.variableCounter += 1
            print(args[i])

        return Predicate(name, negationFlag, args)

class Sentence:
    variableMap = dict()
    variableCounter = 0

    def __init__(self, predicates):
        self.predicates = predicates

    # Overloading the print function
    def __str__(self):
        predicateString = list()
        for predicate in self.predicates:
            predicateString.append(str(predicate))
        sentence = ','.join(predicateString)
        return "[" + sentence + "]"

    # Print each sentence in the list
    def printSentences(sentences):
        for sentence in sentences:
            print(sentence)

    def negateSentence(self):
        for predicate in self.predicates:
            predicate.negate()

    # Make a sentence from a string
    def makeSentence(sentenceString):
        predicates = list()

        if "=>" in sentenceString:
            # List of predicates splited by "=>"
            splitSpring = sentenceString.split("=>")
            print(splitSpring)

            # TODO: Check for OR as well
            premise = splitSpring[0].split("&")

            for each in premise:
                p = Predicate.makePredicate(each)
                p.negate()
                predicates.append(p)
            conclusion = Predicate.makePredicate(splitSpring[1])
            predicates.append(conclusion)

        else:
            predicates.append(Predicate.makePredicate(sentenceString))
        Sentence.variableMap.clear()
        return Sentence(predicates)

    def getPossibleClauses(self):
        pass
    
class FOLResolution:
    def __init__(self):
        self.nOfKB = 0
        self.KB = list()
        self.Query = list()

    # Print each sentence in the list
    def printSentences(sentences):
        for sentence in sentences:
            print(sentence)

    # Read input file and process it
    def processInput(self, inputFile):
        file = open(inputFile, "r")
        Lines = file.readlines()

        # Query
        query = Lines[0].strip().replace(" ", "")
        self.Query.append(Sentence.makeSentence(query))
        print("Query: ")
        FOLResolution.printSentences(self.Query)

        # Number of sentences given in the KB
        self.nOfKB = int(Lines[1])
        print(self.nOfKB)

        # List of sentences in the KB
        for i in range(2, self.nOfKB + 2):
            sentence = Lines[i].strip().replace(" ", "")
            self.KB.append(Sentence.makeSentence(sentence))
        print("KB: ")
        FOLResolution.printSentences(self.KB)

    def writeOutput(self):
        outputFile = open("output.txt", "w")
        KBToAsk = copy.copy(self.KB)
        result = self.ask(KBToAsk, self.Query[0])
        print(result)

        if result:
            outputFile.write("TRUE")
        else:
            outputFile.write("FALSE")

    def ask(self, kb, query):
        queryAsked = copy.copy(query)
        print("Query asked: ")
        print(queryAsked)
        queryAsked.negateSentence()
        kb.append(queryAsked)
        kb.sort(key = lambda x: len(x.predicates))

        while True:
            newKB = list()
            for sentence in kb:
                clauses = sentence.getPossibleClauses()
                for clause in clauses:
                    resolvents = sentence.resolve(clause)
                    for resolvent in resolvents:
                        if len(resolvent.predicates) == 1 and resolvent.predicates[0].name == "TRUE":
                            return True
                    
                    newKB += resolvents
            kbWithRemovedDuplicates = self.removeDuplicates(newKB)
            if len(kbWithRemovedDuplicates) == 0:
                break
            differenceBtwKB = self.difference(kb, kbWithRemovedDuplicates)

            if len(kbWithRemovedDuplicates) == 0:
                break

            kb = kbWithRemovedDuplicates
            kb.sort(key = lambda x: len(x.predicates))

        return False


def main():
    fol = FOLResolution()
    fol.processInput('input.txt')
    fol.writeOutput()

if __name__ == "__main__":
    main()
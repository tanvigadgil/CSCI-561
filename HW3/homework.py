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
    # Format: [Name, True, [arg1, arg2, ...]]
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

    # Overloading the equal function
    def __eq__(self, other):
        if self.negationFlag != other.negationFlag:
            return False
        
        if self.name != other.name:
            return False
        
        if len(self.args) != len(other.args):
            return False
        
        for i in range(len(self.args)):
            if (not Predicate.isVariable(self.args[i])) and (not Predicate.isVariable(other.args[i])) and self.args[i] != other.args[i]:
                return False
        return True

    # Change the negation flag
    def negate(self):
        self.negationFlag = not self.negationFlag

    # Check if the argument is a variable
    def isVariable(variable):
        if variable[0].islower():
            return True
        return False

    # Make a predicate from a string
    def createPredicate(predicateString):
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

    # Check if two predicates can be unified
    def canBeUnified(self, factPredicate):
        for i in range(len(self.args)):
            if (not Predicate.isVariable(self.args[i])) and (not Predicate.isVariable(factPredicate.args[i])) and (self.args[i] != factPredicate.args[i]):
                return False
        return True

    # Check if two predicates can be canceled
    def canBeCanceled(self, factPredicate):
        if self.name == factPredicate.name and self.negationFlag != factPredicate.negationFlag:
            if self.canBeUnified(factPredicate):
                return True
            return False

    # Unify two predicates
    def unify(predicate1, predicate2):
        unificationMap = dict()
        isUnified = False

        for i in range(len(predicate1.args)):
            # If both are variables
            if Predicate.isVariable(predicate1.args[i]) and Predicate.isVariable(predicate2.args[i]):
                unificationMap[predicate1.args[i]] = predicate2.args[i]
                
            # If first is constant and second is variable
            elif not Predicate.isVariable(predicate1.args[i]) and Predicate.isVariable(predicate2.args[i]):
                unificationMap[predicate2.args[i]] = predicate1.args[i]
                isUnified = True

            # If first is variable and second is constant
            elif Predicate.isVariable(predicate1.args[i]) and not Predicate.isVariable(predicate2.args[i]):
                unificationMap[predicate1.args[i]] = predicate2.args[i]
                isUnified = True

            # If both are constants and arguments are equal
            elif not Predicate.isVariable(predicate1.args[i]) and not Predicate.isVariable(predicate2.args[i]) and predicate1.args[i] == predicate2.args[i]:
                unificationMap[predicate1.args[i]] = predicate2.args[i]
                isUnified = True

            # If both are constants and arguments are not equal
            elif not Predicate.isVariable(predicate1.args[i]) and not Predicate.isVariable(predicate2.args[i]) and predicate1.args[i] != predicate2.args[i]:
                isUnified = False
                break

        if not isUnified:
            unificationMap.clear()

        return unificationMap

class Sentence:
    variableMap = dict()
    variableCounter = 0

    # Format: [predicate1, predicate2, ...]
    def __init__(self, predicates):
        self.predicates = predicates

    # Overloading the print function
    def __str__(self):
        predicateString = list()
        for predicate in self.predicates:
            predicateString.append(str(predicate))
        sentence = ','.join(predicateString)
        return "[" + sentence + "]"

    # Negate the sentence by negating each predicate
    def negateSentence(self):
        for i in range(len(self.predicates)):
            self.predicates[i].negate()

    # Make a sentence from a string
    def createSentence(sentenceString):
        predicates = list()

        if "=>" in sentenceString:
            # List of predicates splited by "=>"
            splitSpring = sentenceString.split("=>")
            print(splitSpring)

            # TODO: Check for OR as well
            premise = splitSpring[0].split("&")

            for each in premise:
                p = Predicate.createPredicate(each)
                p.negate()
                predicates.append(p)
            conclusion = Predicate.createPredicate(splitSpring[1])
            predicates.append(conclusion)

        else:
            predicates.append(Predicate.createPredicate(sentenceString))
        Sentence.variableMap.clear()
        return Sentence(predicates)

    # Check if the sentence can be resolved
    def canBeResolved(self, fact):
        for predicate in self.predicates:
            for factPredicate in fact.predicates:
                if predicate.canBeCanceled(factPredicate):
                    return True
        return False

    # Get all the possible clauses that can be resolved
    def getPossibleClauses(self, kb):
        clauses = list()
        for fact in kb:
            if self.canBeResolved(fact):
                clauses.append(fact)
        return clauses

    # Get all the possible substitutions
    def getPossibleSubstitutions(self, clause):
        substitutes = list()
        for predicate in self.predicates:
            for clausePredicate in clause.predicates:
                if predicate.name == clausePredicate.name:
                    unificationMap = Predicate.unify(predicate, clausePredicate)
                    if len(unificationMap) != 0:
                        substitutes.append(unificationMap)
        return substitutes
    
    # Substitute the variables in the sentence
    def substitute(predicate1, predicate2, substitution):
        inference = list()

        return Sentence(inference)

    # Resolve the sentence with the given clause
    def resolve(self, clause):
        inferences = list()
        substitutions = self.getPossibleSubstitutions(clause)
        print(substitutions)
        for substitution in substitutions:
            substitute = Sentence.substitute(self, clause, substitution)
            print(substitute)
            inferences.append(substitute)
            print(inferences)
        return inferences

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
        self.Query.append(Sentence.createSentence(query))
        print("Query: ")
        FOLResolution.printSentences(self.Query)

        # Number of sentences given in the KB
        self.nOfKB = int(Lines[1])
        print(self.nOfKB)

        # List of sentences in the KB
        for i in range(2, self.nOfKB + 2):
            sentence = Lines[i].strip().replace(" ", "")
            self.KB.append(Sentence.createSentence(sentence))
        print("KB: ")
        FOLResolution.printSentences(self.KB)

    # Write the output to the output file
    def writeOutput(self):
        outputFile = open("output.txt", "w")
        KBToAsk = copy.copy(self.KB)
        result = self.ask(KBToAsk, self.Query[0])
        print(result)

        if result:
            outputFile.write("TRUE")
        else:
            outputFile.write("FALSE")

    # Remove duplicates from the list
    def removeDuplicates(self, kb):
        toBeRemoved = list()
        withNoDuplicates = list()
        return withNoDuplicates

    # Difference between two lists
    def difference(self, kb1, kb2):
        differenceList = list()

        return differenceList

    # Ask the query
    def ask(self, kb, query):
        queryAsked = copy.copy(query)
        print("Query asked: ")
        print(queryAsked)
        queryAsked.negateSentence()
        kb.append(queryAsked)
        FOLResolution.printSentences(kb)
        kb.sort(key = lambda x: len(x.predicates))
        print("Sorted KB: ")
        FOLResolution.printSentences(kb)

        while True:
            newKB = list()
            for fact in kb:
                print("Fact: ")
                print(fact)
                clauses = fact.getPossibleClauses(kb)
                for clause in clauses:
                    print(fact, clause)
                    resolvents = fact.resolve(clause)
                    for resolvent in resolvents:
                        if len(resolvent.predicates) == 1 and resolvent.predicates[0].name == "TRUE":
                            return True
                    
                    newKB += resolvents

            kbWithRemovedDuplicates = self.removeDuplicates(newKB)
            FOLResolution.printSentences(kbWithRemovedDuplicates)
            if len(kbWithRemovedDuplicates) == 0:
                break

            differenceBtwKB = self.difference(kb, kbWithRemovedDuplicates)
            FOLResolution.printSentences(differenceBtwKB)
            if len(differenceBtwKB) == 0:
                break

            kb += differenceBtwKB
            kb.sort(key = lambda x: len(x.predicates))
            FOLResolution.printSentences(kb)

        return False


def main():
    fol = FOLResolution()
    fol.processInput('input.txt')
    fol.writeOutput()

if __name__ == "__main__":
    main()
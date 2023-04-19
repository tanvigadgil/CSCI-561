import copy
import time

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
    def __eq__(self, predicate2):
        if self.negationFlag != predicate2.negationFlag:
            return False
        
        if self.name != predicate2.name:
            return False
        
        if len(self.args) != len(predicate2.args):
            return False
        
        for i in range(len(self.args)):
            if (not Predicate.isVariable(self.args[i])) and (not Predicate.isVariable(predicate2.args[i])) and self.args[i] != predicate2.args[i]:
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
        
        # print("Predicate String: " + predicateString)
        splitString = predicateString.split("(")
        # print("Split String: ")
        # print(splitString)

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
        if len(self.args) != len(factPredicate.args):
            return False
        
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

    # Check if two predicates are the same
    def isSame(self, predicate2):
        if self.name != predicate2.name:
            return False
        if len(self.args) != len(predicate2.args):
            return False
        
        for i in range(len(self.args)):
            if self.args[i] != predicate2.args[i]:
                return False
        return True


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
                predicate = Predicate.createPredicate(each)
                predicate.negate()
                predicates.append(predicate)
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
        substitutions = list()
        for predicate in self.predicates:
            for clausePredicate in clause.predicates:
                if predicate.name == clausePredicate.name:
                    unificationMap = Predicate.unify(predicate, clausePredicate)
                    if len(unificationMap):
                        substitutions.append(unificationMap)
        return substitutions
    
    # Substitute the variables in the sentence
    def substitute(clause1, clause2, substitution):
        inference = list()
        clause1Substitution = list()
        clause2Substitution = list()

        for predicate in clause1.predicates:
            args = []
            for i in range(len(predicate.args)):
                if predicate.args[i] in substitution and Predicate.isVariable(predicate.args[i]):
                    args.append(substitution[predicate.args[i]])
                else:
                    args.append(predicate.args[i])
            clause1Substitution.append(Predicate(predicate.name, predicate.negationFlag, args))

        for predicate in clause2.predicates:
            args = []
            for i in range(len(predicate.args)):
                if predicate.args[i] in substitution and Predicate.isVariable(predicate.args[i]):
                    args.append(substitution[predicate.args[i]])
                else:
                    args.append(predicate.args[i])
            clause2Substitution.append(Predicate(predicate.name, predicate.negationFlag, args))

        for predicates1 in clause1Substitution:
            isCompliment = False
            for predicates2 in clause2Substitution:
                if predicates1.isSame(predicates2) and predicates1.negationFlag != predicates2.negationFlag:
                    isCompliment = True
                    break
            if not isCompliment:
                inference.append(predicates1)
        
        for predicates2 in clause2Substitution:
            isCompliment = False
            for predicates1 in clause1Substitution:
                if predicates2.isSame(predicates1) and predicates2.negationFlag != predicates1.negationFlag:
                    isCompliment = True
                    break
            if not isCompliment:
                inference.append(predicates2)

        if len(inference) == 0:
            inference.append(Predicate("TRUE", False, []))

        return Sentence(inference)

    # Resolve the sentence with the given clause
    def resolve(self, clause):
        inferences = list()
        substitutions = self.getPossibleSubstitutions(clause)
        # print(substitutions)
        for substitution in substitutions:
            substitute = Sentence.substitute(self, clause, substitution)
            # print(substitute)
            inferences.append(substitute)
            # print(inferences)
        return inferences

class FOLResolution:
    def __init__(self):
        self.nOfKB = 0
        self.KB = list()
        self.Query = list()
        self.startTime = time.time()

    # Print each sentence in the list
    def printSentences(sentences):
        for sentence in sentences:
            print(sentence)

    # Read input file and process it
    def processInput(self, inputFile):
        print("-------------------- Processing input file: " + inputFile + " --------------------")
        file = open(inputFile, "r")
        lines = file.readlines()

        # Query
        query = lines[0].strip().replace(" ", "")
        self.Query.append(Sentence.createSentence(query))
        print("Query: ")
        FOLResolution.printSentences(self.Query)

        # Number of sentences given in the KB
        self.nOfKB = int(lines[1])
        print(self.nOfKB)

        # List of sentences in the KB
        for i in range(2, self.nOfKB + 2):
            sentence = lines[i].strip().replace(" ", "")
            self.KB.append(Sentence.createSentence(sentence))
        print("KB: ")
        FOLResolution.printSentences(self.KB)

    # Write the output to the output file
    def writeOutput(self):
        outputFile = open("output.txt", "w")
        KBToAsk = copy.copy(self.KB)
        result = self.ask(KBToAsk, self.Query[0])
        print("-------------------- Writing output --------------------")
        print(result)

        if result:
            outputFile.write("TRUE")
        else:
            outputFile.write("FALSE")

    # Check if the given lists are same
    def areListsSame(self, predicateList1, predicateList2):
        match = []
        isP1Same = False

        for predicate1 in predicateList1:
            for predicate2 in predicateList2:
                if time.time() - self.startTime > 25:
                    break
                if predicate1 == predicate2:
                    match.append(predicate1)
                    break
            if time.time() - self.startTime > 25:
                break
        
        # print(match)
        if len(match) == len(predicateList1):
            isP1Same = True
        
        match = []
        isP2Same = False

        for predicate2 in predicateList2:
            for predicate1 in predicateList1:
                if time.time() - self.startTime > 25:
                    break
                if predicate2 == predicate1:
                    match.append(predicate2)
                    break
            if time.time() - self.startTime > 25:
                break

        # print(match)
        if len(match) == len(predicateList2):
            isP2Same = True
        return isP1Same and isP2Same

    # Remove duplicates from the list
    def removeDuplicates(self, kb):
        toBeRemoved = list()

        for i in range(len(kb) - 1):
            predicate1 = kb[i].predicates
            for j in range(i + 1, len(kb)):
                if time.time() - self.startTime > 25:
                    break
                predicate2 = kb[j].predicates
                if self.areListsSame(predicate1, predicate2):
                    toBeRemoved.append(j)

            if time.time() - self.startTime > 25:
                break

        withNoDuplicates = list()
        for i in range(len(kb)):
            if i not in toBeRemoved:
                withNoDuplicates.append(kb[i])

        return withNoDuplicates

    # Difference between two lists
    def difference(self, kb1, kb2):
        differenceList = list()

        for clauses2 in kb2:
            predicateList2 = clauses2.predicates
            isSame = False

            for clauses1 in kb1:
                if time.time() - self.startTime > 25:
                    break
                predicateList1 = clauses1.predicates
                if self.areListsSame(predicateList1, predicateList2):
                    isSame = True
                    break

            if time.time() - self.startTime > 25:
                break
            if not isSame: 
                differenceList.append(clauses2)

        return differenceList

    # Ask the query
    def ask(self, kb, query):
        self.startTime = time.time()
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
            if time.time() - self.startTime > 25:
                break

            newKB = list()
            for fact in kb:
                if time.time() - self.startTime > 25:
                    break
                # print("Fact: ")
                # print(fact)
                clauses = fact.getPossibleClauses(kb)

                if (fact.predicates[0].name == queryAsked.predicates[0].name) and len(clauses) == 0:
                    return False
                for clause in clauses:
                    if time.time() - self.startTime > 25:
                        break
                    # print(fact, clause)
                    resolvents = fact.resolve(clause)
                    for resolvent in resolvents:
                        if len(resolvent.predicates) == 1 and resolvent.predicates[0].name == "TRUE":
                            return True
                    
                    newKB += resolvents

                if time.time() - self.startTime > 25:
                    break

            if time.time() - self.startTime > 25:
                break

            kbWithRemovedDuplicates = self.removeDuplicates(newKB)
            if time.time() - self.startTime > 25:
                break

            # print("KB with removed duplicates: ")
            # FOLResolution.printSentences(kbWithRemovedDuplicates)
            if len(kbWithRemovedDuplicates) == 0:
                break

            differenceBtwKB = self.difference(kb, kbWithRemovedDuplicates)
            if time.time() - self.startTime > 25:
                break

            # print("Difference between KB and KB with removed duplicates: ")
            # FOLResolution.printSentences(differenceBtwKB)
            if len(differenceBtwKB) == 0:
                break

            kb += differenceBtwKB
            kb.sort(key = lambda x: len(x.predicates))
            # print("Sorted KB: ")
            # FOLResolution.printSentences(kb)

        return False


def main():
    fol = FOLResolution()
    fol.processInput('input.txt')
    fol.writeOutput()

if __name__ == "__main__":
    main()
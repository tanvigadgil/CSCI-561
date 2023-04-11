def convertToCNF(sentence):
    index = sentence.find("=>")

    if index == -1:
        pass
    else:
        predicate = sentence[:index]
        conclusion = sentence[index + 2:]
        # TODO: Do I need to strip the spaces from the predicate and conclusion?
        # TODO: Negation operations on predicate
        
        fact = predicate + '|' + conclusion

        print(fact)
        return fact


if __name__ == "__main__":
    # Read input file
    file = open('input1.txt', 'r')
    Lines = file.readlines()

    query = Lines[0]
    print(query)
    noOfSentences = int(Lines[1])
    print(noOfSentences)

    # Create a list of sentences
    listOfSentences = list()
    for i in range(2, noOfSentences + 2):
        listOfSentences.append(Lines[i].strip('\n'))
    print(listOfSentences)

    for sentence in listOfSentences:
        convertToCNF(sentence)
import sys
import math
import re

filenames = []

for i in range(1, len(sys.argv)):
    filenames += [sys.argv[i]]

model = open(sys.argv[1])
text = open(sys.argv[2])

genreList = ['soap', 'novel', 'info']
wordDict = {} # {"word" : {genre : P(F|G), genre : P(F|G), genre : P(F|G)}}
wordCount = {} # {"word" : #occurrences, ...}
priors = [0, 0, 0]
probs = {'soap' : 0, 'novel' : 0, 'info' : 0}
# wordProbs = {}
best = {}
totalProb = 0


for line in model:
    newLine = line.split()

    newLine[1] = newLine[1].rstrip()
    newLine[3] = float(newLine[3])
    if newLine[1] == 'PRIOR':
        priors[genreList.index(newLine[0])] = newLine[3]
    elif newLine[1] in wordDict:
        wordDict[newLine[1]][newLine[0]] = newLine[3]
    else:
        wordDict[newLine[1]] = {newLine[0] : newLine[3]}

allWords = list(wordDict)

for line in text:
    newLine = line.lower().split()
    j = 0
    while j < len(newLine):
        match = re.match(r'[a-z0-9]+$|[a-z0-9]*\-*[a-z0-9]*$', newLine[j])
        if not match:
            del newLine[j]
        elif newLine[j] not in allWords:
            del newLine[j]
        elif newLine[j] not in wordCount:
            wordCount[newLine[j]] = 1
            j += 1
        else:
            wordCount[newLine[j]] += 1
            j += 1
#     for word in newLine:
#         if word in allWords:
#             if word in wordCount:
#                 wordCount[word] += 1
#             else:
#                 wordCount[word] = 1
                
#         else:
#             print(word, end=' ========== ')
# print()

wordList = list(wordCount)
for word in wordList:
    for Genre in genreList:
        probs[Genre] += wordCount[word]*wordDict[word][Genre]

        # if word in wordProbs:
        #     wordProbs[word][Genre] = wordDict[word][Genre]# + priors[genreList.index(Genre)]
        # else:
        #     wordProbs[word] = {Genre : wordDict[word][Genre] + priors[genreList.index(Genre)]}
        #     wordProbs[word][genreList[(genreList.index(Genre) + 1) % 3]] = 0
        #     wordProbs[word][genreList[(genreList.index(Genre) + 2) % 3]] = 0

for genre in range(3):
    probs[genreList[genre]] += priors[genre]


def big(dic):
    if len(dic) == 0:
        print("Idiot.")
        return
    lis = list(dic)
    size = dic[lis[0]]
    string = lis[0]
    for entry in lis:
        if size < dic[entry]:
            size = dic[entry]
            string = entry
    return string

print('b)')
Genre = big(probs)
print(Genre)

print('c)')
for g in genreList:
    print(str(g) + ' : ' + str(probs[g]))

def getBigs(diction, num=15):
    kv = diction.keys()
    ls = []
    for key in kv:
        if len(ls) == 0:
            ls += [key]
        else:
            l=0
            while l < len(ls):
                if diction[ls[l]] < diction[key]:
                    ls[l:l] = [key]
                    break
                elif l+1 == len(ls):
                    ls[l+1:l+1] = [key]
                    break
                else:
                    l += 1
    return(ls[:15])

for genre in genreList:
    totalProb += probs[genre]

theVeryBest = {}
# print(probs)
PROB = 0
for word in wordList:
    PROB += (math.e ** wordDict[word][Genre]) * wordCount[word]


# print('PROB: ' + str(PROB))
# print('e^probs[Genre]: ' + str(math.e**probs[Genre]))

for feature in wordList:
    # PROB = 0
    # for genre in genreList:
    #     PROB += (math.e ** wordDict[feature][genre])
    imp = wordCount[feature]*(math.e ** wordDict[feature][Genre])
    # print(feature + ': ' + str(imp))
    
    best[feature] = math.log(imp/PROB)

    # wordProbs[feature] = math.log(wordCount[feature])+wordDict[feature][Genre] # sets val for each word to c(F)*P(F|G)
    # for genre in genreList:
    #     if genre == Genre:
    #         wordProbs[feature] += wordDict[feature][genre]
    #     else:
    #         wordProbs[feature] -= wordDict[feature][genre]


theVeryBest = getBigs(best)

# print('word count of "lost": ' + str(wordCount['lost']))
# print('best[\'lost\']: ' + str(best['lost']), end='IS THIS LOSS?\n')
# print(theVeryBest)

for good in range(len(theVeryBest)):
    print(str(good) + ' : ' + theVeryBest[good] + ' ' + str(best[theVeryBest[good]]))

# print(best)
# print(wordList)
# print(wordCount)
# print('soap almost: ' + str(wordDict['almost']['soap']))


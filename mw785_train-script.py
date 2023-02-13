import sys
import re
import math
import io

files = []
filenames = []
fileProp = {'soap' : 0, 'novel' : 0, 'info' : 0}
genreList = ['soap', 'novel', 'info']
gpriors = {'soap' : 0, 'novel' : 0, 'info' : 0}
output = ''

for i in range(1, len(sys.argv)):
    filenames += [sys.argv[i]]
    files += [open(sys.argv[i])]

stopwordFile = open("stopwords.txt")
stopwords = []
for line in stopwordFile:
    stopwords += [line.rstrip()]

def addToWords(genre, word, words):
    newWords = words
    if word in newWords:
        newWords[word][genreList[genre]] += 1
    else:
        newWords[word] = {genreList[genre] : 1}
        genre += 1
        genre %= 3
        newWords[word][genreList[genre]] = 0
        genre += 1
        genre %= 3
        newWords[word][genreList[genre]] = 0
    return newWords

wordDict = {} # {"word" : {genre : count, genre : count, genre : count}}
wordCounts = {"soap" : 0, "novel" : 0, "info" : 0} # pretty self-explanatory
wordProbs = {} # like wordDict, but instead of the counts of that word in each genre, has the log prob of the word - P(F | G)

# for each file: labels the genre of the file (increments corresp proportion); tokenizes words as groups of word characters
for i in range(len(files)):
    genre = -1
    if 'soap' in filenames[i]: # if the corresp filename contains "soap", "novel", or "info", add to corresp dict
        genre = 0
        fileProp['soap'] += 1
    elif 'novel' in filenames[i]:
        genre = 1
        fileProp['novel'] += 1
    elif 'info' in filenames[i]:
        genre = 2
        fileProp['info'] += 1
    
    text = files[i].read()
    text = text.lower()
    text = text.split()
    j = 0
    while j < len(text):
        match = re.match(r'[a-z0-9]+$|[a-z0-9]*\-*[a-z0-9]*$', text[j])
        if not match:
            del text[j]
        elif text[j] in stopwords:
            del text[j]
        else:
            wordDict = addToWords(genre, text[j], wordDict)
            wordCounts[genreList[genre]] += 1
            j += 1

# removes any word with less than 10 overall occurences from wordDict and machine and does add-one smoothing
wordList = list(wordDict)
for word in wordList:
    occurences = [0, 0, 0]
    total = 0
    for genre in range(3):
        occurences[genre] += wordDict[word][genreList[genre]]
        total += wordDict[word][genreList[genre]]
    if total < 10:
        del wordDict[word]
        for genre in range(3):
            wordCounts[genreList[genre]] -= occurences[genre]

# SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING SMOOTHING
wordList = list(wordDict)
for word in wordList:
    for genre in range(3):
        wordDict[word][genreList[genre]] += 1
        wordCounts[genreList[genre]] += 1

# sets genre priors, add to output
for Genre in genreList:
    gpriors[Genre] = math.log(fileProp[Genre]/len(filenames))
for Genre in gpriors:
    output += Genre + ' PRIOR : '  + str(gpriors[Genre]) + '\n'

# look at wordDict[word][genreList[genre]] for P(F | G) = c(F in G)/c(G)
for word in wordList:
    wordProbs[word] = {genreList[0] : math.log(wordDict[word][genreList[0]]/wordCounts[genreList[0]])}
    for genre in range(1, 3):
        wordProbs[word][genreList[genre]] = math.log(wordDict[word][genreList[genre]]/wordCounts[genreList[genre]])

# print('almost counts: ' + str(wordDict['almost'])) # should be {2, 38, 4} (after smoothing)
# print('almost probs: ' + str(wordProbs['almost']))
# print('soap counts: ' + str(wordCounts['soap'])) # should be 3076
# count1 = 0
# count2 = 0
# for genre in genreList:
#     for word in wordList:
#         count1 += wordDict[word][genre]
#     count2+= wordCounts[genre]
# print('in wordDict: ' + str(count1))
# print('in wordCounts: ' + str(count2))

for word in wordList:
    for genre in range(3):
        output += genreList[genre] + ' ' + word + ' : ' + str(wordProbs[word][genreList[genre]]) + '\n'

# print(output)

model = open('nb.params', 'w')
model.write(output)
model.close()



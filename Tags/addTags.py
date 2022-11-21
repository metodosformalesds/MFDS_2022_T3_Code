def getKeywords(id):
    keywords = []
    with open('keywords.csv', 'r', encoding='utf-8') as f:
        for line in f:
            if str(id) in line:
                keywords.append(line.split('|')[1])
    return keywords


def appendKeywords():
    with open('ENudemy2.csv', 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        f.seek(0)

        for line in lines:
            #get the id
            id = line.split("|")[0]
            #call getKeywords(id)
            keywords = getKeywords(id)
            f.write(line.rstrip('\n') + '|' + str(keywords) + '\n')
            f.truncate()

appendKeywords()
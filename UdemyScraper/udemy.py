### FLUJO ###
# 1.- Se obtiene una lista de cursos y se guarda en udemy.csv
# 2.- Se crea un archivo udemy3 el cual contiene el id y descripcion de cada curso
# 3.- Para extrar las etiquetas se utiliza un archivo de Jupyter Notebooks, el cual
# crea el archivo keywords.csv que contiene 10 etiquetas de cada curso.
# 4.- Se le añaden las etiquetas correspondientes al archivo original (udemy.csv)

import requests
# Get id, title, rating, price, language, url, instructor, description

# Categories: Fullstack, Data Science, Backend, Frontend, Languages, Cybersecurity


def main():
    pageSize = str(100)
    pageNumber = str(1)
    search = "frontend"
    category = "frontend"  # Esta no afecta en la busqueda
    language = "es"  # es = español, en = english

    results = getCourses(pageNumber, pageSize, search, language)

    data = results.json()
    getCount(data)
    IdAndDescriptionCSV(data)
    saveResultsCSV(data, category, language)


def headers(url):
    payload = {}
    headers = {
        'Authorization': 'Basic N3NZNFl1OFhmY2M4ZXMxWmNsVkdqUkY2czhyaUh3bVY3NnRWcnQyOTpxUkphVFozaTlJVHZFeXV0MFBhc1l4eW5Ha1RWNmdYZ3lTUG5ya2wyZnZOeTdES1o0SUNaVTR4aGFBYzhudDJJSmlFaTFkVGhiRk5FTXp3Yk1SQmpwTjFkQzBmUmRybXQ2VXFreDdtaVBHSVNVUzdMWTJIcVVDV1V2bUR5VjBTOQ==',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=utf-8',
        'Cookie': 'evi="3@FSm5gHp5AmLh1TyDhXX6ynvvsnwiefE9tf7nDETV3Ge6xaaVDI4RrRU3"; ud_rule_vars="eJx9jcsKwyAUBX8luG0Trq_G-C0BMXpNpaVSNdmE_HsDbaGrbg9nZjZSbZ6xojdrLLGmrIepVygEBk-d4AgD94xTMcnAhXRUaJfSLSLRDdlGEmIu9c0abyuOxz4SBoy1lLYgGpCa9VqojikKPTsBaICRnI_X3R5oTYu7mpptCNGZkpbs0Kw2RzvdP7aUZ_uI7gfK-Fyw_C8OHYOL7NW3uJP9Ba58R9Y=:1oqpF7:15xhJmK5v6SB4k6pP10bcXY0TDs"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response
    else:
        print("Error: ", str(response.status_code))
        return None


def getCourses(pageNumber, pageSize, search, language):
    url = "https://www.udemy.com/api-2.0/courses/?page=" + pageNumber + "&page_size=" + pageSize + "&search=" + search + \
        "&category=Development&price=price-paid&is_affiliate_agreed=True&is_deals_agreed=True&language=" + \
        language + "&instructional_level=all&ordering=relevance&ratings=4.0"
    data = headers(url)

    return data


def getCourseRating(id):
    url2 = "https://www.udemy.com/api-2.0/courses/" + \
        str(id) + "/?fields[course]=@all"
    indData = headers(url2)

    rating = indData.json()['rating']

    return rating


def getCourseDescription(id):
    url3 = "https://www.udemy.com/api-2.0/courses/" + \
        str(id) + "/?fields[course]=@all"
    Data3 = headers(url3)

    # si la description contiene \n remplazarlos, de lo contrario guardarlo tal como viene
    if '\n' in Data3.json()['description']:
        description = Data3.json()['description'].replace('\n', '')
    else:
        description = Data3.json()['description']

    return description


def getCount(data):
    count = data['count']
    return count


def IdAndDescriptionCSV(data):
    with open('udemy3.csv', 'r+', encoding='utf-8') as f:
        for course in data['results']:
            description = getCourseDescription(course['id'])
            f.write(str(course['id']) + "|" + description + "\n")


def saveResultsCSV(data, category, language):
    with open('udemy2.csv', 'r+', encoding='utf-8') as f:
        if f.readline().startswith("id"):
            for course in data['results']:
                rating = getCourseRating(course['id'])
                description = getCourseDescription(course['id'])
                f.write(str(course['id']) + "|" + course['title'] + "|"
                        + str(course['price_detail']['amount']) + "|" + course['url'] +
                        "|" + category + "|" + str(round(rating, 1)) + "|"
                        + language + "|" + course['visible_instructors'][0]['display_name'] + '|' + description + "\n")
        else:
            f.write("id|title|price|url|category|rating|language|instructor|tags\n")
            for course in data['results']:
                rating = getCourseRating(course['id'])
                description = getCourseDescription(course['id'])
                f.write(str(course['id']) + "|" + course['title'] + "|"
                        + str(course['price_detail']['amount']) + "|" + course['url'] +
                        "|" + category + "|" + str(round(rating, 1)) + "|"
                        + language + "|" + course['visible_instructors'][0]['display_name'] + '|' + description + "\n")


main()

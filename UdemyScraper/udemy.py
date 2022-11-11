import requests

#Categories: Web Development, Data Science, Mobile Development, Programming Languages, Game Development, Database Design & Development
#Software Testing, Software Engineering, Software Development Tools, No-Code Development

def main():
  pageSize = str(10)
  pageNumber = str(1)
  search = "sql"
  category = "bases de datos"     #Esta no afecta en la busqueda
  language = "es"     #es = español, en = english
  level = "beginner"  #beginner, intermediate, expert

  results = getCourseDetails(pageNumber, pageSize, search, language, level)

  data = results.json()
  getCount(data)
  saveResultsCSV(data, category)
  

def headers(url):
  payload={}
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

def getCourseDetails(pageNumber, pageSize, search, language, level):
  url = "https://www.udemy.com/api-2.0/courses/?page=" + pageNumber + "&page_size=" + pageSize + "&search=" + search + "&category=Development&price=price-paid&is_affiliate_agreed=True&is_deals_agreed=True&language=" + language + "&instructional_level=" + level + "&ordering=relevance"
  data = headers(url)

  return data

def getCount(data):
  count = data['count']
  return count

def saveResultsCSV(data, category):
  with open('udemy.csv', 'r+') as f:
    if f.readline().startswith("id"):
      for course in data['results']:
        f.write(str(course['id']) + ";" + course['title'] + ";" + str(course['price_detail']['amount']) + ";" + course['url'] +  ";" + category + "\n")
    else:
      f.write("id;title;price;url\n")
      for course in data['results']:
        f.write(str(course['id']) + ";" + course['title'] + ";" + str(course['price_detail']['amount']) + ";" + course['url'] +  ";" + category + "\n")
  
main()






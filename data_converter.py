import json
import random

# # JSON 파일 읽기
# data = {}
# with open('_youtube_data.json', 'r', encoding="utf-8") as file:
#     data = json.load(file)
    
# print(data["contents"][0])

# new_data = []
# for i, item in enumerate(data["contents"]):
#   content = {}
#   content["id"] = i
#   content["url"] = item["URL"]
#   words = item["서브 키워드"].split(",")
#   words.append(item["메인 키워드"])
#   content["keywords"] = words
#   new_data.append(content)

# with open('youtube_data.json','w', encoding="utf-8") as file:
#    json.dump(new_data, file,ensure_ascii=False)
   
   
def get_youtube_url(question): 
    question = question.replace(" ","")
    question = question.lower()
    youtube_data = []
    with open('youtube_data.json', 'r', encoding="utf-8") as file:
        youtube_data = json.load(file)
        
    urls = []
    for content in youtube_data:
        keywords = content["keywords"]
        for keyword in keywords:
            keyword = keyword.replace(" ","")
            keyword = keyword.lower()
            if keyword in question:
                
                key = keyword+str(content["id"])
                urls.append(content["url"])

                break
    if len(urls) > 0:
        url = random.sample(urls, 1)[0]
    else:
        url = ""
    return url



link = get_youtube_url("쿠팡")
if link :
  print(link)
else:
  print("업서")
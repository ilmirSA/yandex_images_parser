import json
#
with open('result.json','r',encoding='utf-8')as file:
    data=json.load(file)
    print(data)




# with open('j.txt', 'r') as f:
#         print(f.readlines())

# import json
# with open('result.json', 'r') as f:
#     data = json.load(f)
#     print(len(data))

# with open('processed_images.txt', 'r') as f:
#     #processed_files = [line.strip() for line in f.readlines()]
#     for i in f.readlines():
#         print(i.strip())
# for i in data:
#     print(i['image_link'])


#     print(i)


# response=requests.get('https://yandex.eu/showcaptcha?mt=FDE0C47414C61F8BA01A504DD8DBC612EC32790476310766DC45F5DA3228FF264DB0CB9B7F1276E96723CE9C0EE74C890FDF0A6C429654F17BC751A0DF3B918F1A1EBF9730118113952881935BEF57A543FD5A30B21C9F073692&retpath=aHR0cHM6Ly95YW5kZXguZXUvaW1hZ2VzL3NlYXJjaD9ycHQ9aW1hZ2V2aWV3_1ea1e6efe65647b014af470227cef552&t=3/1685085905/1970662cb6ccd4519b550f42dd868357&u=ea522a22-feffd176-313cdd13-254f465a&s=6e8b6195e1908be40f53cbba5001c04b')
# print(response.text)

# import json
# import os
#
# import requests
# from bs4 import BeautifulSoup
#
#
# def read_json_file(filename):
#     with open(filename, 'r') as file:
#         for line in file:
#             data = json.loads(line)
#             yield {'img': data['img'], 'url': data['url']}
#
#
#
#
# def text_and_url_extraction(img_name, img_url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
#
#     url = f'https://yandex.ru/images/search?rpt=imageview&url={img_url}'
#
#     response = requests.get(url, headers=headers)
#     print(response.text)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     main_url_image = soup.find('img', class_='CbirPreview-Image').get('src')
#     links_text = [{link.get('href'): link.text} for link in soup.find_all('a', class_='Link Link_view_default')]
#
#     result = {
#         'image_name': img_name,
#         'image_link': main_url_image,
#         'image_text': links_text,
#     }
#
#     return result
#
#
# def main():
#     for data in read_json_file('dataset_dict.json'):
#
#         if not os.path.exists('result.json'):
#             dataset = []
#             with open('result.json', 'w') as f:
#                 json.dump(dataset, f)
#
#         result = text_and_url_extraction(data['img'], data['img'])
#
#         with open('result.json', 'r') as f:
#             data = json.load(f)
#             data.append(result)
#         with open('result.json', 'w') as f:
#             json.dump(data, f)
#
#
# if __name__ == '__main__':
#     main()

# -------------------------------------------------------

# In[15]:

#
# start_url = 1180
# end_url = 1200
#
# # In[17]:
#
#
# for i in range(start_url, end_url):
#     try:
#         data_extractor = text_and_url_extraction(url_list[i])
#         if data_extractor == 0:
#             print('Proxy list is empty')
#             break
#         text_from_img = data_extractor[0]
#         urls_from_img = data_extractor[1]
#     except:
#         with open('url_errors.txt', 'a', encoding='utf-8') as errors:
#             errors.write(f'{i} {url_list[i]} {img_dict.get(url_list[i])}\n')
#         print(f'{i} is failed')
#         time.sleep(180)
#         continue
#     else:
#         json_text_dict = {'img': img_dict.get(url_list[i]),
#                           'img_text': text_from_img,
#                           'url': url_list[i],
#                           'urls': urls_from_img}
#         with open('text_description.json', 'a', encoding='utf-8') as texting:
#             json.dump(json_text_dict, texting)
#             texting.write('\n')
#         print(f'{i} is done!')
#
# # In[19]:
#
#
# with open('text_description.json', 'r', encoding='utf-8') as json_text_file:
#     image_text = {}
#     for line in json_text_file:
#         image_text[json.loads(line)['img']] = json.loads(line)['img_text']
#
# # In[20]:
#
#
# with open('url_errors.txt', 'r', encoding='utf-8') as errors:
#     dict_list = [(line.split(' ')[0], line.split(' ')[1], line.split(' ')[2].replace('\n', '')) for line in
#                  errors.readlines()]
#
# # In[ ]:
#
#
# i = len(dict_list) - 1
# while i >= 0:
#     try:
#         data_extractor = text_and_url_extraction(dict_list[i][1])
#         text_from_img = data_extractor[0]
#         urls_from_img = data_extractor[1]
#     except:
#         print(f'{dict_list[i][0]} is failed')
#     else:
#         json_text_dict = {'img': dict_list[i][2],
#                           'img_text': text_from_img,
#                           'url': dict_list[i][1],
#                           'urls': urls_from_img}
#         with open('text_description.json', 'a', encoding='utf-8') as texting:
#             json.dump(json_text_dict, texting)
#             texting.write('\n')
#         del dict_list[i]
#         i -= 1
#         with open('url_errors.txt', 'w', encoding='utf-8') as errors:
#             for j in range(len(dict_list)):
#                 errors.write(f'{dict_list[j][0]} {dict_list[j][1]} {dict_list[j][2]}\n')
#         print(f'{dict_list[i][0]} is done!')
#     i -= 1

# In[ ]:

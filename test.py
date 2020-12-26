import requests

Base = 'http://127.0.0.1:5000/'


# response = requests.put(Base + 'tweet/1', data={'content':'tweet 2', 'comments':1888, 'retweets':'5', 'likes':152})
# print(response.json())
# input()
response = requests.delete(Base + "tweet/1")

response = requests.get(Base + 'tweet/1')
print(response.json())

# response = requests.delete(Base + "tweet/1")
# print(response.status_code)
# response = requests.get(Base + 'tweet/1')
# print(response.json())
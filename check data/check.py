import requests
url      = input("Enter the URL : ")
response = requests.get(url)
print(response.text)
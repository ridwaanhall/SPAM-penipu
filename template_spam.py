import requests, random

# enter a url from website form
url = 'change_to_your_url'

'''
headers example
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}
'''
headers = {
    # add headers here, you can use example below
}

loop_value = int(input("number of spam: "))

for loop in range(1, loop_value+1):
    '''
    data_example = {
        'example': 'example',
        'example2': 'example2',
        'example3': 'example3'
    }
    '''
    data = {
        # enter data here
    }
    response = requests.post(url, data=data, headers=headers)
    loop = str(loop).zfill(5)
    print(loop)
    print(response.status_code)
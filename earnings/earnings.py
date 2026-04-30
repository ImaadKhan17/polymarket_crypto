import requests as re




all_earnings = re.get('https://gamma-api.polymarket.com/events', params={
    'tag_id': '1013',
    'closed': False,
    'order':'volume',
    'ascending': False
})

data = all_earnings.json()

for i in data:
    print(i['title'])
    print('Prob')
    for market in i['markets']:
        print(market['outcomePrices'])
        print(market['volume'])

print(len(data))


# print(data[0]['markets'][0]['endDateIso'])
# print(data[0]['markets'][0]['question'])
# print(data[0]['markets'][0]['description'])
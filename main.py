import requests
import time

def get_arrival_time():
    resp = requests.get('https://api-v3.mbta.com/predictions?filter[stop]=place-mispk')
    if resp.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    
    arrival_time = resp.json()['data'][1]['attributes']['arrival_time']
    arrival_time = arrival_time.split('T')[1].split('-')[0]
    return arrival_time

timestamp = time.strftime('%H:%M:%S')
print(timestamp)
print(get_arrival_time())
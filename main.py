import requests
import time
from datetime import datetime

def get_arrival_time():
    resp = requests.get('https://api-v3.mbta.com/predictions?filter[stop]=place-mispk')
    if resp.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    
    trains = resp.json()['data']
    count=0
    while True:
        direction = trains[count]['attributes']['direction_id']
        # 0 for East Bound 1 for West Bound
        if direction is 0:
            print(count)
            arrival_time = resp.json()['data'][count]['attributes']['arrival_time']
            break
        count+=1
    
    arrival_time = arrival_time.split('T')[1].split('-')[0]
    return arrival_time


def get_time_until_arrival():
    now = time.strftime('%H:%M:%S')
    now = datetime.strptime(now, '%H:%M:%S')
    arrival_time = get_arrival_time()
    arrival_time = datetime.strptime(arrival_time, '%H:%M:%S')
    time_until_arrival = arrival_time - now
    time_until_arrival.seconds/60
    return time_until_arrival

print(get_time_until_arrival())
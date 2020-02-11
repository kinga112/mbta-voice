import requests
import time
from datetime import datetime

def get_time_until_arrival():
    resp = requests.get('https://api-v3.mbta.com/predictions?filter[stop]=place-mispk')
    mbta = resp.json()['data']
    count=0
    while True:
        direction = mbta[count]['attributes']['direction_id']
        # 1 for East Bound, 0 for West Bound
        if direction is 1:
            arrival_time = mbta[count]['attributes']['arrival_time']
            arrival_time = arrival_time.split('T')[1].split('-')[0]
            now = time.strftime('%H:%M:%S')
            now = datetime.strptime(now, '%H:%M:%S')
            arrival_time = datetime.strptime(arrival_time, '%H:%M:%S')
            time_until_arrival = arrival_time - now
            time_until_arrival.seconds/60
            if 'day' in str(time_until_arrival):
                arrival_time = ''
            else:
                break
        count+=1
    return time_until_arrival


print(get_time_until_arrival())
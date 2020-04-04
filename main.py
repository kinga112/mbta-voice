import json
import requests
import time

from datetime import datetime
from flask import Flask


def get_time_until_arrival():
    # Stop id: place-mispk
    resp = requests.get('https://api-v3.mbta.com/predictions?filter[stop]=place-mispk')
    mbta = resp.json()['data']
    count = 0
    under_30sec = False
    running = True
    while True:
        try:
            direction = mbta[count]['attributes']['direction_id']
        except:
            running = False
            minutes = '00'
            seconds = '00'
            break
        # 1 for East Bound, 0 for West Bound
        if direction == 0 and running is True:
            # string of arrival time in full format
            arrival_time = mbta[count]['attributes']['arrival_time']
            # split string into only arrival time in 24 hour format
            arrival_time = arrival_time.split('T')[1].split('-')[0]
            # get time right now
            now = time.strftime('%H:%M:%S')
            # convert to datetime
            now = datetime.strptime(now, '%H:%M:%S')
            # convert to datetime
            arrival_time = datetime.strptime(arrival_time, '%H:%M:%S')
            # can subtract datetimes to get time until arrival
            time_until_arrival = arrival_time - now
            time_until_arrival.seconds/60
            # split string to get minutes and seconds
            time_until_arrival = f'{time_until_arrival}'
            minutes = time_until_arrival[2:4]
            seconds = time_until_arrival[5:7]
            # print('sec after int', type(int(seconds)))
            # when train just arrives and leaves, it prints wierd
            # format of data that isnt useful so I ignore that one
            # and get time until next train
            if 'day' in str(time_until_arrival):
                arrival_time = ''
            # sends next train if current one comes
            # in less than 30 seconds
            elif int(minutes) == 0 and int(seconds) < 30:
                print('seconds 0:', seconds[0])
                under_30sec == True
                arrival_time = ''
            else:
                break
        count += 1
    return minutes, seconds, under_30sec, running


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST', 'PUT'])
def main():
    minutes = get_time_until_arrival()[0]
    seconds = get_time_until_arrival()[1]
    under_30sec = get_time_until_arrival()[2]
    running = get_time_until_arrival()[3]
    # slice starting 0's out of string
    if seconds[0] == '0':
        seconds = seconds[1]
    if minutes[0] == '0':
        minutes = minutes[1]
    if minutes == '0':
        time_string = f'Next train in {seconds} seconds'
    if under_30sec is True:
        time_string = f'Next train comes in less than 30 seconds. Following train coming in {minutes} minutes and {seconds} seconds'
    if running is False:
        time_string = f'MBTA is closed until the morning.'
    else:
        time_string = f'Next train in {minutes} minutes and {seconds} seconds'    
    response = {
        "expectUserResponse": False,
        "finalResponse": {
            "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                            'ssml': f'<speak>{time_string}!</speak>'
                            }
                        }
                    ]
                }
            }
        }

    response_text = json.dumps(response, indent=2, sort_keys=True)
    return response_text, 200


app.run()

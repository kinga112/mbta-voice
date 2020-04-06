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
    running = True
    under_1min = False

    while True:
        # checks if MBTA is running if dict has info
        try:
            direction = mbta[count]['attributes']['direction_id']
        except:
            running = False
            minutes = '00'
            seconds = '00'
            break

        # 1 for East Bound, 0 for West Bound
        if direction == 1 and running is True:
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
            # when train just arrives and leaves, it prints wierd
            # format of data that isnt useful so I ignore that one
            # and get time until next train
            if 'day' in str(time_until_arrival):
                arrival_time = ''
            # sends next train if current one comes
            # in less than 30 seconds
            if int(minutes) < 1:
                under_1min = True
            else:
                break
        count += 1
    return minutes, seconds, running, under_1min


app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def main():
    minutes = get_time_until_arrival()[0]
    seconds = get_time_until_arrival()[1]
    running = get_time_until_arrival()[2]
    under_1min = get_time_until_arrival()[3]
    
    # slice starting 0's out of string
    if seconds[0] == '0':
        seconds = seconds[1]
    if minutes[0] == '0':
        minutes = minutes[1]
    
    # Assistant answers accordingly
    time_string = f'Next train arrives in {minutes} minutes and {seconds} seconds'
    if under_1min is True:
        time_string = f'Next train arrives in less than 1 minute. Following train arrives in {minutes} minutes and {seconds} seconds'
    if running is False:
        time_string = f'MBTA is closed until the morning'

    response = {
        "expectUserResponse": False,
        "finalResponse": {
            "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                            'ssml': f'<speak>{time_string}</speak>'
                            }
                        }
                    ]
                }
            }
        }

    response_text = json.dumps(response, indent=2, sort_keys=True)
    return response_text, 200


app.run()

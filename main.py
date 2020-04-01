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
    while True:
        direction = mbta[count]['attributes']['direction_id']
        # 1 for East Bound, 0 for West Bound
        if direction == 0:
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
            else:
                break
        count += 1
    return minutes, seconds


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST', 'PUT'])
def main():
    minutes = get_time_until_arrival()[0]
    seconds = get_time_until_arrival()[1]
    response = {
        'expectUserResponse': True,
        'expectedInputs': [
            {
                'possibleIntents': {'intent': 'actions.intent.TEXT'},
                'inputPrompt': {
                    'richInitialPrompt': {
                        'items': [
                            {
                                'simpleResponse': {
                                    'ssml': f'<speak>Next train in {minutes} minutes and {seconds} seconds?</speak>'
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
    response_text = json.dumps(response, indent=2, sort_keys=True)
    return response_text, 200


app.run()

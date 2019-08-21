#!/usr/bin/env python3
import json
from datetime import datetime
from urllib.parse import urlparse

LOG_FILE = 'app.log'
RESULT_FILE = 'our_clients.txt'


def read_log_file():
    try:
        with open(LOG_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File with logs was not found")
        exit(2)


def parse_log(data):
    user_activity = dict()

    for log in data.get('logs'):
        domain_name_ref = urlparse(log.get('document.referer')).netloc

        client = log.get('client_id')

        if client not in user_activity.keys():
            user_activity[client] = [(log.get('document.location'), domain_name_ref)]
        else:
            user_activity[client].append((log.get('document.location'), domain_name_ref))

    return user_activity


def main(user_activity):
    users = list()

    for user in user_activity:
        for i, activity in enumerate(user_activity[user]):
            if activity[0] == 'https://shop.com/checkout':
                for activity2 in user_activity[user][:i][::-1]:
                    if ('theirs1.com' or 'theirs2.com') in activity2[1]:
                        break
                    if 'ours.com' in activity2[1]:
                        users.append(user)
                        break

    return users


def write_result(results):
    with open(RESULT_FILE, 'a') as file:
        for res in results:
            file.write(res + '\n')


if __name__ == '__main__':
    data = read_log_file()

    user_activity = parse_log(data)

    result_list = main(user_activity)

    write_result(result_list)

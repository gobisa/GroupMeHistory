import os
import json
import requests
import sqlite3

try:
    GROUPME_ACCESS_TOKEN = os.environ['GROUPME_ACCESS_TOKEN']
    GROUPME_GROUP_ID = os.environ['GROUPME_GROUP_ID']
except KeyError as error:
    print("Couldn't find GROUPME_ACCESS_TOKEN or GROUPME_GROUP_ID environment variables. " + str(error))
    exit()

#static url components
base_url = 'https://api.groupme.com/v3'
group_url_postfix = '/groups/{}/messages'.format(GROUPME_GROUP_ID)
full_url = base_url + group_url_postfix

#set parameters
limit = 100
url_parameters = {
    'token': GROUPME_ACCESS_TOKEN,
    'limit': limit,
}

sender_ids = set()

count = 0

conn = sqlite3.connect("chat.db")
c = conn.cursor()

while True:
    r = requests.get(full_url, params=url_parameters)
    if r.status_code == 304:
        print("End of messages reached.")
        break

    try:
        data = json.loads(r.text)
    except json.decoder.JSONDecodeError as error:
        print("JSON had error: " + str(error))
        print("JSON was passed data: " + r.text)
        break 

    count += limit
    if count % 1000 == 0:
        print("retrieved {} of {} messages".format(count, data["response"]["count"]))

    last_message_id = data['response']['messages'][-1]['id']
    url_parameters["before_id"] = last_message_id

    for message in data["response"]["messages"]:
        if message["sender_id"] not in sender_ids:
            sender_ids.add(message["sender_id"])
            c.execute('''
                      INSERT INTO users(sender_id, username)
                      VALUES(?, ?)
                      ''',
                      (message["sender_id"], message["name"]))

        if message["attachments"] and message["attachments"][0]["type"] == "image":
            c.execute('''
                      INSERT INTO
                      messages(message_id, sender_id, text_contents, num_likes, attachment_url)
                      VALUES(?, ?, ?, ?, ?)
                      ''',
                      (message["id"], message["sender_id"],
                       message["text"],
                       len(message["favorited_by"]),
                       message["attachments"][0]["url"]))
        else:
            c.execute('''
                      INSERT INTO
                      messages(message_id, sender_id, text_contents, num_likes)
                      VALUES(?, ?, ?, ?)
                      ''',
                      (message["id"], message["sender_id"],
                       message["text"],
                       len(message["favorited_by"])))

conn.commit()
conn.close()

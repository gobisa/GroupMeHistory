import requests
import os.path
import sqlite3
import urllib3

# Squash SSL authentication warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

working_dir = os.getcwd()
images = os.path.join(working_dir, "images")
try:
    os.mkdir(images)
except OSError:
    print("Cannot create image directory at " + working_dir)
else:
    print("Image directory created")

# Load DB
conn = sqlite3.connect('/Users/conor/GroupMeHistory/chat.db')
c = conn.cursor()

# Retrieve the URLs that are hosted by groupme
results = c.execute("SELECT * from messages where attachment_url is not null and attachment_url like '%i.groupme.com%'")

printed = 0

# Retreive file names and download new files
for rnum, row in enumerate(results):
    URL = row[4]
    file_name = ''
    if 'jpeg'  in URL:
        temp = URL.split(".jpeg.", 1)
        file_name = temp[1] + '.jpeg'
    elif 'gif' in URL:
        temp = URL.split(".gif.", 1)
        file_name = temp[1] + '.gif'
    elif 'png' in URL:
        temp = URL.split(".png.", 1)
        file_name = temp[1] + '.png'

    with open(os.path.join(images, file_name), 'wb') as f:
        resp = requests.get(URL, verify=False)

        if not os.path.exists(file_name):
            printed += 1
            print(str(rnum) + ": Writing " + file_name)
            f.write(resp.content)
        else:
            print("File already downloaded")
print("Saved " + str(printed) + " files to " + images)

from google_play_scraper import app
from datetime import datetime, timedelta
import json
import os


def info(playstore):
    # today's date
    today = datetime.today().date()
    
    target = datetime.strptime(f"Dec 31, {today.year}", "%b %d, %Y").date()
    
    # convert date string to datetime object
    date_object = datetime.strptime(playstore['released'], "%b %d, %Y").date()

    # Convert the date object to a datetime object and get the timestamp
    released_timestamp = int(datetime.combine(date_object, datetime.min.time()).timestamp())
    
    # convert timestamp to datetime object
    dt_object = datetime.fromtimestamp(playstore['updated'])
    
    updated = dt_object.strftime("%b %d, %Y")
    
    # calculate the number of days between today and the date
    delta = today - date_object
    pr = target - date_object
    
    rate = playstore['realInstalls']/delta.days

    json = {}
    json['title'] = playstore['title']
    json['version'] = playstore['version']
    json['summary'] = playstore['summary']
    json['id'] = playstore['appId']
    json['installs'] = playstore['realInstalls']
    json['rate'] = round(rate, 2)
    json['released'] = playstore['released']
    json['releasedTimestamp'] = released_timestamp
    json['updated'] = updated
    json['updatedTimestamp'] = playstore['updated']
    json['projection'] = int(pr.days * rate)
    json['year'] = today.year
    json['icon'] = playstore['icon']
    json['header'] = playstore['headerImage']
    json['genre'] = playstore['genre']
    
    return json

apps = ['com.fbiego.chronos', 'com.fbiego.esp32.ota', 'com.fbiego.tweet']

output = {}
header = '''
# google-play-scraper
 Monitoring Google Play app stats

### apps
'''

# folder_path = "apps"

# if not os.path.exists(folder_path):
#     os.mkdir(folder_path)

file = open('README.md', 'w')
file.write(header)
file.write('| Icon | Name | Version | Installs | Av. Installs Daily | \n')
file.write('| -- | -- | -- | -- | -- | \n')
for a in apps:
 ap = app(a)
 output[a] = info(ap)
    #  file_name = a + ".txt"
    #  file_path = os.path.join(folder_path, file_name)
    #  
    #  with open(file_path, "a") as f:
    #      f.write("" + str(int(datetime.now().timestamp())) + "," + str(output[a]['installs']) + "," + str(output[a]['rate']) + "," + str(output[a]['projection']) + "\n")
 file.write("| <a href='https://play.google.com/store/apps/details?id=" + ap['appId'] + "'><img alt='Get it on Google Play' height=\"50px\" src='" + ap['icon'] + "'/></a> |  " + ap['title'] + " | v" + ap['version'] + " | " + str(ap['realInstalls']) + " | " + str(info(ap)['rate']) + " | \n")

file.close()

with open("console.json", "w") as outfile:
    json.dump(output, outfile, indent=4)
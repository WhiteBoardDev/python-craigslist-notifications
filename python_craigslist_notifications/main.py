"""Usage: main.py CONFIG_FILE

Continually scans craigslist and sends notification via an IFTTT webhook.

Arguments:
  FILE        configuration file

Options:
  -h --help
"""
from craigslist import CraigslistForSale
from tinydb import TinyDB, Query
import requests
import json
from docopt import docopt
import schedule
import time

arguments = docopt(__doc__)
print(arguments)
with open(arguments['CONFIG_FILE'], 'r') as f:
    config = json.load(f)
db = TinyDB(config['database_file'])
listings_table = db.table('listings')
pending_notifications_table = db.table('pending_notifications')
Listing = Query()


def search():
    for search_config in config['scans']['for_sale']:
        print('Scanning ForSale')
        print(search_config)
        for site in search_config['sites']:
            craigslist_query = CraigslistForSale(site=site, category=search_config['category'], filters=search_config['filters'])
            for result in craigslist_query.get_results(sort_by='newest', limit=50):
                print('Web Result')
                print(result)
                if len(listings_table.search(Listing.id == result['id'])) == 0:
                    print('Detected new listing')
                    print(result)
                    listings_table.insert(result)
                    pending_notifications_table.insert(result)


max_notifications_per_run = 10

def notify():
    notifications_sent=0
    for notification in pending_notifications_table.all():
        if(notifications_sent >= max_notifications_per_run):
            print('Max notifications per run met')
            return
        print('Sending Notification')
        print(notification)
        result = requests.post(url=config['ifttt_webhook_url'],
                      json={'value1': notification['name'] + ' ' + str(notification['price']) + ' ' + str(notification['where']),
                            'value2': notification['url']},
                      headers={'Content-Type': 'application/json'})
        print(result.status_code)
        pending_notifications_table.remove(doc_ids=[notification.doc_id])
        notifications_sent += 1


def job():
    search()
    notify()


job()
schedule.every(config['run_every_in_minutes']).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(5)

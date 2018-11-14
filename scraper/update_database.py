import sqlite3
from pprint import pprint
from time import sleep
import sys
from scrape_scripts.ab_scraper import ABScraper
from scrape_scripts.flagey_scraper import FlageyScraper

SCRAPERS = [
    ABScraper(),
    FlageyScraper()
]

def get_event(conn, remote_id, title):
    command = "SELECT * FROM events WHERE remote_id == ? and title == ?"
    return conn.execute(command, (remote_id, title)).fetchall()


def add_new_event(conn, event_title, event_url, remote_id, event_image, event_datetime, event_description, event_price, event_tags, previews):
    command1 = "insert into events (title, remote_id, event_datetime, event_price, event_image_url, event_description, event_url) \
                VALUES (?, ?, ?, ?, ?, ?, ?);"
    cursor = conn.execute(command1, (event_title, str(remote_id), event_datetime, event_price, event_image, event_description, event_url))
    event_id = cursor.lastrowid
    for tag in event_tags:
        add_tag_command = "insert or ignore into tags (tag_name) values (?)"
        conn.execute(add_tag_command, (tag, ))
        tag_id = conn.execute("select tag_id from tags where tag_name == ?", (tag, )).fetchone()[0]
        add_junction_cmd = "insert into event_tags_junction (event_id, tag_id) values (?, ?);"
        conn.execute(add_junction_cmd, (event_id, tag_id))

    for preview_url in previews:
        add_preview_command = "insert or ignore into previews (url) values (?)"
        conn.execute(add_preview_command, (preview_url, ))
        preview_url_id = conn.execute("select preview_id from previews where url == ?", (preview_url, )).fetchone()[0]
        add_junction_cmd = "insert into event_previews_junction (event_id, preview_id) values (?, ?);"
        conn.execute(add_junction_cmd, (event_id, preview_url_id))

    conn.commit()


class DatabaseUpdater:
    def __init__(self):
        self.update_inteval = 60  # In seconds.
        self.should_update = True
        self.conn = sqlite3.connect('database.db')

    def start_update_cycle(self, once=False, results_limit=False):
        while self.should_update:
            log = {'added': 0, 'updated': 0}
            for scraper in SCRAPERS:
                print(f'Scraping {scraper.venue_name}')
                results = scraper.start_scrape(results_limit=results_limit)
                results_counter = 0
                for event_dict in results:
                    results_counter += 1
                    saved_events = get_event(self.conn, event_dict['remote_id'], event_dict['event_title'])
                    if saved_events:
                        # Event exists. Check if anything changed.
                        pass
                    else:
                        # new event. Add it to the database.
                        add_new_event(self.conn,
                                      event_dict['event_title'],
                                      event_dict['event_url'],
                                      event_dict['remote_id'],
                                      event_dict['event_image'],
                                      event_dict['event_datetime'],
                                      event_dict['event_description'],
                                      event_dict['event_price'],
                                      event_dict['event_tags'],
                                      event_dict['previews'])
                        log['added'] += 1
                print(f'Done Scraping {scraper.venue_name}')
            pprint(log)
            if once:
                self.should_update = False
                break
            else:
                sleep(self.update_inteval)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise Exception('Invalid command line args')

    dbu = DatabaseUpdater()
    run_once = 'run-once' in sys.argv
    results_limit = [sys.argv[i+1] for (i, arg) in enumerate(sys.argv) if arg == 'limit-results']
    if results_limit:
        results_limit = int(results_limit[0])
    print(f"Running with run_once={run_once}, results_limit={results_limit}")
    dbu.start_update_cycle(once=run_once, results_limit=results_limit)



import sqlite3
import os
import pprint
from time import sleep
import array
from ab_parser import ABScraper
from flagey2 import FlageyScraper
import json
SCRAPERS = [ABScraper, FlageyScraper]


def get_event(conn, remote_id, title):
    command = "SELECT * FROM events WHERE remote_id == ? and title == ?"
    return conn.execute(command, (remote_id, title)).fetchall()


def add_new_event(conn, event_title, event_url, remote_id, event_image, event_datetime, event_description, event_price, event_tags, previews):
    command1 = "insert into events (title, remote_id, event_datetime, event_price, event_image_url, event_description, event_url) \
                VALUES (?, ?, ?, ?, ?, ?, ?);"
    conn.execute(command1, (event_title, str(remote_id), event_datetime, event_price, event_image, event_description, event_url))
    conn.commit()


class DatabaseUpdater:
    def __init__(self):
        self.update_inteval = 60  # In seconds.
        self.should_update = True
        self.conn = sqlite3.connect('database.db')
        self.start_update_cycle()

    def start_update_cycle(self):
        while self.should_update:
            for Scraper in SCRAPERS:
                s = Scraper()
                print(f'Scraping {s.venue_name}')
                results = s.start_scrape()
                print(f'Done Scraping {s.venue_name}')
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

            sleep(self.update_inteval)


if __name__ == '__main__':
    dbu = DatabaseUpdater()
    dbu.start_update_cycle()


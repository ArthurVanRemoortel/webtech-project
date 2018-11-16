""" DatabaseUpdater docs.

How to use this module:

Example:
    There are 2 ways to use this module. DatabaseUpdater can run forever and
    continuously update the databse every x seconds.
        $ python update_database.py

    Or you can update the database a single time.
        $ python update_database.py run-once

    Additionally, you can limit the amount of results generated by the scrapers. 
    Scraping is a slow process, so this is usefull for testing.
        $ python update_database.py run_once limit_results=5
    If this example, each parser would stop after generating 5 results.

Attributes:
    SCRAPERS: Classes of the scrapers currently available.
              If you write your own scraper, simply add the name of class to this list.
              The scraper only requires a method named start_scrape(limit_results) that
              returns a list of dictionaries.

    UPDATE_INTERVAL: Number of seconds between updates.
"""
import sqlite3
from pprint import pprint
from time import sleep
import sys
# TODO: IDE complains about scrape_scripts imports, but works anyway.
from scrape_scripts.ab_scraper import ABScraper
from scrape_scripts.flagey_scraper import FlageyScraper

SCRAPERS = [
    ABScraper(),
    #FlageyScraper()
]
UPDATE_INTERVAL = 3600


def get_event(conn, remote_id, title):
    """
    Returns an events from the database. Where the title and remote_id match.
    A remote_id is an id the original website uses.
    :param conn: the database connection.
    :param ...
    :return: list.
    """
    command = "SELECT * FROM events WHERE remote_id == ? and title == ?"
    event_result = conn.execute(command, (remote_id, title)).fetchone()  # There should only be one event.
    if event_result:
        event_db_id = event_result[0]
        event_dict = {
                'event_url': event_result[7],
                'remote_id': event_result[2],
                'event_title': event_result[1],
                'event_image': event_result[5],
                'event_datetime': event_result[3],
                'event_description': event_result[6],
                'event_price': event_result[4],
                'event_tags':  get_tags_of_event(conn, event_db_id),
                'previews': get_previews_of_event(conn, event_db_id)
                }
        # Add tags and previews to dict.
        return event_dict
    else:
        return None


def get_tags_of_event(conn, event_id):
    tags_commans = "SELECT tag_name \
                            FROM event_tags_junction et \
                    INNER JOIN tags t ON t.tag_id = et.tag_id \
                            WHERE et.event_id = (?)"
    tags = list(map(lambda tag_result: tag_result[0], conn.execute(tags_commans, (event_id, )).fetchall()))
    return tags


def get_previews_of_event(conn, event_id):
    tags_commans = "SELECT url \
                            FROM event_previews_junction ep \
                    INNER JOIN previews p ON p.preview_id = ep.preview_id \
                            WHERE ep.event_id = (?)"
    tags = list(map(lambda preview_result: preview_result[0], conn.execute(tags_commans, (event_id, )).fetchall()))
    return tags


def add_tag_to_event(conn, tag, event_id):
    """
    A preview is a link to a youtube video (or something else).
    Links a previews  to an event. Creates a new it if it doesn't exist.
    :param conn: db connection.
    :param event_id: the primary key of the event in the db.
    """
    add_tag_command = "insert or ignore into tags (tag_name) values (?)"
    conn.execute(add_tag_command, (tag,))
    tag_id = conn.execute("select tag_id from tags where tag_name == ?", (tag,)).fetchone()[0]
    add_junction_cmd = "insert into event_tags_junction (event_id, tag_id) values (?, ?);"
    conn.execute(add_junction_cmd, (event_id, tag_id))
    conn.commit()


def add_preview_to_event(conn, preview_url, event_id):
    """
    Links a tag to an event. Creates a new it if it doesn't exist.
    :param conn: db connection.
    :param event_id: the primary key of the event in the db.
    """
    add_preview_command = "insert or ignore into previews (url) values (?)"
    conn.execute(add_preview_command, (preview_url,))
    preview_url_id = conn.execute("select preview_id from previews where url == ?", (preview_url,)).fetchone()[0]
    add_junction_cmd = "insert into event_previews_junction (event_id, preview_id) values (?, ?);"
    conn.execute(add_junction_cmd, (event_id, preview_url_id))
    conn.commit()


def add_new_event(conn, event_title, event_url, remote_id, event_image, event_datetime, event_description, event_price, event_tags, previews):
    """
    # Adds a new event to the database. Also adds tags, previews and "links" them to the event with a junction table.
    :param conn: database connection.
    :param ...
    """
    command1 = "insert into events (title, remote_id, event_datetime, event_price, event_image_url, event_description, event_url) \
                VALUES (?, ?, ?, ?, ?, ?, ?);"
    cursor = conn.execute(command1, (event_title, str(remote_id), event_datetime, event_price, event_image, event_description, event_url))
    event_id = cursor.lastrowid
    for tag in event_tags:
        add_tag_to_event(conn, tag, event_id)

    for preview_url in previews:
        add_preview_to_event(conn, preview_url, event_id)
    conn.commit()


class DatabaseUpdater:
    def __init__(self):
        self.should_update = True
        self.conn = sqlite3.connect('database.db')

    def start_update_cycle(self, once=False, limit_results=False):
        while self.should_update:
            log = {'added': 0, 'updated': 0, 'results': 0}
            for scraper in SCRAPERS:
                print(f'Scraping {scraper.venue_name}')
                results = scraper.start_scrape(limit_results=limit_results)
                log['results'] += len(results)
                for event_dict in results:
                    saved_events = get_event(self.conn, event_dict['remote_id'], event_dict['event_title'])
                    if saved_events:
                        # Event exists. Check if anything changed.
                        # TODO: Verify if anything has changed.
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
                sleep(UPDATE_INTERVAL)


if __name__ == '__main__':
    run_once = False
    limit_results = False
    if len(sys.argv) > 1:
        run_once = 'run_once' in sys.argv
        limit_results = [int(arg.split('=')[-1]) for arg in sys.argv if 'limit_results=' in arg][0]

    print(f"Running with run_once={run_once}, limit_results={limit_results}")

    dbu = DatabaseUpdater()
    #pprint(get_event(dbu.conn, "20853", "Marco Borsato"))
    dbu.start_update_cycle(once=run_once, limit_results=limit_results)



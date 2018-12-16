from time import sleep
from django.utils.dateparse import parse_datetime
try:
    from .settings import SEARCH_PAGE_LIMIT
    from .helpers import get_parsable_html, extract_price_from_raw_string, clean_up_string
except ModuleNotFoundError:
    from settings import SEARCH_PAGE_LIMIT
    from helpers import get_parsable_html, extract_price_from_raw_string, clean_up_string

BLACKLISTED = ['Meet']  # Events with these tags probably aren't concerts. Ignore them.
DONT_SEARCH_PREVIEW = ['Hosted events', 'Workshop']  # Events with these tags will probably not be found on youtube/last.fm/...


class FlageyScraper(object):
    def __init__(self):
        self.venue_name = 'Flagey'
        self.root_url = "https://www.flagey.be"
        self.search_page = "https://www.flagey.be/nl/program/1-music"
        self.description = "Flagey Square, is a square in the Brussels municipality of Ixelles, Belgium. With ten streets converging at Flagey Square, it is one of the best connected crossroads in the city, directly adjacent to the neighbouring Ixelles Ponds. A large flood control reservoir and a parking lot have been built under the square."
        self.venue_image = "https://www.flagey.be/assets/img/og_image_20170607.png"
        self.venue_addres = "Place Sainte-Croix, 1050 Bruxelles"

    def start_scrape(self, limit_results=False):
        results = []
        soup = get_parsable_html(self.search_page)
        current_page_n = 1
        while current_page_n <= SEARCH_PAGE_LIMIT:
            next_page_url = None
            for pager_item in soup.find_all('li', class_='pager__item'):
                try:
                    if int(pager_item.text) == current_page_n + 1:
                        next_page_url = self.root_url + pager_item.a['href']
                        break
                except (ValueError, TypeError):
                    pass

            events_items = soup.find_all('li', class_='item item--4 item--activity')
            for i, item in enumerate(events_items):
                tags = list(map(clean_up_string, item.find('div', class_='tags item__tags').text.split(', ')))
                blacklisted = False
                for blacklisted_tag in BLACKLISTED:
                    if blacklisted_tag in tags:
                        blacklisted = True
                        break

                if not blacklisted:
                    event_url = item.a['href']
                    r = self.scrape_event(event_url)
                    results.append(r)
                    sleep(0.2)
                if limit_results and len(results) >= limit_results:
                    next_page_url = None
                    break

            if next_page_url:
                current_page_n += 1
                soup = get_parsable_html(next_page_url)
            else:
                break
        return results

    def scrape_event(self, event_url):
        """
        :param event_url: The page of the event
        :return: dict: All the important data scraped from the page.
        """
        soup = get_parsable_html(event_url)
        remote_id = event_url.split('/')[-1].split('-')[0]
        event_title = soup.find('h2', class_='header__title').text
        event_image = soup.find('img', class_='js-parallax')['src']
        try:
            event_description = soup.find('div', class_='text').p.text
        except AttributeError:
            event_description = None
        event_tags = list(map(clean_up_string, soup.find('div', class_='tags').text.split(', ')))
        event_datetime_str = soup.find('div', class_='infos__datetime').time['datetime']
        event_price = extract_price_from_raw_string(soup.find('span', class_='infos__price').text)
        event_datetime = parse_datetime(event_datetime_str)
        return {'event_url': event_url,
                'remote_id': remote_id,  # Optional. Found in the url of the event.
                'event_title': event_title,
                'event_image': event_image,
                'event_datetime': event_datetime,
                'event_description': event_description,
                'event_price': event_price,
                'event_tags': event_tags,
                'previews': []}


if __name__ == '__main__':
    from pprint import pprint
    s = FlageyScraper()
    r = s.start_scrape(limit_results=True)
    pprint(r)

from time import sleep
import datetime
try:
    from .settings import SEARCH_PAGE_LIMIT
    from .helpers import get_parsable_html, extract_price_from_raw_string, clean_up_string
except ModuleNotFoundError:
    from settings import SEARCH_PAGE_LIMIT
    from helpers import get_parsable_html, extract_price_from_raw_string, clean_up_string

def translate_datetime_string(date_string):
    # Python's datetime module doesn't work well with Dutch weakdays.
    # Translates Dutch to English.
    date_string = date_string.replace('ma', 'Monday')
    date_string = date_string.replace('di', 'Tuesday')
    date_string = date_string.replace('wo', 'Wednesday')
    date_string = date_string.replace('do', 'Thursday')
    date_string = date_string.replace('vr', 'Friday')
    date_string = date_string.replace('za', 'Saturday')
    date_string = date_string.replace('zo', 'Sunday')
    return date_string


class ABScraper(object):
    def __init__(self):
        self.venue_name = 'AB'
        self.root_url = "https://www.abconcerts.be"
        self.search_page = "https://www.abconcerts.be/nl/agenda/evenementen/?category[]=20"

    def start_scrape(self, limit_results=None):
        """
        Scrapes all upcoming events
        :param limit_results: If set, the scraping will end early.
        :return: list of dictionaries.
        """
        results = []
        soup = get_parsable_html(self.search_page)
        current_page_n = 1
        while current_page_n <= SEARCH_PAGE_LIMIT:  # NOTE: for testing only. Stops searching after n pages.
            next_page_url = None
            for pageination_item in soup.findAll('li', class_='pagination__page'):
                page_n = pageination_item.text
                try:
                    page_url = pageination_item.a['href']
                    if int(page_n) == current_page_n + 1:
                        next_page_url = page_url
                        break
                except (ValueError, TypeError):
                    pass

            for event_item in soup.find_all('div', class_='overview__item'):
                event_url = event_item.a['href']
                event_alert = event_item.find('li', class_='alert')
                skip_event = False
                if event_alert and clean_up_string(event_alert.text) == 'Verplaatst':
                    skip_event = True
                if not skip_event:
                    try:
                        r = self.scrape_event(event_url)
                        results.append(r)
                    except Exception as e:
                        print(f'FAILED: {event_url}')
                        raise e
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
        remote_id = event_url.split('/')[-2]
        event_title = soup.find('div', class_='masthead__title').h1.text  # TODO: Include other artists.
        event_image = soup.find('img', class_='masthead__img')['src']
        event_description_raw = soup.find('div', class_='event__summary')
        event_description = event_description_raw.p.text if event_description_raw else None
        event_tags_raw = list(soup.find('ul', class_='overview__tags'))
        event_tags = []
        for tag in event_tags_raw:
            if tag != '\n':
                event_tags.append(tag.text)
        event_datetime_str = soup.find('div', class_='masthead__title').span.text
        # TODO: Time is missing.
        event_datetime = datetime.datetime.strptime(translate_datetime_string(event_datetime_str), '%A %d.%m.%y')
        # TODO: Always pick the price for VVK if available. see doc for extract_price_from_raw_string.
        event_price = extract_price_from_raw_string(soup.find('ul', class_='event__aside__list').findAll('li')[0].text)
        video_section = soup.find('ul', class_='event__videos')
        if video_section:
            previews = list(map(lambda iframe: iframe['src'][2:], video_section.findAll('iframe')))
        else:
            previews = []

        return {'event_url': event_url,
                'remote_id': remote_id,  # Found in the url of the event.
                'event_title': event_title,
                'event_image': event_image,
                'event_datetime': event_datetime,
                'event_description': event_description,
                'event_price': event_price,
                'event_tags': event_tags,
                'previews': previews}


if __name__ == '__main__':
    from pprint import pprint
    s = ABScraper()
    r = s.start_scrape()
    pprint(r)

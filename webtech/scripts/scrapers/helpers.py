from bs4 import BeautifulSoup
import requests
import re


def get_parsable_html(url):
    """
    Downloads the url and returns a BeautifulSoup object.
    :param url: string
    :return: bs4.BeautifulSoup
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def extract_price_from_raw_string(price_string):
    """
    # e.g "€18 VVK of €20 aan de deur" --> 20.0
    :param price_string: string
    :return: tuple
    """
    event_price = 0
    if 'gratis' not in price_string.lower():
        try:
            event_price = max(map(float, re.findall(r'\d+', price_string)))
        except:
            event_price = 0

    return event_price

def clean_up_string(text):
    """
    Cleans up strings with empty padding and other unexpected characters"
    e.g. "      this is \n a text.   " --> "this is a text."
    :param text: string
    :return: string
    """
    text = text.replace("\n", "")
    while text[0] == " ":
        text = text[1:]
    while text[-1] == " ":
        text = text[:-1]
    return text
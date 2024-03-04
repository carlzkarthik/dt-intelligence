import threading

import requests
import re
from .print_utils import *

from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from requests_tor import RequestsTor
from .crypto_transaction import *


def connect_to_tor():
    sess = requests.session()
    sess.proxies = {'http': 'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return sess


def get_web_content(url):
    try:
        rt = RequestsTor(tor_ports=(9050,), tor_cport=(9150,))
        web_content = rt.get(url).text
        return web_content
    except:
        print_error(f"Error While Enumerating {url}")
        return -1


def get_web_content_selenium():
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'socksProxy': '127.0.0.1:9050',
        'socksVersion': 5,
    })
    options = Options()
    options.proxy = proxy
    options.binary_location = "/home/dimitri/Downloads/tor-browser/Browser/firefox"
    # options.binary_location = '/path/to/normal/firefox'  # works
    driver = Firefox(options=options)  # use path to standard `Firefox`
    url = 'http://breachedu76kdyavc6szj6ppbplfqoz3pgrk3zw57my4vybgblpfeayd.onion/'
    driver.get(url)
    contents = driver.page_source
    driver.quit()
    return contents


def get_emails(web_content):
    email_pattern = r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-z]+'
    matches = re.findall(email_pattern, web_content)
    return matches


def get_onion_links(web_content):
    onion_link_pattern = r'[htp\/\/:]{0,7}[a-z0-9]{16,56}\.onion\/*'
    matches = re.findall(onion_link_pattern, web_content)
    unique_urls = set()
    for m in matches:
        m = m.rstrip('/')
        if m.startswith("http://"):
            unique_urls.add(m)
        else:
            url = "http://" + m
            unique_urls.add(url)

    return unique_urls


def enumerate_crypto_address(address):
    print(address)
    bc = Blockchain()
    bc.get_transaction(address)


def update_onion_link_queue(onion_links):
    pass

def threat_search(keyword):
    pass

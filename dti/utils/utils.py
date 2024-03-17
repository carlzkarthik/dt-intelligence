import re
from .print_utils import *

from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from requests_tor import RequestsTor
from .crypto_transaction import *


def connect_to_tor():
    """
    connect to TOR network
    @return: session object
    """
    sess = requests.session()
    sess.proxies = {'http': 'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return sess


def get_web_content(url):
    """
    Get HTML contents of a web page
    @param url: URL of the web page
    @return: HTML web content or -1 if an error occurs
    """

    print_info(f"Requesting web page {url}")
    try:
        rt = RequestsTor(tor_ports=(9050,), tor_cport=(9150,))
        web_content = rt.get(url).text
        return web_content
    except:
        print_error(f"Error while requesting webpage for ---> {url}")
        return -1


def get_web_content_selenium(url):
    """
    Get HTML contents of a web page using selenium
    @param url: URL of the web page
    @return: HTML web content or -1 if an error occurs
    """
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

    try:
        driver.get(url)
        contents = driver.page_source
        driver.quit()
    except:
        print_error(f"Error While Enumerating {url}")
        driver.close()
        return -1

    return contents


def get_emails(web_content):
    """
    Get emails from web page contents using regular expression
    @param web_content: HTML web content
    @return: List of email addresses
    """
    email_pattern = r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-z]+'
    matches = re.findall(email_pattern, web_content)
    return matches


def get_onion_links(web_content):
    """
    Get onion links from web page contents using regular expression
    @param web_content: HTML web content
    @return: List of onion links
    """
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


def update_onion_link_queue(onion_links):

    """
    Update onion links queue
    If onion link already exists, do nothing else add it to queue(Database table)
    @param onion_links: List of onion links
    @return: None
    """
    pass

def enumerate_crypto_address(address):
    print(address)
    bc = Blockchain()
    bc.get_transaction(address)

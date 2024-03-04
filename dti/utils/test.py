from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


# Set the proxy to use Tor
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Set the proxy for Tor browser
proxy_ip = "127.0.0.1"  # Replace with your Tor proxy IP
proxy_port = 9050  # Replace with your Tor proxy port
options = Options()
# options.add_argument('-headless')
options.binary_location = "/home/graham/Downloads/tor-browser/Browser/firefox"
options.set_preference('network.proxy.type', 1)
options.set_preference('network.proxy.socks', proxy_ip)
options.set_preference('network.proxy.socks_port', proxy_port)
driver = Firefox(options=options)

driver.get(url="http://breachedu76kdyavc6szj6ppbplfqoz3pgrk3zw57my4vybgblpfeayd.onion/")
print(driver.page_source)

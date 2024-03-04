import requests
from bs4 import BeautifulSoup


class BitcoinTransaction():

    def __init__(self):
        pass


class Blockchain:

    def __init__(self):
        self.base_url = "https://www.blockchain.com/explorer/addresses/btc/"

    def get_transaction(self, address):
        response = requests.get(
            "https://blockchair.com/bitcoin/address/bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97")
        if response.status_code == 200:
            bs4_contents = BeautifulSoup(response.text, 'html.parser')
            print(
                f"Current Balance --- {bs4_contents.find('div', class_='account-hash__balance').find('span', class_='wb-ba').get_text()}")

            print(
                f"Total BTC received --- {bs4_contents.find('div', class_='account-hash__balance__row').find('span', class_='wb-ba').get_text()}")

            print(f"Total BTC Sent --- {bs4_contents.find('div', class_='account-hash__balance__row')}")
            # print(bs4_contents.prettify())

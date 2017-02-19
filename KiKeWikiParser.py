from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import unicodedata


class GetData:
    def __init__(self, url):
        self._url = url

        """ Get Html content """
        web_page = requests.get(self._url)
        self.html_content = BeautifulSoup(web_page.text, 'html.parser')

    def get_data(self):
        return self.html_content

    def get_tables(self):
        return self.html_content.find_all('table')


class GetFeatures(GetData):
    def __init__(self, url):
        super().__init__(url)

    def get_info_box(self):
        t_to_json = Converter(self.html_content.find_all('table', class_='infobox')[0])
        return t_to_json.table_to_json()


class Converter:
    def __init__(self, data):
        self._data = data
        pass

    def table_to_json(self):
        trs = self._data.find_all('tr')
        table_data = {}
        for tr in trs:
            key = None
            value = None
            data = self.data_to_array(tr)

            for i, item in enumerate(data):

                if i == 0:
                    if hasattr(item, 'string'):
                        key = self.process_td_key(item)
                        key = self.string_normalize(key)
                else:
                    value = self.process_td_value(item)
                    value = self.string_normalize(value)

            if key and value is not None: table_data[key] = value

        return table_data

    @staticmethod
    def process_td_key(item):
        for string in item.find_all(string=True):
            return string

    @staticmethod
    def process_td_value(items):
        strings = ''
        for string in items.find_all(string=True):
            if string != '\n': strings += string
        return strings

    @staticmethod
    def data_to_array(data):
        try:
            while '\n' in data.contents: data.contents.remove('\n')
        except:
            pass
        return data

    @staticmethod
    def string_normalize(string):
        if string is not None:
            string = unicodedata.normalize("NFKD", string)
            string = string.replace('\n', ' ')
            string = string.replace('[1]', ' ')
            string = string.replace('[2]', ' ')
        return string


# Method to get info box from wikipedia
def infoBox(url):
    features = GetFeatures(url)
    return features.get_info_box()


# Main functions
def wiki_parser(url):
    soup = GetData(url)


if __name__ == "__main__": wiki_parser("https://en.wikipedia.org/wiki/Methane")

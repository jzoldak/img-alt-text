"""
Script to generate report on image alt tags.

Usage:

    python find_images.py

Input:

    A flat file of URLs

Output:

    A tab delimited report of the images in each of the pages, with
    their src and alt text

"""
import sys
import requests
from bs4 import BeautifulSoup
import os

BASE = 'https://test.edx.org'
USER = 'foo'
PASS = 'bar'
INPUT_FILE = 'urls.txt'
OUTPUT_FILE = 'output.txt'

class URL(object):
    """
    A URL that you want to navigate to and find the image links on
    """
    def __init__(self, path):
        """
        Load the html from the url, process it, and output the results.
        """
        self._imgs = []
        self.path = path

        if self._load_html(path):
            self._parse_imgs()

        if len(self._imgs) > 0:
            self._output_results()


    def _load_html(self, path):
        url = '{}{}'.format(BASE, path)
        resp = requests.get(url, auth=(USER, PASS))
        if resp.status_code == 200:
            self.soup = BeautifulSoup(resp.text, from_encoding='utf-8')
            return True
        else:
            print '{} {}'.format(resp.status_code, url)
            return False


    def _parse_imgs(self):
        for img in self.soup.find_all('img'):
            alt = img.get('alt', '')
            src = img.get('src', '')
            self._imgs.append({'alt': alt, 'src': src})


    def _output_results(self):
        with open(OUTPUT_FILE,'a') as out_file:
            for row in self._imgs:
                line = u'{}\t{}\t{}\n'.format(self.path, row['alt'], row['src'])
                out_file.write(line.encode('utf8'))


def main(args):

    url_file = open(INPUT_FILE, 'r')

    # Clear out the output file
    if os.path.isfile(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    for line in url_file:
        url = line.strip()

        # You can use the hash character to comment out a line in the input file.
        if not url.startswith('#'):
            URL(url)


if __name__ == '__main__':
    main(sys.argv)

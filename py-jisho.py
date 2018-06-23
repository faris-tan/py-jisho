#!/usr/bin/env python
'''Python3 module for getting shit out of jisho.org api'''

import sys

import logging
import requests


class JishoSearcher(object):

    LOOKUP_QUERY = 'https://jisho.org/api/v1/search/words?keyword='

    def __init__(self, word):
        self.word = word

    @staticmethod
    def _ExtractMeanings(word_entry):
        readings = [(k['word'], k['reading']) for k in word_entry['japanese']]
        meanings = []
        for s in word_entry['senses']:
            meanings.append([d for d in s['english_definitions']])
        return (readings, meanings)

    def GetResults(self):
        query = self.LOOKUP_QUERY+self.word
        try:
            r = requests.get(query).json()
        except Exception as e:
            logging.error(e)
        status = r['meta'].get('status')
        if status != 200:
            logging.error('Request for %s somewhat failed with %s',
                          self.word, status)
            return ''
        data = r['data']
        if not data:
            return ''
        # Ignore anything past the top 5 results
        return [self._ExtractMeanings(d) for d in data[:5]]


def main(argv):
    if len(argv) < 2:
        return
    searcher = JishoSearcher(argv[1])
    for (r, m) in searcher.GetResults():
        for reading in r:
            print('  %s - %s' % reading)
        for meaning in m[:7]:
            print('    %s' % ', '.join(meaning))
        if len(m) > 7:
            print('    。。。')

    sys.stdout.flush()

if __name__ == '__main__':
    main(sys.argv)

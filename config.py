#!/usr/bin/env python


import csv


class _Config(object):

    def __init__(self):
        self.config_map = dict()
        with open('CONFIG') as config_tsv:
            reader = csv.DictReader(config_tsv, dialect='excel-tab')
            for row in reader:
                self.config_map[row['CONFIG_KEY']] = row['CONFIG_VALUE']


_singleton = _Config()


def get(requested_key): return _singleton.config_map[requested_key]

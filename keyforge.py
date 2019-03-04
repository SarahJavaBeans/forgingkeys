#!/usr/bin/env python


import argparse
import compendium
import csv
import dok
import json
import os
import vault
from decks import Deck


def get_stats(decks):
	compendium.client().lookup_decks(decks)
	vault.client().lookup_decks(decks)
	dok.client().lookup_decks(decks)


def decks_from_tsv(filename):
	decks = []
	with open(filename) as tsvfile:
		reader = csv.DictReader(tsvfile, dialect='excel-tab')
		for row in reader:
			deck = Deck(id=row['Deck Id'], name=row['Deck Name'])
			decks.append(deck)
	return decks


def test_decks():
	return [Deck(id='18736cb4-88f4-47af-92f2-4172fb3586a2'), Deck(id='869ecc00-4527-4061-b9cb-6c1e1bf4910d'), Deck(id='87220b2f-6f59-4095-abb0-14a50d1c53b8')]


def to_json(decks):
	for deck in decks:
		print(deck)
#	print(json.dumps(decks, indent=4))


def valid_file(filename):
	if not os.path.exists(filename):
		raise argparse.ArgumentTypeError("{0} does not exist".format(filename))
	return filename


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Retrieve and format Keyforge deck stats.")
	parser.add_argument("-f", "--filename", dest="filename", type=valid_file,
	                    help="TSV file to parse, should contain a column for Deck Name or Deck Id",
	                    metavar="FILE")
	parser.add_argument("-t", "--tsv", dest="tsv", action='store_true')
	parser.set_defaults(tsv=False)
	args = parser.parse_args()
	#if args.filename:
		#decks = get_stats(args.filename)
	#else:
	decks = test_decks()

	get_stats(decks)
	#if args.tsv:
		#to_tsv(decks)
	#else:
	to_json(decks)

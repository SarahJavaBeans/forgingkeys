#!/usr/bin/env python


import config
import json
import requests
import time
import traceback


class _CompendiumClient(object):

	def __init__(self):
		self.api_key = config.get('compendium_api_key')
		self.api_pass = config.get('compendium_api_pass')
		self.rps = config.get('compendium_api_max_requests_per_second')

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

	def lookup_decks(self, decks):
		request_rate = 0
		for deck in decks:
			self.lookup_deck(deck)
			if request_rate >= self.rps:
				request_rate = 0
				time.wait(1) # wait for 1 second
			else:
				request_rate = request_rate + 1

	def lookup_deck(self, deck):
		if deck.Id:
			deck_id = deck.Id
		elif deck.get(deck.Name):
			deck_id = 'by_name/'+deck.Name
		else:
			return

		try:
			r = requests.get('https://keyforge-compendium.com/api/v1/decks/'+str(deck_id), auth=(self.api_key, self.api_pass))
			compendium_deck = json.loads(r.text)
			deck.Name = compendium_deck['name']
			deck.Id = compendium_deck['uuid']
			deck.with_adhd(compendium_deck["a_rating"], compendium_deck["b_rating"], compendium_deck["c_rating"], compendium_deck["e_rating"], compendium_deck["consistency_rating"])
		except Exception as err:
			traceback.print_exc()
			print 'Unable to retrieve deck in Compendium: ' + str(deck.Id)
			return

_singleton = _CompendiumClient()


def client(): return _singleton


#!/usr/bin/env python


import config
import json
import requests
import time
import traceback


class _DOKClient(object):
	def __init__(self):
		self.api_key = config.get('dok_api_key')
		self.rps = config.get('dok_api_max_requests_per_second')

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

	def lookup_decks(self, decks):
		request_rate = 0
		for deck in decks:
			self.lookup_deck(deck)
			if request_rate >= self.rps:
				request_rate = 0
				time.wait(1)  # wait for 1 second
			else:
				request_rate = request_rate + 1

	def lookup_deck(self, deck):
		try:
			r = requests.get('https://decksofkeyforge.com/public-api/v3/decks/' + str(deck.Id), headers={"Api-Key": self.api_key})
			dok_deck = (json.loads(r.text))['deck']
			deck.with_sas(sas=int(dok_deck['sasRating']), card_rating=int(dok_deck['cardsRating']), synergy=int(dok_deck['synergyRating']), antisynergy=int(dok_deck['antisynergyRating']))
			deck.with_aerc(a=float(dok_deck['amberControl']), e=float(dok_deck['expectedAmber']), r=float(dok_deck['artifactControl']), c=float(dok_deck['creatureControl']))
		except Exception as err:
			traceback.print_exc()
			print 'Unable to retrieve deck in DOK: ' + str(deck.Id)
			return


_singleton = _DOKClient()


def client(): return _singleton

import config
import json
import requests
import time
import traceback
from decks import Deck

expansions = {
	341: "Call of the Archons",
}

property_count = "count"

property_data = "data"
property_data_name = "name"
property_data_expansion = "expansion"
property_data_power_level = "power_level"
property_data_chains = "chains"
property_data_wins = "wins"
property_data_losses = "losses"
property_data_id = "id"
property_data_links = "_links"
property_data_links_houses = "houses"  # array of ids
property_data_links_cards = "cards"  # array of card id strings

property_linked = "_linked"
property_linked_houses = "houses"
property_linked_houses_id = "id"
property_linked_houses_name = "name"
property_linked_houses_image = "image"  # image URL

property_linked_cards = "cards"
property_linked_cards_id = "id"
property_linked_cards_title = "card_title"
property_linked_cards_house = "house"
property_linked_cards_type = "card_type"
property_linked_cards_front_image = "front_image"  # image URL
property_linked_cards_text = "card_text"
property_linked_cards_traits = "traits"
property_linked_cards_amber = "amber"
property_linked_cards_power = "power"
property_linked_cards_armor = "armor"
property_linked_cards_rarity = "rarity"
property_linked_cards_flavor_text = "flavor_text"
property_linked_cards_number = "card_number"
property_linked_cards_expansion = "expansion"
property_linked_cards_is_maverick = "is_maverick"  # boolean


class _VaultClient(object):
	def __init__(self):
		self.rps = config.get('vault_api_max_requests_per_second')

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

	def lookup_all_decks(self):
		#request_rate = 0
		page = 0
		try:
			page = page + 1
			#if request_rate >= self.rps:
				#request_rate = 0
				#time.wait(1)  # wait for 1 second
			#else:
				#request_rate = request_rate + 1

			r = requests.get('https://www.keyforgegame.com/api/decks/?page='+str(page)+'&page_size=25&links=cards')
			vault_deck = json.loads(r.text)#[0]
			print(vault_deck)
		except Exception as err:
			traceback.print_exc()
			print('Unable to retrieve page: '+str(page))
			return

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
		if deck.Id:
			try:
				r = requests.get('https://www.keyforgegame.com/api/decks/' + str(deck.Id))
				vault_deck = (json.loads(r.text))['data']
				deck.Id = vault_deck['id']
				deck.Name = vault_deck['name']
				deck.Expansion = expansions[vault_deck['expansion']]
				deck.PowerLevel = vault_deck['power_level']
				deck.Chains = vault_deck['chains']
				deck.Wins = vault_deck['wins']
				deck.Losses = vault_deck['losses']
			except Exception as err:
				traceback.print_exc()
				print 'Unable to retrieve deck in DOK: ' + str(deck.Id)
				return


_singleton = _VaultClient()


def client(): return _singleton

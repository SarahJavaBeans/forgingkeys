#!/usr/bin/env python


class Deck(object):
	def __init__(self, id=0, name='', expansion='', powerLevel=0, chains=0, wins=0, losses=0):
		self.Id = id
		self.Name = name
		self.Expansion = expansion
		self.PowerLevel = powerLevel
		self.Chains = chains
		self.Wins = wins
		self.Losses = losses
		self.with_adhd()
		self.with_aerc()
		self.with_sas()

	def with_sas(self, sas=0, card_rating=0, synergy=0, antisynergy=0):
		self.SAS = sas
		self.SAS_Cards = card_rating
		self.SAS_Synergy = synergy
		self.SAS_Antisynergy = antisynergy

	def with_aerc(self, a=0, e=0, r=0, c=0):
		self.AERC_A = a
		self.AERC_E = e
		self.AERC_R = r
		self.AERC_C = c
		self.AERC = a + e + r + c

	def with_adhd(self, a=0, b=0, c=0, e=0, consistency=0):
		self.ADHD_A = a
		self.ADHD_B = b
		self.ADHD_C = c
		self.ADHD_E = e
		self.ADHD_Consistency = consistency

	def __str__(self):
		return str(self.__dict__)

import argparse
import csv
import json
import os
import requests

data_id = 'id'
data_name = 'name'
data_abce_a = 'abce_a'
data_abce_b = 'abce_b'
data_abce_c = 'abce_c'
data_abce_e = 'abce_e'
data_abce_consistency = 'abce_consistency'
data_ct_rares = 'ct_rares'
data_ct_fixed = 'ct_fixed'
data_ct_variants = 'ct_variants'
data_ct_mavericks = 'ct_mavericks'
data_aerc_a_pct_from_avg = 'aerc_a_pct_from_avg'
data_aerc_e_pct_from_avg = 'aerc_e_pct_from_avg'
data_aerc_r_pct_from_avg = 'aerc_r_pct_from_avg'
data_aerc_c_pct_from_avg = 'aerc_c_pct_from_avg'
data_abce_a_pct_from_avg = 'abce_a_pct_from_avg'
data_abce_b_pct_from_avg = 'abce_b_pct_from_avg'
data_abce_c_pct_from_avg = 'abce_c_pct_from_avg'
data_abce_e_pct_from_avg = 'abce_e_pct_from_avg'
data_sas_synergy_pct_from_avg = 'sas_synergy_pct_from_avg'
data_sas_antisynergy_pct_from_avg = 'sas_antisynergy_pct_from_avg'
data_sas = 'sas'
data_sas_card_rating = 'sas_card_rating'
data_sas_synergy = 'sas_synergy'
data_sas_antisynergy = 'sas_antisynergy'
data_aerc_a = 'aerc_a'
data_aerc_e = 'aerc_e'
data_aerc_r = 'aerc_r'
data_aerc_c = 'aerc_c'
data_dok_creature_power = 'dok_creature_power'

output_order = [
    data_id,
    data_name,
    data_abce_consistency,
    data_sas,
    data_aerc_a_pct_from_avg,
    data_aerc_e_pct_from_avg,
    data_aerc_r_pct_from_avg,
    data_aerc_c_pct_from_avg,
    data_abce_a_pct_from_avg,
    data_abce_b_pct_from_avg,
    data_abce_c_pct_from_avg,
    data_abce_e_pct_from_avg,
    data_sas_synergy_pct_from_avg,
    data_sas_antisynergy_pct_from_avg,
    data_ct_rares,
    data_ct_mavericks,
    data_ct_fixed,
    data_ct_variants,
    data_sas_card_rating,
    data_sas_synergy,
    data_sas_antisynergy,
    data_aerc_a,
    data_aerc_e,
    data_aerc_r,
    data_aerc_c,
    data_abce_a,
    data_abce_b,
    data_abce_c,
    data_abce_e,
    data_dok_creature_power
]

compendium_api_key = ''
compendium_api_pass = ''

def compendium_lookup(deck):
    if deck.get(data_id):
        deck_id = deck[data_id]
    elif deck.get(data_name):
        deck_id = 'by_name/'+deck[data_name]
    else:
        return

    try:
        r = requests.get('https://keyforge-compendium.com/api/v1/decks/'+str(deck_id), auth=(compendium_api_key, compendium_api_pass))
        compendium_deck = json.loads(r.text)[0]
    except:
        print 'Unable to retrieve deck: '+deck_id
        return

    deck[data_id] = compendium_deck["uuid"]
    deck[data_abce_a] = compendium_deck["a_rating"]
    deck[data_abce_b] = compendium_deck["b_rating"]
    deck[data_abce_c] = compendium_deck["c_rating"]
    deck[data_abce_e] = compendium_deck["e_rating"]
    deck[data_abce_consistency] = compendium_deck["consistency_rating"]
    deck[data_ct_rares] = compendium_deck["rare_count"]
    deck[data_ct_fixed] = compendium_deck["fixed_count"]
    deck[data_ct_variants] = compendium_deck["variant_count"]
    deck[data_ct_mavericks] = compendium_deck["maverick_count"]

def percent_difference_from_average(deck_value, average_value):
    return int(((deck_value - average_value)/average_value) * 100)

def add_derived_stats(deck):
    try:
        deck[data_aerc_a_pct_from_avg] = percent_difference_from_average(deck['aerc_a'], 7)
        deck[data_aerc_e_pct_from_avg] = percent_difference_from_average(deck['aerc_e'], 20)
        deck[data_aerc_r_pct_from_avg] = percent_difference_from_average(deck['aerc_r'], 1)
        deck[data_aerc_c_pct_from_avg] = percent_difference_from_average(deck['aerc_c'], 13)
        deck[data_sas_synergy_pct_from_avg] = percent_difference_from_average(deck['sas_synergy'], 7)
        deck[data_sas_antisynergy_pct_from_avg] = percent_difference_from_average(deck['sas_antisynergy'], 1)
    except KeyError:
        pass

    try:
        deck[data_abce_a_pct_from_avg] = percent_difference_from_average(deck['abce_a'], 17.54)
        deck[data_abce_b_pct_from_avg] = percent_difference_from_average(deck['abce_b'], 18.28)
        deck[data_abce_c_pct_from_avg] = percent_difference_from_average(deck['abce_c'], 5.51)
        deck[data_abce_e_pct_from_avg] = percent_difference_from_average(deck['abce_e'], 7.58)
    except KeyError:
        pass

def get_stats(filename):
    decks = []
    with open(filename) as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            deck_name = row['Deck Name']
            deck = dict()
            deck[data_name] = deck_name
            deck[data_sas] = int(row['SAS'])
            deck[data_sas_card_rating] = int(row['Cards'])
            deck[data_sas_synergy] = int(row['Synergy'])
            deck[data_sas_antisynergy] = int(row['Antisyn'])
            deck[data_aerc_a] = float(row['A'])
            deck[data_aerc_e] = float(row['E'])
            deck[data_aerc_r] = float(row['R'])
            deck[data_aerc_c] = float(row['C'])
            deck[data_dok_creature_power] = float(row['Creature Power'])
            compendium_lookup(deck)
            add_derived_stats(deck)
            decks.append(deck)
    return decks

def to_json(decks):
    print(json.dumps(decks, indent=4))

def to_tsv(decks):
    print('\t'.join(output_order))
    for deck in decks:
        row = []
        for data_point in output_order:
            row.append(str(deck.get(data_point,'')))
        print('\t'.join(row))

def valid_file(filename):
    if not os.path.exists(filename):
        raise argparse.ArgumentTypeError("{0} does not exist".format(filename))
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve and format Keyforge deck stats.")
    parser.add_argument("-f", "--filename", dest="filename", required=True, type=valid_file,
                        help="TSV file to parse, should contain a column for Deck Name",
                        metavar="FILE")
    parser.add_argument("-j", "--json", dest="json", action='store_true')
    parser.set_defaults(json=False)
    args = parser.parse_args()
    decks = get_stats(args.filename)
    if args.json:
        to_json(decks)
    else:
        to_tsv(decks)

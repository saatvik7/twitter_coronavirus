#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--output_folder',default='outputs')
args = parser.parse_args()

# imports
import os
import zipfile
import datetime
import json
from collections import Counter,defaultdict

# load keywords
hashtags = [
    '#코로나바이러스',  # korean
    '#コロナウイルス',  # japanese
    '#冠状病毒',        # chinese
    '#covid2019',
    '#covid-2019',
    '#covid19',
    '#covid-19',
    '#coronavirus',
    '#corona',
    '#virus',
    '#flu',
    '#sick',
    '#cough',
    '#sneeze',
    '#hospital',
    '#nurse',
    '#doctor',
    ]
# load Country Code Dictionary
country_dict = {
	'AF': 'AFGHANISTAN',
	'AX': 'ÅLAND ISLANDS',
	'AL': 'ALBANIA',
	'DZ': 'ALGERIA',
	'AS': 'AMERICAN SAMOA',
	'AD': 'ANDORRA',
	'AO': 'ANGOLA',
	'AI': 'ANGUILLA',
	'AQ': 'ANTARCTICA',
	'AG': 'ANTIGUA AND BARBUDA',
	'AR': 'ARGENTINA',
	'AM': 'ARMENIA',
	'AW': 'ARUBA',
	'AU': 'AUSTRALIA',
	'AT': 'AUSTRIA',
	'AZ': 'AZERBAIJAN',
	'BS': 'BAHAMAS',
	'BH': 'BAHRAIN',
	'BD': 'BANGLADESH',
	'BB': 'BARBADOS',
	'BY': 'BELARUS',
	'BE': 'BELGIUM',
	'BZ': 'BELIZE',
	'BJ': 'BENIN',
	'BM': 'BERMUDA',
	'BT': 'BHUTAN',
	'BO': 'BOLIVIA, PLURINATIONAL STATE OF',
	'BQ': 'BONAIRE, SINT EUSTATIUS AND SABA',
	'BA': 'BOSNIA AND HERZEGOVINA',
	'BW': 'BOTSWANA',
	'BV': 'BOUVET ISLAND',
	'BR': 'BRAZIL',
	'IO': 'BRITISH INDIAN OCEAN TERRITORY',
	'BN': 'BRUNEI DARUSSALAM',
	'BG': 'BULGARIA',
	'BF': 'BURKINA FASO',
	'BI': 'BURUNDI',
	'KH': 'CAMBODIA',
	'CM': 'CAMEROON',
	'CA': 'CANADA',
	'CV': 'CAPE VERDE',
	'KY': 'CAYMAN ISLANDS',
	'CF': 'CENTRAL AFRICAN REPUBLIC',
	'TD': 'CHAD',
	'CL': 'CHILE',
	'CN': 'CHINA',
	'CX': 'CHRISTMAS ISLAND',
	'CC': 'COCOS (KEELING) ISLANDS',
	'CO': 'COLOMBIA',
	'KM': 'COMOROS',
	'CG': 'CONGO',
	'CD': 'CONGO, THE DEMOCRATIC REPUBLIC OF THE',
	'CK': 'COOK ISLANDS',
	'CR': 'COSTA RICA',
	'CI': 'CÔTE D\'IVOIRE',
	'HR': 'CROATIA',
	'CU': 'CUBA',
	'CW': 'CURAÇAO',
	'CY': 'CYPRUS',
	'CZ': 'CZECH REPUBLIC',
	'DK': 'DENMARK',
	'DJ': 'DJIBOUTI',
	'DM': 'DOMINICA',
	'DO': 'DOMINICAN REPUBLIC',
	'EC': 'ECUADOR',
	'EG': 'EGYPT',
	'SV': 'EL SALVADOR',
	'GQ': 'EQUATORIAL GUINEA',
	'ER': 'ERITREA',
	'EE': 'ESTONIA',
	'ET': 'ETHIOPIA',
	'FK': 'FALKLAND ISLANDS (MALVINAS)',
	'FO': 'FAROE ISLANDS',
	'FJ': 'FIJI',
	'FI': 'FINLAND',
	'FR': 'FRANCE',
	'GF': 'FRENCH GUIANA',
	'PF': 'FRENCH POLYNESIA',
	'TF': 'FRENCH SOUTHERN TERRITORIES',
	'GA': 'GABON',
	'GM': 'GAMBIA',
	'GE': 'GEORGIA',
	'DE': 'GERMANY',
	'GH': 'GHANA',
	'GI': 'GIBRALTAR',
	'GR': 'GREECE',
	'GL': 'GREENLAND',
	'GD': 'GRENADA',
	'GP': 'GUADELOUPE',
	'GU': 'GUAM',
	'GT': 'GUATEMALA',
	'GG': 'GUERNSEY',
	'GN': 'GUINEA',
	'GW': 'GUINEA-BISSAU',
	'GY': 'GUYANA',
	'HT': 'HAITI',
	'HM': 'HEARD ISLAND AND MCDONALD ISLANDS',
	'VA': 'HOLY SEE (VATICAN CITY STATE)',
	'HN': 'HONDURAS',
	'HK': 'HONG KONG',
	'HU': 'HUNGARY',
	'IS': 'ICELAND',
	'IN': 'INDIA',
	'ID': 'INDONESIA',
	'IR': 'IRAN, ISLAMIC REPUBLIC OF',
	'IQ': 'IRAQ',
	'IE': 'IRELAND',
	'IM': 'ISLE OF MAN',
	'IL': 'ISRAEL',
	'IT': 'ITALY',
	'JM': 'JAMAICA',
	'JP': 'JAPAN',
	'JE': 'JERSEY',
	'JO': 'JORDAN',
	'KZ': 'KAZAKHSTAN',
	'KE': 'KENYA',
	'KI': 'KIRIBATI',
	'KP': 'KOREA, DEMOCRATIC PEOPLE\'S REPUBLIC OF',
	'KR': 'KOREA, REPUBLIC OF',
	'KW': 'KUWAIT',
	'KG': 'KYRGYZSTAN',
	'LA': 'LAO PEOPLE\'S DEMOCRATIC REPUBLIC',
	'LV': 'LATVIA',
	'LB': 'LEBANON',
	'LS': 'LESOTHO',
	'LR': 'LIBERIA',
	'LY': 'LIBYAN ARAB JAMAHIRIYA',
	'LI': 'LIECHTENSTEIN',
	'LT': 'LITHUANIA',
	'LU': 'LUXEMBOURG',
	'MO': 'MACAO',
	'MK': 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF',
	'MG': 'MADAGASCAR',
	'MW': 'MALAWI',
	'MY': 'MALAYSIA',
	'MV': 'MALDIVES',
	'ML': 'MALI',
	'MT': 'MALTA',
	'MH': 'MARSHALL ISLANDS',
	'MQ': 'MARTINIQUE',
	'MR': 'MAURITANIA',
	'MU': 'MAURITIUS',
	'YT': 'MAYOTTE',
	'MX': 'MEXICO',
	'FM': 'MICRONESIA, FEDERATED STATES OF',
	'MD': 'MOLDOVA, REPUBLIC OF',
	'MC': 'MONACO',
	'MN': 'MONGOLIA',
	'ME': 'MONTENEGRO',
	'MS': 'MONTSERRAT',
	'MA': 'MOROCCO',
	'MZ': 'MOZAMBIQUE',
	'MM': 'MYANMAR',
	'NA': 'NAMIBIA',
	'NR': 'NAURU',
	'NP': 'NEPAL',
	'NL': 'NETHERLANDS',
	'NC': 'NEW CALEDONIA',
	'NZ': 'NEW ZEALAND',
	'NI': 'NICARAGUA',
	'NE': 'NIGER',
	'NG': 'NIGERIA',
	'NU': 'NIUE',
	'NF': 'NORFOLK ISLAND',
	'MP': 'NORTHERN MARIANA ISLANDS',
	'NO': 'NORWAY',
	'OM': 'OMAN',
	'PK': 'PAKISTAN',
	'PW': 'PALAU',
	'PS': 'PALESTINIAN TERRITORY, OCCUPIED',
	'PA': 'PANAMA',
	'PG': 'PAPUA NEW GUINEA',
	'PY': 'PARAGUAY',
	'PE': 'PERU',
	'PH': 'PHILIPPINES',
	'PN': 'PITCAIRN',
	'PL': 'POLAND',
	'PT': 'PORTUGAL',
	'PR': 'PUERTO RICO',
	'QA': 'QATAR',
	'RE': 'RÉUNION',
	'RO': 'ROMANIA',
	'RU': 'RUSSIAN FEDERATION',
	'RW': 'RWANDA',
	'BL': 'SAINT BARTHÉLEMY',
	'SH': 'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA',
	'KN': 'SAINT KITTS AND NEVIS',
	'LC': 'SAINT LUCIA',
	'MF': 'SAINT MARTIN (FRENCH PART)',
	'PM': 'SAINT PIERRE AND MIQUELON',
	'VC': 'SAINT VINCENT AND THE GRENADINES',
	'WS': 'SAMOA',
	'SM': 'SAN MARINO',
	'ST': 'SAO TOME AND PRINCIPE',
	'SA': 'SAUDI ARABIA',
	'SN': 'SENEGAL',
	'RS': 'SERBIA',
	'SC': 'SEYCHELLES',
	'SL': 'SIERRA LEONE',
	'SG': 'SINGAPORE',
	'SX': 'SINT MAARTEN (DUTCH PART)',
	'SK': 'SLOVAKIA',
	'SI': 'SLOVENIA',
	'SB': 'SOLOMON ISLANDS',
	'SO': 'SOMALIA',
	'ZA': 'SOUTH AFRICA',
	'GS': 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS',
	'SS': 'SOUTH SUDAN',
	'ES': 'SPAIN',
	'LK': 'SRI LANKA',
	'SD': 'SUDAN',
	'SR': 'SURINAME',
	'SJ': 'SVALBARD AND JAN MAYEN',
	'SZ': 'SWAZILAND',
	'SE': 'SWEDEN',
	'CH': 'SWITZERLAND',
	'SY': 'SYRIAN ARAB REPUBLIC',
	'TW': 'TAIWAN, PROVINCE OF CHINA',
	'TJ': 'TAJIKISTAN',
	'TZ': 'TANZANIA, UNITED REPUBLIC OF',
	'TH': 'THAILAND',
	'TL': 'TIMOR-LESTE',
	'TG': 'TOGO',
	'TK': 'TOKELAU',
	'TO': 'TONGA',
	'TT': 'TRINIDAD AND TOBAGO',
	'TN': 'TUNISIA',
	'TR': 'TURKEY',
	'TM': 'TURKMENISTAN',
	'TC': 'TURKS AND CAICOS ISLANDS',
	'TV': 'TUVALU',
	'UG': 'UGANDA',
	'UA': 'UKRAINE',
	'AE': 'UNITED ARAB EMIRATES',
	'GB': 'UNITED KINGDOM',
	'US': 'UNITED STATES',
	'UM': 'UNITED STATES MINOR OUTLYING ISLANDS',
	'UY': 'URUGUAY',
	'UZ': 'UZBEKISTAN',
	'VU': 'VANUATU',
	'VE': 'VENEZUELA, BOLIVARIAN REPUBLIC OF',
	'VN': 'VIET NAM',
	'VG': 'VIRGIN ISLANDS, BRITISH',
	'VI': 'VIRGIN ISLANDS, U.S.',
	'WF': 'WALLIS AND FUTUNA',
	'EH': 'WESTERN SAHARA',
    'XK': 'KOSOVO, REPUBLIC OF',
	'YE': 'YEMEN',
	'ZM': 'ZAMBIA',
	'ZW': 'ZIMBABWE',
	'ZZ': 'Unknown or unspecified country'
}


# initialize counters
counter_lang = defaultdict(lambda: Counter())
counter_country = defaultdict(lambda: Counter())

# open the zipfile
with zipfile.ZipFile(args.input_path) as archive:

    # loop over every file within the zip file
    for i,filename in enumerate(archive.namelist()):
        print(datetime.datetime.now(),args.input_path,filename)

        # open the inner file
        with archive.open(filename) as f:

            # loop over each line in the inner file
            for line in f:

                # load the tweet as a python dictionary
                tweet = json.loads(line)

                # convert text to lower case
                text = tweet['text'].lower()

                # search hashtags
                for hashtag in hashtags:
                    lang = tweet['lang']
                    place = tweet['place']
		    # Set default country code to "ZZ"
                    country_code = "ZZ"
		    # If the place dictionary is not null, then get the country code.	 
                    if (place != None):
                        country_code = place['country_code']
                    # if there is no code then set it to ZZ which means
                    # unspecified.
                    if country_code == "":
                        country_code = "ZZ"
                    country = country_dict[country_code]
                    if hashtag in text:
                        counter_lang[hashtag][lang] += 1
                        counter_country[hashtag][country] += 1
                    counter_lang['_all'][lang] += 1
                    counter_country['_all'][country] += 1

# open the outputfile
try:
    os.makedirs(args.output_folder)
except FileExistsError:
    pass
output_path_base = os.path.join(args.output_folder,os.path.basename(args.input_path))

output_path_lang = output_path_base+'.lang'
output_path_country = output_path_base+'.country'
print('saving',output_path_lang)
print('saving',output_path_country)
with open(output_path_lang,'w') as f:
    f.write(json.dumps(counter_lang))
with open(output_path_country,'w') as f:
    f.write(json.dumps(counter_country))

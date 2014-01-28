import sys
import argparse
import subprocess
import os
import shutil
from os.path import expanduser
import codecs
from xml.dom.minidom import parse, parseString
import json

#Arguments
parser = argparse.ArgumentParser(description="Change the carrier name in the iOS Simulator")
parser.add_argument("-c", "--carrier", help="The new carrier name", type=str) 
parser.add_argument("-r", "--restore", help="Restore values from defaultValues.json", 
					action="store_true")
parser.add_argument("-b", "--backup", help="Generate defaultValues.json from current values. Don't do this if you've already changed the carrier name.", 
					action="store_true")
parser.add_argument("-l", "--languages", nargs='+', type=str, help="Provide a list of languages, by default, the carrier will be changed for all languages")
args = parser.parse_args()

#General purpose variables
json_data=open('./carrierDefaults.json').read()
defaults = json.loads(json_data)

all_langs = defaults["languages"]
# all_langs = ['ar', 'ca', 'cs', 'da', 'de', 'el', 'en_GB', 'en', 'es', 'fi', 'fr', 'he', 
# 'hr', 'hu', 'id', 'it', 'ja', 'ko', 'ms', 'nl', 'no', 'pl', 'pt_PT', 'pt', 'ro', 
# 'ru', 'sk', 'sv', 'th', 'tr', 'uk', 'vi', 'zh_CN', 'zh_TW']

#Paths
temp_path = expanduser("~") + "/Desktop/SpringBoard/"
production_path = ("/Applications/Xcode.app/Contents/Developer/Platforms/"
			"iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator7.0.sdk/System/"
			"Library/CoreServices/SpringBoard.app/")


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)



class CarrierChanger(object):
	"""Changes the carrier name in the iOS Simulator"""
	def __init__(self, langs, carrier):
		self.langs = langs
		self.carrier = carrier
		

	def print_description(self):
		print "Languages" + str(self.langs)
		print "Carrier: " + self.carrier

# Main methods
	def generate_defaults(self, langs):
		print "Generating defaultValues.json"
		defaults = {"languages": langs, "defaultValues": []}
		for index, lang in enumerate(langs):
			name = self.get_default_value(lang)
			defaults["defaultValues"].append({"language": lang, "carrierName" : name})

		# print json.dumps(defaults, sort_keys=True, indent=4, separators=(',', ': '))
		for item in defaults["defaultValues"]:
			print item["language"] +": " + item["carrierName"]
		self.save_defaults_to_file(defaults)

	def change_carrier_name(self, langs, new_name):
		for lang in langs:
			print "Changing carrier name for "+lang +" to: "+new_name
			self.copy_source_file(lang)
			self.convert_binary_to_xml(lang)
			self.manipulate_carrier_name(lang, new_name)
			self.copy_changed_file_into_production(lang)

	def restore_defaults(self):
		print "Restoring defaults from json file"
		for item in defaults["defaultValues"]:
			# print item["language"] + ": " + item["carrierName"]
			language = item["language"]
			name = item["carrierName"]
			self.change_carrier_name([language], name)

# Helpers
	def copy_source_file(self, lang):
	# Copy the files to a folder on the desktop
		src = (production_path+lang+".lproj/SpringBoard.strings")
		dst = temp_path
		ensure_dir(dst)
		filename = "SpringBoard-"+lang+".strings"
		dst = dst + filename
		shutil.copyfile(src, dst)

	def convert_binary_to_xml(self, lang):
		os.system("plutil -convert xml1 "+temp_path+"SpringBoard-"+lang+".strings")

	def manipulate_carrier_name(self, lang, carrierName):
		filename = temp_path + "SpringBoard-"+lang+".strings"
		content = open(filename)
		
		content = parse(content)
		dictElement = content.getElementsByTagName("dict")[0]
		
		keys = dictElement.getElementsByTagName("key")
		strings = dictElement.getElementsByTagName("string")
		
		for index, key in enumerate(keys):
			if (key.firstChild.nodeValue == "SIMULATOR_CARRIER_STRING"):
				print lang+": "+ strings[index].firstChild.nodeValue + " --> " + carrierName
				strings[index].firstChild.nodeValue = carrierName

		self.save_xml_content_to_file(lang, content.toxml())

	def save_xml_content_to_file(self, lang, xml_content):
		filename = temp_path+"/"+lang+"/SpringBoard.strings"
		ensure_dir(filename)
		if os.path.isfile(filename):
			os.remove(filename)

		f = codecs.open(filename,'a+',encoding='utf-8')
		f.write(xml_content)
		f.close()

	def copy_changed_file_into_production(self, lang):
		src = temp_path+"/"+lang+"/SpringBoard.strings"
		dst = ( production_path+lang+".lproj/SpringBoard.strings")
		shutil.copyfile(src, dst)

	def save_defaults_to_file(self, defaults):
		print "Saving carrierDefaults.json"
		filename = "./carrierDefaults.json"
		ensure_dir(filename)
		if os.path.isfile(filename):
			os.remove(filename)

		f = codecs.open(filename,'a+',encoding='utf-8')
		dump = json.dumps(defaults, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
		# print dump
		f.write(dump)
		f.close()

	def get_default_value(self, lang):
		self.copy_source_file(lang)
		self.convert_binary_to_xml(lang)
		filename = temp_path + "SpringBoard-"+lang+".strings"
		content = open(filename)
		content = parse(content)
		dictElement = content.getElementsByTagName("dict")[0]
		keys = dictElement.getElementsByTagName("key")
		strings = dictElement.getElementsByTagName("string")
		
		for index, key in enumerate(keys):
			if (key.firstChild.nodeValue == "SIMULATOR_CARRIER_STRING"):
				return strings[index].firstChild.nodeValue


#-----------------------------------------------------------
# Go through the args
if not args.restore and not args.carrier and not args.backup:
	parser.print_help()
	sys.exit()
else:
	changer = CarrierChanger([], "")

if args.restore:
    changer.restore_defaults()

if args.backup:
	changer.generate_defaults(all_langs)



if args.languages and not args.restore and not args.backup:
	all_clear = True
	# Make sure the languages are all valid
	for lang in args.languages:
		if not lang in all_langs:
			all_clear = False
			print lang + " not valid."
	if all_clear:
		changer.langs = args.languages
		changer.print_description()
	else:
		print "Please check your languages."
		sys.exit()
else:
	changer.langs = all_langs

if args.carrier:
	changer.carrier = args.carrier
	changer.change_carrier_name(changer.langs, changer.carrier)




		
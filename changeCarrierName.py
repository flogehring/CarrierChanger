
import subprocess
import os
import shutil
from os.path import expanduser
import codecs
from xml.dom.minidom import parse, parseString
import json




def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def tempPath():
	path = expanduser("~")
	# path = ""
	path = path +"/Desktop/SpringBoard/"
	return path;

def copySourceFile(lang):

	# Copy the files to a folder on the desktop
	src = ("/Applications/Xcode.app/Contents/Developer/Platforms/"
			"iPhoneSimulator.platform/Developer/SDKs"
			"/iPhoneSimulator7.0.sdk/System/Library/CoreServices/"
			"SpringBoard.app/"+lang+".lproj/SpringBoard.strings" )
	dst = tempPath()
	ensure_dir(dst)
	filename = "SpringBoard-"+lang+".strings"
	dst = dst + filename
	shutil.copyfile(src, dst)

def convertBinaryToXML(lang):
	os.system("plutil -convert xml1 "+tempPath()+"SpringBoard-"+lang+".strings")

def manipulateCarrierName(lang, carrierName):
# codecs.open(filename,'a+',encoding='utf-8')
	filename = tempPath() + "SpringBoard-"+lang+".strings"
	# content = codecs.open(filename, encoding='utf-8')
	content = open(filename)
	
	content = parse(content)
	dictElement = content.getElementsByTagName("dict")[0]
	
	keys = dictElement.getElementsByTagName("key")
	strings = dictElement.getElementsByTagName("string")
	
	for index, key in enumerate(keys):
		if (key.firstChild.nodeValue == "SIMULATOR_CARRIER_STRING"):
			print lang+": "+ strings[index].firstChild.nodeValue
			strings[index].firstChild.nodeValue = carrierName
			print lang+": "+ strings[index].firstChild.nodeValue

	saveXMLContentToFile(lang, content.toxml())

def saveXMLContentToFile(lang, xml):
	filename = tempPath()+"/"+lang+"/SpringBoard.strings"
	ensure_dir(filename)
	if os.path.isfile(filename):
		os.remove(filename)

	f = codecs.open(filename,'a+',encoding='utf-8')
	f.write(xml)
	f.close()

def copyChangedFileIntoProduction(lang):
	src = tempPath()+"/"+lang+"/SpringBoard.strings"
	dst = ( "/Applications/Xcode.app/Contents/Developer/Platforms/"
			"iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator7.0.sdk/System/"
			"Library/CoreServices/SpringBoard.app/"+lang+".lproj/SpringBoard.strings")
	# print dst
	shutil.copyfile(src, dst)

def changeCarrierName(langs, new_name):
	for lang in langs:
		print "Changing carrier name for "+lang
		copySourceFile(lang)
		convertBinaryToXML(lang)
		manipulateCarrierName(lang, new_name)
		copyChangedFileIntoProduction(lang)



# Generating the defaults
def getDefaultValue(lang):
	copySourceFile(lang)
	convertBinaryToXML(lang)
	filename = tempPath() + "SpringBoard-"+lang+".strings"
	content = open(filename)
	content = parse(content)
	dictElement = content.getElementsByTagName("dict")[0]
	keys = dictElement.getElementsByTagName("key")
	strings = dictElement.getElementsByTagName("string")
	
	for index, key in enumerate(keys):
		if (key.firstChild.nodeValue == "SIMULATOR_CARRIER_STRING"):
			return strings[index].firstChild.nodeValue

def generateDefaults(langs):
	defaults = {"languages": langs, "defaultValues": []}
	for index, lang in enumerate(langs):
		name = getDefaultValue(lang)
		defaults["defaultValues"].append({"language": lang, "carrierName" : name})

	# print json.dumps(defaults, sort_keys=True, indent=4, separators=(',', ': '))
	for item in defaults["defaultValues"]:
		print item["language"] +": " + item["carrierName"]
	saveDefaultsToFile(defaults)

def saveDefaultsToFile(defaults):
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

# Restoring
def restoreDefaults():
	json_data=open('./carrierDefaults.json').read()
	defaults = json.loads(json_data)
	for item in defaults["defaultValues"]:
		print item["language"] + ": " + item["carrierName"]
		language = item["language"]
		name = item["carrierName"]
		changeCarrierName([language], name)


all_langs = ['ar', 'ca', 'cs', 'da', 'de', 'el', 'en_GB', 'en', 'es', 'fi', 'fr', 'he', 
'hr', 'hu', 'id', 'it', 'ja', 'ko', 'ms', 'nl', 'no', 'pl', 'pt_PT', 'pt', 'ro', 
'ru', 'sk', 'sv', 'th', 'tr', 'uk', 'vi', 'zh_CN', 'zh_TW']

langs = ['de', 'en', 'fr', 'sv', 'da', 'hu', 'pt', 'cs', 'sk', 'pl', 'nl', 'no', 'ro']


# Functions
# generateDefaults(all_langs)
# changeCarrierName(all_langs, "My carrier")
# restoreDefaults()








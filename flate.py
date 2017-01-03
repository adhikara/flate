# FR-EN translator using multiple methods

import sys
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen
try:
    import simplejson as json
except (ImportError):
    import json
from urllib.parse import quote
from bs4 import BeautifulSoup
import string
from wiktionaryparser import WiktionaryParser
import requests

parser = WiktionaryParser()
parser.set_default_language('french')
wordie = quote(sys.argv[1])

def local (word): # search through the wiktionary dumps

	word = word.lower()
	try:
		file1 = open("dictionary/"+word[:1]+".txt", "r")
		for string in file1:
			collection = string.split(";")
			if (collection[0] == word):
				answer = collection[3] # need to learn how to send an array of definitions & have html handle them
				file1.close()

				a2 = checkPP(answer)

				if a2 != "nothing":
					answer = a2 #+ " [local]"
				return answer #+ " [local]"

		file1.close()
		answer = "word not found"
		return answer
	except:
		answer = "word not found"
		return answer

def wiki1 (word): # search using WiktionaryParser
	word = word.lower()
	wikiAns = parser.fetch(word)
	if (wikiAns != []):
		try:
			output = wikiAns[0]['definitions'][0]['text']
			responses = output.split("\n")
			answer = responses[1]
			file2 = open("dictionary/"+word[:1]+".txt", "a")
			file2.write(word+";X;TR-FR-EN;"+answer+";X;\n")
			file2.close()
			return answer
		except IndexError:
			answer = "word not found"
			return answer
	answer = "word not found"
	return answer

def wiki2 (word):

#
# search through wiktionaryparser for the past participle or pronoun.
# will need to modify for new classes of words when lookup fails.
#
	word = word.lower()
	wikiLink = "https://en.wiktionary.org/w/api.php?format=json&action=query&titles="+word+"&rvprop=content&prop=revisions&redirects=1" 
	wikii = requests.get(wikiLink)
	wikiJSON = wikii.json()

	try:
		for pageId in wikiJSON["query"]["pages"]:
			output = wikiJSON["query"]["pages"][pageId]["revisions"][0]["*"]
		try:
			arr = output.split("----")
		except:
			arr = output

		lookAt = []
		for y in arr:
			if "=French=" in y:
				lookAt.append(y)

		if len(lookAt) > 0:
			temp = lookAt[0].split("\n\n")
			lookAt = temp
		else:
			toReturn = "word not found"
			return toReturn

		definitions = []
		for x in lookAt:
			if x.startswith("#"):
				transform = ['#', "{", "}", "[", "]", "'", ":", '"']
				transform2 = ["|"]
				translator = str.maketrans({key: None for key in transform})
				translator2 = str.maketrans({key: " " for key in transform2})
				x = x.translate(translator)
				x = x.translate(translator2)
				definitions.append(x[1:])
				definitions = definitions[0].split("\n")

		if (checkPP(definitions[0]) != "nothing"):
			toReturn = checkPP(definitions[0]) #+ " [wik]"
			#print toReturn
		else:
			toReturn = definitions[0] #+ " [wiki2]"
	except IndexError:
		toReturn = "word not found"
	
	return toReturn

def checkPP(word): # find definition of the past participle or forms of adjectives
	options = ['singular of', 'plural of', 'participle of', 'inflection of','present indicative', 'conditional of']

	for d in options:
		if d in word:
			arr = word.split(" ")
			for x in range (0, len(arr)-1):
				if arr[x] == "of":
					lookup = arr[x+1]
			tryThis = tryDefine(lookup)
			if(tryThis != "word not found"):
				return tryThis
	return "nothing"

def linguee(word):

#
# crawl through linguee for a definition.
# will create new functions for API calls to Collins, Oxford, Glosbed etc when I get API keys for them approved
#
# will rely on Glosbed as a secondary look-up service, with Collins next and Linguee as a last option.
#
	word = word.lower()
	lingueeLink = "http://www.linguee.com/english-french/search?source=auto&query=" + quote(word)
	page = urlopen(lingueeLink)
	initial = BeautifulSoup(page, "html.parser")
	definition = initial.find('a', class_="dictLink featured")

	if definition is not None:
		definition = initial.find('a', class_="dictLink featured").get_text()
		file2 = open("dictionary/"+word[:1]+".txt", "a")
		file2.write(word+";X;TR-FR-EN;"+definition+";X;\n")
		file2.close()
	else:
		definition = "word not found"
	return definition + " [l]"


def tryDefine(word): # generate the translation

	# the API does NOT like it when you include these

	wikiNotLikey = ["d’", "l’", "n’", "s’", "s'", "d'", "l'", "n'"]

	if "\xa0" in word:
		word = word[3:]
	if "qu'" in word:
		word = word[3:]
	if "qu’" in word:
		word = word[3:]

	for notLike in wikiNotLikey:
		if notLike in word:
			word = word[2:]

	localSearch = local(word) # METHOD 1 = Look through Wiktionary dumps

	if localSearch != "word not found":
		return localSearch

	parserSearch = wiki1(word) # METHOD 2 = Look through Wiktionary using JSON parser

	if parserSearch != "word not found":
		return parserSearch

	wikiSearch = wiki2(word) # METHOD 3 = Look through Wiktionary dumps for nuances like participles and singulars

	if wikiSearch != "word not found":
		return wikiSearch

	return linguee(word) # METHOD 4 = crawl through Linguee as a final recourse

def flate (word):
	try:
		return tryDefine(word)
	except:
		return "word not found"


print (flate(wordie))
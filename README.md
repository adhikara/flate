# flate

In a nutshell: translate from french to english.

# usage

You need to first `pip install wiktionaryparser` and `bs4`.

Then simply use `python flate.py [french word]`.

# about flate

This code relies on Wiktionary to translate from french to English. To make things faster, this is the order it follows to retreive the translation:

* search in the local Wiktionary dump I downloaded from this [repository](https://github.com/pquentin/wiktionary-translations)
* search using the wiktionaryparser (will probably get rid of eventually)
* search Wiktionary using a function I created
* search Linguee (scraping)

This code also returns the infinitive's meaning for words in the past participle and other forms. Wikitionary does not currently support this directly.

# warning

* Linguee has rules about how it is used. Consult [them](http://www.linguee.com/english-french/page/termsAndConditions.php)
* This code is not finished yet. Currently it does not support lookup for terms like "l'homme", as opposed to "homme"
* Only the first definition retrieved is returned. This is silly, I know, but I have not expanded it as I'm still testing this

# the future

* I want to transfer the text files dictionary into a SQLite or PostgreSQL database

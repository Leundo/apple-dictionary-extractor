import sqlite3
import os
import json
from ADParser.xml_parser import AppleDictionary

DICTIONARY_TABLE_NAME_DIC = {
	AppleDictionary.SIMPLIFIED_CHINESE_JAPANESE: 'SCJ'
}

DATABASE_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'dictionary.db')

def creat_table(dictionary):
	con = sqlite3.connect(DATABASE_FILE_PATH)
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS %s' % DICTIONARY_TABLE_NAME_DIC[dictionary])
	if dictionary == AppleDictionary.SIMPLIFIED_CHINESE_JAPANESE:
		cur.execute("""
			CREATE TABLE %s(
			idx CHAR(50) PRIMARY KEY NOT NULL,
			title CHAR(50) NOT NULL,
			prn CHAR(50),
			json TEXT NOT NULL
			)
			""" % DICTIONARY_TABLE_NAME_DIC[dictionary])
	con.commit()
	con.close()

def insert_entry(entry_it, dictionary):
	con = sqlite3.connect(DATABASE_FILE_PATH)
	cur = con.cursor()
	if dictionary == AppleDictionary.SIMPLIFIED_CHINESE_JAPANESE:
		for entry in entry_it:
			cur.execute("""
				INSERT INTO %s (idx, title, prn, json) VALUES (?, ?, ?, ?)
				""" % DICTIONARY_TABLE_NAME_DIC[dictionary],
				(entry['idx'], entry['title'], entry['prn'], json.dumps(entry, indent=None, ensure_ascii=False)))
	con.commit()
	con.close()

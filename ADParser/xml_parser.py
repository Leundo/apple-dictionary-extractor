import xml.sax
import json
from enum import Enum
import os
from ADParser.scjd_controller import SCJDController


DEBUG_XML_PATH = os.path.join(os.path.dirname(__file__), 'log', 'error.xml')

class AppleDictionary(Enum):
	SIMPLIFIED_CHINESE_JAPANESE = 0


class DictionaryHandler(xml.sax.ContentHandler):

	handler_cache = {}

	def __init__(self, dictionary, debug=False):
		self.controller = None
		if dictionary == AppleDictionary.SIMPLIFIED_CHINESE_JAPANESE:
			self.controller = SCJDController(debug)
	
	def startElement(self, tag, attrs):
		self.controller.startElement(tag, attrs)

	def endElement(self, tag):
		self.controller.endElement(tag)

	def characters(self, chars):
		self.controller.characters(chars)

	def startDocument(self):
		self.controller.startDocument()

	def endDocument(self):
		self.controller.endDocument()
		DictionaryHandler.handler_cache = self.controller.get_entry()


def parse_xml(xml_it, dictionary, debug=False):
	handler = DictionaryHandler(dictionary, debug)
	for item in xml_it:
		try:
			xml.sax.parseString(item, handler)
		except:
			if True:
				with open(DEBUG_XML_PATH, 'w') as f:
					f.write(f'{item}')
			raise
		if 'idx' in DictionaryHandler.handler_cache:
			yield DictionaryHandler.handler_cache

def test_xml_file(dictionary, path):
	with open(path, 'r') as f:
		for item in parse_xml(iter([f.read()]), dictionary, debug=True):
			pass

def test_dump_file(line_num, dictionary, path='../xml/dump.xml'):
	with open(path, 'r') as f:
		for i, line in enumerate(f.readlines()):
			if i == line_num:
				for item in parse_xml(iter(eval(line)), dictionary, debug=True):
					pass


if __name__ == '__main__':
	test_dump_file(235, AppleDictionary.SIMPLIFIED_CHINESE_JAPANESE)
	test_xml_file(AppleDictionary.SIMPLIFIED_CHINESE_JAPANESE, '../xml/IT.xml')


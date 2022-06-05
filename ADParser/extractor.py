import zlib
import itertools
import os
from ADParser.xml_parser import parse_xml, AppleDictionary

__DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'simplified_chinese_japanese.data')


def parse_xml_factory(dictionary):
	def parse_xml_(xml_it):
		return parse_xml(xml_it, dictionary)
	return parse_xml_

def deliver_factory():
	def deliver(xml_it):
		for item in xml_it:
			yield item
	return deliver

def print_entry_title_factory():
	def print_entry_title(entry_it):
		for entry in entry_it:
			print(entry['title'])
	return print_entry_title

def print_factory():
	def print_(entry_it):
		for entry in entry_it:
			print(entry)
	return print_

def save_factory(path):
	def save(entry_it):
		with open(path, 'a+') as f:
			f.write(f'{list(entry_it)}\n')
	return save

"""
Any adjacent XML strings are separated by LF character and 4 bytes, so total separated bytes is 5.
"""
def split(input_bytes):
	input_bytes = input_bytes[4:]
	while True:
		try:
			next_offset = input_bytes.index('\n'.encode('utf-8'))
		except ValueError:
			break
		entry_text = input_bytes[:next_offset].decode('utf-8')
		yield entry_text
		input_bytes = input_bytes[next_offset + 5:]

"""
The Apple dictoinary data file structure is like this:
file.data = <Header> [ <Zip Block> <Unknown Block> ](repate)
Anyway, there Zip Blocks are concatenated together at intervals of Unknown Blocks.
"""
def read_date(path=__DATA_FILE_PATH):
	with open(path, 'rb') as f:
		content_bytes = f.read()
	while True:
		decompressobj = zlib.decompressobj()
		try:
			content_decompressed = decompressobj.decompress(content_bytes)
		except zlib.error:
			content_bytes = content_bytes[1:]
		else:
			yield content_decompressed
			content_bytes = decompressobj.unused_data
			if len(content_bytes) == 0:
				break

def extract(handle, store, path):
	date_it = read_date(path)
	for entry_it in map(handle, map(split, date_it)):
		store(entry_it)


if __name__ == '__main__':

	pass






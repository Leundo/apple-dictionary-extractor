import os
from ADParser.xml_parser import AppleDictionary as AD, test_xml_file, test_dump_file
import ADParser.extractor as e

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'simplified_chinese_japanese.data')

if __name__ == '__main__':

	# e.extract(handle=e.deliver_factory(), store=e.save_factory('xml/dump.xml'), path=DATA_FILE_PATH)
	# e.extract(handle=e.deliver_factory(), store=e.print_factory(), path=DATA_FILE_PATH)
	# e.extract(handle=e.parse_xml_factory(AD.SIMPLIFIED_CHINESE_JAPANESE), store=e.print_entry_title_factory(), path=DATA_FILE_PATH)
	e.extract(handle=e.parse_xml_factory(AD.SIMPLIFIED_CHINESE_JAPANESE), store=e.save_entry_to_db_factory(AD.SIMPLIFIED_CHINESE_JAPANESE), path=DATA_FILE_PATH, pre_execute=e.creat_table_factory(AD.SIMPLIFIED_CHINESE_JAPANESE), is_tqdm=True)

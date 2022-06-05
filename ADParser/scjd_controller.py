import functools
from enum import Enum
import json
import re

class SCJDEntry:
	def __init__(self):
		self.data = {}

	def set_title(self, title):
		self.data['title'] = title

	def set_id(self, idx):
		self.data['idx'] = idx

	def glue_pronounce(self, prn):
		if 'prn' in self.data:
			self.data['prn'] += prn
		else:
			self.data['prn'] = prn

	def push_kanji(self, kanji):
		if 'kanjis' in self.data:
			self.data['kanjis'].append(kanji)
		else:
			self.data['kanjis'] = [kanji]

	def push_void_definition(self):
		if 'defs' in self.data:
			self.data['defs'].append({})
		else:
			self.data['defs'] = [{}]

	def set_definition_order(self, order):
		self.data['defs'][-1]['order'] = order


	def glue_definition_indicator(self, ind):
		if 'defs' in self.data:
			if 'ind' in self.data['defs'][-1]:
				self.data['defs'][-1]['ind'] += ind
			else:
				self.data['defs'][-1]['ind'] = ind


	def push_definition_chinese_translation(self, trans):
		if 'chi_transs' in self.data['defs'][-1]:
			self.data['defs'][-1]['chi_transs'].append(trans)
		else:
			self.data['defs'][-1]['chi_transs'] = [trans]

	def push_definition_english_translation(self, trans):
		if 'eng_transs' in self.data['defs'][-1]:
			self.data['defs'][-1]['eng_transs'].append(trans)
		else:
			self.data['defs'][-1]['eng_transs'] = [trans]

	def push_void_definition_sentence_example(self):
		if 'sent_exs' in self.data['defs'][-1]:
			self.data['defs'][-1]['sent_exs'].append({})
		else:
			self.data['defs'][-1]['sent_exs'] = [{}]

	def glue_definition_sentence_example(self, jpn_sent, chi_sent):
		if jpn_sent is not None:
			if 'jpn_sent' in self.data['defs'][-1]['sent_exs'][-1]:
				self.data['defs'][-1]['sent_exs'][-1]['jpn_sent'] += jpn_sent
			else:
				self.data['defs'][-1]['sent_exs'][-1]['jpn_sent'] = jpn_sent

		if chi_sent is not None:
			if 'chi_sent' in self.data['defs'][-1]['sent_exs'][-1]:
				self.data['defs'][-1]['sent_exs'][-1]['chi_sent'] += chi_sent
			else:
				self.data['defs'][-1]['sent_exs'][-1]['chi_sent'] = chi_sent

	def push_void_phrase(self):
		if 'phrs' in self.data:
			self.data['phrs'].append({})
		else:
			self.data['phrs'] = [{}]

	def set_phrase_idx(self, idx):
		self.data['phrs'][-1]['idx'] = idx

	def glue_phrase_first_title(self, title):
		if 'titles' in self.data['phrs'][-1]:
			self.data['phrs'][-1]['titles'][0] += title
		else:
			self.data['phrs'][-1]['titles'] = [title]

	def push_phrase_title(self, title):
		self.data['phrs'][-1]['titles'].append(title)

	def push_void_phrase_section(self):
		if 'secs' in self.data['phrs'][-1]:
			self.data['phrs'][-1]['secs'].append({})
		else:
			self.data['phrs'][-1]['secs'] = [{}]

	def push_phrase_section_translation(self, trans):
		if 'transs' in self.data['phrs'][-1]['secs'][-1]:
			self.data['phrs'][-1]['secs'][-1]['transs'].append(trans)
		else:
			self.data['phrs'][-1]['secs'][-1]['transs'] = [trans]

	def push_void_phrase_section_sentence_example(self):
		if 'sent_exs' in self.data['phrs'][-1]['secs'][-1]:
			self.data['phrs'][-1]['secs'][-1]['sent_exs'].append({})
		else:
			self.data['phrs'][-1]['secs'][-1]['sent_exs'] = [{}]

	def glue_phrase_section_sentence_example(self, jpn_sent, chi_sent):
		if jpn_sent is not None:
			if 'jpn_sent' in self.data['phrs'][-1]['secs'][-1]['sent_exs'][-1]:
				self.data['phrs'][-1]['secs'][-1]['sent_exs'][-1]['jpn_sent'] += jpn_sent
			else:
				self.data['phrs'][-1]['secs'][-1]['sent_exs'][-1]['jpn_sent'] = jpn_sent

		if chi_sent is not None:
			if 'chi_sent' in self.data['phrs'][-1]['secs'][-1]['sent_exs'][-1]:
				self.data['phrs'][-1]['secs'][-1]['sent_exs'][-1]['chi_sent'] += chi_sent
			else:
				self.data['phrs'][-1]['secs'][-1]['sent_exs'][-1]['chi_sent'] = chi_sent





	def get_data(self):
		return self.data

class SCJDStateMachine:
	class Node(Enum):
		IGNORE = 0
		ROOT = 1
		D_ENTRY = 2
		D_PRN = 3
		D_DEF = 4
		A = 5

		HWG_SPAN = 10
		HW_SPAN = 11
		HV_SPAN = 12
		GRAMB_SPAN = 13
		SEMB_SPAN = 14
		TRG_SPAN = 15
		OUP_LABEL_SPAN = 16
		TRANS_SPAN = 17
		IDMB_SPAN = 18
		IDMSEC_SPAN = 19
		IDM_SPAN = 20
		EXG_SPAN = 21
		EX_SPAN = 22
		IND_SPAN = 23
		CB_SPAN = 24
		CSEC_SPAN = 25
		CW_SPAN = 26
		CV_SPAN = 27


	class State(Enum):
		NUMBNESS = 0
		BEGIN = 1

		GRAMB = 10
		GRAMB_SEMB = 11
		GRAMB_OUP_LABEL = 12
		GRAMB_TRG_AFTER_OUP_LABEL = 13
		GRAMB_EXG = 14

		IDMB = 20
		IDMB_FIRST_IDM = 21
		IDMB_NOT_FIRST_IDM = 22
		IDMB_SEMB = 23
		IDMB_EXG = 24

		CB = 30
		CB_GRAMB = 31
		CB_SEMB = 32
		CB_EXG = 33

		def get_gramb_cluster():
			return [SCJDStateMachine.State.GRAMB, SCJDStateMachine.State.GRAMB_SEMB, SCJDStateMachine.State.GRAMB_OUP_LABEL, SCJDStateMachine.State.GRAMB_EXG, SCJDStateMachine.State.GRAMB_TRG_AFTER_OUP_LABEL]

		def get_idmb_cluster():
			return [SCJDStateMachine.State.IDMB, SCJDStateMachine.State.IDMB_FIRST_IDM, SCJDStateMachine.State.IDMB_NOT_FIRST_IDM, SCJDStateMachine.State.IDMB_SEMB, SCJDStateMachine.State.IDMB_EXG]

		def get_cb_cluster():
			return [SCJDStateMachine.State.CB, SCJDStateMachine.State.CB_GRAMB, SCJDStateMachine.State.CB_SEMB, SCJDStateMachine.State.CB_EXG]

	IGNORE_SPAN = {'hvg', 'gp', 'x_xoh', 'ty_pinyin', 'x_xdh', 'sn', 'gl', 'cwg', 'cvg', 'tail', 'ty_日中比較', 'x_xopt', 'pr', 'ty_参考', 'ty_参考参照', 'ty_項目参照', 'ty_注意', 'gr', 'ty_文化', 'ph', 'xr', 'xrlabelGroup', 'xrlabel', 'underline'}
	INHERIT_SPAN = {'rf', 'tg_ind', 't_fld', 'subEnt'}

	def __init__(self):
		self.reinit()

	def reinit(self):
		self.stk = [SCJDStateMachine.Node.ROOT]
		self.sta = SCJDStateMachine.State.BEGIN

	def get_node(self):
		return self.stk[-1]

	def get_state(self):
		return self.sta

	def push_node(self, node):
		self.stk.append(node)

	def pop_node(self):
		return self.stk.pop()

	def numb(self):
		self.sta = SCJDStateMachine.State.NUMBNESS

	def is_numb(self):
		return self.get_state() == SCJDStateMachine.State.NUMBNESS

	def startelement_move(self, tag, attrs):

		if tag == 'd:entry':
			self.push_node(SCJDStateMachine.Node.D_ENTRY)

		elif tag == 'span':
			attrs_keys = attrs.getQNames()
			if 'class' in attrs_keys:
				attrs_class_values = attrs['class'].split(' ')

				if not SCJDStateMachine.INHERIT_SPAN.isdisjoint(attrs_class_values):
					self.push_node(self.get_node())

				elif not SCJDStateMachine.IGNORE_SPAN.isdisjoint(attrs_class_values):
					self.push_node(SCJDStateMachine.Node.IGNORE)

				elif 'hwg' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.HWG_SPAN)

				elif 'hw' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.HW_SPAN)

				elif 'hv' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.HV_SPAN)

				elif 'gramb' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.GRAMB_SPAN)
					if self.get_state() == SCJDStateMachine.State.BEGIN:
						self.sta = SCJDStateMachine.State.GRAMB

					elif self.get_state() in SCJDStateMachine.State.get_cb_cluster():
						self.sta = SCJDStateMachine.State.CB_GRAMB

					else:
						raise RuntimeError(f'{self.get_state()}')

				elif 'semb' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.SEMB_SPAN)

					if self.get_state() in SCJDStateMachine.State.get_gramb_cluster():
						self.sta = SCJDStateMachine.State.GRAMB_SEMB

					elif self.get_state() in SCJDStateMachine.State.get_idmb_cluster():
						self.sta = SCJDStateMachine.State.IDMB_SEMB

					elif self.get_state() in SCJDStateMachine.State.get_cb_cluster():
						self.sta = SCJDStateMachine.State.CB_SEMB

					else:
						raise RuntimeError(f'{self.get_state()}')

				elif 'trg' in attrs_class_values:
					"""
					Generally, there is only one "oup_label" span in "gramb-semb" span, except in some rare cases.
					This happens when there is more than one kinds of translation in one "gramb-semb" span.
					An example is where id = j_CRJC000115, and title = 相手役.
					That "[芝居など] 配角" and "[ダンス] 舞伴" show up here is weird.
					And this is the reason why I put "tg_ind" span into INHERIT_SPAN instead of IGNORE_SPAN.
					Otherwise, key of ind in entry will become "芝居などダンス" instead of "[芝居など][ダンス]".
					"""
					if 'x_xd2' in attrs_class_values:
						if self.get_state() == SCJDStateMachine.State.GRAMB_OUP_LABEL:
							self.sta = SCJDStateMachine.State.GRAMB_TRG_AFTER_OUP_LABEL

						elif self.get_state() == SCJDStateMachine.State.GRAMB_EXG:
							pass

						elif self.get_state() == SCJDStateMachine.State.GRAMB_SEMB:
							pass

						elif self.get_state() == SCJDStateMachine.State.GRAMB_TRG_AFTER_OUP_LABEL:
							pass

						else:
							raise RuntimeError(f'{self.get_state()}')

					self.push_node(SCJDStateMachine.Node.TRG_SPAN)

				elif 'oup_label' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.OUP_LABEL_SPAN)

					if self.get_state() == SCJDStateMachine.State.GRAMB_SEMB:
						self.sta = SCJDStateMachine.State.GRAMB_OUP_LABEL

					elif self.get_state() == SCJDStateMachine.State.GRAMB_TRG_AFTER_OUP_LABEL:
						self.sta = SCJDStateMachine.State.GRAMB_OUP_LABEL

						"""
						Generally, there is no "oup_label" span in "idmb" span, except in some rare cases.
						An example is where id = j_CRJC010600, and title = 塞翁が馬.
						"""
					elif self.get_state() == SCJDStateMachine.State.IDMB_SEMB:
						pass

					else:
						raise RuntimeError(f'{self.get_state()}')

				elif 'trans' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.TRANS_SPAN)

				elif 'idmb' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.IDMB_SPAN)
					self.sta = SCJDStateMachine.State.IDMB

				elif 'idmsec' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.IDMSEC_SPAN)

				elif 'idm' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.IDM_SPAN)

					if self.get_state() == SCJDStateMachine.State.IDMB or self.get_state() == SCJDStateMachine.State.IDMB_EXG or self.get_state() == SCJDStateMachine.State.IDMB_SEMB:
						self.sta = SCJDStateMachine.State.IDMB_FIRST_IDM

					elif self.get_state() == SCJDStateMachine.State.IDMB_FIRST_IDM:
						self.sta = SCJDStateMachine.State.IDMB_NOT_FIRST_IDM

				elif 'exg' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.EXG_SPAN)

					if self.get_state() in SCJDStateMachine.State.get_gramb_cluster():
						self.sta = SCJDStateMachine.State.GRAMB_EXG

					elif self.get_state() in SCJDStateMachine.State.get_idmb_cluster():
						self.sta = SCJDStateMachine.State.IDMB_EXG

					elif self.get_state() in SCJDStateMachine.State.get_cb_cluster():
						self.sta = SCJDStateMachine.State.CB_EXG

					else:
						raise RuntimeError(f'{self.get_state()}')

				elif 'ex' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.EX_SPAN)

				elif 'ind' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.IND_SPAN)

				elif 'fld' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.IND_SPAN)

				elif 'cb' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.CB_SPAN)
					self.sta = SCJDStateMachine.State.CB

				elif 'csec' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.CSEC_SPAN)

				elif 'cw' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.CW_SPAN)

				elif 'cv' in attrs_class_values:
					self.push_node(SCJDStateMachine.Node.CV_SPAN)

				else:
					raise RuntimeError(f"SPAN with {attrs_class_values} in class key is not defined")

			else:
				raise RuntimeError(f"SPAN with {attrs_keys} key is not defined")

		elif tag == 'd:prn':
			self.push_node(SCJDStateMachine.Node.D_PRN)

		elif tag == 'd:def':
			self.push_node(SCJDStateMachine.Node.D_DEF)

		elif tag == 'a':
			self.push_node(SCJDStateMachine.Node.A)

		else:
			raise RuntimeError(f"TAG {tag} is not defined")

	def endelement_move(self, tag):
		self.pop_node()
		
	def startdocument_move(self):
		self.reinit()

	def enddocument_move(self):
		pass



def log(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if args[0].debug:
			if func.__name__ == 'startElement':
				print(f'SM: {args[0].sm.stk}, State: {args[0].sm.sta}')
				print(f'Tag: {args[1]}, class: {args[2].getValueByQName("class") if "class" in args[2].getQNames() else None}')
				print(f'{args[0].entry.get_data()}')
				print(f'==========')
			elif func.__name__ == 'endElement':
				print(f'Tag: {args[1]}')
				print(f'==========')
			elif func.__name__ == 'characters':
				print(f'Chars: {args[1]}')
				print(f'==========')
		return func(*args, **kwargs)
	return wrapper


class SCJDController:
	def __init__(self, debug=False):
		self.reinit()
		self.debug = debug

	def reinit(self):
		self.sm = SCJDStateMachine()
		self.entry = SCJDEntry()

	def get_entry(self):
		return self.entry.data

	@log
	def startElement(self, tag, attrs):
		if self.sm.is_numb():
			return

		self.sm.startelement_move(tag, attrs)

		if self.sm.get_node() == SCJDStateMachine.Node.D_ENTRY:
			if re.search("^j_CRJC.*", attrs['id']) is not None:
				self.entry.set_title(attrs['d:title'])
				self.entry.set_id(attrs['id'])
			else:
				self.sm.numb()

		elif self.sm.get_node() == SCJDStateMachine.Node.SEMB_SPAN:
			if self.sm.get_state() in SCJDStateMachine.State.get_gramb_cluster():
				self.entry.push_void_definition()
				if 'ord' in attrs.getQNames():
					self.entry.set_definition_order(attrs['ord'])
				else:
					self.entry.set_definition_order('1')

			elif self.sm.get_state() in SCJDStateMachine.State.get_idmb_cluster():
				self.entry.push_void_phrase_section()

			elif self.sm.get_state() in SCJDStateMachine.State.get_cb_cluster():
				self.entry.push_void_phrase_section()

			else:
				raise RuntimeError(f"Node {self.sm.get_node()} with State {self.sm.get_state()} startElement function is not defined")

		elif self.sm.get_node() == SCJDStateMachine.Node.IDMSEC_SPAN:
			self.entry.push_void_phrase()
			self.entry.set_phrase_idx(attrs['id'])

		elif self.sm.get_node() == SCJDStateMachine.Node.EXG_SPAN:
			if self.sm.get_state() in SCJDStateMachine.State.get_idmb_cluster():
				self.entry.push_void_phrase_section_sentence_example()

			elif self.sm.get_state() in SCJDStateMachine.State.get_gramb_cluster():
				self.entry.push_void_definition_sentence_example()

			elif self.sm.get_state() in SCJDStateMachine.State.get_cb_cluster():
				self.entry.push_void_phrase_section_sentence_example()

			else:
				raise RuntimeError(f"Node {self.sm.get_node()} with State {self.sm.get_state()} startElement function is not defined")

		elif self.sm.get_node() == SCJDStateMachine.Node.CSEC_SPAN:
			self.entry.push_void_phrase()
			self.entry.set_phrase_idx(attrs['id'])


	@log
	def endElement(self, tag):
		if self.sm.is_numb():
			return
		self.sm.endelement_move(tag)

	@log
	def characters(self, chars):
		if self.sm.is_numb():
			return
		def process_chars(chars):
			return chars.strip()

		if self.sm.get_node() == SCJDStateMachine.Node.HW_SPAN:
			self.entry.glue_pronounce(process_chars(chars))

		elif self.sm.get_node() == SCJDStateMachine.Node.HV_SPAN:
			self.entry.push_kanji(process_chars(chars))

		elif self.sm.get_node() == SCJDStateMachine.Node.TRANS_SPAN:
			if self.sm.get_state() == SCJDStateMachine.State.GRAMB_SEMB:
				self.entry.push_definition_chinese_translation(process_chars(chars))

			elif self.sm.get_state() == SCJDStateMachine.State.GRAMB_TRG_AFTER_OUP_LABEL:
				self.entry.push_definition_chinese_translation(process_chars(chars))

			elif self.sm.get_state() == SCJDStateMachine.State.GRAMB_OUP_LABEL:
				self.entry.push_definition_english_translation(process_chars(chars))

			elif self.sm.get_state() == SCJDStateMachine.State.GRAMB_EXG:
				self.entry.glue_definition_sentence_example(None, process_chars(chars))

			elif self.sm.get_state() == SCJDStateMachine.State.IDMB_SEMB:
				self.entry.push_phrase_section_translation(chars.strip())

			elif self.sm.get_state() == SCJDStateMachine.State.IDMB_EXG:
				self.entry.glue_phrase_section_sentence_example(None, chars.strip())

			elif self.sm.get_state() == SCJDStateMachine.State.CB_SEMB:
				self.entry.push_phrase_section_translation(chars.strip())

			elif self.sm.get_state() == SCJDStateMachine.State.CB_EXG:
				self.entry.glue_phrase_section_sentence_example(None, chars.strip())

			else:
				raise RuntimeError(f"Node {self.sm.get_node()} with State {self.sm.get_state()} characters function is not defined")

		elif self.sm.get_node() == SCJDStateMachine.Node.IDM_SPAN:
			if self.sm.get_state() == SCJDStateMachine.State.IDMB_FIRST_IDM:
				self.entry.glue_phrase_first_title(process_chars(chars))

			elif self.sm.get_state() == SCJDStateMachine.State.IDMB_NOT_FIRST_IDM:
				self.entry.push_phrase_title(process_chars(chars))

			else:
				raise RuntimeError(f"Node {self.sm.get_node()} with State {self.sm.get_state()} characters function is not defined")

		elif self.sm.get_node() == SCJDStateMachine.Node.EX_SPAN:
			if self.sm.get_state() == SCJDStateMachine.State.IDMB_EXG:
				self.entry.glue_phrase_section_sentence_example(process_chars(chars), None)

			elif self.sm.get_state() == SCJDStateMachine.State.CB_EXG:
				self.entry.glue_phrase_section_sentence_example(process_chars(chars), None)

			elif self.sm.get_state() == SCJDStateMachine.State.GRAMB_EXG:
				self.entry.glue_definition_sentence_example(process_chars(chars), None)

			else:
				raise RuntimeError(f"Node {self.sm.get_node()} with State {self.sm.get_state()} characters function is not defined")

		elif self.sm.get_node() == SCJDStateMachine.Node.IND_SPAN:
			self.entry.glue_definition_indicator(process_chars(chars))

		elif self.sm.get_node() == SCJDStateMachine.Node.CW_SPAN:
			self.entry.glue_phrase_first_title(process_chars(chars))

		elif self.sm.get_node() == SCJDStateMachine.Node.CV_SPAN:
			self.entry.push_phrase_title(process_chars(chars))

	def startDocument(self):
		self.sm.startdocument_move()
		self.reinit()

	def endDocument(self):
		if self.sm.is_numb():
			return
		self.sm.enddocument_move()
		# print(self.entry.data['title'])


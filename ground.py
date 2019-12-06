#The standard edition is that published by Wilhelm Streitberg in 1910 as Die Gotische Bibel (The Gothic Bible).


import os, sys
from cube.api import Cube
from gothic_ipa import ipa_transformer, gothic_script_transformer, gothic2latin_script_transformer
from clean_dict import get_voc_from_flat_dict, get_voc_from_csv, merge_vocs
from cltk.phonology.old_english.orthophonology import OldEnglishOrthophonology as oe
import gen_mods
from tqdm import tqdm
import pickle
import epitran
import re

import pandas as pd

import pdb

flatten = lambda l: [item for sublist in l for item in sublist]

# Analysis fields
index = 0
word = 1
lemma = 2
upos = 3
xpos = 4
attrs = 5
head = 6
label = 7
deps = 8
space_after = 9


# Files and Languages
lang_acron = {'gothic':'got', 'latin':'la', 'italian':'it', 'german':'de', 'greek':'grc'}
lang_file = {'gothic':'gothic/gothic_latin_utf8.txt', 'latin':'latin/latin_vulgata_clementina_utf8.txt', 'italian':'italian/italian_riveduta_1927_utf8.txt',
			 'german':'german/german_luther_1912_utf8.txt', 'greek':'greek/greek_byzantine_2000_utf8.txt', 'english':'english/basic_english_utf8.txt',
			 'old_english':'old_english/douay_rheims_utf8.txt'}
all_languages = ['Lat', 'Ger', 'Rus', 'Eng', 'OEng', 'Gre', 'it', 'es', 'pt', 'da', 'yi', 'Got']
#['Got', 'Eng', 'Ger', 'Rus', 'OEng', 'Gre', 'Lat']
csv_file = 'entirePGMC_daughters.csv'
indo_file = 'entirePIE_daughters.csv'
flat_dict_file = 'gothic_dict.txt'
lemmatizer_file = 'Goth_form_lemma_alignment.csv'



def load_lemmatizer(fname='Goth_form_lemma_alignment.csv', statistics=True):
	if os.path.isfile(fname[:-3]+'p'):
		lemmatizer = pickle.load(open(fname[:-3]+'p', 'rb'))
		return lemmatizer

	df = pd.read_csv(fname, encoding ='latin1').dropna()
	lemmatizer = {}
	words = list(set(df['form']))
	len_words = len(words)
	for i in tqdm(range(len_words)):
		lemmatizer[words[i]] = df[df['form']==words[i]]['lemma'].values.tolist()[0]

	if statistics:
		print('Forms: {}\nLemmas per Form: {}'.format(len(lemmatizer), float(sum([len(lemmatizer[k]) for k in lemmatizer]))/len(lemmatizer)))

	pickle.dump(lemmatizer, open(fname[:-3]+'p', 'wb'))
	return lemmatizer


def load_bible(f):
	bible = {}
	text = 0
	
	for l in f:
		l = l.strip().split('\t')
		
		if text == 0 and 'orig_chapter' not in l: # Not yet column titles
			continue
		elif 'orig_chapter' in l: # Saving the columns
			book = l.index('orig_book_index')-1
			chapter = l.index('orig_chapter')-1
			verse = l.index('orig_verse')-1
			try:
				subverse = l.index('orig_subverse')-1
			except:
				pass
			text = l.index('text')-1
			continue

		if len(l) >= text+1: # Saving the dictionary
			if l[book] not in bible:
				bible[l[book]] = {}	
			if l[chapter] not in bible[l[book]]:
				bible[l[book]][l[chapter]] = {}
			bible[l[book]][l[chapter]][l[verse]] = l[text]
	return bible



def analyze(text, cube, lang='got'):
	line = re.sub(r"\[[A-Z]\]", ' ', text)
	line = re.sub(r"[·\.,;*@#?!&$]+\ *", ' ', line)
	line = re.sub(r"[\[\]\(\)\<\>]*", '', line)
	line = re.sub('-', ' ', line)

	sentences=cube(line)
	analysis = []
	if type(sentences[0]) == list:
		for sentence in sentences:
			for token in sentence:
				if lang == 'got':
					#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after
					analysis.append([token.index, token.word, token.lemma, token.upos, token.xpos, token.head, token.label, token.deps, token.space_after, gothic_script_transformer(token.word), ipa_transformer(token.word, 'gothic')])
				elif lang == 'greek':
					#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after, script, ipa
					analysis.append([token.index, token.word, token.lemma, token.upos, token.xpos, token.head, token.label, token.deps, token.space_after, '_', ipa_transformer(token.word, 'greek')])
				else:
					#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after
					analysis.append([token.index, token.word, token.lemma, token.upos, token.xpos, token.head, token.label, token.deps, token.space_after, '_', '_'])
	else:
		for token in sentences:
				if lang == 'got':
					#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after
					analysis.append([token.index, token.word, token.lemma, token.upos, token.xpos, token.head, token.label, token.deps, token.space_after, gothic_script_transformer(token.word), ipa_transformer(token.word, 'gothic')])
				elif lang == 'greek':
					#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after, script, ipa
					analysis.append([token.index, token.word, token.lemma, token.upos, token.xpos, token.head, token.label, token.deps, token.space_after, '_', ipa_transformer(token.word, 'greek')])
				else:
					#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after
					analysis.append([token.index, token.word, token.lemma, token.upos, token.xpos, token.head, token.label, token.deps, token.space_after, '_', '_'])

	return analysis



def fake_analyze(text, lang='got', lemmatizer={}):
	line = re.sub(r"\[[A-Z]\]", ' ', text)
	line = re.sub(r"[·\.,;*@#?!&$]+\ *", ' ', line)
	line = re.sub(r"[\[\]\(\)\<\>]*", '', line)
	line = re.sub('-', ' ', line)
	line = flatten([re.sub('-', ' ', lemmatizer.get(token, token)).split() for token in line.split()])

	analysis = []
	for token in line:
		if lang == 'got':
			#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after, script, ipa
			analysis.append(['_', '_', token, '_', '_', '_', '_', '_', '_', gothic_script_transformer(token), ipa_transformer(token, 'gothic')])
		elif lang == 'greek':
			#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after, script, ipa
			analysis.append(['_', '_', token, '_', '_', '_', '_', '_', '_', '_', ipa_transformer(token, 'greek')])
		else:
			#index, word, lemma, upos, xpos, attrs, head, label, deps, space_after
			analysis.append(['_', token, token, '_', '_', '_', '_', '_', '_', '_', '_'])
	return analysis


def clean(text):
	line = re.sub(r"\[[A-Z]\]", ' ', text)
	line = re.sub(r"[·\.,;*@#?!&$]+\ *", ' ', line)
	line = re.sub(r"[\[\]\(\)\<\>]*", '', line)
	line = re.sub('-', ' ', line)
	return line



def map_bibles(f1, f2s, voc, l1='gothic', cube1=True, cube2=False, lemmatizer={}):
	f1_dict = load_bible(open(f1, 'r'))

	lemma_l1 = False if cube1 == False else True

	count = 0
	mapped = {}

	all_words_count = 0
	found_words = {}
	unfound_words = {}

	for book in f1_dict:
		if book not in mapped:
			mapped[book] = {}
		for chapter in f1_dict[book]:
			if chapter not in mapped[book]:
				mapped[book][chapter] = {}
			for verse in f1_dict[book][chapter]:
				if verse not in mapped[book][chapter]:
					mapped[book][chapter][verse] = {}

				count += 1
				if count % 500 == 0:
					print(count)

				mapped[book][chapter][verse][l1] = f1_dict[book][chapter][verse]
				if lemma_l1:
					mapped[book][chapter][verse][l1+'_analyzed'] = analyze(f1_dict[book][chapter][verse], cube1, lang='got')
				else:
					mapped[book][chapter][verse][l1+'_analyzed'] = fake_analyze(f1_dict[book][chapter][verse], lang='got', lemmatizer=lemmatizer)
							
				if l1 == 'got':
					mapped[book][chapter][verse][l1+'_translation'] = {}
					lemmas = list(list(zip(*mapped[book][chapter][verse][l1+'_analyzed']))[2])

					for lang in all_languages:
						if lang not in found_words:
							found_words[lang] = {}
						if lang not in unfound_words:
							unfound_words[lang] = {}

						if lang == 'Got':
							mapped[book][chapter][verse][l1+'_translation'][lang] = lemmas
							mapped[book][chapter][verse][l1+'_translation'][lang+'_script'] = [gothic_script_transformer(t) for t in lemmas]
							mapped[book][chapter][verse][l1+'_translation'][lang+'_ipa'] = [ipa_transformer(t, 'gothic') for t in lemmas]
						else:
							if lang not in mapped[book][chapter][verse][l1+'_translation']:
								mapped[book][chapter][verse][l1+'_translation'][lang] = []

							for word in lemmas:
								all_words_count += 1
								if word in voc and lang in voc[word]:
									#if lang == 'Lat':
									#	print(word, voc[word][lang])

									if word not in found_words[lang]:
										found_words[lang][word] = 0
									found_words[lang][word] += 1
									mapped[book][chapter][verse][l1+'_translation'][lang].append(voc[word][lang])
								else:
									if word not in unfound_words[lang]:
										unfound_words[lang][word] = 0
									unfound_words[lang][word] += 1
									mapped[book][chapter][verse][l1+'_translation'][lang].append('_')

	for lang in found_words:
		found = sum([found_words[lang][w] for w in found_words[lang]])
		unfound = sum([unfound_words[lang][w] for w in unfound_words[lang]])
		print('token', lang, found, unfound, '%.4f' % (float(found)/(found+unfound+1)))
		found = len(found_words[lang])
		unfound = len(unfound_words[lang])
		print('\ttype', lang, found, unfound, '%.4f' % (float(found)/(found+unfound+1)))
	print('All words: {}'.format(all_words_count))

	for f in f2s:
		l2 = f.split('/')[0]

		langs_epitran = {'german':'deu-Latn', 'italian':'ita-Latn', 'latin':'ita-Latn', 'spanish':'spa-Latn', 'english':'eng-Latn'}
		if l2 in langs_epitran:
			epi = epitran.Epitran(langs_epitran[l2])

		if cube2:
			lemma_l2 = lemma_l1
			cube2=Cube(verbose=False)
			cube2.load(lang_acron[l2])

		#if f == 'greek/greek_byzantine_2000_utf8.txt':
		#	pdb.set_trace()
		f2_dict = load_bible(open(f, 'r'))
		lemma_l2 = False if cube1 == False else True

		for book in mapped:
			for chapter in mapped[book]:
				for verse in mapped[book][chapter]:
					if book not in f2_dict or chapter not in f2_dict[book] or verse not in f2_dict[book][chapter]:
						#pdb.set_trace()
						continue

					#mapped_words = {'german':'deu-Latn', 'italian':'ita-Latn', 'latin':'ita-Latn', 'spanish':'Es', 'greek':'Gre'}
					mapped[book][chapter][verse][l2] = f2_dict[book][chapter][verse]
					if lemma_l2:
						mapped[book][chapter][verse][l2+'_analyzed'] = analyze(f2_dict[book][chapter][verse], cube2, lang=l2)
					else:
						mapped[book][chapter][verse][l2+'_analyzed'] = fake_analyze(f2_dict[book][chapter][verse], lang=l2)

					# IPA
					text = clean(f2_dict[book][chapter][verse])
					if l2 =='greek':
						mapped[book][chapter][verse][l2+'_ipa'] = ipa_transformer(text, 'greek').split()
					elif l2 == 'old_english':
						try:
							mapped[book][chapter][verse][l2+'_ipa'] = oe(text).split()
						except:
							pass
					elif l2 == 'english':
						try:
							mapped[book][chapter][verse][l2+'_ipa'] = oe(text).split() #gen_mods.get_final(gen_mods.getIPA_CMU(f2_dict[book][chapter][verse]))
						except:
							pass
					else:
						mapped[book][chapter][verse][l2+'_ipa'] = epi.transliterate(text).split()
						
	return mapped



if __name__ == "__main__":
	#try:
	if True:
		lang1 = sys.argv[1]

		try:
			analysis = False if sys.argv[2] == 'False' else True
		except:
			analysis = True

		if os.path.isfile(lang_file[lang1]):
			with open(lang_file[lang1], 'r') as lang1_f:
				if analysis:
					#cube1=Cube(verbose=False)
					#cube1.load(lang_acron[lang1])
					cube1 = False
					lemmatizer = load_lemmatizer(lemmatizer_file)
				else:
					cube1 = False
					lemmatizer = {}

				voc = merge_vocs(get_voc_from_csv(csv_file, indo_file), get_voc_from_flat_dict(flat_dict_file))
				mapped = map_bibles('gothic/gothic_latin_utf8.txt', ['latin/latin_vulgata_clementina_utf8.txt', 'italian/italian_riveduta_1927_utf8.txt', 
									'german/german_luther_1912_utf8.txt', 'greek/greek_byzantine_2000_utf8.txt', 'english/basic_english_utf8.txt',
									'old_english/douay_rheims_utf8.txt'], voc, lang_acron[lang1], cube1=cube1, cube2=False, lemmatizer=lemmatizer)

				pickle.dump(mapped, open('{}.p'.format(lang_acron[lang1]), 'wb'))

			pdb.set_trace()
			print('Finished')

		else:
			print('Error opening the files. Call:\n\n\tpython ground.py gothic_fname other_fname\n')
	#except Exception as e:
	#	print('Error: {}'.format(e))
	#	print('It is possible you have not provided the file names. Call:\n\n\tpython ground.py gothic_fname other_fname\n')





















'''
								pdb.set_trace()
								all_langs = []
								for word in voc:
									for lang in voc[word]:
										all_langs.append(lang)
										'nrf', 'la', 'Noord-Holland', 'Ger', 'Swe', 'ofs', 'pl', 'A32.afta', 
										'ang', 'cu', 'djk', 'nv', 'sco', 'rue', 'lud', 'vls', 'sw', 'smi-pro', 
										'cy', 'gmw-rfr', 'nb', 'uk', 'se', 'el', 'hsb', 'pap', 'de', 'bg', 'mdu', 
										'osx', 'gmq-jmk', 'et', 'ro', 'svm', 'mh', 'gme-cgo', 'id', 'GraubündenandWalserGerman', 
										'gmq-gut', 'head=līnum', 'dialectal', 'lng', 'oc', 'ru', 'sga', 'vi', 'OIr', 'izh', 'io', 
										'fiu-fin-pro', 'Eng', 'gmw-tsx', 'is', 'vot', 'mgl', 'no', 'pt', 'frk', 'nn', 'ga', 'hif',
										'ny', 'bar', 'enm', 'Icl', 'vep', 'gmq-scy', 'xvn', 'es', 'frm', 'for', 'be', 'fur', 'mhn',
										'gmq-osw', 'gem-pro', 'nds-nl', 'lt', 'vro', 'liv', 'sla-pro', 'Dut', 'dsb', 'ast', 'Skt',
										'OHGer', 'nrn', 'vol=III', 'sk', 'haw', 'osp', 'gsw', 'cim', 'pcm', 'nds-de', 'OCS', 'Gre',
										'fo', '13thc.', 'eo', 'li', 'wa', 'sh', 'roa-brg', 'fi', 'dot', 'nl', '*witōþa-', 'Rus', 'mi',
										'mul', 'roa-opt', 'pdt', 'ML.', 'orv', 'VLat', 'stq', 'odt', 'gmh', 'gmq-pro', 'owl', 'en',
										'ca', 'lb', 'tpi', 'sq', '*digra-', 'vec', 'volume=I', 'jut', 'gl', 'da', 'pcd', 'OEng',
										'gmw-ecg', 'goh', 'gmw-zps', 'lībum', 'scn', 'srn', 'szl', 'yi', 'wym', 'pdc', 'non',
										'fro', 'gmq-oda', 'dum', 'sl', 'gmw-stm', 'ON', 'hrx', 'sma', 'ovd', 'smn', 'krl', 'fr',
										'gmq-bot', 'yo', 'it', 'frr', 'sv', 'yol', 'gmw-cfr', 'pro', 'Lat', 'ost', 'gml', 'nds',
										'af', 'ms', 'fy', 'OGer'
								pdb.set_trace()




#mapped = map_bibles(lang1_f, lang2_f, voc, lang_acron[lang1], lang_acron[lang2], cube1, cube2)
def map_bibles_old(f1, f2, voc, l1='gothic', l2='greek', cube1=True, cube2=True):
	f1_dict = load_bible(f1)
	f2_dict = load_bible(f2)

	lemma_l1 = False if cube1 == False else True
	lemma_l2 = False if cube2 == False else True

	count = 0
	mapped = {}
	for book in f1_dict:
		if book in f2_dict:
			if book not in mapped:
				mapped[book] = {}
			for chapter in f1_dict[book]:
				if chapter in f2_dict[book]:
					if chapter not in mapped[book]:
						mapped[book][chapter] = {}
					for verse in f1_dict[book][chapter]:
						if verse in f2_dict[book][chapter]:
							if verse not in mapped[book][chapter]:
								mapped[book][chapter][verse] = {}

							count += 1
							if count % 100 == 0:
								print(count)

							mapped[book][chapter][verse][l1] = f1_dict[book][chapter][verse]
							if lemma_l1:
								mapped[book][chapter][verse][l1+'_analyzed'] = analyze(f1_dict[book][chapter][verse], cube1)
							else:
								mapped[book][chapter][verse][l1+'_analyzed'] = fake_analyze(f1_dict[book][chapter][verse], cube1)
							
							if l1 == 'got':
								mapped[book][chapter][verse][l1+'_translation'] = {}
								lemmas = list(list(zip(*mapped[book][chapter][verse][l1+'_analyzed']))[2])

								for lang in ['Got', 'Eng', 'Ger', 'Rus', 'OEng', 'Gre', 'Lat']:
									if lang == 'Got':
										mapped[book][chapter][verse][l1+'_translation'][lang] = lemmas
									else:
										if lang not in mapped[book][chapter][verse][l1+'_translation']:
											mapped[book][chapter][verse][l1+'_translation'][lang] = []

										for word in lemmas:
											if word in voc and lang in voc[word]:
												mapped[book][chapter][verse][l1+'_translation'][lang].append(voc[word][lang])
											else:
												mapped[book][chapter][verse][l1+'_translation'][lang].append('')

							mapped[book][chapter][verse][l2] = f2_dict[book][chapter][verse]
							if lemma_l2:
								mapped[book][chapter][verse][l2+'_analyzed'] = analyze(f2_dict[book][chapter][verse], cube2, lang=l2)
							else:
								mapped[book][chapter][verse][l2+'_analyzed'] = fake_analyze(f2_dict[book][chapter][verse], cube2, lang=l2)

							if l2 =='grc':
								mapped[book][chapter][verse][l2+'_ipa'] = ipa_transformer(f2_dict[book][chapter][verse], 'greek')
	return mapped
'''
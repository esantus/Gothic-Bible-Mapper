import os
import sys
from cube.api import Cube
import pickle as p
import epitran
import re

from tqdm import tqdm

import pdb


def generate_f1(r, lang='Ger', epi=False):
	lang_map = {'german':'Ger', 'italian':'it', 'latin':'Lat', 'spanish':'es', 'english':'Eng', 
				'russian':'Rus', 'old_english':'OEng', 'greek':'Gre'}
	lang = lang_map[lang]
	f1 = []
	voc = {}
	for book in r:
		for chapter in r[book]:
			for verse in r[book][chapter]:
				sentence = []
				for i, word in enumerate(r[book][chapter][verse]['got_translation']['Got_ipa']):
					other_lang = r[book][chapter][verse]['got_translation'][lang][i]
					if other_lang != [] and epi != False:
						other_lang_ipa = [epi.transliterate(x) for x in other_lang]
					else:
						other_lang_ipa = []
					sentence.append([r[book][chapter][verse]['got_translation']['Got'][i], word, other_lang, other_lang_ipa])
					for j, w in enumerate(other_lang):
						voc[w] = other_lang_ipa[j]
				f1.append(sentence)

	p.dump((f1, voc), open('resurce.p', 'wb'))
	return f1, voc



def get_unlemmatized_vocabulary(text, epi, lang):
	if os.path.isfile('unlemmatized_'+lang+'.p'):
		voc = p.load(open('unlemmatized_'+lang+'.p', 'rb'))
		return voc

	start = True
	voc = {}
	for line in text.split('\n'):
		line = line.strip().split('\t')
		
		if start:
			if 'orig_chapter' in line: # Not yet column titles
				start = False
		else:
			line = line[-1]
			line = re.sub(r"\[[A-Z]\]", ' ', line)
			line = re.sub(r"[·\.,;*@#?!&$]+\ *", ' ', line)
			line = re.sub(r"[\[\]\(\)\<\>]*", '', line)
			line = re.sub('-', ' ', line)

			for w in line.strip().split():
				voc[w] = epi.transliterate(w)
	p.dump(voc, open('unlemmatized_'+lang+'.p', 'wb'))
	return voc




def get_lemmatized_vocabulary(unlemmatized_voc, epi, lang):
	if os.path.isfile('lemmatized_'+lang+'.p'):
		voc = p.load(open('lemmatized_'+lang+'.p', 'rb'))
		return voc

	# Lemmatizer
	lang_acron = {'gothic':'got', 'latin':'la', 'italian':'it', 'german':'de', 'greek':'grc', 'english':'eng'}
	cube =Cube(verbose=False)
	cube.load(lang_acron[lang])

	voc = {}
	keys = list(unlemmatized_voc.keys())
	for i in tqdm(range(len(keys))):
		w = keys[i]
		sents = cube(w)
		if type(sents[0]) == list:
			for sent in sents:
				for token in sent:
					if token.lemma != '_':
						voc[w] = [token.lemma, epi.transliterate(token.lemma), 'L']
					else:
						voc[w] = [token.word, epi.transliterate(token.word), 'T']
		else:
			for token in sents:
				if token.lemma != '_':
					voc[w] = [token.lemma, epi.transliterate(token.lemma), 'L']
				else:
					voc[w] = [token.word, epi.transliterate(token.word), 'T']
	p.dump(voc, open('lemmatized_'+lang+'.p', 'wb'))
	return voc


if __name__ == '__main__':

	langs_epitran = {'german':'deu-Latn', 'italian':'ita-Latn', 'latin':'ita-Latn', 'spanish':'spa-Latn', 'english':'eng-Latn'}
	lang_file = {'gothic':'gothic/gothic_latin_utf8.txt', 'latin':'latin/latin_vulgata_clementina_utf8.txt', 'italian':'italian/italian_riveduta_1927_utf8.txt',
			 'german':'german/german_luther_1912_utf8.txt', 'greek':'greek/greek_byzantine_2000_utf8.txt', 'english':'english/basic_english_utf8.txt',
			 'old_english':'old_english/douay_rheims_utf8.txt'}
	
	try:
		resource_fname = sys.argv[1]
		lang = sys.argv[2]
	except:
		print('Make sure you write all arguments:\n\n\tpython generate_files.py resource language={}'.format(langs_epitran.keys()))

	if True:
		assert lang in langs_epitran, '{} is an unknown language. Select either: {}'.format(lang, langs_epitran.keys())

		epi = epitran.Epitran(langs_epitran[lang])

		if not os.path.isfile('resurce.p'):
			resource = p.load(open(resource_fname, 'rb'))
			f1, resource_voc = generate_f1(resource, lang, epi)
		else:
			f1, resource_voc = p.load(open('resurce.p', 'rb'))

		bible_unlemmatized_voc = get_unlemmatized_vocabulary(open(lang_file[lang], 'r').read(), epi, lang)

		bible_lemmatized_voc = get_lemmatized_vocabulary(bible_unlemmatized_voc, epi, lang)

		unlemmatized = {}
		for w in resource_voc:
			if w in bible_unlemmatized_voc:
				if w not in unlemmatized:
					unlemmatized[w] = 0
				unlemmatized[w] += 1

		print('Unlemmatized in the bible for {}: {}'.format(lang, len(bible_unlemmatized_voc)))
		print('Words in the resource for {}: {}'.format(lang, len(resource_voc)))
		print('Common unlemmatized for {}: type ({}), tokens ({})\n\n'.format(lang, len(unlemmatized), sum([unlemmatized[w] for w in unlemmatized])))

		lemmatized = {}
		for w in resource_voc:
			for w1 in bible_lemmatized_voc:
				if w == bible_lemmatized_voc[w1][0]:
					if w not in lemmatized:
						lemmatized[w] = 0
					lemmatized[w] += 1

		print('Lemmatized in the bible for {}: {}'.format(lang, len(bible_lemmatized_voc)))
		print('Words in the resource for {}: {}'.format(lang, len(resource_voc)))
		print('Common lemmatized for {}: type ({}), tokens ({})\n\n'.format(lang, len(lemmatized), sum([lemmatized[w] for w in lemmatized])))


		with open(lang+'_vocabulary.txt', 'w') as f:
			for w in bible_unlemmatized_voc:
				f.write('\t'.join([w, bible_unlemmatized_voc[w], '\t'.join(bible_lemmatized_voc[w])]) + '\n')


		pdb.set_trace()

	#except:
	#	print('Something went wrong.')
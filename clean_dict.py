import os
import string
import re
import pandas as pd
import pickle
from tqdm import tqdm
import numpy as np
from gothic_ipa import gothic_script_transformer, gothic2latin_script_transformer
import pdb


langs = ['Lat', 'Ger', 'Rus', 'Eng', 'OEn', 'Skt', 'OIr', 'OGer', 'Dut', 'English', 'VLat', 'OCS', 'ON', 'OEng', 'Gre', 'Swe', 'OHGer', 'Icl', 'Russian']
mapped = {'la':'Lat', 'de':'Ger', 'ru':'Rus', 'en':'Eng', 'ang':'OEng', 'OEn':'OEng', 'it':'it', 'es':'es', 'pt':'pt', 'da':'da', 'yi':'yi', 'el':'Gre', 'grc':'Gre'}

def get_voc_from_flat_dict(fname='gothic_dict.txt'):
	# http://web.archive.org/web/20100314053320/http://etymological.fw.hu/Gothic.htm
	voc = {}
	for line in open(fname, 'r'):
		line = re.sub(r"[\[,.;@#?!&$\]]+\ *", ' ', line)
		line = line.split()

		if len(line) < 2:
			continue

		if clean(line[0]) not in voc:
			voc[clean(line[0])] = {}

		if 'akin' in line:
			idx = line.index('akin')

			if not line[idx+2][0].isupper() or line[idx+2].startswith('Comp'):
				continue

			idx += 2
			while line[idx] != ':' and idx < len(line)-1:
				if line[idx] in langs:
					if line[idx] == 'Russian':
						line[idx] = 'Rus'
					if line[idx] == 'English':
						line[idx] = 'Eng'
					if line[idx] not in voc[clean(line[0])]:
						voc[clean(line[0])][line[idx]] = []
					voc[clean(line[0])][line[idx]].append(clean(line[idx+1]))
				idx += 1

	return { k:voc[k] for k in voc if len(voc[k])>0 }


def clean(word):
	line = word
	try:
		line = re.sub('tr=', '', line)
		line = re.sub('head=', '', line)
		line = re.sub(r"\[[A-Z]\]", '', line)
		line = re.sub(r"[·\.,;*@#?!&$]+\ *", '', line)
		line = re.sub(r"[\[\]\(\)\<\>]+\ *", '', line)
		line = re.sub('-', '', line)
	except:
		pdb.set_trace()
	#if line != word:
	#	print(word, line)
	return line



def get_voc_from_csv(fname='entirePGMC_daughters.csv', indo_fname=''):
	# https://drive.google.com/open?id=1D4lmoLDSGyhtyzKcEGC-Jp6wtOuoequw
	
	if os.path.isfile(fname[:-3]+'p'):
		voc = pickle.load(open(fname[:-3]+'p', 'rb'))
		return voc

	df = pd.read_csv(fname).dropna()

	for column in df.columns:
		#print(column)
		if column == 'COGID':
			continue
		df[column] = df[column].apply(clean)

	voc = {}
	words = [clean(x) for x in df.loc[df['LANGUAGE']=='got']['WORD'].values.tolist()]

	for i in tqdm(range(len(words))):
		word = words[i]
		#print('gotic: {}'.format(word))
		if word not in voc:
			voc[word] = {}

		#if i > 10:
		#	continue

		try:
			proto_german = clean(df.loc[(df['WORD']==word) & (df['LANGUAGE']=='got')]['PGMC'].values.tolist()[0])
		except:
			pdb.set_trace()
		#print('protogerman: {}'.format(proto_german))

		for lang in [clean(x) for x in df.loc[(df['PGMC']==proto_german) & (df['LANGUAGE']!='got')]['LANGUAGE'].values.tolist()]:
			#print('lang: {}'.format(lang))

			### REMOVE THIS CONTROL IF YOU WANT TO SAVE ALL THE LANGUAGES
			if lang not in mapped:
				continue

			if lang not in voc[word]:
				voc[word][lang] = []

			lang_word = clean(df.loc[(df['PGMC']==proto_german) & (df['LANGUAGE']==lang)]['WORD'].values.tolist()[0])
			#print('lang_word = {}'.format(lang_word))
			voc[word][lang].append(lang_word)

	
	if indo_fname != '':
		indo_df = pd.read_csv(indo_fname).dropna()

		for column in indo_df.columns:
			#print(column)
			if column == 'COGID':
				continue
			indo_df[column] = indo_df[column].apply(clean)

		gothic_words = [clean(x) for x in indo_df[indo_df['LANGUAGE']=='got']['WORD'].values.tolist()]

		proto_ie = {}
		for word in gothic_words:
			if gothic2latin_script_transformer(word) not in voc:
				voc[gothic2latin_script_transformer(word)] = {}

			# Save all proto-ie from which gothic forms derive
			proto_ie[word] = clean(indo_df[(indo_df['WORD']==word) & (indo_df['LANGUAGE']=='got')]['PIE'].values.tolist()[0])

			for lang in ['la', 'grc', 'yi']:
				#pdb.set_trace()
				temp = indo_df[(indo_df['PIE']==proto_ie[word]) & (indo_df['LANGUAGE']==lang)]['WORD'].values
				if type(temp) == np.ndarray:
					temp = temp.tolist()
				if type(temp) == list and temp != []:
					temp = temp[0]
				if len(temp) > 0:
					#print(type(temp))
					temp = clean(temp)
					if mapped[lang] in voc[gothic2latin_script_transformer(word)]:
						if temp not in voc[gothic2latin_script_transformer(word)][mapped[lang]]:
							voc[gothic2latin_script_transformer(word)][mapped[lang]].append(temp)
					else:
						voc[gothic2latin_script_transformer(word)].update({mapped[lang]:[temp]})

			if voc[gothic2latin_script_transformer(word)] == {}:
				print('Deleting key {}, because empty: {}'.format(gothic2latin_script_transformer(word), voc[gothic2latin_script_transformer(word)]))
				del voc[gothic2latin_script_transformer(word)]

	pickle.dump(voc, open(fname[:-3]+'p', 'wb'))
	return voc



def merge_vocs(voc1, voc2):
	if os.path.isfile('final_voc.p'):
		voc = pickle.load(open('final_voc.p', 'rb'))
		return voc

	voc = {}
	for word in voc1:
		if word not in voc:
			voc[word] = {}

		for lang in voc1[word]:
			try:
				if lang in mapped:
					new_lang = mapped[lang]
				elif lang in langs:
					new_lang = lang
				else:
					continue

				if new_lang not in voc[word]:
					voc[word][new_lang] = []

				voc[word][new_lang].extend(voc1[word][lang])
			except:
				pdb.set_trace()
				print(lang, voc)

	for word in voc2:
		if word not in voc:
			voc[word] = {}

		for lang in voc2[word]:
			try:
				if lang in mapped:
					new_lang = mapped[lang]
				elif lang in langs:
					new_lang = lang
				else:
					continue
				
				if new_lang not in voc[word]:
					voc[word][new_lang] = []
				voc[word][new_lang].extend(voc2[word][lang])
			except:
				pdb.set_trace()
				print(lang, voc)

	for word in voc:
		for lang in voc[word]:
			if type(voc[word][lang]) == list:
				voc[word][lang] = list(set(voc[word][lang]))

	pickle.dump(voc, open('final_voc.p', 'wb'))
	return voc

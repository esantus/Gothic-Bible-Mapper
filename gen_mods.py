# Adapted from https://github.com/mphilli/IPA_generator

import re 
import pdb

file_object = open("CMU_phonetic_dictionary.txt", 'r+')  

words = []
element = []

def getIPA_CMU(userInput):
    IPA_CMUT = ""; ele_num = 0; mult_num = []
    for w in userInput:
        if w == "a":
            IPA_CMUT += "a "
        w = re.sub("[^a-zA-Z]", "", w)
        file_lines = file_object.readlines()
        for line in file_lines:
            words.append(line.lower())
        w = " " + w.strip().lower() + " "
        w2 = " " + w.strip().lower() + "("
        
        for string in words:
            string = " " + string
            if w in string:
                
                ele_num = ele_num + 1
                element.append(ele_num)
                IPA_CMU = string.replace(w, "").strip().replace(" ", "")
                IPA_CMU = re.sub("[0-9]", "", IPA_CMU)
                IPA_CMUT += IPA_CMU + " "
            if w2 in string:
                multiple = []; mult_num = []
                mult_num.append(ele_num)
                multiple.append(string)
                get_multiple(multiple,w2)
                multiple = get_IPA(get_multiple(multiple,w2))
            if w == string:
                pass      
    aslist = IPA_CMUT.split()
    if mult_num:
        #print('multiple entries found: ')
        for m in mult_num:
            old = aslist[m-1]
            aslist[m-1] = aslist[m-1].replace(old, multiple) 
            asliststring = " ".join(aslist)
            get_finalPrint(asliststring)     
    return IPA_CMUT; 

def multIPA(word, IPA):
    return IPA;

def get_multiple(multiple,w2):
    IPA_CMU = ""
    IPA_CMUT = ""
    for CMU_strings in multiple: 
        IPA_CMU = CMU_strings.replace(w2, "").strip().replace(" ", "")
        IPA_CMU = re.sub("[0-9]", "", IPA_CMU)
        IPA_CMU = re.sub('[()]', "", IPA_CMU)
        IPA_CMUT += IPA_CMU
    return IPA_CMUT; 



def get_IPA(IPA_CMU):
    #convert CMU to standard IPA
    IPA = "" # final string
    IPA_CMU = IPA_CMU.split()
    for w in IPA_CMU:
        if w == "a":   w = w.replace("a", "ə")
        if "ey" in w:  w = w.replace("ey", "e")
        if "aa" in w:  w = w.replace("aa", "ɑ")    
        if "ae" in w:  w = w.replace("ae", "æ")
        if "ah" in w:  w = w.replace("ah", "ə")
        if "ao" in w:  w = w.replace("ao", "ɔ")
        if "aw" in w:  w = w.replace("aw", "aʊ")
        if "ay" in w:  w = w.replace("ay", "aɪ")
        if "ch" in w:  w = w.replace("ch", "ʧ")
        if "dh" in w:  w = w.replace("dh", "ð")
        if "eh" in w:  w = w.replace("eh", "ɛ")
        if "er" in w:  w = w.replace("er", "ər")
        if "hh" in w:  w = w.replace("hh", "h")
        if "ih" in w:  w = w.replace("ih", "ɪ")
        if "jh" in w:  w = w.replace("jh", "ʤ")
        if "ng" in w:  w = w.replace("ng", "ŋ")
        if "ow" in w:  w = w.replace("ow", "oʊ")
        if "oy" in w:  w = w.replace("oy", "ɔɪ")
        if "sh" in w:  w = w.replace("sh", "ʃ")
        if "th" in w:  w = w.replace("th", "θ")
        if "uh" in w:  w = w.replace("uh", "ʊ")
        if "uw" in w:  w = w.replace("uw", "u")
        if "zh" in w:  w = w.replace("zh", "ʒ")
        if "iy" in w:  w = w.replace("iy", "i")
        if "y" in w:   w = w.replace("y", "j")
        IPA += w + " "
    return(IPA.strip());

def get_final(IPA_CMU):
    final_IPA = '[IPA]: [' + get_IPA(IPA_CMU) + ']'
    return final_IPA;

def get_finalRAW(IPA_CMU):
    final_IPA_RAW = get_IPA(IPA_CMU)
    return final_IPA_RAW;

def get_finalPrint(IPA_CMU):
    final_IPA = '[IPA]: [' + get_IPA(IPA_CMU) + ']'
    print(final_IPA)

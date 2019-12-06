import re
test_sentence = 'και βαπτισθεις ο ιησους ανεβη ευθυς απο του υδατος και ιδου ανεωχθησαν αυτω οι ουρανοι και ειδεν το πνευμα του θεου καταβαινον ωσει περιστεραν και ερχομενον επ αυτον'
def ipa_transformer(sentence, language):#only for latin-transliterated Gothic and Greek without diacritics
    if language == 'gothic':
        #vowels
        sentence = re.sub(r"ah", "aːh", sentence)
        sentence = re.sub(r"aih", "ɛh", sentence)
        sentence = re.sub(r"air", "ɛr", sentence)
        sentence = re.sub(r"ai", "ɛː", sentence)
        sentence = re.sub(r"auh", "ɔh", sentence)
        sentence = re.sub(r"aur", "ɔr", sentence)
        sentence = re.sub(r"au", "ɔː", sentence)
        sentence = re.sub(r"ei", "iː", sentence)
        sentence = re.sub(r"e", "eː", sentence)
        sentence = re.sub(r"o", "oː", sentence)
        sentence = re.sub(r"ur", "uːr", sentence)
        sentence = re.sub(r"uh", "uːh", sentence)


        #consonants
        sentence = re.sub(r"ab", "aβ", sentence)
        sentence = re.sub(r"ɛb", "ɛβ", sentence)
        sentence = re.sub(r"ɔb", "ɔβ", sentence)
        sentence = re.sub(r"ib", "iβ", sentence)
        sentence = re.sub(r"eb", "eβ", sentence)
        sentence = re.sub(r"ob", "oβ", sentence)
        sentence = re.sub(r"ub", "uβ", sentence)
        sentence = re.sub(r"bd", "βd", sentence)
        sentence = re.sub(r"bn", "βn", sentence)
        sentence = re.sub(r"bm", "βm", sentence)
        sentence = re.sub(r"bg", "βg", sentence)
        sentence = re.sub(r"bl", "βl", sentence)
        sentence = re.sub(r"bj", "βj", sentence)
        sentence = re.sub(r"br", "βr", sentence)
        sentence = re.sub(r"bw", "βw", sentence)
        sentence = re.sub(r"bz", "βz", sentence)
        sentence = re.sub(r" β", " b", sentence)

        sentence = re.sub(r"ad", "að", sentence)
        sentence = re.sub(r"ɛd", "ɛð", sentence)
        sentence = re.sub(r"ɔd", "ɔð", sentence)
        sentence = re.sub(r"id", "ið", sentence)
        sentence = re.sub(r"ed", "eð", sentence)
        sentence = re.sub(r"od", "oð", sentence)
        sentence = re.sub(r"ud", "uð", sentence)
        sentence = re.sub(r"db", "ðb", sentence)
        sentence = re.sub(r"dβ", "ðβ", sentence)
        sentence = re.sub(r"dn", "ðn", sentence)
        sentence = re.sub(r"dm", "ðm", sentence)
        sentence = re.sub(r"dg", "ðg", sentence)
        sentence = re.sub(r"dl", "ðl", sentence)
        sentence = re.sub(r"dj", "ðj", sentence)
        sentence = re.sub(r"dr", "ðr", sentence)
        sentence = re.sub(r"dw", "ðw", sentence)
        sentence = re.sub(r"dz", "ðz", sentence)
        sentence = re.sub(r" ð", " d", sentence)

        sentence = re.sub(r"f", "ɸ", sentence)

        sentence = re.sub(r"gw", "ɡʷ", sentence)
        sentence = re.sub(r"hw", "hʷ", sentence)


        sentence = re.sub(r"ag", "aɣ", sentence)
        sentence = re.sub(r"ɛg", "ɛɣ", sentence)
        sentence = re.sub(r"ɔg", "ɔɣ", sentence)
        sentence = re.sub(r"ig", "iɣ", sentence)
        sentence = re.sub(r"eg", "eɣ", sentence)
        sentence = re.sub(r"og", "oɣ", sentence)
        sentence = re.sub(r"ug", "uɣ", sentence)
        sentence = re.sub(r"gb", "ɣb", sentence)
        sentence = re.sub(r"gβ", "ɣβ", sentence)
        sentence = re.sub(r"gn", "ɣn", sentence)
        sentence = re.sub(r"gm", "ɣm", sentence)
        sentence = re.sub(r"gg", "ŋg", sentence)
        sentence = re.sub(r"gl", "ɣl", sentence)
        sentence = re.sub(r"gj", "ɣj", sentence)
        sentence = re.sub(r"gr", "ɣr", sentence)
        sentence = re.sub(r"gw", "ɣw", sentence)
        sentence = re.sub(r"gz", "ɣz", sentence)

        sentence = re.sub(r"gp", "xp", sentence)
        sentence = re.sub(r"gt", "xt", sentence)
        sentence = re.sub(r"gk", "ŋk", sentence)
        sentence = re.sub(r"gɸ", "xɸ", sentence)
        sentence = re.sub(r"gh", "xh", sentence)
        sentence = re.sub(r"gs", "xs", sentence)
        sentence = re.sub(r"gþ", "xþ", sentence)
        sentence = re.sub(r"gq", "xq", sentence)

        sentence = re.sub(r" ɣ", " g", sentence)
        sentence = re.sub(r" x", " g", sentence)

        sentence = re.sub(r"qw", "kʷ", sentence)
        sentence = re.sub(r"þ", "θ", sentence)

    if language == 'greek':#koine-greek transcription of the 4th century (time when the bible was translated to Gothic)
        #vowels

        sentence = re.sub(r"αι", "e", sentence)
        sentence = re.sub(r"αυ", "av", sentence)
        sentence = re.sub(r"ευ", "ev", sentence)

        sentence = re.sub(r"ου", "u", sentence)
        sentence = re.sub(r"οι", "y", sentence)
        sentence = re.sub(r"υι", "y", sentence)


        sentence = re.sub(r"ει", "i", sentence)
        sentence = re.sub(r"ι", "i", sentence)
        sentence = re.sub(r"η", "i", sentence)
        sentence = re.sub(r"ε", "e", sentence)
        sentence = re.sub(r"υ", "y", sentence)
        sentence = re.sub(r"α", "a", sentence)
        sentence = re.sub(r"ω", "o", sentence)
        #consonants

        sentence = re.sub(r"π", "p", sentence)
        sentence = re.sub(r"β", "v", sentence)

        sentence = re.sub(r"φ", "f", sentence)
        sentence = re.sub(r"τ", "t", sentence)
        sentence = re.sub(r"δ", "ð", sentence)
        sentence = re.sub(r"κ", "k", sentence)
        sentence = re.sub(r"γ", "ɣ", sentence)
        sentence = re.sub(r"χ", "x", sentence)

        sentence = re.sub(r"μ", "m", sentence)
        sentence = re.sub(r"λ", "l", sentence)
        sentence = re.sub(r"σ", "s", sentence)
        sentence = re.sub(r"ρ", "r", sentence)
        sentence = re.sub(r"ν", "n", sentence)
        sentence = re.sub(r"ζ", "z", sentence)
        sentence = re.sub(r"ς", "s", sentence)



    return sentence


def gothic_script_transformer(sentence):#can only be applied to the non-ipa transliteration

        sentence = re.sub(r"a", "𐌰", sentence)
        sentence = re.sub(r"e", "𐌴", sentence)
        sentence = re.sub(r"i", "𐌹", sentence)
        sentence = re.sub(r"o", "𐍉", sentence)
        sentence = re.sub(r"u", "𐌿", sentence)

        sentence = re.sub(r"b", "𐌱", sentence)
        sentence = re.sub(r"d", "𐌳", sentence)
        sentence = re.sub(r"f", "𐍆", sentence)
        sentence = re.sub(r"g", "𐌲", sentence)
        sentence = re.sub(r"hw", "𐍈", sentence)
        sentence = re.sub(r"h", "𐌷", sentence)
        sentence = re.sub(r"j", "𐌾", sentence)
        sentence = re.sub(r"k", "𐌺", sentence)
        sentence = re.sub(r"l", "𐌻", sentence)
        sentence = re.sub(r"m", "𐌼", sentence)
        sentence = re.sub(r"n", "𐌽", sentence)
        sentence = re.sub(r"p", "𐍀", sentence)
        sentence = re.sub(r"q", "𐌵", sentence)
        sentence = re.sub(r"r", "𐍂", sentence)
        sentence = re.sub(r"s", "𐍃", sentence)
        sentence = re.sub(r"t", "𐍄", sentence)
        sentence = re.sub(r"þ", "𐌸", sentence)
        sentence = re.sub(r"w", "𐍅", sentence)
        sentence = re.sub(r"z", "𐌶", sentence)
        return sentence




def gothic2latin_script_transformer(sentence):#can only be applied to the non-ipa transliteration

        sentence = re.sub(r"𐌰", "a", sentence)
        sentence = re.sub(r"𐌴", "e", sentence)
        sentence = re.sub(r"𐌹", "i", sentence)
        sentence = re.sub(r"𐍉", "o", sentence)
        sentence = re.sub(r"𐌿", "u", sentence)

        sentence = re.sub(r"𐌱", "b", sentence)
        sentence = re.sub(r"𐌳", "d", sentence)
        sentence = re.sub(r"𐍆", "f", sentence)
        sentence = re.sub(r"𐌲", "g", sentence)
        sentence = re.sub(r"𐍈", "hw", sentence)
        sentence = re.sub(r"𐌷", "h", sentence)
        sentence = re.sub(r"𐌾", "j", sentence)
        sentence = re.sub(r"𐌺", "k", sentence)
        sentence = re.sub(r"𐌻", "l", sentence)
        sentence = re.sub(r"𐌼", "m", sentence)
        sentence = re.sub(r"𐌽", "n", sentence)
        sentence = re.sub(r"𐍀", "p", sentence)
        sentence = re.sub(r"𐌵", "q", sentence)
        sentence = re.sub(r"𐍂", "r", sentence)
        sentence = re.sub(r"𐍃", "s", sentence)
        sentence = re.sub(r"𐍄", "t", sentence)
        sentence = re.sub(r"𐌸", "þ", sentence)
        sentence = re.sub(r"𐍅", "w", sentence)
        sentence = re.sub(r"𐌶", "z", sentence)
        return sentence



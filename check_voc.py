import pickle as p
from collections import Counter
import pdb


flatten = lambda l: [item for sublist in l for item in sublist]

ds = p.load(open('entirePGMC_daughters.p', 'rb'))

print(Counter(flatten([list(ds[k].keys()) for k in ds])))
pdb.set_trace()




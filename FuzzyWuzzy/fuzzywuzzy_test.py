#Import.
import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
Str_A = 'FuzzyWuzzy is a lifesaver!'
Str_B = 'fuzzy wuzzy is a LIFE SAVER.' 
ratio = fuzz.ratio(Str_A.lower(), Str_B.lower())
print('Similarity score: {}'.format(ratio))
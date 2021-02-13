from nltk.stem import PorterStemmer

"""Script that creates a dictionary of Porter Stemmer words, using a dictionary of regular words"""

load_path = "/home/mathias/Projects/spam_classifier/dataset/dictionary"
save_path = "/home/mathias/Projects/spam_classifier/dataset/ps_dictionary"

f_load = open(load_path, "r")

raw_dictionary = f_load.read().lower().split("\n")

ps = PorterStemmer()
ps_raw_dictionary = [ps.stem(word) for word in raw_dictionary]

# Initialize dictionary with words we absolutely need
dictionary = ["httpaddr", "emailaddr", "dollar", "number"]

# Put single occurrences of words in the raw dictionary into the real dictionary
for word in ps_raw_dictionary:
    if word not in dictionary and len(word):
        dictionary.append(word)

# Sort dictionary
dictionary.sort()

f_save = open(save_path, "w+")
f_save.write("\n".join(dictionary))
f_save.close()


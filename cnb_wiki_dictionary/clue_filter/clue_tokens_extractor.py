import spacy
from nltk.corpus import wordnet as wn

from cnb_wiki_dictionary.utils.utils import get_title_tokens

nlp = spacy.load("en_core_web_sm")


def is_person(summary):
    doc = nlp(summary)
    for token in doc:
        if token.tag_.startswith("NN"):
            return token.ent_type_ == "PERSON"
    return False


def extract_unique_tokens(tokens):
    return [token for token in tokens if len(wn.synsets(token.lower())) == 0]


def extract_clue_tokens(title, summary):
    tokens = get_title_tokens(title)

    if len(tokens) == 1:
        return tokens

    if is_person(summary):
        return tokens[0], tokens[-1]

    return extract_unique_tokens(tokens)

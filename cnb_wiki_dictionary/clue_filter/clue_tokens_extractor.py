import spacy
from nltk.corpus import wordnet as wn

from cnb_wiki_dictionary.utils.title import get_title_tokens, tokenize, extract_title

nlp = spacy.load("en_core_web_sm")


def is_person(summary):
    doc = nlp(summary)
    for token in doc:
        if token.tag_.startswith("NN"):
            return token.ent_type_ == "PERSON"
    return False


def is_split_title(title):
    title = extract_title(title)
    return title.count(":") == 1


def get_split_title_tokens(title):
    # If title is of the form Title:Subtitle ie. Magic: The Gathering
    title, subtitle = title.split(":")

    title_tokens = tokenize(title)
    subtitle_tokens = tokenize(subtitle)
    
    clue_tokens = []
    if len(title_tokens) == 1:
        clue_tokens += title_tokens
    if len(subtitle_tokens) == 1:
        clue_tokens += subtitle_tokens
    return clue_tokens


def extract_unique_tokens(tokens):
    return [token for token in tokens if len(wn.synsets(token.lower())) == 0]


def extract_clue_tokens(title, summary):
    tokens = get_title_tokens(title)

    if len(tokens) == 1:
        return tokens

    if is_person(summary):
        return tokens[0], tokens[-1]
    
    if is_split_title(title):
        return get_split_title_tokens(title)

    return extract_unique_tokens(tokens)

import spacy
from spacy.matcher import Matcher
from nltk.corpus import wordnet as wn

from cnb_wiki_dictionary.utils.title import get_title_tokens, tokenize, extract_title

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_entities")

TRIM_SUFFIX = ["INC."]

def get_first_noun_span(doc):
    # Merge things like "Donald Trump's tenure" or "Meniere's disease"
    matcher = Matcher(nlp.vocab)
    pattern = [ {"POS": { "IN": [ "NOUN", "PROPN" ] }, "OP": "+"}, {"POS": "PART", "OP": "*"}, {"POS": { "IN": [ "NOUN", "PROPN" ] }, "OP": "*"} ]
    matcher.add("Merger", [pattern])
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    spans = spacy.util.filter_spans(spans)
    return spans[0]


def is_person(doc):
    noun_span = get_first_noun_span(doc)
    return noun_span[-1].ent_type_ == "PERSON"


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


def get_children_by_dep(token, dep_types):
    return [child for child in token.children if child.dep_ in dep_types]


def get_auxilary(doc):
    for token in doc:
        if token.pos_ == "AUX":
            return token
    return None


def get_nsubj(auxilary):
    nsubj_children = get_children_by_dep(auxilary, ["nsubj", "nsubjpass"])
    if len(nsubj_children) == 0:
        return None
    return nsubj_children[0]


def get_appos_tokens(doc):
    auxilary = get_auxilary(doc)
    if auxilary is None:
        return []
    
    nsubj = get_nsubj(auxilary)
    if nsubj is None:
        return []

    appos_children = get_children_by_dep(nsubj, ["appos"])
    if len(appos_children) == 0:
        return []
    appos = appos_children[0]
    if appos.ent_type_ is not None:
        return extract_title_tokens(appos.text, appos.ent_type_ == "PERSON")
    return []


def extract_title_tokens(title, is_person):
    tokens = get_title_tokens(title)

    if len(tokens) == 0:
        return []

    if tokens[-1] in TRIM_SUFFIX:
        tokens = tokens[:-1]

    if len(tokens) == 1:
        return tokens

    if is_person:
        return [tokens[0], tokens[-1]]

    if is_split_title(title):
        return get_split_title_tokens(title)
    
    return extract_unique_tokens(tokens)


def extract_clue_tokens(title, summary):
    if len(summary.strip()) == 0:
        return []

    doc = nlp(summary)
    clue_tokens = extract_title_tokens(title, is_person(doc))
    clue_tokens += get_appos_tokens(doc)
    return clue_tokens
import spacy
from spacy.matcher import Matcher

from cnb_wiki_dictionary.utils.title import title_to_text
from .path_matcher import get_children_by_path, PathRule

SUFFIXES = ["Inc.", "LLC"]

nlp = spacy.load("en_core_web_sm")


def retokenize(doc):
    # Merge things like "Donald Trump's tenure" or "Meniere's disease" or "Halo: Reach"
    matcher = Matcher(nlp.vocab)
    pattern = [
        {"POS": "INTJ", "OP": "*"},
        {"LOWER": { "IN": ["'", "!", "the"]}, "OP": "*"},
        {"POS": { "IN": [ "NOUN", "PROPN" ] }, "OP": "+"},
        {"LOWER": { "IN": [ "'s", ":", "of", "the", "'", "!" ] }, "OP": "*"},
        {"POS": { "IN": [ "NOUN", "PROPN" ] }, "OP": "*"},
        {"LOWER": { "IN": ["'", "!"]}, "OP": "*"},
    ]

    matcher.add("Merger", [pattern])
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    spans = spacy.util.filter_spans(spans)

    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(doc[span[0].i:span[-1].i + 1])


def get_auxilary(doc):
    for token in doc:
        if token.pos_ == "AUX":
            return token
    return None


def get_forms_from_summary(doc):
    retokenize(doc)

    auxilary = get_auxilary(doc)
    if auxilary is None:
        return []
    
    word_forms = []
    word_forms += get_children_by_path(auxilary, [
        PathRule(deps=["nsubj", "nsubjpass"], tag="NN")
    ])
    word_forms += get_children_by_path(auxilary, [
        PathRule(deps=["nsubj", "nsubjpass"]),
        PathRule(deps=["appos"])
    ])
    word_forms += get_children_by_path(auxilary, [
        PathRule(deps=["nsubj", "nsubjpass"]),
        PathRule(deps=["acl"]),
        PathRule(deps=["prep"], texts=["as"]),
        PathRule(deps=["pobj"])
    ])

    # For Meta_Platforms the appositional form is "Inc.", which is not desirable.
    return [word_form for word_form in word_forms if word_form is not None and word_form not in SUFFIXES]


def get_word_forms(title, doc):
    word_forms = [title_to_text(title)]
    word_forms += get_forms_from_summary(doc)
    
    for word_form in word_forms.copy():
        for suffix in SUFFIXES:
            trimmed = word_form.removesuffix(suffix).strip().strip(",")
            if len(trimmed) > 0 and trimmed != word_form:
                word_forms.append(trimmed)
    return list(set(word_forms))
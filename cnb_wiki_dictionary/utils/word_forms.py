import spacy
from spacy.matcher import Matcher, PhraseMatcher

from cnb_wiki_dictionary.utils.title import title_to_text
from cnb_wiki_dictionary.utils.is_proper import is_proper
from .path_matcher import get_children_by_path, PathRule

SUFFIXES = ["Inc.", "LLC"]

nlp = spacy.load("en_core_web_sm")

def retokenize(doc):
    # Merge things like "Donald Trump's tenure" or "Meniere's disease" or "Halo: Reach"
    matcher = Matcher(nlp.vocab)
    pattern = [
        {"POS": { "IN": [ "NOUN", "PROPN", "ADJ" ] }, "OP": "+"}
    ]

    matcher.add("Merger", [pattern])
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    spans = spacy.util.filter_spans(spans)

    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(doc[span[0].i:span[-1].i + 1])


def retokenize_phrase(title_text, doc):
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add("TITLE", [nlp(title_text)])
    matches = matcher(doc)

    spans = [doc[start:end] for _, start, end in matches]

    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(doc[span[0].i:span[-1].i + 1])



def get_root_verb(doc):
    # The root verb is the main acting verb "Mammoth **is** ...", "Romantic orientation **indicates** ..."
    # All variants of the subject should occur before the root verb
    # Usually an auxilary verb or a present verb
    for token in doc:
        if token.tag_ == "VBZ" or token.pos_ == "AUX":
            return token
    return None


def get_nsubj(doc):
    # Find the noun that corresponds to the subject of the article.
    # It should be the first noun and must occur before the first verb.
    # It shouldn't be a prepositional object either ie "In international law ..."
    for token in doc:
        if token.tag_.startswith("NN"):
            if token.dep_ == "pobj":
                continue
            return token
        if token.tag_.startswith("VB"):
            return None
    return None


def filter_word_form(word_form):
    return word_form is not None and word_form not in SUFFIXES


def get_forms_from_summary(doc, title_text):
    retokenize_phrase(title_text, doc)
    retokenize(doc)

    nsubj = get_nsubj(doc)
    if nsubj is None:
        return []
    
    root_verb = get_root_verb(doc)
    token_filter = lambda token: root_verb is None or token.i < root_verb.i

    word_forms = [nsubj.text]
    word_forms += get_children_by_path(nsubj, [
        PathRule(deps=["appos"])
    ], token_filter)
    word_forms += get_children_by_path(nsubj, [
        PathRule(deps=["acl"]),
        PathRule(deps=["prep"], texts=["as"]),
        PathRule(deps=["pobj"])
    ], token_filter)

    # For Meta_Platforms the appositional form is "Inc.", which is not desirable.
    return [word_form for word_form in word_forms if filter_word_form(word_form)]


def get_word_forms(title, doc):
    title_text = title_to_text(title)
    word_forms = [title_text]

    if is_proper(doc):
        # Non-proper articles are too difficult to find word forms for in the summary
        # "Person of color" or "Next of kin" as examples
        word_forms += get_forms_from_summary(doc, title_text)
    
    for word_form in word_forms.copy():
        for suffix in SUFFIXES:
            trimmed = word_form.removesuffix(suffix).strip().strip(",")
            if len(trimmed) > 0 and trimmed != word_form:
                word_forms.append(trimmed)
    return list(set(word_forms))
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_entities")

def make_doc(text):
    return nlp(text)
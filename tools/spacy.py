from argparse import ArgumentParser
from spacy import displacy
import spacy

from cnb_wiki_dictionary.utils.word_forms import retokenize


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("text", type=str)
    parser.add_argument("type", type=str, nargs='?', default="ent")
    parser.add_argument("-r", "--retokenize", dest="should_retokenize", action="store_true")
    args = parser.parse_args()
    return args.text, args.type, args.should_retokenize


def main():
    text, type, should_retokenize = parse_args()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    if should_retokenize:
        retokenize(doc)
    
    for token in doc:
        print(token, token.tag_, token.pos_)

    displacy.serve(doc, style=type, port=5001)

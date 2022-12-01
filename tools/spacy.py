from argparse import ArgumentParser
from spacy import displacy
import spacy


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("text", type=str)
    parser.add_argument("type", type=str, nargs='?', default="ent")
    args = parser.parse_args()
    return args.text, args.type


def main():
    text, type = parse_args()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    for token in doc:
        print(token, token.tag_, token.pos_)

    displacy.serve(doc, style=type, port=5001)

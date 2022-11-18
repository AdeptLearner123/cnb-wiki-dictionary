from argparse import ArgumentParser
from spacy import displacy
import spacy


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("text", type=str)
    args = parser.parse_args()
    return args.text


def main():
    text = parse_args()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    displacy.serve(doc, style="ent", port=5001)

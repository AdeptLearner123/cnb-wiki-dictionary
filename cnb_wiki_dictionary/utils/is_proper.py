def is_proper(doc):
    for token in doc:
        if token.tag_.startswith("NN"):
            return token.tag_ == "NNP"
    return False
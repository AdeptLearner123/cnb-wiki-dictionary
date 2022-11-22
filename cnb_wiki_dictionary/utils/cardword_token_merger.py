from config import CARDWORDS

class CardwordTokenMerger:
    def __init__(self):
        with open(CARDWORDS, "r") as file:
            cardwords = file.read().splitlines()
            self._merge_tokens = self._get_merge_tokens(cardwords)
    
    def _get_merge_tokens(self, cardwords):
        cardword_tokens = [ cardword.split(" ") for cardword in cardwords ]
        return [ tokens for tokens in cardword_tokens if len(tokens) > 1]


    def merge(self, tokens):
        # Assume that merge tokens are split by spaces only
        # Assume that tokens list only matches merge tokens once
        for merge_tokens in self._merge_tokens:
            for i in range(len(tokens) - len(merge_tokens) + 1):
                span_tokens = tokens[i:i + len(merge_tokens)]
                upper_tokens = [ token.upper() for token in span_tokens ]
                if upper_tokens == merge_tokens:
                    tokens = tokens[:i] + [" ".join(tokens[i:i + len(span_tokens)])] + tokens[i + len(merge_tokens):]
                    return tokens
        return tokens
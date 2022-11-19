import math

def views_to_knownness(views):
    # Logarithmic interpolation so that max = 1 and min = 0
    # Caps at 1
    return min(math.log(views / MIN_VIEWS, 10) / math.log(MAX_VIEWS / MIN_VIEWS, 10), 1)

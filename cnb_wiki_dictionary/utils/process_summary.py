def process_summary(summary):
    # Edge case: Sometimes wikipedia extract includes image information that needs to be trimmed out
    # Ie. "Face"
    if "}}" in summary:
        return summary.split("}}")[1]
    return summary
from dataclasses import dataclass

@dataclass
class PathRule:
    deps: list
    texts: list = None


def get_children_by_dep(token, dep_types):
    return [child for child in token.children if child.dep_ in dep_types]


def get_children_by_path(token, path):
    matches = []

    if len(path) == 0:
        return [token.text]

    path_rule = path[0]
    children = get_children_by_dep(token, path_rule.deps)
    if path_rule.texts is not None:
        children = [ child for child in children if child.text in path_rule.texts ]
    
    for child in children:
        matches += get_children_by_path(child, path[1:])
    
    return matches
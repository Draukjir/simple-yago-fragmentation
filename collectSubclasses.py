def collect_subclasses(taxonomy_file: str, target_class: str):
    import lightrdf
    from collections import defaultdict, deque
    import constants as c

    parser = lightrdf.Parser()

    children = defaultdict(set)

    for triple in parser.parse(taxonomy_file, base_iri=None):
        s, p, o = triple

        if p == c.SUBCLASS:
            children[o].add(s)

    subclasses = set()
    queue = deque([target_class])

    while queue:
        current = queue.popleft()

        for child in children[current]:
            if child not in subclasses:
                subclasses.add(child)
                queue.append(child)

    return subclasses
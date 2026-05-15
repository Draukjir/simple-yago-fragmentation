def collect_subclasses(target_class: str):
    import lightrdf
    from collections import defaultdict, deque
    import signature

    parser = lightrdf.Parser()

    sig = signature.Signature()

    children = defaultdict(set)

    for triple in parser.parse(sig.TAXONOMY, base_iri=None):
        s, p, o = triple

        if p == sig.SUBCLASS:
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
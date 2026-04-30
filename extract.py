import lightrdf
import sys
import constants as c
import collectSubclasses

# Rollennamen / Relationen aus YAGO
role_names = [
    c.SPOUSE,
    c.ACTED_BY,
    c.DIRECTED_BY
]

# Konzeptnamen / YAGO-Klassen
concept_names = {
    c.ACTOR,
    c.DIRECTOR,
    c.MOVIE
}

#Sammeln aller Subklassen von den Konzeptnamen/Klassen, da immer nur die untersten Klassen / Blätter als Typen für die Entitäten gespeichert werden
subclassesOfActor = collectSubclasses.collect_subclasses(c.TAXONOMY, c.ACTOR)
subclassesOfDirector = collectSubclasses.collect_subclasses(c.TAXONOMY, c.DIRECTOR)
subclassesOfMovies = collectSubclasses.collect_subclasses(c.TAXONOMY, c.MOVIE)

concept_pool = (
    set(concept_names)
    | subclassesOfActor
    | subclassesOfDirector
    | subclassesOfMovies
)

domain = set()
 
parser = lightrdf.Parser()

with open("result.nt", "w") as f:
    
    def write_triple(triple):
        f.write("{} {} {} .\n".format(triple[0], triple[1], triple[2]))
    
    # TEIL 1: SCHEMA
    print("Processing yago-schema.ttl")
    for subj, pred, obj in parser.parse(c.SCHEMA, base_iri=None):
        if not ("shacl" in pred or "shacl" in obj):
            write_triple((subj, pred, obj))
    print("Done")
    
    #TEIL 2: TAXONOMIE
    print("Processing yago-taxonomy.ttl")
    for subj, pred, obj in parser.parse(c.TAXONOMY, base_iri=None):
        if not ("shacl" in pred or "shacl" in obj):
            write_triple((subj, pred, obj))
    
    # TEIL 3.1: Erster Durchlauf durch die Fakten
    # Rollennamen und Konzeptnamen durchgehen und Individuen hinzufügen
    print("Processing yago-facts.ttl == First Pass")
    for triple in parser.parse(c.FACTS, base_iri=None):
        subj, pred, obj = triple # Subjekte sind Individuen, Prädikate können Rollen oder auch Typzuweisung sein, Objekte können Individuen oder auch Klassen sein

        # Behandlung der Rollennamen, also z.B. bei (FightClub, ACTOR, BradPitt) sowohl FightClub, als auch BradPitt hinzufügen
        if pred in role_names:
            domain.add(subj) #Individuum
            domain.add(obj) #Individuum

        # Behandlung der Konzeptnamen, also z.B. bei (BradPitt, TYPE, Actor) -> Brad Pitt hinzufügen
        if pred == c.TYPE:
            if obj in concept_pool:
                domain.add(subj)

    print("Collected {} individuals".format(len(domain)))
    print("Done")
    
    # TEIL 3.2: Zweiter Durchlauf durch die Fakten
    # Nur Tripel speichern, die die gewünschten Konzeptnamen / Rollennahmen enthalten und zu denen die gesammelten Individuen gehören

    print("Processing yago-facts.ttl == Second Pass")
    for triple in parser.parse(c.FACTS, base_iri=None):
        subj, pred, obj = triple

        # Ist es eine Rolle oder Typzuweisung/Klassenzuweisung
        if pred not in role_names and pred != c.TYPE:
            continue
        # Ist das Individuum Teil der Domäne
        if subj not in domain:
            continue
        # Ist das (erreichte) Individuum Teil der Domäne oder die zugewiesene Klasse Teil der Konzepte
        if obj not in domain and obj not in concept_pool:
            continue

        if pred in role_names:
            write_triple(triple)
        elif pred == c.TYPE:
            if obj in subclassesOfActor:
                obj = c.ACTOR
            elif obj in subclassesOfDirector:
                obj = c.DIRECTOR
            elif obj in subclassesOfMovies:
                obj = c.MOVIE
                
            write_triple((subj, pred, obj))

    print("Done == Fragment written to result.nt")
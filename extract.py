import lightrdf
import sys
import constants as c
import collectSubclasses

# Rollennamen / Relationen aus YAGO
role_names = [
    c.SPOUSE,
    c.ACTED_IN,
    c.DIRECTED 
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

domain = set()
 
parser = lightrdf.Parser()

with open("result.nt", "w") as f:
    
    def write_triple(triple):
        f.write("{} {} {} .\n".format(triple[0], triple[1], triple[2]))
    
    # TEIL 1: SCHEMA
    print("Processing yago-schema.ttl")
    for triple in parser.parse(c.SCHEMA, base_iri=None):
        if not ("shacl" in triple[1]):
            write_triple(triple)
    print("Done")
    
    #TEIL 2: TAXONOMIE
    print("Processing yago-taxonomy.ttl")
    for triple in parser.parse(c.TAXONOMY, base_iri=None):
        if not ("shacl" in triple[1]):
            write_triple(triple)
    
    # TEIL 3: Erster Durchlauf durch die Fakten
    # Rollennamen und Konzeptnamen durchgehen und Individuen hinzufügen
    print("Processing yago-facts.ttl == First Pass")
    for triple in parser.parse(c.FACTS, base_iri=None):

        # Behandlung der Rollennamen, also z.B. bei (FightClub, ACTOR, BradPitt) sowohl FightClub, als auch BradPitt hinzufügen
        if triple[1] in role_names:
            domain.add(triple[0])
            domain.add(triple[2])

        # Behandlung der Konzeptnamen, also z.B. bei (BradPitt, TYPE, Actor) -> Brad Pitt hinzufügen
        if triple[1] == c.TYPE:
            if triple[2] in concept_names:
                domain.add(triple[0])
            elif triple[2] in subclassesOfActor or triple[2] in subclassesOfDirector or triple[2] in subclassesOfMovies:
                domain.add(triple[0])


    print("Collected {} individuals".format(len(domain)))
    print("Done")
    
    # TEIL 3: Zweiter Durchlauf durch die Fakten
    # Nur Tripel speichern, die die gewünschten Konzeptnamen / Rollennahmen enthalten und zu denen die gesammelten Individuen gehören

    print("Processing yago-facts.ttl == Second Pass")
    for triple in parser.parse(c.FACTS, base_iri=None):
        # Ist es eine Rolle oder Typzuweisung
        if triple[1] not in role_names and triple[1] != c.TYPE:
            continue
        # Ist das Individuum Teil der Domäne
        if triple[0] not in domain:
            continue
        # Ist das Individuum oder Klasse Teil der Domäne
        if triple[2] not in domain:
            continue

        if triple[1] in role_names:
            write_triple(triple)
        elif triple[1] == c.TYPE:
            obj = triple[2]

            if obj in subclassesOfActor:
                obj = c.ACTOR
            elif obj in subclassesOfDirector:
                obj = c.DIRECTOR
            elif obj in subclassesOfMovies:
                obj = c.MOVIE
                
            write_triple((triple[0], triple[1], obj))

    print("Done == Fragment written to result.nt")
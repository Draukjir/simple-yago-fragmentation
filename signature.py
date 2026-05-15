class Signature:
    def __init__(self):
        # file_names
        self.TAXONOMY = "yago-taxonomy.ttl"
        self.SCHEMA = "yago-schema.ttl"
        self.FACTS = "yago-facts.ttl"

        # important rdf_relations
        self.SUBCLASS = "<http://www.w3.org/2000/01/rdf-schema#subClassOf>"
        self.TYPE = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"

        # concepts or roles which we are looking for in the 1st pass
        self.domain_signature = {
            "<http://yago-knowledge.org/resource/Actor>",
            "<http://yago-knowledge.org/resource/Film_director>",
            "<http://schema.org/Movie>"
        }
        
        # concept_names which will be in the domain - 3rd pass
        self.concept_names = {
            "<http://schema.org/Person>",
            "<http://yago-knowledge.org/resource/Actor>",
            "<http://yago-knowledge.org/resource/Film_director>",
            "<http://schema.org/Movie>"
        }

        # role_names - 2nd pass
        self.role_names = {
            "<http://schema.org/spouse>",
            "<http://schema.org/actor>",
            "<http://schema.org/director>"
        }

        # target concept for definition extraction
        self.target_concept = "<http://yago-knowledge.org/resource/Actor>"
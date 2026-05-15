This is a tool to extract simplified fragments of the knowledge graph YAGO 4.5.
The signature is currently based on popular people and their jobs and relations e.g. Actors or Film Directors

## Obtain Yago 4.5.0.2 

```
wget https://yago-knowledge.org/data/yago4.5/yago-4.5.0.2.zip
```

## Extracting the needed files

```
unzip yago-4.5.0.2.zip yago-schema.ttl yago-taxonomy.ttl yago-facts.ttl
```

## Extract the fragments
You need two fragments, one with our target concept class and one without it.

This requires the lightrdf library[ https://github.com/ozekik/lightrdf](https://github.com/ozekik/lightrdf) (fastest way I found to process lots of rdf)

```
python extractSampleFragments.py
```



## Convert to OWL and add gender concept names

This requires <https://github.com/ontodev/robot>

```
robot merge --input custom-schema.owl --input result.nt --output yago-fragment.owl
```
```
robot merge --input custom-schema.owl --input result_without_target.nt --output yago-fragment-without-target.owl
```
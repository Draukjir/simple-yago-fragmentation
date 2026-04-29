## Obtain Yago 4.5.0.2 

```
wget https://yago-knowledge.org/data/yago4.5/yago-4.5.0.2.zip
```

## Extracting the needed files

```
unzip yago-4.5.0.2.zip yago-schema.ttl yago-taxonomy.ttl yago-facts.ttl
```

## Extract the fragment

This requires the lightrdf library[ https://github.com/ozekik/lightrdf](https://github.com/ozekik/lightrdf) (fastest way I found to process lots of rdf)

```
python extract.py
```

## Convert to OWL and add gender concept names

This requires <https://github.com/ontodev/robot>

```
robot merge --input custom-schema.owl --input result.nt --output yago-fragment.owl
```
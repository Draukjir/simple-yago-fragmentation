import collectSubclasses
import constants as c

# Beispiel: alle Unterklassen von Actor sammeln
subs = collectSubclasses.collect_subclasses(c.TAXONOMY, c.ACTOR)

print("Anzahl Unterklassen von Actor:", len(subs))
print()

for x in sorted(subs):
    print(x)
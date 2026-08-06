# <Entreprise>

## Metadata

A placer en frontmatter YAML en tete du fichier final :

```yaml
---
updated: YYYY-MM-DD
sources:
  - organisation: <organisation ou auteur>
    date: YYYY-MM-DD
raw:
  - ../../raw/<topic>/<fichier>.md
reliability: <haute/estime/declaratif/nc>
status: <actif/obsolete/conteste>
---
```

## Identite

- Pays : <pays ou [nc]>
- Ville : <ville ou [nc]>
- SIREN : <siren ou [nc]>
- NAF : <code ou [nc]>
- Segment : <segment ou [nc]>

## Activite

- <ce que l'entreprise fait concretement> [fiabilite]

## Donnees economiques

- CA : <valeur ou [nc]> ; annee : YYYY ; source : <raw> ; fiabilite : haute/estime/declaratif/nc
- Effectif : <valeur ou [nc]> ; annee : YYYY ; source : <raw> ; fiabilite : haute/estime/declaratif/nc

## Lecture industrielle

- Capacite : <impact capacite ou [nc]> [fiabilite]
- Differenciation : <source de marge, qualite, delai ou [nc]> [fiabilite]
- Risque : <risque d'execution, cyclicite, concentration client ou [nc]> [fiabilite]
- Maillon de chaine de valeur : <maillon ou [nc]> [fiabilite]

## Implication business

- <diligenter, rapprocher, transformer, prioriser, internaliser, externaliser ou eviter> : <raison chiffree ou [nc]>

## Voir aussi

- [[<article>]]

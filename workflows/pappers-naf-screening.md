# Screening Pappers par code NAF

Construire un inventaire brut d'entreprises Pappers dans `database/raw-pappers/` pour alimenter ensuite les qualifications et promotions eventuelles vers `wiki/companies/`.

References utiles :

- /references/codes-naf-installateurs-cvc-pac-photovoltaique.md
- /references/buy-and-build-thesis.md
- /policies/source-fidelity.md

## Perimetre initial

- CVC, pompe a chaleur, climatisation : `43.22B`
- Photovoltaique residentiel ou tertiaire en toiture : `43.21A`

Attention : si une consigne mentionne `42.31A` pour le photovoltaique, verifier avant collecte. Le code de screening retenu pour le PV toiture dans la reference est `43.21A`; `42.31A` ne doit pas etre utilise sans confirmation explicite.

## Arborescence cible

```text
database/raw-pappers/
  43.22B/
    <SIREN>-<slug-entreprise>/
      pappers.md
  43.21A/
    <SIREN>-<slug-entreprise>/
      pappers.md
```

Regles de nommage :

- Dossier code NAF : code exact avec point et lettre, exemple `43.22B`.
- Dossier entreprise : `<SIREN>-<slug-nom-entreprise>`.
- `SIREN` : 9 chiffres sans espace.
- `slug-nom-entreprise` : minuscules ASCII, tirets, sans forme juridique sauf si necessaire pour distinguer.
- Fichier source : `pappers.md`.

## Discipline credits Pappers

Minimiser les appels API Pappers.

- Ne jamais appeler un endpoint lourd avant d'avoir verifie que l'information n'existe pas deja dans `database/raw-pappers/`.
- Faire une recherche paginee par code NAF avec des `return_fields` strictement minimaux.
- Eviter les champs payants ou lourds, notamment `scoring_financier`, `scoring_non_financier`, cartographie, comptes complets, actes, beneficiaires effectifs et documents, sauf demande explicite.
- Ne pas appeler `informations_entreprise` pour chaque resultat brut si la reponse de recherche contient deja les champs necessaires au resume minimal.
- Dedupliquer les SIREN entre pages et entre codes avant tout appel de detail.
- Traiter par batch limite : collecter une page, ecrire les fiches manquantes, puis continuer seulement si l'utilisateur demande plus de profondeur ou une zone geographique precise.
- Preferer enrichir une fiche existante plutot que refaire une recherche globale.

## Champs minimaux de recherche

Pour `recherche_entreprises`, demander seulement les champs utiles au tri initial :

- `siren`
- `nom_entreprise`
- `denomination`
- `code_naf`
- `libelle_code_naf`
- `date_creation`
- `entreprise_cessee`
- `statut_rcs`
- `siege`
- `effectif`
- `effectif_min`
- `effectif_max`
- `tranche_effectif`
- `annee_effectif`
- `forme_juridique`
- `representants`
- `sites_internet`

Ajouter des filtres seulement s'ils servent la decision :

- `code_naf` obligatoire.
- `entreprise_cessee=false` par defaut pour un screening d'acquisition.
- `siege=true` si l'objectif est de compter les societes plutot que les etablissements.
- `departement` ou `region` si la recherche est geographique.
- `effectif_min`, `effectif_max`, `chiffre_affaires_min` ou `chiffre_affaires_max` seulement si la these impose une taille cible.

## Procedure

### 1. Verifier l'existant

- Lister `database/raw-pappers/<code-naf>/`.
- Relever les SIREN deja collectes.
- Si le dossier code NAF n'existe pas, le creer.
- Si une fiche entreprise existe deja, ne pas la reecrire integralement : completer uniquement les champs manquants et conserver la source precedente.

### 2. Rechercher les entreprises

- Appeler Pappers `recherche_entreprises` une fois par code NAF et par page necessaire.
- Utiliser `par_page` eleve si disponible et raisonnable pour reduire les appels.
- Demander uniquement les champs minimaux.
- Stocker le curseur ou numero de page utilise dans la note de collecte si la pagination doit reprendre plus tard.

Exemple d'intention d'appel :

```text
recherche_entreprises(
  code_naf=<43.22B ou 43.21A>,
  entreprise_cessee=false,
  par_page=<maximum raisonnable>,
  return_fields=<champs minimaux>
)
```

### 3. Dedupliquer

- Normaliser chaque resultat par SIREN.
- Ignorer les doublons deja presents dans le dossier du code NAF.
- Si une entreprise apparait dans plusieurs codes ou a change de dominante, conserver une fiche par emplacement de collecte et noter le code source.

### 4. Creer une fiche brute par entreprise

Pour chaque resultat retenu :

- Creer `database/raw-pappers/<code-naf>/<SIREN>-<slug-nom-entreprise>/`.
- Creer `pappers.md`.
- Ne pas promouvoir automatiquement vers `wiki/companies/`.
- Chaque `pappers.md` doit commencer par le frontmatter YAML normalise ci-dessous.
- Les champs inconnus restent a `null`, pas `[nc]`, dans le frontmatter.
- `source_query` doit refleter le filtre utilise, au format `naf-<code-naf-minuscule-sans-point>`, exemple `naf-4322b`.
- `pappers_url` doit utiliser le format `https://www.pappers.fr/entreprise/<slug-nom-entreprise>-<SIREN>` quand l'URL exacte n'est pas fournie par Pappers.
- `business_types` doit contenir au moins une valeur. Utiliser `autre-a-qualifier` tant que le metier reel n'est pas qualifie.

Frontmatter obligatoire de `pappers.md` :

```markdown
---
record_type: "company"
source: "pappers"
source_query: "naf-4322b"
company_name: "<Nom entreprise>"
siren: "<SIREN>"
country: "france"
city: "<ville siege ou null>"
area_code: "<departement ou null>"
naf_code: "<43.22B ou 43.21A>"
date_created: "<date_creation ou null>"
revenue_2023: null
revenue_2024: null
revenue_2025: null
employee_numbers: "<effectif ou tranche_effectif ou null>"
qualified: false
wiki_topic: null
pappers_url: "https://www.pappers.fr/entreprise/<slug-nom-entreprise>-<SIREN>"
website: null
business_types:
  - autre-a-qualifier
---

# <Nom entreprise>

- Source : Pappers
- Date de collecte : <YYYY-MM-DD>
- SIREN : <SIREN>
- Code NAF collecte : <43.22B ou 43.21A>
- Libelle NAF : <libelle_code_naf>
- Statut : <statut_rcs / entreprise_cessee>
- Siege : <adresse, code postal, ville, departement, region>
- Forme juridique : <forme_juridique>
- Creation : <date_creation>
- Effectif : <effectif ou tranche_effectif, annee_effectif>
- Dirigeants : <representants disponibles dans la reponse minimale>
- Site web : <sites_internet ou [nc]>
- Resume brut : <1-3 bullets factuels>
- Interet buy-and-build : <qualification initiale ou [nc]>
- Limites : <champs absents, donnees non appelees pour economiser les credits>
```

### 5. Enrichir seulement si necessaire

Appeler `informations_entreprise` uniquement pour les entreprises qui passent un premier filtre business :

- taille compatible avec la these ;
- zone geographique pertinente ;
- activite plausible d'installation CVC/PAC/clim ou PV toiture ;
- signal de qualite, specialisation, anciennete, dirigeant ou site web exploitable.

Champs d'enrichissement autorises sans demande supplementaire :

- `objet_social`
- `etablissements`
- `representants`
- `sites_internet`
- `telephone`
- `email`
- `procedures_collectives`
- `procedure_collective_existe`
- `procedure_collective_en_cours`

Champs a eviter sauf validation explicite :

- `scoring_financier`
- `scoring_non_financier`
- `cartographie_entreprise`
- `comptes_entreprise` avec bilan complet
- documents, actes, statuts et beneficiaires effectifs

### 6. Qualifier sans polluer le wiki

- Les fiches `database/raw-pappers/` restent des donnees brutes.
- Promouvoir vers `wiki/companies/` seulement si l'entreprise devient qualifiee pour diligence, comparaison, rapprochement, transformation ou exclusion documentee.
- Lors d'une promotion, appliquer /references/article-types.md et /templates/company.md.

## Controle qualite

- Chaque fiche contient un SIREN et un code NAF collecte.
- Aucun chiffre n'est invente : valeur absente = `[nc]`.
- Les dates et effectifs sont repris tels que Pappers les retourne.
- Le resume distingue les faits Pappers des hypotheses buy-and-build.
- Le nombre d'appels Pappers realises est note dans le compte rendu de collecte.

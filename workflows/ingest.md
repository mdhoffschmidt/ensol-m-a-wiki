# Ingestion

Recuperer la source dans `raw/`, puis compiler uniquement la matiere utile dans `wiki/`.

References utiles :

- /references/business-analysis-grid.md
- /references/article-types.md

## 1. Recuperer

- Obtenir le contenu source. Si la source est inaccessible, demander a l'utilisateur de la coller.
- Choisir un topic dans `raw/` ou en creer un seulement si aucun topic existant ne convient.
- Enregistrer la source avec /templates/raw-source.md.
- Preserver le texte original : nettoyer le bruit, ne pas reformuler.

## 2. Trier

- Chercher dans `wiki/` les entites, concepts, alias et affirmations proches.
- Decider la disposition : `Nouveau`, `Mise a jour`, `Conteste` ou `Sans matiere`.
- `Sans matiere` est exclusif : garder le raw, journaliser, s'arreter.

## 3. Compiler

- Choisir le type de note avec /references/article-types.md.
- Utiliser le bon dossier : `wiki/articles/`, `wiki/companies/`, `wiki/people/` ou `wiki/concepts/`.
- Utiliser le template correspondant dans `/templates`.
- Mettre a jour `updated`, `sources`, `raw`, `reliability` et `status` dans le frontmatter.
- Une source peut alimenter plusieurs notes.

## 4. Propager

- Chercher les notes affectees dans tout `wiki/`, pas seulement dans l'index.
- Mettre a jour les notes materiellement touchees.
- Si une source depasse ou contredit une affirmation, conserver l'ancienne information et appliquer /policies/contradiction-preservation.md.

## 5. Cloturer

- Mettre a jour `wiki/index.md` avec /templates/index-entry.md.
- Journaliser dans `wiki/log.md` avec /templates/log-entry.md.

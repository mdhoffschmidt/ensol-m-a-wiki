# Lint

Controler la coherence mecanique et editoriale du wiki.

## Corriger automatiquement

- Note wiki absente de `wiki/index.md` : ajouter une entree avec `(pas de resume)`.
- Entree d'index pointant dans le vide : marquer `[MANQUANT]`.
- Lien interne casse : corriger seulement si une seule cible evidente existe.
- Date d'index divergente : aligner sur `updated` dans le frontmatter.

## Signaler sans corriger

- Source raw non referencee et non journalisee `Sans matiere`.
- Note avec chiffres mais sans source raw.
- Valeur chiffree non retrouvable dans le raw.
- Contradiction non marquee `Conteste` ou `Obsolete`.
- Note dans le mauvais dossier : article, company, person ou concept.
- Note orpheline ou lien croise manifestement manquant.
- Fichier hors architecture.

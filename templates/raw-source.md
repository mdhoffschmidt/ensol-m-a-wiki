## Regle

Une source brute est enregistree dans `raw/<topic>/<YYYY-MM-DD-slug>.md`.

Si la date de publication est inconnue, utiliser la date de collecte dans le nom du fichier et `published: Inconnu`.

## Template

```markdown
---
source:
source_type: article | rapport | site | entretien | registre | autre
source_url:
collected: YYYY-MM-DD
published: YYYY-MM-DD | Inconnu
author:
organisation:
topic:
status: brut | lu | sans_matiere | compile
---

# Titre original de la source

Texte original nettoye du bruit de mise en forme, non reformule.
```

Ne pas modifier une source raw apres compilation, sauf correction de collecte.

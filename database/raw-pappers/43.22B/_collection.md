# Collecte Pappers 43.22B

- Source : Pappers
- Code NAF : 43.22B
- Date derniere collecte : 2026-08-06
- Filtres : code_naf=43.22B, entreprise_cessee=false, departement=<01-60>, classement=tranche_effectifs, cible locale=tranche_effectif 12
- Pagination traitee : page 1, par_page=100, departements 01 a 60 traites ; departements 61 a 95 non traites
- Appels Pappers realises : 65 appels productifs ou de test sur 43.22B ; 35 tentatives refusees en 401 sur 61-95
- SIREN crees : 420 fiches presentes dans ce dossier, dont 407 creees pendant la collecte nationale
- SIREN ignores car deja presents : 169 doublons ou fiches deja existantes ignores pendant la collecte nationale
- Prochaine reprise : departements 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 apres resolution de l'erreur 401
- Limites : filtre direct effectif_min/effectif_max refuse par le connecteur comme reserve Pappers Pro ; contournement par departement + tri tranche_effectifs. Total France actif 43.22B releve precedemment : 39554. L'API HTTP a refuse la reprise a partir du departement 61 avec HTTP 401 Unauthorized. Fiches creees seulement pour les resultats en tranche_effectif 12, soit 20-49 salaries ; aucun appel detail Pappers.

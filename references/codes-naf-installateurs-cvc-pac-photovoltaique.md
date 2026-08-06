# Codes NAF installateurs CVC, PAC et photovoltaique

Utiliser cette reference pour filtrer, qualifier ou comparer des etablissements lors d'un screening Sirene, Pappers ou CRM dans la these buy-and-build photovoltaique, climatisation et pompe a chaleur.

## Regle de classement

- Le code NAF/APE de l'etablissement suit l'activite principale exercee, pas toutes les activites vendues.
- Pour un acteur multi-metiers, regarder la dominante de chiffre d'affaires, d'equipes terrain, de references chantier et de positionnement commercial avant de qualifier le segment.
- Le code NAF est un indicateur de tri, pas une preuve suffisante de metier : verifier site web, qualifications, avis, references, effectifs, dirigeant et historique de chantiers.

## Codes prioritaires pour screening

| Dominante etablissement | Code NAF/APE a prioriser | Libelle | Usage buy-and-build |
|---|---:|---|---|
| CVC, pompe a chaleur, climatisation | `43.22B` | Travaux d'installation d'equipements thermiques et de climatisation | Identifier installateurs ou mainteneurs CVC/PAC/clim a diligenter, comparer ou rapprocher. |
| Photovoltaique residentiel ou tertiaire en toiture | `43.21A` | Travaux d'installation electrique dans tous locaux | Identifier installateurs PV batiment, electriciens solarises et acteurs mixtes electricite/PV. |

## Interpretation operationnelle

- `43.22B` : bon premier filtre pour climatisation, pompe a chaleur air-air, air-eau, chauffage, equipements thermiques et maintenance associee.
- `43.21A` : bon premier filtre pour photovoltaique pose sur batiment, car l'installation PV toiture est classee dans l'installation electrique.
- Un installateur qui vend PAC + PV peut ressortir en `43.22B` ou `43.21A` selon sa dominante historique ; ne pas exclure automatiquement les acteurs mixtes.
- Les centrales solaires au sol, parcs solaires et activites de production d'electricite ne doivent pas etre confondues avec les installateurs PV toiture.

## NAF 2025 a surveiller

- `43.22H` reprend le libelle "Travaux d'installation d'equipements thermiques et de climatisation".
- `43.21G` reprend le libelle "Travaux d'installation electrique dans tous locaux" et mentionne explicitement les systemes photovoltaiques sur les batiments.
- Pour les extractions historiques ou Pappers/Sirene en 2026, conserver `43.22B` et `43.21A` comme codes de screening principaux, puis mapper vers les nouveaux codes quand la source utilise la NAF 2025.

## Sources

- INSEE, NAF rev.2, sous-classe `43.21A` : Travaux d'installation electrique dans tous locaux ; comprend aussi l'installation de capteurs d'energie solaire electriques asservis aux locaux. https://www.insee.fr/fr/metadonnees/nafr2/sousClasse/43.21a
- INSEE, NAF 2025, sous-classe `43.21G` : Travaux d'installation electrique dans tous locaux ; comprend les systemes photovoltaiques sur les batiments et les systemes de stockage d'energie. https://www.insee.fr/fr/metadonnees/naf2025/sousClasse/43.21G
- INSEE, NAF 2025, classe `43.22` : Travaux de plomberie et installation de chauffage et de conditionnement d'air ; comprend installation, reparation et entretien des systemes de chauffage et de conditionnement d'air. https://www.insee.fr/fr/metadonnees/naf2025/classe/43.22

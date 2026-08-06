#!/usr/bin/env python3
import argparse
import json
import os
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path


DEPARTMENTS = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "2A",
    "2B", "21", "22", "23", "24", "25", "26", "27", "28", "29",
    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
    "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
    "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
    "60", "61", "62", "63", "64", "65", "66", "67", "68", "69",
    "70", "71", "72", "73", "74", "75", "76", "77", "78", "79",
    "80", "81", "82", "83", "84", "85", "86", "87", "88", "89",
    "90", "91", "92", "93", "94", "95",
]


TRANCHE_LABELS = {
    "12": "20-49 salaries",
}


def slugify(value):
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "entreprise"


def clean_text(value):
    if value is None:
        return None
    return str(value).replace("\n", " ").strip()


def yaml_value(value):
    if value is None or value == "":
        return "null"
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def pappers_url(name, siren):
    return f"https://www.pappers.fr/entreprise/{slugify(name)}-{siren}"


def request_json(token, params, timeout):
    query = urllib.parse.urlencode(params)
    url = f"https://api.pappers.fr/v2/recherche?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": "ensol-wiki-collector/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def address_line(siege):
    if not siege:
        return "[nc]"
    parts = [
        clean_text(siege.get("adresse_ligne_1")),
        clean_text(siege.get("adresse_ligne_2")),
        clean_text(siege.get("code_postal")),
        clean_text(siege.get("ville")),
    ]
    return ", ".join([part for part in parts if part]) or "[nc]"


def write_company(base_dir, company, source_query, dry_run=False):
    siren = company.get("siren")
    name = company.get("nom_entreprise") or company.get("denomination") or siren
    slug = slugify(name)
    company_dir = base_dir / f"{siren}-{slug}"
    path = company_dir / "pappers.md"
    if path.exists():
        return False, path

    siege = company.get("siege") or {}
    tranche = company.get("tranche_effectif")
    tranche_label = TRANCHE_LABELS.get(tranche, f"tranche {tranche}" if tranche else None)
    year = company.get("annee_effectif")
    employee_numbers = None
    if tranche_label and year:
        employee_numbers = f"{tranche_label} (tranche {tranche}, annee {year})"
    elif tranche_label:
        employee_numbers = f"{tranche_label} (tranche {tranche})"

    content = f"""---
record_type: "company"
source: "pappers"
source_query: "{source_query}"
company_name: {yaml_value(name)}
siren: "{siren}"
country: "france"
city: {yaml_value(siege.get("ville"))}
area_code: {yaml_value((siege.get("code_postal") or "")[:2] if siege.get("code_postal") else None)}
naf_code: {yaml_value(company.get("code_naf"))}
date_created: {yaml_value(company.get("date_creation"))}
revenue_2023: null
revenue_2024: null
revenue_2025: null
employee_numbers: {yaml_value(employee_numbers)}
qualified: false
wiki_topic: null
pappers_url: "{pappers_url(name, siren)}"
website: null
business_types:
  - cvc-pac-clim-a-qualifier
---

# {name}

- Source : Pappers
- Date de collecte : {os.environ.get("COLLECTION_DATE", "2026-08-06")}
- SIREN : {siren}
- Code NAF collecte : {company.get("code_naf") or "[nc]"}
- Libelle NAF : {company.get("libelle_code_naf") or "[nc]"}
- Statut : {company.get("statut_rcs") or "[nc]"} / {"entreprise active" if company.get("entreprise_cessee") in (0, False) else "entreprise cessee [a verifier]"}
- Siege : {address_line(siege)}, {(siege.get("code_postal") or "")[:2] if siege.get("code_postal") else "[nc]"}
- Forme juridique : {company.get("forme_juridique") or "[nc]"}
- Creation : {company.get("date_creation") or "[nc]"}
- Effectif : {employee_numbers or "[nc]"}
- Dirigeants : [nc]
- Site web : [nc]
- Resume brut : entreprise active classee en installation d'equipements thermiques et de climatisation.
- Interet buy-and-build : cible CVC/PAC/clim a qualifier.
- Limites : fiche creee depuis recherche legere ; aucun appel detail Pappers.
"""
    if not dry_run:
        company_dir.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True, path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--naf", default="43.22B")
    parser.add_argument("--target-tranche", default="12")
    parser.add_argument("--par-page", type=int, default=100)
    parser.add_argument("--sleep", type=float, default=0.15)
    parser.add_argument("--departments", nargs="*", default=DEPARTMENTS)
    parser.add_argument("--base-dir", default="database/raw-pappers")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("PAPPERS_API_TOKEN")
    if not token:
        raise SystemExit("PAPPERS_API_TOKEN missing")

    base_dir = Path(args.base_dir) / args.naf
    base_dir.mkdir(parents=True, exist_ok=True)
    source_query = f"naf-{args.naf.lower().replace('.', '')}"

    calls = 0
    created = 0
    skipped = 0
    totals = {}
    errors = {}
    pages_seen = {}

    for dept in args.departments:
        page = 1
        dept_pages = 0
        while True:
            params = {
                "api_token": token,
                "code_naf": args.naf,
                "entreprise_cessee": "false",
                "departement": dept,
                "classement": "tranche_effectifs",
                "page": page,
                "par_page": args.par_page,
            }
            try:
                payload = request_json(token, params, 30)
            except Exception as exc:
                errors[dept] = str(exc)
                break

            calls += 1
            dept_pages += 1
            results = payload.get("resultats") or []
            totals[dept] = payload.get("total")
            saw_target = False
            saw_lower_after_target_or_any_lower = False

            for company in results:
                tranche = company.get("tranche_effectif")
                if tranche == args.target_tranche:
                    saw_target = True
                    was_created, _ = write_company(base_dir, company, source_query, args.dry_run)
                    if was_created:
                        created += 1
                    else:
                        skipped += 1
                elif tranche and tranche < args.target_tranche:
                    saw_lower_after_target_or_any_lower = True

            if not results:
                break
            if saw_lower_after_target_or_any_lower:
                break
            if not payload.get("curseurSuivant") and page * args.par_page >= int(payload.get("total") or 0):
                break
            page += 1
            time.sleep(args.sleep)

        pages_seen[dept] = dept_pages
        time.sleep(args.sleep)

    summary = {
        "naf": args.naf,
        "target_tranche": args.target_tranche,
        "calls": calls,
        "created": created,
        "skipped_existing": skipped,
        "departments": args.departments,
        "department_totals": totals,
        "department_pages": pages_seen,
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

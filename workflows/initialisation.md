# Initialisation

Declenchee uniquement a la premiere ingestion.

Ne creer que ce qui manque, ne jamais ecraser :

- `raw/`
- `wiki/`
- `wiki/articles/`
- `wiki/companies/`
- `wiki/people/`
- `wiki/concepts/`
- `wiki/index.md` avec le titre `# Index de la base de connaissances`
- `wiki/log.md` avec le titre `# Journal du wiki`

Si une question ou un audit ne trouve pas la structure, le dire sans rien creer. Un wiki cree par une question qui n'a rien trouve rend impossible de distinguer "rien n'a ete ingere" de "la reponse n'y est pas".

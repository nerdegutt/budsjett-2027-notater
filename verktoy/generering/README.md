# Slik ble sidekartet og kapittellista laget (engangsjobb)

Disse skriptene trengs ikke for å lage nye sider. De dokumenterer hvordan `sidekart.json` og
`framsikt-lenker.json` ble generert 23. september 2026, i tilfelle noe må gjøres om.

1. `crawl.py`: åpner alle 115 kapitlene i Framsikt med headless Chrome (`--dump-dom`, virtuelt
   tidsbudsjett 45–150 sekunder) og leser ut overskrifts-id-ene (`t-N`). Innholdsfilene i Framsikt
   (`content/text/…`) svarer tomt uten nettleser, derfor Chrome. Tok ca. 45 minutter med 5 parallelle.
2. `extract_anchors.py`: plukker ankre ut av én rendret side. To formater: `<div class="row h2" id="t-N">`
   på etats- og sektorsider, `<h2 id="t-N" bookmark="true">` på innledningskapitlene.
3. `map_pages.py` og `map_pages2.py`: kobler hver PDF-side til kapittel (via innholdsfortegnelsen) og
   avsnitt (via overskrifter i sideteksten, kontrollert mot at sidens tekst finnes under avsnittet).
4. `make_sidekart.py`: lager `sidekart.json`/`.md` for alle 685 sider. `make_support_doc.py`: lager
   `framsikt-lenker.json`/`.md`.

Stiene `SIDER/`, `INNHOLD.md` og `NETTSIDE/` er plassholdere for tekstuttrekket per side, innholdsfortegnelsen
og dette repoet. Tekstuttrekket lages med `pdftotext -layout` av PDF-en, delt på formfeed til én fil per side.

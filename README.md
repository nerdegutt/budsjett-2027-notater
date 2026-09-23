# Budsjett 2027 – notater (statisk nettside)

Lokal, statisk nettside som samler det vi finner ut om byrådets budsjettforslag for 2027.
Bygd med Punkt (Oslo kommunes designsystem) lastet fra punkt-cdn.oslo.kommune.no.
Publisert med GitHub Pages: https://nerdegutt.github.io/budsjett-2027-notater/

## Filer

- `index.html` – forside med lenker til temasidene og oversikt over dokumentets oppbygning
- `dig-2027.html` – Digitaliseringsetaten (DIG) i budsjett 2027
- `site.css` – egne tilpasninger oppå Punkt, lagt i `@layer app`

## Legge til et nytt tema

1. Kopier `dig-2027.html` til `<tema>.html` og bytt ut innholdet.
2. Legg til et kort på forsiden under «Temaer» og en lenke i `<pkt-header>` på alle sidene.
3. Oppgi sidetall fra PDF-en ved hvert tall og hver påstand (`<span class="ref">s. 604</span>`).
4. Oppdater datoen i bunnteksten.

## Kilde

Vedlegg 1, Byrådets forslag til Budsjett 2027 og økonomiplan 2027–2030 (Sak 1), 685 sider, lagt fram 23. september 2026.
PDF-en og tekstuttrekk per side ligger i arbeidsmappa lokalt, ikke i dette repoet.

- PDF: https://www.oslo.kommune.no/get-file/2498126/fa442cefc25087e0981d4abf1b623a30b2ab70bf3e15776a796bbc1015e36c91
- Digital versjon (Framsikt): https://oslokommune.framsikt.net/2027/oslo/bm-2027-sak1b2027#/
- Samleside: https://www.oslo.kommune.no/politikk/budsjett-regnskap-og-rapportering/budsjett-2027/budsjettforslag-2027-og-okonomiplan-2027-2030/

## Lenker til den digitale versjonen

Kapitlene i Framsikt har faste adresser. Mønsteret er:

- Sektor: `#/budsa/orgstructuremain/<sektor-id>` (FIN = 60, SET = 20, HLS = 15, UTD = 25, MOS = 35/40, KON = 45, BLK = 55, bydelene = 10)
- Etat/kapittel: `#/generic/orgstructuremain/<sektor-id>/<kapittelnr>` (DIG = 60/128, OKF = 60/127)
- Innledningskapitler: `#/generic/summary/introduction/<guid>-cn`
- Avsnitt i et kapittel: legg til `?scrollTo=t-<n>`; id-ene finnes ved å klikke i kapittelmenyen i Framsikt

Full liste over kapittel-adresser ligger i `framsikt-kapitler.json`.

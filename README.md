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

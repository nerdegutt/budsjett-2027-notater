# Budsjett 2027 – notater (statisk nettside)

Lokal, statisk nettside som samler det vi finner ut om byrådets budsjettforslag for 2027.
Bygd med Punkt (Oslo kommunes designsystem) lastet fra punkt-cdn.oslo.kommune.no.
Publisert med GitHub Pages: https://nerdegutt.github.io/budsjett-2027-notater/

## Filer

- `index.html` – forside i tre lag: «Fort & gæli», «For deg som vil vite litt mer», «Hva med andre virksomheter og store prosjekter?»
- Fort & gæli: `om-budsjettet.html`, `kommunemaal.html`, `dig-2027.html` (DIG på ett ark), `hva-skjer-naa.html`
- For deg som vil vite litt mer: `dig-penger.html`, `dig-mal.html`, `sikkerhet.html`, `fellessystemer.html`, `innbyggertjenester.html`, `klima.html`
- Hva med andre virksomheter og store prosjekter?: `andre-sektorer.html`, `okf.html`, `bydelsreformen.html`, `epj.html`, `usynlige-prosjekter.html`
- `site.css` – egne tilpasninger oppå Punkt, lagt i `@layer app`

Alle sider skiller mellom oppsummering fra budsjettet og avsnitt merket «Claudes vurdering» (gul, stiplet ramme).

## Legge til et nytt tema

1. Kopier en eksisterende temaside til `<tema>.html` og bytt ut innholdet (samme hode, meny, hero, innholdsliste og bunn).
2. Legg til et kort på forsiden i riktig lag.
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

Ferdige oppslagsverk, generert én gang ved å rendre alle kapitlene i Framsikt med headless Chrome:

- `framsikt-lenker.md` / `.json`: alle 115 kapitler med alle avsnittsankre (1 043 stykker)
- `sidekart.md` / `.json`: alle 685 PDF-sider → kapittel, avsnitt, Framsikt-lenke og PDF-lenke (`#page=N`)

Bruk `sidekart.json` når du skriver nye temasider: hvert sidetall i en `<span class="ref">` kan gjøres om til
en inline-lenke til Framsikt, med en liten `pdf`-lenke ved siden av. Kolonnen «kontroll» i sidekartet viser om
sidens tekst ble gjenfunnet under det valgte avsnittet («ok»), eller om siden har flere avsnitt / duplisert tekst.


## Slik fortsetter du i en ny økt

**Det som ligger lokalt (ikke i repoet):** PDF-en, `budsjett2027.txt` (hele teksten), `sider/NNN.txt` (én fil per side,
filnummer = sidetall) og `innhold.md` ligger i arbeidsmappa ved siden av dette repoet. Mangler de, lag dem på nytt:

```sh
pdftotext -layout Vedlegg-1-Byradets-forslag-til-Budsjett-2027-og-okonomiplan-2027-2030.pdf budsjett2027.txt
# del på formfeed til sider/001.txt … sider/685.txt
```

**Arbeidsflyt for et nytt tema**

1. Finn stoffet: `grep -l -i "søkeord" sider/*.txt` gir sidetall, `cat sider/604.txt` gir siden. `innhold.md` er kartet.
2. Bygg siden med `verktoy/sitegen.py` (`page()`, `section()`, `table()`, `assessment()`), se hvordan de eksisterende
   sidene er satt sammen. Skriv sidetall som ren tekst: `<span class="ref">s. 604</span>`, eller `s. 46, 583` og `s. 580–582`.
3. Legg til et kort på forsiden i riktig lag.
4. Kjør `verktoy/publish.sh "melding"`. Den gjør sidetallene om til lenker (Framsikt og PDF), kontrollerer at alle lenker
   peker på riktig kapittel og eksisterende avsnitt, validerer HTML og interne lenker, committer og pusher.

**Konvensjoner**

- Oppsummering fra budsjettet og egne vurderinger holdes adskilt. Vurderinger ligger i `assessment()`-bokser merket
  «Claudes vurdering», skrevet i spørrende form: still spørsmålene stoffet reiser, ikke slå fast hva som kommer til å skje. Ingen synsing utenfor boksene.
- Alle tall og påstander har sidetall. Tall gjengis som i kilden (1 000 kr i tabeller, «mill.» i løpende tekst).
- Ordet er «samfunnsfloke», aldri «flok».
- Én push per ferdig temaside. Innholdslista på hver side er i én kolonne. Sidetallene er selve lenkene.
- Publisering skjer bare til dette repoet. Ingenting annet sendes ut av maskinen uten eksplisitt ja.

**Status 23. september 2026:** femten sider, alle lag på forsiden fylt. Se `VIDERE.md` for åpne spørsmål og ideer.

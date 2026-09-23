# Videre arbeid og åpne spørsmål

Sist oppdatert 23. september 2026, dagen Sak 1 ble lagt fram.

## Når nye dokumenter kommer

- **Tilleggsinnstillingen (november):** oppdater `hva-skjer-naa.html` (loggen og tabellen), DIG-tallene på
  `dig-penger.html` (pensjonssats, eventuelle rammeendringer) og frie inntekter der de er omtalt.
- **Politiske spørsmål og svar** i Framsikt (`#/generic/summary/psqafrontpage`): partienes spørsmål om kapittel 128
  er det tidligste signalet om hva bystyret vil endre. Kandidat til egen seksjon på «Hva skjer nå?».
- **Bystyrets vedtak (desember, Dok 3):** sammenlign med Sak 1 og oppdater alle tall. Verbalvedtak om DIG kommer
  typisk her, ikke i Sak 1.

## Ideer til nye temasider

- **Klimabudsjettet og DIG:** virkemiddel 13 (brukstid på IKT-utstyr, PC-er inntil fem år, ansvar OKF og DIG, s. 20)
  og ombruk. DIG-kapitlet sier «ingen klimagassutslipp av betydning» (s. 610), men klimabudsjettet gir likevel ansvar.
- **Bydelsreformen sett fra DIG:** 150 mill. til IKT i 2027 på kapittel 192 (s. 37, 640) uten beskrivelse. Hvem eier
  pengene, og hva skal de brukes til?
- **EPJ og fagsystemfornyelsen i helse:** det største digitaliseringsprosjektet i kommunen, med 20 mill. til oppstart
  (s. 153). Hva krever det av plattform, integrasjon og sikkerhet fra DIG?
- **Økonomireglementet (s. 654–673):** fullmakter, instruks for investeringer, hva DIG kan og ikke kan uten bystyret.
- **Budsjettekniske merknader (s. 674–678):** pris- og lønnskompensasjon, endringer i kapittelinndelingen.
- **Historikk:** hvordan så Origo- og UKE-kapitlene ut i Sak 1/2026 og Dok 3/2026? Krever fjorårets dokumenter.

## Ting som ikke er verifisert eller er uklare i kilden

- Årsprofilen for nettverksutstyr (148 mill. i 2027, 1,4 mill. i 2028) forklares ikke (s. 609).
- Hvordan UKEs ramme ble fordelt mellom DIG og OKF står ikke i dokumentet (s. 587, 599, 606).
- «Målbildet for kommunens portaler og nettløsninger» nevnes uten innhold (s. 605).
- M365-hoppet fra 12,5 mill. i 2028 til 54 mill. i 2029 har ingen tallforklaring (s. 606, 608).
- To virksomheter sto utenfor felles IKT-plattform i 2025, mot null i 2024, uten forklaring (s. 580).
- Datoene for innspillsmøtene på `om-budsjettet.html` er fra oslo.kommune.no, ikke fra dokumentet.
- Vurderingene («Claudes vurdering») er tolkninger og bør sjekkes mot dem det gjelder før de brukes videre.

## Teknisk

- Framsikt-lenker: kapittel `#/budsa/orgstructuremain/<sektor>` eller `#/generic/orgstructuremain/<sektor>/<kap>`,
  avsnitt med `?scrollTo=t-N`. Alle id-er ligger i `framsikt-lenker.json`, koblingen side → avsnitt i `sidekart.json`.
- PDF-lenker: `<pdf-url>#page=N`, serveren sender PDF-en inline så det virker i nettleseren.
- Punkt lastes fra `punkt-cdn.oslo.kommune.no` (CSS i `@layer punkt`, egne stiler i `@layer app` i `site.css`).
  Header og varsler er Punkt-elementer (`pkt-header`, `pkt-alert`), resten er ren CSS.

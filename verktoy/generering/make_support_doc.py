import json, re
BASE="https://oslokommune.framsikt.net/2027/oslo/bm-2027-sak1b2027#"
res=json.load(open('framsikt_anchors.json'))
# sorter: innledning (summary/introduction) først, så sektorer/etater i tre-rekkefølge, så øvrige summary
def key(r):
    u=r['url']
    if '/summary/introduction/' in u: return (0,u)
    if '/orgstructuremain/' in u:
        parts=u.split('/'); sek=int(parts[3]); kap=parts[4] if len(parts)>4 else ''
        return (1,sek,0 if not kap else 1,kap)
    return (2,u)
res.sort(key=key)
md=["# Lenker til den digitale versjonen av budsjett 2027 (Framsikt)","",
"Støttedokument, generert automatisk ved å rendre hvert kapittel i Framsikt og lese ut overskrifts-id-ene.",
f"Grunnadresse: `{BASE}`. Avsnittslenker lages som `<kapitteladresse>?scrollTo=<id>`.","",
"Framsikt-siden endres ikke etter framleggelsen, så id-ene er stabile.",""]
sections={0:"## Innledningskapitler",1:"## Sektorer og kapitler",2:"## Felleskapitler og vedlegg"}
cur=None
for r in res:
    k=key(r)[0]
    if k!=cur: md.append(sections[k]); md.append(""); cur=k
    url=BASE+r['url']
    md.append(f"### {r['name']}")
    md.append(f"- Kapittel: {url}")
    if r['status']!='ok': md.append(f"- *Status: {r['status']}*")
    for i,lvl,txt in r['anchors']:
        indent = "  " if lvl in ('h3','h4') else ""
        md.append(f"{indent}- `{i}` {txt} → {url}?scrollTo={i}")
    md.append("")
open('framsikt-lenker.md','w',encoding='utf-8').write("\n".join(md))
# kompakt json for programmatisk bruk
compact={r['url']:{'name':r['name'],'anchors':{i:txt for i,l,txt in r['anchors']}} for r in res}
json.dump(compact, open('framsikt-lenker.json','w'), ensure_ascii=False, indent=1)
ok=sum(1 for r in res if r['status']=='ok'); print(f"{len(res)} kapitler, {ok} med ankre, {sum(len(r['anchors']) for r in res)} ankre totalt")

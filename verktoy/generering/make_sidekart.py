import json, re, sys
from map_pages2 import anchor_for, best_for_page, index, pages, BASE
PDF="https://www.oslo.kommune.no/get-file/2498126/fa442cefc25087e0981d4abf1b623a30b2ab70bf3e15776a796bbc1015e36c91"
out={}
for p in range(1,686):
    a=anchor_for(p)
    n,ranked=best_for_page(p)
    why=a['why'] if a else '-'
    if a and a['anchor'] and ranked:
        (u,aid),h=ranked[0]
        if u==a['url'] and aid!=a['anchor'] and h>=5:
            t=next(x['title'] for x in index[u]['sections'] if x['id']==aid)
            a={'url':u,'chapter':pages[u],'anchor':aid,'title':t,'why':f'linjetreff ({h} linjer)'}
    kontroll='-'
    if a and a['anchor'] and ranked:
        (u,aid),h=ranked[0]
        kontroll='ok' if (u==a['url'] and aid==a['anchor']) else ('annet kapittel' if u!=a['url'] else f'annet avsnitt ({aid})')
    if a:
        url=BASE+a['url']+(f"?scrollTo={a['anchor']}" if a['anchor'] else '')
        out[p]={'kapittel':a['chapter'],'avsnitt':a['title'],'anker':a['anchor'],'framsikt':url,'pdf':f'{PDF}#page={p}','metode':a['why'],'kontroll':kontroll}
    else:
        out[p]={'kapittel':None,'avsnitt':None,'anker':None,'framsikt':None,'pdf':f'{PDF}#page={p}','metode':'ikke funnet','kontroll':'-'}
    if p%100==0: print(p, file=sys.stderr)
json.dump(out,open('sidekart.json','w'),ensure_ascii=False,indent=1)
md=["# Sidekart: PDF-side til digital versjon","",
"Én rad per side i PDF-en (Vedlegg 1, Sak 1). «Framsikt» er lenke til kapittel og avsnitt i den digitale versjonen, «PDF» åpner riktig side i PDF-en.",
"Generert automatisk: kapittel via innholdsfortegnelsen, avsnitt via overskrifter i teksten, kontrollert mot at sidens tekst finnes under avsnittet.","",
"| Side | Kapittel | Avsnitt | Framsikt | PDF | Kontroll |","|---:|---|---|---|---|---|"]
for p,r in out.items():
    fs=f"[{r['anker'] or 'kapittel'}]({r['framsikt']})" if r['framsikt'] else '-'
    md.append(f"| {p} | {r['kapittel'] or '-'} | {r['avsnitt'] or '-'} | {fs} | [s. {p}]({r['pdf']}) | {r['kontroll']} |")
open('sidekart.md','w',encoding='utf-8').write("\n".join(md))
from collections import Counter
c=Counter(r['kontroll'] for r in out.values()); m=Counter(r['metode'].split(' (')[0] for r in out.values())
print('kontroll:',dict(c)); print('metode:',dict(m))
print('uten kapittel:', [p for p,r in out.items() if not r['kapittel']][:30])

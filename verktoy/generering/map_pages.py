import json, re, html, glob, os, sys, unicodedata
BASE="https://oslokommune.framsikt.net/2027/oslo/bm-2027-sak1b2027#"
pages=json.load(open('framsikt_pages.json'))
def norm(t):
    t=html.unescape(t); t=unicodedata.normalize('NFKC',t)
    t=t.replace('­','').replace('​','').replace('‑','-').replace('–','-').replace('−','-')
    t=re.sub(r'\s+',' ',t).strip().lower()
    return t
def key(url): return re.sub(r'[^A-Za-z0-9]+','_',url).strip('_')
ANCH=re.compile(r'<div\b(?=[^>]*\bclass="row (h[1-4])\b)(?=[^>]*\bid="(t-\d+)")[^>]*>|<(h[1-4])\b(?=[^>]*\bid="(t-\d+)")(?=[^>]*bookmark="true")[^>]*>')
def sections(url):
    f=f'crawl/{key(url)}.html'
    if not os.path.exists(f): return None
    s=open(f,encoding='utf-8',errors='ignore').read()
    # begrens til hovedinnholdet: kutt bort alt etter footer-popups om mulig
    ms=list(ANCH.finditer(s))
    if not ms: return []
    out=[]
    for i,m in enumerate(ms):
        aid=m.group(2) or m.group(4)
        end=ms[i+1].start() if i+1<len(ms) else len(s)
        seg=s[m.end():end]
        if m.group(2):   # format A: <div class="row h2" id=..>Tittel</div>
            h=re.match(r'(.*?)</div>', seg, flags=re.S)
        else:            # format B: <h2 id=.. bookmark="true">Tittel</h2>
            h=re.match(r'(.*?)</h[1-4]>', seg, flags=re.S)
        title=norm(re.sub(r'<[^>]+>',' ',h.group(1))) if h else ''
        text=norm(re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',seg,flags=re.S))
        text=re.sub(r'<[^>]+>',' ',text); text=norm(text)
        out.append({'id':aid,'title':title[:80],'text':text})
    return out
# indeks over alle crawla kapitler
index={}
for url,name in pages.items():
    sec=sections(url)
    if sec: index[url]={'name':name,'sections':sec}
print(f'{len(index)} kapitler i indeks', file=sys.stderr)
def page_lines(p):
    t=open(f'SIDER/{p:03d}.txt',encoding='utf-8').read()
    lines=[norm(l) for l in t.splitlines()]
    # bruk bare "prosalinjer": lange nok, ikke tallrader
    good=[l for l in lines if len(l)>=45 and len(re.findall(r'\d',l))<len(l)*0.3]
    return good
def best_for_page(p):
    lines=page_lines(p)
    scores={}
    for url,ch in index.items():
        for sec in ch['sections']:
            hits=sum(1 for l in lines if l in sec['text'])
            if hits: scores[(url,sec['id'])]=hits
    ranked=sorted(scores.items(), key=lambda kv:-kv[1])
    return len(lines), ranked[:4]
if __name__=='__main__':
    want=[int(x) for x in sys.argv[1:]] or [8,9,46,48,73,81,195,202,204,239,263]+list(range(579,592))+list(range(604,611))
    result={}
    for p in want:
        n,ranked=best_for_page(p)
        if ranked:
            (url,aid),hits=ranked[0]
            title=next(s['title'] for s in index[url]['sections'] if s['id']==aid)
            alt=', '.join(f"{index[u]['name'][:18]}/{a}:{h}" for (u,a),h in ranked[1:3])
            print(f"s.{p:<4} {hits:>2}/{n:<2} -> {index[url]['name'][:32]:<32} {aid:<6} {title[:40]:<40} | alt: {alt}")
            result[p]={'url':url,'anchor':aid,'title':title,'hits':hits,'lines':n,'chapter':index[url]['name']}
        else:
            print(f"s.{p:<4}  0/{n:<2} -> INGEN TREFF")
            result[p]=None
    json.dump(result,open('page_map.json','w'),ensure_ascii=False,indent=1)

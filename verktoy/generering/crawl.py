import json, re, html, subprocess, os, sys, concurrent.futures as cf
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE="https://oslokommune.framsikt.net/2027/oslo/bm-2027-sak1b2027#"
pages=json.load(open('framsikt_pages.json'))   # pageUrl -> name
os.makedirs('crawl',exist_ok=True)

def dump(url, key, budget, tmo):
    prof=f'crawl/prof-{key}'
    out=f'crawl/{key}.html'
    with open(out,'w') as fh:
        try:
            subprocess.run([CH,'--headless=new','--disable-gpu','--no-first-run',f'--user-data-dir={prof}',
                            f'--virtual-time-budget={budget}','--dump-dom',BASE+url],
                           stdout=fh, stderr=subprocess.DEVNULL, timeout=tmo)
        except subprocess.TimeoutExpired:
            pass  # Chrome henger etter dump; fila er som regel komplett
    return open(out,encoding='utf-8',errors='ignore').read()

def anchors(s):
    res=[]
    # Format A: <div class="row h2" id="t-N"> (attributtrekkefølge varierer)
    for m in re.finditer(r'<div\b(?=[^>]*\bclass="row (h[1-4])\b)(?=[^>]*\bid="(t-\d+)")[^>]*>', s):
        lvl,i=m.group(1),m.group(2)
        seg=s[m.end():m.end()+500]
        # første overskriftstekst i segmentet
        h=re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', seg, flags=re.S)
        txt=h.group(1) if h else seg
        txt=html.unescape(re.sub(r'<[^>]+>',' ',txt)); txt=re.sub(r'\s+',' ',txt).strip()
        res.append((i,lvl,txt[:120]))
    # Format B: <h2 id="t-N" bookmark="true">tekst</h2>
    for m in re.finditer(r'<(h[1-4])\b(?=[^>]*\bid="(t-\d+)")(?=[^>]*bookmark="true")[^>]*>(.*?)</\1>', s, flags=re.S):
        txt=html.unescape(re.sub(r'<[^>]+>',' ',m.group(3))); txt=re.sub(r'\s+',' ',txt).strip()
        res.append((m.group(2),m.group(1),txt[:120]))
    # dedupliser, behold rekkefølge etter posisjon i dokumentet
    seen=set(); out=[]
    for r in res:
        if r[0] in seen: continue
        seen.add(r[0]); out.append(r)
    return out

def work(item):
    url,name=item
    key=re.sub(r'[^A-Za-z0-9]+','_',url).strip('_')
    result={'url':url,'name':name,'anchors':[],'status':''}
    for budget,tmo in ((45000,110), (150000,260)):
        s=dump(url,key,budget,tmo)
        if len(s)<1000:
            result['status']='tom'; continue
        a=anchors(s)
        loading = bool(re.search(r'<h1[^>]*>\s*loading\s*</h1>', s, flags=re.I))
        if a or not loading:
            result['anchors']=a; result['status']='ok' if a else 'ingen ankre'; break
        result['status']='loading'
    print(f"{result['status']:<12} {len(result['anchors']):>3}  {name}  {url}", flush=True)
    return result

items=list(pages.items())
if len(sys.argv)>1: items=[i for i in items if sys.argv[1] in i[0]]
with cf.ThreadPoolExecutor(max_workers=5) as ex:
    results=list(ex.map(work, items))
json.dump(results, open('framsikt_anchors.json','w'), ensure_ascii=False, indent=1)
print('FERDIG', len(results), 'sider;', sum(1 for r in results if r['status']=='ok'), 'med ankre')

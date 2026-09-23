"""Gjør sidetall i kildehenvisninger om til lenker, og kontrollerer alle lenker.

Bruk:  python3 verktoy/lenker.py            (alle *.html i nettside/)
       python3 verktoy/lenker.py fil.html    (én fil)

Kilder: sidekart.json (PDF-side -> kapittel/avsnitt i Framsikt) og framsikt-lenker.json (alle kapitler og ankre).
Regler: tall som står etter «s.» i <span class="ref">, <p class="ref…">, <span class="kpi__source"> og
<td data-label="Side|Sider" class="ref"> blir lenke til Framsikt, med en liten «pdf»-lenke etter.
Avslutter med feilkode hvis noen lenke peker feil, HTML er ubalansert eller en henvisning står uten lenke.
"""
import json, re, sys, os, glob, html
from html.parser import HTMLParser
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
BASE="https://oslokommune.framsikt.net/2027/oslo/bm-2027-sak1b2027#"
PDF="https://www.oslo.kommune.no/get-file/2498126/fa442cefc25087e0981d4abf1b623a30b2ab70bf3e15776a796bbc1015e36c91"
sidekart={int(k):v for k,v in json.load(open(os.path.join(ROOT,'sidekart.json'),encoding='utf-8')).items()}
kapitler=json.load(open(os.path.join(ROOT,'framsikt-lenker.json'),encoding='utf-8'))   # url -> {name, anchors{id:title}}

def url_for(p):
    r=sidekart.get(p)
    if not r or not r.get('framsikt'): return None,None
    label=(r['kapittel'] or '')+(f" · {r['avsnitt']}" if r.get('avsnitt') else '')
    return r['framsikt'], label

def strip_links(inner):
    inner=re.sub(r'\s*·\s*<a class="pkt-link"[^>]*>[^<]*</a>','',inner)
    inner=re.sub(r'<a class="ref-pdf"[^>]*>pdf</a>','',inner)
    inner=re.sub(r'<a class="pkt-link"[^>]*>([^<]*)</a>',r'\1',inner)
    return inner

NUM=r'(?<![\d–-])(\d{1,3})(?:–\d{1,3})?(?!\d)'
LIST=r'(\bs\.\s*)((?:\d{1,3}(?:–\d{1,3})?)(?:(?:,\s*|\s+og\s+)\d{1,3}(?:–\d{1,3})?)*)'
def linkify(text):
    def rep(m):
        p=int(m.group(1)); u,label=url_for(p)
        pdf=f'<a class="ref-pdf" href="{PDF}#page={p}" target="_blank" rel="noopener" title="Side {p} i PDF-en">pdf</a>'
        if not u: return m.group(0)+pdf
        return f'<a class="pkt-link" href="{u}" target="_blank" rel="noopener" title="{html.escape(label)}">{m.group(0)}</a>'+pdf
    return re.sub(LIST, lambda m: m.group(1)+re.sub(NUM, rep, m.group(2)), text)

def process(d):
    d=re.sub(r'<span class="ref">(.*?)</span>', lambda m: f'<span class="ref">{linkify(strip_links(m.group(1)))}</span>', d, flags=re.S)
    d=re.sub(r'<p class="(ref[^"]*)">(.*?)</p>', lambda m: f'<p class="{m.group(1)}">{linkify(strip_links(m.group(2)))}</p>', d, flags=re.S)
    d=re.sub(r'<span class="kpi__source">(.*?)</span>', lambda m: f'<span class="kpi__source">{linkify(strip_links(m.group(1)))}</span>', d, flags=re.S)
    def td(m):
        inner=strip_links(m.group(2))
        if re.search(r'\bs\.', inner): return f'<td data-label="{m.group(1)}" class="ref">{linkify(inner)}</td>'
        return f'<td data-label="{m.group(1)}" class="ref">{linkify("s. "+inner)[3:]}</td>'
    d=re.sub(r'<td data-label="(Side|Sider)" class="ref">(.*?)</td>', td, d, flags=re.S)
    return d

VOID={'meta','link','br','img','hr','input','col'}
class P(HTMLParser):
    def __init__(s): super().__init__(); s.stack=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.stack.append(t)
    def handle_endtag(s,t):
        if t in VOID: return
        if s.stack and s.stack[-1]==t: s.stack.pop()
        else: s.err.append((s.getpos()[0],t))

def verify(f,d,all_files):
    problems=[]
    for m in re.finditer(r'<a class="pkt-link" href="'+re.escape(BASE)+r'([^"?]+)(?:\?scrollTo=(t-\d+))?"[^>]*>([^<]*)</a>', d):
        url,aid,txt=m.group(1),m.group(2),m.group(3)
        if url=='/': continue   # forsiden til den digitale versjonen
        ch=kapitler.get(url)
        if not ch: problems.append(f'ukjent kapittel {url}'); continue
        if aid and aid not in ch['anchors']: problems.append(f'anker {aid} finnes ikke i «{ch["name"]}»')
        pm=re.match(r'(\d{1,3})', txt.strip())
        if pm:
            p=int(pm.group(1)); r=sidekart.get(p)
            if r and r.get('framsikt') and not r['framsikt'].startswith(BASE+url): problems.append(f'side {p} hører til «{r["kapittel"]}», lenken går til «{ch["name"]}»')
    p=P(); p.feed(d)
    if p.err or p.stack: problems.append(f'ubalansert HTML {p.err[:2]}')
    for m in re.finditer(r'href="([a-z0-9-]+\.html)(#[a-z]+)?"', d):
        tf,anc=m.group(1),m.group(2)
        if tf not in all_files: problems.append(f'intern lenke til manglende fil {tf}'); continue
        if anc and f'id="{anc[1:]}"' not in all_files[tf]: problems.append(f'intern lenke til manglende anker {tf}{anc}')
    for c in re.findall(r'<td data-label="(?:Side|Sider)" class="ref">(.*?)</td>', d)+[c for c in re.findall(r'<span class="ref">(.*?)</span>', d) if re.search(r'\d',c)]:
        if '<a ' not in c: problems.append(f'henvisning uten lenke: {re.sub("<[^>]+>","",c)[:40]}')
    return problems

if __name__=='__main__':
    files=sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT,'*.html')))
    docs={os.path.basename(f):process(open(f,encoding='utf-8').read()) for f in files}
    for f in files: open(f,'w',encoding='utf-8').write(docs[os.path.basename(f)])
    allf={os.path.basename(f):open(f,encoding='utf-8').read() for f in glob.glob(os.path.join(ROOT,'*.html'))}
    bad=0; links=0
    for name,d in docs.items():
        links+=len(re.findall(re.escape(BASE), d))
        for pr in verify(name,d,allf): bad+=1; print('FEIL',name,pr)
    print(f'{len(docs)} filer, {links} Framsikt-lenker, {bad} problemer')
    sys.exit(1 if bad else 0)

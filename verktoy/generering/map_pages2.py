import json, re, sys
from map_pages import index, norm, pages, best_for_page, BASE
# --- kapittelintervaller fra innholdsfortegnelsen ---
toc=[]
for line in open('INNHOLD.md',encoding='utf-8'):
    m=re.match(r'\s*-\s*(.+?)\s*\(s\.\s*(\d+)\)\s*$', line)
    if m: toc.append((norm(m.group(1)), int(m.group(2))))
fs_by_name={norm(n):u for u,n in pages.items()}
# framsikt-kapitler i TOC-rekkefølge med startside
chap=[]
for title,p in toc:
    if title in fs_by_name and fs_by_name[title] not in [c[1] for c in chap]:
        chap.append((title, fs_by_name[title], p))
# "Til Oslo bystyre" osv. finnes; sørg for sortering etter side
chap.sort(key=lambda c:c[2])
def chapter_for(p, top_of_page=True):
    cur=None; prev=None
    for title,url,start in chap:
        if start<=p: prev,cur=cur,(title,url,start)
        else: break
    # Hvis kapitlet starter på denne siden, men ikke øverst (prosa fra forrige kapittel først),
    # hører toppen av siden til forrige kapittel.
    if top_of_page and cur and prev and cur[2]==p:
        lines=page_raw_lines(p)
        for l in lines:
            if l==cur[0] or l.rstrip(':')==cur[0]: break      # kapitteloverskrift kommer før prosa: ok
            if len(l)>60: return prev                            # prosa først: forrige kapittel
    return cur
HDR=norm('Budsjett 2027 og økonomiplan 2027-2030')
def page_raw_lines(p):
    t=open(f'SIDER/{p:03d}.txt',encoding='utf-8').read()
    out=[]
    for l in t.splitlines():
        n=norm(l)
        if not n or n==HDR or re.fullmatch(r'\d+',n): continue
        out.append(n)
    return out
def anchor_for(p):
    ch=chapter_for(p)
    if not ch: return None
    title,url,start=ch
    if url not in index:  # ikke crawlet
        return {'url':url,'chapter':pages[url],'anchor':None,'title':None,'why':'kapittel ikke crawlet'}
    secs=index[url]['sections']
    titles=[s['title'] for s in secs]
    cur=-1
    def scan(lines, stop_at_prose=False):
        nonlocal cur
        for l in lines:
            if stop_at_prose and len(l)>60 and cur>=0: return
            # eksakt overskriftstreff, uavhengig av rekkefølge; ved duplikate titler foretrekkes neste etter gjeldende
            cands=[j for j in range(len(secs)) if titles[j] and (l==titles[j] or l.rstrip(':')==titles[j].rstrip(':'))]
            if cands:
                after=[j for j in cands if j>cur]
                cur=(after or cands)[0]
    for q in range(start, p): scan(page_raw_lines(q))
    top=cur
    scan(page_raw_lines(p), stop_at_prose=True)
    if cur<0: return {'url':url,'chapter':pages[url],'anchor':None,'title':None,'why':'ingen overskrift funnet'}
    s=secs[cur]
    return {'url':url,'chapter':pages[url],'anchor':s['id'],'title':s['title'],'why':'overskrift'}
if __name__=='__main__':
    want=[int(x) for x in sys.argv[1:]]
    if not want:
        import glob
        d=''.join(open(f,encoding='utf-8').read() for f in sorted(glob.glob('NETTSIDE/*.html')))
        fields=re.findall(r'<span class="ref">(.*?)</span>', d, flags=re.S)+re.findall(r'<td data-label="(?:Side|Sider)" class="ref">(.*?)</td>', d, flags=re.S)+re.findall(r'<p class="ref[^"]*">(.*?)</p>', d, flags=re.S)+re.findall(r'<span class="kpi__source">(.*?)</span>', d, flags=re.S)
        nums=set()
        for f in fields:
            txt=re.sub(r'<a class="ref-pdf"[^>]*>pdf</a>','',f); txt=re.sub(r'<[^>]+>','',txt)
            if not re.search(r'\bs\.', txt): txt='s. '+txt   # tabellceller med rene sidetall
            for m in re.finditer(r'\bs\.\s*((?:\d{1,3}(?:–\d{1,3})?)(?:(?:,\s*|\s+og\s+)\d{1,3}(?:–\d{1,3})?)*)', txt):
                nums.update(int(x) for x in re.findall(r'(?<![\d–-])(\d{1,3})(?!\d)', m.group(1)))
        want=sorted(p for p in nums if 1<=p<=685)
    res={}
    for p in want:
        a=anchor_for(p)
        n,ranked=best_for_page(p)
        # foretrekk avsnittet med flest tekstlinjer fra siden, hvis det er i samme kapittel og treffet er solid
        if a and a['anchor'] and ranked:
            (u,aid),h=ranked[0]
            if u==a['url'] and aid!=a['anchor'] and h>=5:
                t=next(x['title'] for x in index[u]['sections'] if x['id']==aid)
                a={'url':u,'chapter':pages[u],'anchor':aid,'title':t,'why':f'linjetreff ({h} linjer)'}
        check=''
        if a and a['anchor'] and ranked:
            (u,aid),h=ranked[0]
            check = 'OK' if (u==a['url'] and aid==a['anchor']) else f"AVVIK: linjetreff peker på {pages[u][:20]}/{aid} ({h} linjer)"
        elif a and a['anchor']: check='(ingen linjetreff å kontrollere mot)'
        if a: print(f"s.{p:<4} {a['chapter'][:34]:<34} {str(a['anchor']):<6} {str(a['title'])[:38]:<38} {a['why']:<24} {check}")
        else: print(f"s.{p:<4} INGEN KAPITTEL")
        res[p]=a
    json.dump(res,open('page_map2.json','w'),ensure_ascii=False,indent=1)

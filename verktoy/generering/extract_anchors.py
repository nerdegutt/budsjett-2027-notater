import re,html,sys,json
f=sys.argv[1]; s=open(f,encoding='utf-8',errors='ignore').read()
out=[]
for m in re.finditer(r'<div[^>]*\bid="(t-\d+)"[^>]*class="row (h[1-4])[^"]*"[^>]*>|<div[^>]*class="row (h[1-4])[^"]*"[^>]*\bid="(t-\d+)"[^>]*>', s):
    i=m.group(1) or m.group(4); lvl=m.group(2) or m.group(3)
    seg=s[m.end():m.end()+400]
    txt=html.unescape(re.sub(r'<[^>]+>',' ',seg)); txt=re.sub(r'\s+',' ',txt).strip()
    txt=txt[:70]
    out.append((i,lvl,txt))
for i,l,t in out: print(f'{i:<6} {l:<3} {t}')
json.dump(out,open(f.replace('.html','.anchors.json'),'w'),ensure_ascii=False)

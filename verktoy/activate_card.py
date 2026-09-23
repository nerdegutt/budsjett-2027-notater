import re, sys, html
title, href, ref = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv)>3 else '')
import os
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','index.html')
d=open(F,encoding='utf-8').read()
pat=re.compile(r'(<article class="panel )([^"]*?) panel--planned(">\s*)<p class="mb-size-8"><span class="pkt-tag pkt-tag--gray pkt-tag--thin-text">Planlagt</span></p>(<h3 class="pkt-txt-22 pkt-txt-24-medium--tablet-up mb-size-8">)'+re.escape(title)+r'(</h3>\s*<p class="pkt-txt-16-light mb-size-8">.*?</p>)\s*(</article>)', re.S)
def rep(m):
    skin=m.group(2).replace('panel--grey','').strip() or 'panel--blue'
    refh=f'\n              <p class="ref">{ref}</p>\n            ' if ref else '\n            '
    return f'{m.group(1)}{skin}{m.group(3)}{m.group(4)}<a class="pkt-link" href="{href}">{title}</a>{m.group(5)}{refh}{m.group(6)}'
d2,n=pat.subn(rep,d)
assert n==1, f'fant {n} kort med tittelen {title!r}'
open(F,'w',encoding='utf-8').write(d2); print('aktivert:',title,'->',href)

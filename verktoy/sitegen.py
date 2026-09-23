import re
import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
_src=open(ROOT+'kommunemaal.html',encoding='utf-8').read()
HEAD=_src.split('<body>')[0]
FOOTER=re.search(r'(<footer class="site-footer.*?</footer>)', _src, re.S).group(1)
NAV=re.search(r'(<pkt-header.*?</pkt-header>)', _src, re.S).group(1)
SEP='          <!-- ================================================================ -->\n'
ALERT_STD='''          <pkt-alert skin="info" compact>
            <p class="mb-size-0">Alle beløp er i 1 000 kroner der ikke annet er sagt. Tallene er byrådets forslag og blir først bindende når bystyret har vedtatt budsjettet i desember. Sidetallene er lenker til den digitale versjonen, «pdf» åpner samme side i PDF-en. Alt er oppsummering fra budsjettet, unntatt avsnitt merket <span class="pkt-tag pkt-tag--yellow pkt-tag--small">Claudes vurdering</span>.</p>
          </pkt-alert>
'''
def assessment(title, body_html, small=True):
    tag='pkt-tag--small' if small else ''
    return f'''            <div class="assessment mt-size-24">
              <p class="mb-size-8"><span class="pkt-tag pkt-tag--yellow {tag}">Claudes vurdering</span></p>
              {f'<h3 class="pkt-txt-18-medium mb-size-8">{title}</h3>' if title else ''}
              {body_html}
            </div>
'''
def section(sid, title, inner, first=False):
    return f'{SEP}          <section id="{sid}"{" class=&quot;mt-size-40&quot;".replace("&quot;",chr(34)) if first else ""}>\n            <h2 class="pkt-txt-26 pkt-txt-36--tablet-up mb-size-16">{title}</h2>\n{inner}\n          </section>\n'
def table(headers, rows, caption=None, compact=True, numcols=()):
    th=''.join(f'<th{" class=&quot;num&quot;".replace("&quot;",chr(34)) if i in numcols else ""}>{h}</th>' for i,h in enumerate(headers))
    body=''
    for r in rows:
        cls=''
        if isinstance(r,dict): cls=f' class="{r["cls"]}"'; r=r['cells']
        tds=''.join(f'<td data-label="{headers[i]}"{" class=&quot;num&quot;".replace("&quot;",chr(34)) if i in numcols else ""}>{c}</td>' for i,c in enumerate(r))
        body+=f'                  <tr{cls}>{tds}</tr>\n'
    cap=f'                <caption class="pkt-txt-14-medium">{caption}</caption>\n' if caption else ''
    return f'''            <div class="table-scroll">
              <table class="pkt-table pkt-table--basic {"pkt-table--compact" if compact else ""} pkt-table--responsive">
{cap}                <thead><tr>{th}</tr></thead>
                <tbody>
{body}                </tbody>
              </table>
            </div>
'''
def page(filename, title, kicker, h1, ingress, sections, toc_items, alert=ALERT_STD, extra_hero=''):
    toc='<nav class="pkt-cell pkt-cell--span12 pkt-cell--span3-laptop-up toc" aria-label="Innhold på siden">\n          <p class="pkt-txt-16-medium mb-size-8">På denne siden</p>\n          <ol class="pkt-txt-16-light">\n'+''.join(f'            <li><a class="pkt-link" href="#{i}">{t}</a></li>\n' for i,t in toc_items)+'          </ol>\n        </nav>'
    html=f'''{HEAD.replace(re.search(r'<title>.*?</title>',HEAD).group(0), f'<title>{title}</title>')}<body>
<div class="pkt-layout">
  {NAV}

  <main>
    <section class="site-hero py-size-48">
      <div class="pkt-container">
        <p class="pkt-txt-14-medium mb-size-8">{kicker}</p>
        <h1 class="pkt-txt-36 pkt-txt-54--tablet-up mb-size-16">{h1}</h1>
        <p class="pkt-txt-20-light pkt-txt-24-light--tablet-up mb-size-0" style="max-width: 46rem">{ingress}</p>
        {extra_hero}
      </div>
    </section>

    <div class="pkt-container py-size-40">
      <div class="pkt-grid">
        {toc}
        <article class="pkt-cell pkt-cell--span12 pkt-cell--span9-laptop-up">
{alert}
{''.join(sections)}
        </article>
      </div>
    </div>
  </main>

  {FOOTER}
</div>
</body>
</html>
'''
    open(ROOT+filename,'w',encoding='utf-8').write(html)
    return filename

"""Legg til et kort på forsiden i et gitt lag.
Bruk: python3 verktoy/add_card.py <lag 1|2|3> <fil.html> "Tittel" "Ingress" "Kilde: s. …" [skin] [tagtekst tagklasse]
"""
import re, sys, os
lag, href, title, text, ref = sys.argv[1:6]
skin = sys.argv[6] if len(sys.argv) > 6 else ''
tag = f'<p class="mb-size-8"><span class="pkt-tag {sys.argv[8]} pkt-tag--thin-text">{sys.argv[7]}</span></p>' if len(sys.argv) > 8 else ''
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
d = open(F, encoding='utf-8').read()
card = f'''          <div class="pkt-cell pkt-cell--span12 pkt-cell--span6-tablet-up pkt-cell--span4-laptop-up">
            <article class="panel {skin}">
              {tag}<h3 class="pkt-txt-22 pkt-txt-24-medium--tablet-up mb-size-8"><a class="pkt-link" href="{href}">{title}</a></h3>
              <p class="pkt-txt-16-light mb-size-8">{text}</p>
              <p class="ref">{ref}</p>
            </article>
          </div>
'''
# finn seksjonen for laget og sett kortet inn sist i dens pkt-grid
m = re.search(r'<p class="pkt-txt-14-medium mb-size-4">Lag ' + re.escape(lag) + r'</p>.*?<div class="pkt-grid">(.*?)\n        </div>', d, re.S)
assert m, f'fant ikke lag {lag}'
d = d[:m.end(1)] + '\n' + card.rstrip('\n') + d[m.end(1):]
open(F, 'w', encoding='utf-8').write(d)
print('kort lagt til i lag', lag, '->', href)

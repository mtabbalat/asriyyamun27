"""Apply the requested 2027 editorial content to the static conference pages."""
from pathlib import Path
from bs4 import BeautifulSoup
import copy, json
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
content=json.loads((ROOT/'content.json').read_text())

def read(name): return BeautifulSoup((DIST/name).read_text(),'html.parser')
def save(name,soup): (DIST/name).write_text(str(soup))

def letter(kind):
 s=read('letter-from-the-sg.html')
 data=content[kind]
 s.main.h1.string='The Secretary-General' if kind=='sg' else 'The Head of Conference'
 s.title.string=f"Letter from the {'SG' if kind=='sg' else 'HOC'} — AsriyyaMUN’27"
 description=s.find('meta',attrs={'name':'description'})
 description['content']=f"A welcome from {data['role']} {data['name']} for AsriyyaMUN’27."
 section=s.main.section
 columns=section.find('div',recursive=False)
 portrait,body=columns.find_all('div',recursive=False)
 image=portrait.img
 image['src']=data['image'];image['alt']=f"{data['name']}, {data['role']}"
 image['width']='1550' if kind=='hoc' else '1568';image['height']='1600' if kind=='hoc' else '1573'
 image['loading']='eager'; image['class']=list(dict.fromkeys(image['class']+['letter-portrait']))
 captions=portrait.find_all('p',recursive=False)
 captions[0].string=data['name'];captions[1].string=data['role']
 body.clear()
 for text in data['paragraphs']:
  p=s.new_tag('p',attrs={'class':'mb-5 leading-relaxed text-ink/80'})
  p.string=text;body.append(p)
 signature=s.new_tag('p',attrs={'class':'mt-8 leading-relaxed text-ink/80'})
 if kind=='hoc':
  role=s.new_tag('span',attrs={'class':'text-sm text-ink/60'});role.string='(Head Of Conference)'
  signature.append(role);signature.append(s.new_tag('br'))
 name=s.new_tag('span',attrs={'class':'font-display text-lg text-sand'});name.string=data['name'];signature.append(name)
 body.append(signature)
 save(f'letter-from-the-{kind}.html',s)

letter('sg');letter('hoc')
s=read('theme.html')
s.title.string='Turn The Tide — AsriyyaMUN’27'
s.find('meta',attrs={'name':'description'})['content']='Turn The Tide — the theme for AsriyyaMUN’27.'
s.main.h1.clear()
title=s.new_tag('span',attrs={'class':'italic'});title.append('Turn The ')
highlight=s.new_tag('span',attrs={'class':'text-sand'});highlight.string='Tide';title.append(highlight);s.main.h1.append(title)
subtitle=s.main.h1.find_next_sibling('p')
if subtitle:subtitle.decompose()
s.main.section.clear()
for i,text in enumerate(content['theme']['paragraphs']):
 reveal=s.new_tag('div',attrs={'class':'reveal-hidden','style':f'animation-delay:{i*60}ms'})
 p=s.new_tag('p',attrs={'class':'mb-6 text-lg leading-relaxed text-ink/80 first-letter:font-display first-of-type:first-letter:float-left first-of-type:first-letter:mr-3 first-of-type:first-letter:text-6xl first-of-type:first-letter:leading-[0.9] first-of-type:first-letter:text-sand'})
 p.string=text;reveal.append(p);s.main.section.append(reveal)
save('theme.html',s)

for file in DIST.rglob('*.html'):
 s=BeautifulSoup(file.read_text(),'html.parser')
 # Keep the same shared navigation on every route.
 nav=s.header.nav
 sg=nav.find('a',href='/letter-from-the-sg')
 if sg and not nav.find('a',href='/letter-from-the-hoc'):
  hoc=copy.deepcopy(sg);hoc['href']='/letter-from-the-hoc';hoc.string='Letter from the HOC';sg.insert_after(hoc)
 for node in list(s.find_all(string=True)):
  value=str(node)
  if 'Shifting Sands' in value:
   value=value.replace('Shifting Sands — navigating a world defined by change.','Turn The Tide')
   value=value.replace('Shifting Sands','Turn The Tide')
   node.replace_with(value)
 # Synchronize the home letter teaser with its new author.
 for teaser in s.main.select('a[href="/letter-from-the-sg"] p'):
  if 'A welcome from Secretary-General' in teaser.get_text():teaser.string='A welcome from Secretary-General Lina El-Jawhari.'
 for old in s.select('#mobile-navigation'):old.decompose()
 mobile=s.new_tag('nav',attrs={'class':'mobile-navigation','id':'mobile-navigation','aria-label':'Mobile navigation','hidden':''})
 for i,group in enumerate(nav.find_all('div',recursive=False)):
  parent=group.find('a',recursive=False)
  if not parent:continue
  wrap=s.new_tag('div');row=s.new_tag('div',attrs={'class':'mobile-row'})
  link=copy.deepcopy(parent)
  for icon in link.select('svg'):icon.decompose()
  link.attrs.pop('class',None);row.append(link)
  submenu=group.find('div',recursive=False)
  if submenu:
   button=s.new_tag('button',attrs={'type':'button','aria-label':f"Expand {link.get_text(strip=True)} menu",'aria-expanded':'false','aria-controls':f'mobile-submenu-{i}'})
   icon=parent.find('svg')
   if icon:button.append(copy.deepcopy(icon))
   row.append(button)
  wrap.append(row)
  if submenu:
   children=s.new_tag('div',attrs={'class':'mobile-children','id':f'mobile-submenu-{i}','hidden':''})
   for a in submenu.find_all('a'):
    child=copy.deepcopy(a);child.attrs.pop('class',None);children.append(child)
   wrap.append(children)
  mobile.append(wrap)
 s.header.append(mobile)
 toggle=s.header.find('button',attrs={'aria-label':'Toggle menu'})
 toggle['type']='button';toggle['aria-expanded']='false';toggle['aria-controls']='mobile-navigation'
 nav['aria-label']='Main navigation'
 for element in s.select('footer form input, footer form textarea'):
  placeholder=element.get('placeholder','')
  field='name' if placeholder=='Name' else 'email' if placeholder=='Email' else 'message'
  element['name']=field;element['aria-label']=placeholder
  if field!='message':element['autocomplete']=field
 for button in s.select('main button'):
  if button.img:button['type']='button';button['data-gallery-image']=''
 if not s.find('link',href='/site.css'):
  s.head.append(s.new_tag('link',attrs={'rel':'stylesheet','href':'/site.css'}))
 if not s.find('script',src='/site.js'):
  s.head.append(s.new_tag('script',attrs={'src':'/site.js','defer':''}))
 file.write_text(str(s))
print('Updated',len(list(DIST.rglob('*.html'))),'pages.')

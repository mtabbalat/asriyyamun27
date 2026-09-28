"""Update team cards, using CSS viewports to crop the supplied portrait sheets.

The original JPEGs remain unchanged. Crop coordinates in team.json refer to
the 900 × 1600 supplied sheets; each viewport excludes the white margins and
printed labels while preserving the photograph's proportions.
"""
from pathlib import Path
import copy
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / 'dist/team.html'
people = json.loads((ROOT / 'team.json').read_text())
soup = BeautifulSoup(page.read_text(), 'html.parser')
section = soup.main.find('section')
grid = section.find('div', class_='grid')
template = copy.deepcopy(grid.find('div', recursive=False))
grid.clear()

for i, person in enumerate(people):
    card = copy.deepcopy(template)
    card['style'] = f'animation-delay:{(i % 4) * 90}ms'
    card['data-team-member'] = person['name']
    card.h2.string = person['name']
    card.find('p').string = person['role']
    frame = card.select_one('.aspect-square')
    frame.clear()
    viewport = soup.new_tag('div', attrs={
        'class': 'team-portrait-crop transition-transform duration-500 group-hover:scale-105',
        'style': 'position:absolute;inset:0;overflow:hidden'
    })
    x, y, size = person['crop']
    image = soup.new_tag('img', attrs={
        'src': f"/images/team-2027/team-sheet-{person['sheet']:02d}.jpeg",
        'alt': person['name'],
        'width': '900',
        'height': '1600',
        'loading': 'eager' if i < 4 else 'lazy',
        'decoding': 'async',
        'style': (
            f'position:absolute;max-width:none;width:{900 / size * 100:.8f}%;'
            f'height:{1600 / size * 100:.8f}%;'
            f'left:{-x / size * 100:.8f}%;top:{-y / size * 100:.8f}%;'
            'object-fit:fill'
        )
    })
    viewport.append(image)
    frame.append(viewport)
    grid.append(card)

# The new supplied roster replaces the former roster in full.
for old_section in soup.main.find_all('section', recursive=False)[1:]:
    old_section.decompose()

page.write_text(str(soup))
print(f'Updated {len(people)} team cards.')

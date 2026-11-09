from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import fitz, shutil

def svg2png(*,bytestring,write_to,output_width=None,output_height=None):
    src=fitz.open(stream=bytestring,filetype='svg')
    pdf=fitz.open(stream=src.convert_to_pdf(),filetype='pdf')
    page=pdf[0]
    scale=(output_width/page.rect.width) if output_width else 1
    page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=True).save(write_to)

ROOT=Path(__file__).parent
BRAND=ROOT/'identidad'
WEB=ROOT/'web/assets'
BRAND.mkdir(exist_ok=True,parents=True)
WEB.mkdir(exist_ok=True,parents=True)
INK='#173D38'
LIME='#D8EEA0'
PAPER='#F7F8F2'

def icon(fill=INK, line='white', dot=LIME):
    return f'<rect width="72" height="72" rx="21" fill="{fill}"/><path d="M49 22a20 20 0 1 0 3 24V36H37" fill="none" stroke="{line}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="49" cy="22" r="4.5" fill="{dot}"/>'

font=TTFont(WEB/'montserrat-bold.woff')
glyphs=font.getGlyphSet()
cmap=font.getBestCmap()
units=font['head'].unitsPerEm
def paths(text, size=43,tracking=-.7):
    s=size/units
    x=0
    bits=[]
    for ch in text:
        name=cmap[ord(ch)]
        pen=SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        bits.append(f'<path d="{pen.getCommands()}" transform="translate({x:.4f} 0)"/>')
        x+=glyphs[name].width+tracking/s
    return f'<g transform="scale({s} {-s})">'+''.join(bits)+'</g>',x*s

word,w=paths('GuíaTrámite')
for name,fill,line,dot,text in [
    ('principal',INK,'#FFFFFF',LIME,INK),
    ('blanco','#FFFFFF',INK,INK,'#FFFFFF'),
    ('monocromo',INK,'#FFFFFF','#FFFFFF',INK),
    ('negro','#111111','#FFFFFF','#FFFFFF','#111111')]:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w+100:.0f}" height="80" viewBox="0 0 {w+100:.0f} 80"><title>GuíaTrámite</title><g transform="translate(0 4)">{icon(fill,line,dot)}</g><g transform="translate(91 56)" fill="{text}">{word}</g></svg>'
    (BRAND/f'guiatramite-logo-{name}.svg').write_text(svg)
    svg2png(bytestring=svg.encode(),write_to=str(BRAND/f'guiatramite-logo-{name}.png'),output_width=int((w+100)*4),output_height=320)
    if name=='principal': shutil.copy(BRAND/f'guiatramite-logo-{name}.svg',WEB/'logo.svg')
    if name=='blanco': shutil.copy(BRAND/f'guiatramite-logo-{name}.svg',WEB/'logo-white.svg')

icon_svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="72" height="72"><title>GuíaTrámite</title>{icon()}</svg>'
(BRAND/'guiatramite-simbolo.svg').write_text(icon_svg)
shutil.copy(BRAND/'guiatramite-simbolo.svg',WEB/'favicon.svg')
for size in [32,180,512,1024]:
    svg2png(bytestring=icon_svg.encode(),write_to=str(BRAND/f'guiatramite-simbolo-{size}.png'),output_width=size,output_height=size)
shutil.copy(BRAND/'guiatramite-simbolo-180.png',WEB/'apple-touch-icon.png')

# Self-contained social card with vector letterforms.
headline,hw=paths('Cada paso, más claro.',size=64)
social=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="{PAPER}"/><circle cx="1090" cy="520" r="290" fill="{LIME}"/><path d="M910 600V230a110 110 0 0 1 110-110h200" stroke="{INK}" stroke-width="28" fill="none"/><g transform="translate(75 65)">{icon()}</g><g fill="{INK}" transform="translate(165 118)">{word}</g><g fill="{INK}" transform="translate(75 335)">{headline}</g><text x="78" y="410" fill="{INK}" font-size="28" font-family="sans-serif">Orientación para personas. Apoyo para instituciones.</text><rect x="78" y="490" width="240" height="42" rx="21" fill="{INK}"/><text x="102" y="518" font-size="19" font-family="sans-serif" fill="white">Proyecto en desarrollo</text></svg>'
(BRAND/'guiatramite-social.svg').write_text(social)
svg2png(bytestring=social.encode(),write_to=str(WEB/'social.png'))
shutil.copy(WEB/'social.png',BRAND/'guiatramite-social.png')

def text_path(text,x,y,size=22,fill=INK):
    shape,_=paths(text,size=size,tracking=-.3)
    return f'<g fill="{fill}" transform="translate({x} {y})">{shape}</g>'

board=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720"><rect width="1200" height="720" fill="'+PAPER+'"/>']
board.append(text_path('GUÍATRAMITE / NUEVA IDENTIDAD',75,72,size=15))
scale=1050/(w+100)
board.append(f'<g transform="translate(75 144) scale({scale})"><g transform="translate(0 4)">{icon()}</g><g transform="translate(91 56)" fill="{INK}">{word}</g></g>')
board.append(text_path('Una G que marca el camino.',75,452,size=36))
board.append(text_path('Un recorrido continuo. Un punto de orientación.',75,496,size=20,fill='#637366'))
board.append(text_path('Símbolo a tamaño de uso',75,557,size=14,fill='#637366'))
for x,size in [(75,32),(141,48),(225,72)]:
    board.append(f'<g transform="translate({x} 584) scale({size/72})">{icon()}</g>')
board.append(f'<rect x="602" y="544" width="523" height="128" rx="20" fill="{INK}"/>')
board.append(f'<g transform="translate(627 566) scale({473/(w+100)})"><g transform="translate(0 4)">{icon("#FFFFFF",INK,INK)}</g><g transform="translate(91 56)" fill="#FFFFFF">{word}</g></g>')
board.append('</svg>')
board=''.join(board)
(BRAND/'GuiaTramite_Nueva_Identidad.svg').write_text(board)
svg2png(bytestring=board.encode(),write_to=str(BRAND/'GuiaTramite_Nueva_Identidad.png'))
print('Assets ready')

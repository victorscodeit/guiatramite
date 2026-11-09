"""Build the standalone review page and the delivery archives from current source."""
from pathlib import Path
import base64,re,zipfile,shutil

ROOT=Path(__file__).parent
WEB=ROOT/'web'
MIMES={'.svg':'image/svg+xml','.png':'image/png','.woff':'font/woff','.pdf':'application/pdf'}
def uri(path):
    return 'data:'+MIMES[path.suffix]+';base64,'+base64.b64encode(path.read_bytes()).decode()

html=(WEB/'index.html').read_text()
def inline_css(match):
    text=(WEB/match[1]).read_text()
    def inline_url(m):
        return "url('"+uri(WEB/m[1])+"')"
    text=re.sub(r"url\(['\"]?(assets/[^)'\"]+)['\"]?\)",inline_url,text)
    return '<style>'+text+'</style>'
html=re.sub(r'<link rel="stylesheet" href="([^"]+)">',inline_css,html)
html=re.sub(r'<link rel="preload"[^>]+>','',html)
html=html.replace('<script src="app.js" defer></script>','')
for path in sorted((WEB/'assets').iterdir()):
    if path.suffix in ['.svg','.png']:
        data=uri(path)
        html=html.replace('/assets/'+path.name,data).replace('assets/'+path.name,data)
pdf=WEB/'downloads/GuiaTramite_Propuesta_Piloto.pdf'
html=html.replace('downloads/'+pdf.name,uri(pdf))
html=html.replace('</body>','<script>'+(WEB/'app.js').read_text()+'</script></body>')
assert 'href="styles.css"' not in html and 'href="reference.css"' not in html
assert 'src="assets/' not in html and "url('assets/" not in html
(ROOT/'GuiaTramite_Landing.html').write_text(html)

with zipfile.ZipFile(ROOT/'GuiaTramite_Imagen_Corporativa.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for p in sorted((ROOT/'identidad').iterdir()):
        if p.is_file():archive.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(ROOT/'GuiaTramite_Proyecto_Completo.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for folder in ['web','identidad','documentos']:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file():archive.write(p,p.relative_to(ROOT))
    for name in ['README.md','GuiaTramite_Landing.html','package_project.py','build_assets.py','build_documents.py']:
        archive.write(ROOT/name,name)
for name in ['GuiaTramite_Imagen_Corporativa.zip','GuiaTramite_Proyecto_Completo.zip']:
    with zipfile.ZipFile(ROOT/name) as archive:assert archive.testzip() is None
for name in ['GuiaTramite_Landing.html','GuiaTramite_Imagen_Corporativa.zip','GuiaTramite_Proyecto_Completo.zip']:
    print(name,(ROOT/name).stat().st_size)

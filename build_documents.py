from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from xml.sax.saxutils import escape
import json, shutil, fitz

ROOT=Path(__file__).parent
OUT=ROOT/'documentos'
OUT.mkdir(exist_ok=True)
W,H=A4
INK='#173D38'; LIME='#D8EEA0'; PAPER='#F7F8F2'; MUTED='#637366'; LINE='#D5DFCF'
for name,file in [('Guide','DejaVuSans.ttf'),('GuideBold','DejaVuSans-Bold.ttf'),('GuideItalic','DejaVuSans.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('Guide',normal='Guide',bold='GuideBold',italic='GuideItalic',boldItalic='GuideBold')
styles={
 'body':ParagraphStyle('body',fontName='Guide',fontSize=10,leading=15,textColor=colors.HexColor(INK),spaceAfter=9),
 'small':ParagraphStyle('small',fontName='Guide',fontSize=8.6,leading=12.7,textColor=colors.HexColor(MUTED)),
 'title':ParagraphStyle('title',fontName='GuideBold',fontSize=29,leading=34,textColor=colors.HexColor(INK)),
 'h2':ParagraphStyle('h2',fontName='GuideBold',fontSize=13,leading=18,textColor=colors.HexColor(INK)),
 'quote':ParagraphStyle('quote',fontName='Guide',fontSize=11,leading=17,textColor=colors.HexColor(INK)),
 'cell':ParagraphStyle('cell',fontName='Guide',fontSize=8.2,leading=12,textColor=colors.HexColor(INK)),
 'cellhead':ParagraphStyle('cellhead',fontName='GuideBold',fontSize=8.2,leading=12,textColor=colors.white),
}
def P(text,style='body'):
    return Paragraph(text,styles[style])

class Doc:
    def __init__(self,name,label):
        self.path=OUT/name;self.c=canvas.Canvas(str(self.path),pagesize=A4);self.label=label;self.n=0;self.y=0
        self.c.setTitle(label+' | GuíaTrámite');self.c.setAuthor('GuíaTrámite');self.md=[]
    def page(self,kicker,title,lead=None):
        if self.n:self.c.showPage()
        self.n+=1;c=self.c;c.setFillColor(colors.HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
        c.drawImage(str(ROOT/'identidad/guiatramite-logo-principal.png'),43,H-70,width=177,height=40.5,mask='auto',preserveAspectRatio=True)
        c.setFillColor(colors.HexColor(MUTED));c.setFont('Guide',8);c.drawRightString(W-43,H-48,self.label)
        c.setStrokeColor(colors.HexColor(LINE));c.line(43,43,W-43,43)
        c.setFont('Guide',7.5);c.setFillColor(colors.HexColor(MUTED));c.drawString(43,28,'GuíaTrámite · Noviembre 2026');c.drawRightString(W-43,28,f'{self.n:02d}')
        self.y=H-110
        self.eyebrow(kicker)
        self.para(title,'title',after=17)
        if lead:self.para(lead,'body',after=16)
        self.md.extend(['\n# '+title.replace('<br/>',' '),'',lead or '',''])
    def eyebrow(self,text):
        self.c.setFillColor(colors.HexColor('#6B8261'));self.c.setFont('GuideBold',8);self.c.drawString(43,self.y,text.upper());self.y-=22
    def para(self,text,style='body',after=10):
        para=P(text,style);_,h=para.wrap(W-86,2000)
        if self.y-h<60:raise ValueError(f'Overflow on page {self.n}: {text[:70]} y={self.y} h={h}')
        para.drawOn(self.c,43,self.y-h);self.y-=h+after
    def heading(self,text):
        self.y-=5;self.para(text,'h2',after=9);self.md.extend(['\n## '+text,''])
    def body(self,text,small=False):
        self.para(text,'small' if small else 'body',after=10);self.md.append(text.replace('<b>','**').replace('</b>','**')+'\n')
    def quote(self,text):
        para=P(text,'quote');_,h=para.wrap(W-116,2000)
        if self.y-h-28<60:raise ValueError('quote overflow')
        self.c.setFillColor(colors.HexColor('#EAF0E2'));self.c.roundRect(43,self.y-h-25,W-86,h+25,8,fill=1,stroke=0)
        para.drawOn(self.c,58,self.y-h-12);self.y-=h+40;self.md.append('> '+text+'\n')
    def bullets(self,items):
        for item in items:
            self.body('• '+item)
    def table(self,headers,rows,widths):
        cells=[[P(escape(str(s)),'cellhead') for s in headers]]+[[P(str(s),'cell') for s in row] for row in rows]
        tab=Table(cells,colWidths=widths,hAlign='LEFT')
        tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(INK)),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#EDF2E7')]),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#CFD9C8')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10)]))
        _,h=tab.wrap(W-86,2000)
        if self.y-h<60:raise ValueError('table overflow')
        tab.drawOn(self.c,43,self.y-h);self.y-=h+16
        self.md.extend(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows]+[''])
    def finish(self,markdown=False):
        self.c.save()
        if markdown:self.path.with_suffix('.md').write_text('\n'.join(self.md))
        return self.path

meeting=Doc('GuiaTramite_Reunion_Ayuntamiento.pdf','Guion de reunión')
meeting.page('01  Objetivo y enfoque','Preparar una reunión<br/>útil con el ayuntamiento','Objetivo: salir con un problema prioritario identificado, una persona de referencia y un siguiente paso acordado para valorar un piloto. La reunión es una conversación de descubrimiento apoyada por una demostración de la propuesta.')
meeting.quote('GuíaTrámite es un proyecto de IA para ayudar a las personas recién llegadas a entender sus siguientes pasos y a los equipos municipales a preparar mejor su atención.')
meeting.heading('El problema que conviene contrastar')
meeting.body('La hipótesis es que parte de las consultas y visitas de repetición se debe a información difícil de comprender, documentación incompleta o dudas sobre el servicio adecuado. Se debe comprobar con el equipo, sin asumir que todos los servicios tienen el mismo problema.')
meeting.heading('Cómo presentar lo que existe hoy')
meeting.body('El equipo está formado por cuatro ingenieros. El proyecto está en desarrollo. La landing y la demo muestran la experiencia propuesta; las respuestas están preparadas y los datos son ficticios. La IA real, los contenidos municipales y el seguimiento de casos deben concretarse y validarse.')
meeting.heading('Cómo mejorar el enfoque inicial')
meeting.body('Conservar la cercanía y la invitación a aportar experiencia. Sustituir la urgencia de “otros municipios os adelantarán” por la posibilidad de participar en el diseño de un piloto ajustado a su servicio. Hablar de objetivos medibles, sin prometer reducciones de tiempos ni beneficios que todavía no se han comprobado.')
meeting.heading('Qué decisión buscamos')
meeting.body('No pedir una contratación inmediata. Proponer una sesión de trabajo con el referente del servicio y, cuando corresponda, las personas de sistemas y protección de datos. Tras esa sesión, preparar una propuesta de alcance, calendario, recursos y coste para su valoración.')

meeting.page('02  Apertura en castellano','Discurso de apertura','Duración orientativa: entre dos y tres minutos. Habla una persona del equipo, con naturalidad. Después se cede la palabra al ayuntamiento.')
speech_es=[
 'Gracias por recibirnos. Estamos desarrollando GuíaTrámite, una herramienta para ayudar a las personas recién llegadas a entender qué paso les toca dar, qué información deben preparar y a qué servicio deben dirigirse.',
 'Partimos de una situación muy concreta: una persona llega a una oficina, le falta un documento o no ha entendido bien qué necesita y tiene que volver. Para ella supone tiempo e incertidumbre. Para vuestro equipo puede significar repetir explicaciones y dedicar otra atención al mismo motivo. Nos gustaría saber hasta qué punto os ocurre y en qué trámites se concentra.',
 'La propuesta tiene dos partes. Para la persona, una guía que explique el recorrido en un lenguaje sencillo y en su idioma, con pasos claros y una lista de preparación. Para el equipo municipal, un espacio de apoyo que permita ver en qué punto está el acompañamiento, qué queda por revisar y cuándo hace falta intervenir.',
 'Queremos que la información se construya a partir de fuentes que vuestro equipo pueda validar y actualizar. Cuando falte una respuesta fiable o el caso necesite criterio profesional, la herramienta debería derivarlo a la persona adecuada. La orientación apoyaría la atención; las valoraciones y las decisiones administrativas seguirían correspondiendo a profesionales y a la administración.',
 'Hoy os enseñaremos una demostración de la experiencia que estamos diseñando. Es una maqueta interactiva con ejemplos ficticios; todavía hay que concretar y validar el funcionamiento real. Por eso esta reunión nos interesa especialmente: queremos entender vuestro trabajo antes de cerrar el producto.',
 'Nuestra propuesta sería empezar por un servicio y dos o tres recorridos frecuentes, acordar qué resultado sería útil y probar de forma acotada. Si observamos una mejora, tendremos una base para decidir si merece la pena ampliar. Para empezar, ¿qué situaciones hacen que una persona tenga que volver o que vuestro equipo repita más explicaciones?'
]
for s in speech_es:meeting.body(s)
meeting.heading('Versión breve de 30 segundos')
meeting.quote('Estamos creando GuíaTrámite para que las personas recién llegadas entiendan mejor qué hacer y los equipos municipales puedan atenderlas con más contexto. Queremos contrastar un piloto pequeño, con información validada por vosotros, y comprobar si mejora la preparación de las visitas. ¿Dónde os genera más trabajo hoy la falta de información o documentación?')

meeting.page('03  Conducir la conversación','Una reunión de 30 minutos','Una persona conduce y otra toma notas. Quien conoce la demo la muestra; la persona técnica interviene cuando las preguntas lo requieren. Evitad que los cuatro miembros presenten el proyecto por separado.')
meeting.table(['Tiempo','Actividad','Resultado buscado'],[
 ['0–3 min','Presentación breve','Acordar el propósito de la conversación'],
 ['3–13 min','Escuchar al servicio','Identificar situaciones repetidas y su impacto'],
 ['13–18 min','Demo con un caso ficticio','Comprobar si la propuesta encaja'],
 ['18–25 min','Definir el posible piloto','Elegir servicio, recorridos e indicadores'],
 ['25–30 min','Acordar continuidad','Referente y siguiente sesión de trabajo']
],[65,190,W-86-255])
meeting.heading('Preguntas que aportan información')
meeting.bullets([
 '¿Cuáles son las tres consultas que más se repiten y cuáles obligan a volver?',
 '¿Qué suele faltar o entenderse mal? ¿Tenéis datos o una estimación del volumen?',
 '¿En qué idiomas aparecen más dificultades? ¿Cómo ayudáis a quien no usa móvil?',
 '¿Dónde está la información que utiliza el personal y quién la actualiza?',
 '¿Qué necesita ver el profesional antes de atender? ¿Qué no debería automatizarse?',
 '¿Quién debería participar para valorar un piloto y cómo se tramitaría esa valoración?'
])
meeting.heading('Mostrar la demo en tres minutos')
meeting.body('Mostrar primero un recorrido para la persona y abrir uno de sus pasos. Cambiar el idioma del ejemplo. Pasar después a la vista municipal, seleccionar una ficha ficticia y filtrar los pendientes. Terminar con: “¿Qué información os faltaría aquí para que esto os resultara útil?”')
meeting.body('No improvisar respuestas sobre requisitos de extranjería, documentación concreta, direcciones o citas. En esta fase se muestra cómo se organizaría la orientación; el contenido real lo debe validar la administración competente.',small=True)

meeting.page('04  Propuesta de piloto','Un piloto acotado<br/>que permita aprender','Propuesta inicial sujeta a acuerdo: un servicio municipal, dos o tres recorridos frecuentes y los idiomas priorizados por el equipo. Calendario orientativo de seis a ocho semanas; no es un compromiso de entrega.')
meeting.table(['Fase','Trabajo','Condición para avanzar'],[
 ['Definición','Elegir recorridos, fuentes, responsables e indicadores. Recoger una referencia inicial.','Alcance y validadores identificados.'],
 ['Preparación','Prototipo con información pública y casos ficticios. Revisar comprensión y accesibilidad.','Contenido y pruebas aceptados por el servicio.'],
 ['Prueba limitada','Uso supervisado, solo cuando estén validadas las condiciones técnicas y de datos.','Incidencias registradas y posibilidad de detener la prueba.'],
 ['Evaluación','Comparar resultados, recoger experiencia y proponer ajustes.','Decisión conjunta de mejorar, ampliar o parar.']
],[80,230,W-86-310])
meeting.heading('Reparto de responsabilidades')
meeting.body('<b>GuíaTrámite:</b> configurar el prototipo, documentar sus límites, facilitar formación y registrar incidencias. <b>Ayuntamiento:</b> designar un referente, validar el contenido y el canal de atención, facilitar pruebas y valorar los requisitos institucionales. La dedicación de ambas partes se fija en la propuesta.')
meeting.heading('Qué mediremos y cómo')
meeting.body('<b>Repetición:</b> visitas repetidas por información o documentación incompleta / visitas observadas del recorrido. <b>Preparación:</b> visitas con la información necesaria / visitas evaluadas. <b>Tiempo:</b> mediana de minutos dedicados a orientar en casos comparables. <b>Comprensión:</b> personas que explican correctamente su siguiente paso / personas consultadas.')
meeting.body('Acordar antes las definiciones, el periodo de referencia y el método de recogida. Registrar también errores y derivaciones. Los objetivos numéricos se fijan con la referencia inicial; una muestra pequeña ofrecerá señales orientativas, no demostrará por sí sola un efecto causal.',small=True)

meeting.page('05  Respuestas y cierre','Responder sin prometer<br/>lo que falta por validar','La credibilidad depende de explicar qué está previsto, qué puede enseñarse y qué debe comprobarse con el servicio.')
objections=[
 ('¿Y si la IA se equivoca?','El diseño debe vincular las respuestas a información validada, señalar la incertidumbre y derivar a profesionales. El piloto debe comprobar errores y criterios de parada antes de ampliar el uso.'),
 ('Ya tenemos una web y atención presencial','Queremos comprobar si una guía por pasos facilita entender esa información y preparar la visita. Partiríamos de vuestras fuentes y de cómo ya trabaja el equipo.'),
 ('¿Añadirá trabajo al personal?','Habrá una dedicación inicial para validar recorridos y probarlos. La propuesta debe definir esa carga y medir si el uso posterior compensa el esfuerzo.'),
 ('¿Y quien no usa móvil o no sabe leer bien?','Hay que prever uso asistido en el punto de atención, lenguaje claro y pruebas con personas usuarias. Otros formatos, como audio, se valorarían según la necesidad detectada.'),
 ('¿Cuánto cuesta?','Tras delimitar el piloto presentaremos un precio cerrado con alcance y dedicación definidos. El uso posterior se presupuestaría por separado. Hoy no estamos proponiendo una compra ni comprometiendo una vía de contratación.'),
 ('¿Dónde se guardarían los datos?','La demo no guarda expedientes. La arquitectura, los proveedores, las ubicaciones y los plazos del servicio real deben detallarse y revisarse con la institución antes de utilizar datos personales.')
]
for q,a in objections:meeting.heading(q);meeting.body(a)

meeting.page('06  Obertura en català','Discurs per a la reunió','Versió per a una reunió en català. Durada orientativa: dos minuts. Adapteu les paraules a la manera de parlar de qui el presenti.')
speech_ca=[
 'Gràcies per rebre’ns. Estem desenvolupant GuíaTrámite, una eina per ajudar les persones nouvingudes a entendre quin pas han de fer, quina informació han de preparar i a quin servei s’han d’adreçar.',
 'Partim d’una situació molt concreta: una persona arriba a una oficina, li falta un document o no ha entès bé què necessita i ha de tornar. Per a ella això significa temps i incertesa. Per al vostre equip pot significar repetir explicacions i dedicar una altra atenció al mateix motiu. Ens agradaria saber fins a quin punt us passa i en quins tràmits es concentra.',
 'La proposta té dues parts. Per a la persona, una guia que expliqui el recorregut en un llenguatge senzill i en el seu idioma, amb passos clars i una llista de preparació. Per a l’equip municipal, un espai de suport per veure en quin punt és l’acompanyament, què queda per revisar i quan cal intervenir.',
 'Volem partir d’informació que el vostre equip pugui validar i actualitzar. Quan falti una resposta fiable o el cas necessiti criteri professional, l’eina hauria de derivar-lo a la persona adequada. Les valoracions i les decisions administratives continuarien corresponent als professionals i a l’administració.',
 'Avui us mostrarem una demostració de l’experiència que estem dissenyant. És una maqueta interactiva amb exemples ficticis. Encara cal concretar i validar el funcionament real, i per això volem escoltar-vos abans de tancar el producte.',
 'Proposem començar per un servei i dos o tres recorreguts habituals, acordar què consideraríem una millora i fer una prova acotada. Per començar, quines situacions fan que una persona hagi de tornar o que el vostre equip hagi de repetir més explicacions?'
]
for s in speech_ca:meeting.body(s)
meeting.heading('Tancament proposat')
meeting.quote('Pel que ens heu explicat, sembla que tindria sentit estudiar aquest recorregut. Podem fixar una sessió amb la persona de referència per revisar dos o tres casos ficticis i preparar una proposta d’abast, calendari i cost?')

meeting.page('07  Preparar la continuidad','Lo que debe quedar<br/>anotado al salir','El interés se convierte en una oportunidad concreta cuando sabemos qué problema resolver, quién debe participar y cuál será el siguiente entregable.')
meeting.bullets([
 'Servicio y recorrido prioritarios, con un ejemplo real descrito sin datos personales.',
 'Idiomas y dificultades de comprensión o acceso que merecen atención.',
 'Fuentes oficiales disponibles y persona responsable de validarlas.',
 'Referente municipal, participantes necesarios y fecha tentativa de la sesión siguiente.',
 'Información que necesita el ayuntamiento para valorar alcance, recursos y coste.'
])
meeting.heading('Antes de usar datos reales')
meeting.body('Revisar con la persona delegada de protección de datos y con sistemas las finalidades, los datos mínimos, las responsabilidades, los proveedores, los accesos, la conservación y las medidas de seguridad. Determinar las evaluaciones, condiciones de accesibilidad y requisitos del ENS que correspondan al servicio. No presentar la landing como una certificación de cumplimiento.')
meeting.heading('Fuentes institucionales para preparar esas preguntas')
meeting.body('<link href="https://www.aepd.es/derechos-y-deberes/cumple-tus-deberes/directrices-de-aplicacion/administraciones-publicas" color="#41683E">AEPD · Orientación a las Administraciones Públicas</link><br/><link href="https://www.boe.es/eli/es/rd/2018/09/07/1112" color="#41683E">BOE · Real Decreto 1112/2018 · Accesibilidad del sector público</link><br/><link href="https://www.boe.es/eli/es/rd/2022/05/03/311" color="#41683E">BOE · Real Decreto 311/2022 · Esquema Nacional de Seguridad</link><br/>Referencias consultadas el 7 de noviembre de 2026. Revisar su aplicación con la institución.',small=True)
meeting.heading('Cierre propuesto')
meeting.quote('Por lo que nos habéis explicado, parece que tendría sentido estudiar el recorrido que más os preocupa. ¿Podemos fijar una sesión con la persona de referencia para revisar dos o tres casos ficticios y preparar una propuesta concreta de alcance, calendario y coste?')
meeting.finish(markdown=True)

# A separate, public-facing two-page proposal for the landing.
proposal=Doc('GuiaTramite_Propuesta_Piloto.pdf','Propuesta de piloto')
proposal.page('Orientación para personas  Apoyo para instituciones','Un camino más claro<br/>desde el primer día','GuíaTrámite es un proyecto en desarrollo que propone utilizar inteligencia artificial para facilitar la orientación de las personas recién llegadas y apoyar a los equipos municipales que las acompañan.')
proposal.quote('Que una persona entienda qué necesita, qué debe preparar y dónde acudir. Que el equipo pueda acompañarla con información más clara.')
proposal.heading('Una experiencia para las personas')
proposal.body('Recorridos paso a paso, lenguaje comprensible y orientación en los idiomas priorizados por el municipio. La información de cada recorrido partiría de fuentes oficiales validadas por el servicio. Cuando la consulta necesite criterio profesional, se derivaría al equipo adecuado.')
proposal.heading('Un apoyo para la institución')
proposal.body('Una vista propuesta del estado del acompañamiento, los pasos pendientes y las revisiones que requieren intervención. El objetivo es preparar mejor la atención y comprobar si se reducen las visitas de repetición por información o documentación incompleta.')
proposal.heading('Propuesta inicial de colaboración')
proposal.table(['Ámbito','Punto de partida propuesto'],[
 ['Servicio','Un servicio de acogida, atención ciudadana u orientación municipal.'],
 ['Recorridos','Dos o tres situaciones frecuentes, elegidas con el equipo.'],
 ['Idiomas','Los que se prioricen según las necesidades del servicio.'],
 ['Calendario','Seis a ocho semanas como referencia, sujeto a acuerdo.'],
 ['Primera fase','Información pública y situaciones ficticias.']
],[110,W-196])
proposal.body('La web muestra una demostración con ejemplos preparados y datos ficticios. No consulta una IA, no gestiona expedientes y no reserva citas.',small=True)
proposal.page('Un alcance concreto  Una evaluación compartida','Empezar con un piloto<br/>y decidir con evidencias','La primera reunión sirve para comprender cómo trabaja el servicio, identificar dónde se concentra la dificultad y acordar si merece la pena preparar una propuesta de piloto.')
proposal.heading('Cómo lo planteamos')
proposal.body('<b>Escuchar:</b> identificar las consultas frecuentes, las fuentes disponibles y los puntos de confusión. <b>Preparar:</b> validar los recorridos con el equipo y probar con casos ficticios. <b>Comprobar:</b> evaluar resultados y decidir juntos los siguientes pasos.')
proposal.heading('Qué indicadores podemos acordar')
proposal.bullets(['Visitas repetidas por información o documentación incompleta.','Preparación de la visita y comprensión del siguiente paso.','Tiempo dedicado a orientar en casos comparables.','Errores detectados y derivaciones a profesionales.'])
proposal.body('Las definiciones, los objetivos y el método de evaluación se fijarían antes de comenzar. Los resultados de una prueba pequeña se interpretarían según su alcance y las características de los casos.',small=True)
proposal.heading('Qué necesita cada parte')
proposal.body('<b>El municipio:</b> una persona de referencia, información validable y un espacio de trabajo con el servicio. <b>GuíaTrámite:</b> preparar la propuesta, configurar la experiencia y facilitar las pruebas. La dedicación, el presupuesto y las condiciones se acordarían por escrito.')
proposal.heading('Condiciones para el servicio real')
proposal.body('Antes de utilizar datos personales deberán concretarse y validarse las responsabilidades, las medidas técnicas y organizativas, la accesibilidad y las condiciones de operación. La orientación propuesta no sustituye las decisiones profesionales ni las resoluciones administrativas.')
proposal.quote('Siguiente paso: una sesión de trabajo para elegir el servicio y los recorridos, designar un referente y preparar una propuesta de alcance, calendario y coste.')
proposal.finish()
shutil.copy(proposal.path,ROOT/'web/downloads'/proposal.path.name)

# A visual brand guide with reusable production assets.
brand=Doc('GuiaTramite_Identidad_Corporativa.pdf','Identidad visual')
brand.page('01  Idea de marca','Cada paso más claro','GuíaTrámite acompaña a las personas a entender un recorrido y ayuda a las instituciones a ofrecer una atención más comprensible. La identidad busca cercanía, claridad y confianza.')
c=brand.c
c.drawImage(str(ROOT/'identidad/guiatramite-logo-principal.png'),68,brand.y-104,width=455,height=104,mask='auto',preserveAspectRatio=True);brand.y-=123
brand.heading('Una G que marca el camino')
brand.body('El símbolo dibuja la G de GuíaTrámite con un trazo continuo, como un recorrido. El punto verde claro marca el inicio. La letra, el contraste y el detalle reducido facilitan reconocer la marca en cabeceras, avatares y favicons.')
brand.heading('Paleta principal')
palette=[('Verde profundo',INK),('Verde claro',LIME),('Fondo cálido',PAPER),('Salvia suave','#EAF0E5'),('Texto secundario',MUTED)]
sw=(W-86-32)/5
for i,(name,hexcode) in enumerate(palette):
    x=43+i*(sw+8);c.setFillColor(colors.HexColor(hexcode));c.setStrokeColor(colors.HexColor(LINE));c.roundRect(x,brand.y-51,sw,51,6,fill=1,stroke=1)
    c.setFillColor(colors.HexColor(INK));c.setFont('GuideBold',6.3);c.drawString(x,brand.y-67,name);c.setFont('Guide',8);c.drawString(x,brand.y-82,hexcode)
brand.y-=108
brand.heading('Uso del color')
brand.body('Verde profundo para títulos, texto principal y llamadas a la acción. Verde claro para acompañar y destacar sobre fondo oscuro. Fondo cálido y salvia para organizar la lectura. El verde claro funciona como superficie o acento; no se utiliza como texto pequeño sobre blanco.')
brand.heading('Tipografía')
brand.body('Montserrat Regular y Bold para la web y Bold para el logotipo. Las letras del logotipo están convertidas en trazados SVG, sin depender de fuentes instaladas. Los PDF utilizan DejaVu Sans. Licencias incluidas en el proyecto.')

brand.page('02  Variantes y reproducción','Una identidad que<br/>se reconoce en cada uso','Los archivos maestros son los SVG. Los PNG tienen fondo transparente y sirven para aplicaciones que no acepten vector.')
def logo_panel(y,dark=False,mono=False):
    c=brand.c;c.setFillColor(colors.HexColor(INK if dark else '#FFFFFF'));c.setStrokeColor(colors.HexColor(LINE));c.roundRect(43,y-92,W-86,92,8,fill=1,stroke=1)
    name='blanco' if dark else 'monocromo' if mono else 'principal'
    c.drawImage(str(ROOT/f'identidad/guiatramite-logo-{name}.png'),70,y-82,width=320,height=73.2,mask='auto',preserveAspectRatio=True)
for dark,mono in [(False,False),(True,False),(False,True)]:
    logo_panel(brand.y,dark,mono);brand.y-=108
brand.heading('Espacio de protección y tamaños')
brand.body('Reservar alrededor del logotipo al menos un cuarto de la altura del símbolo. Anchura mínima recomendada del conjunto: 150 px en pantalla o 35 mm en impresión. Usar el símbolo aislado en favicons, avatares o espacios más pequeños; verificar su legibilidad en el soporte final.')
brand.heading('Reglas de reproducción')
brand.body('Mantener las proporciones y utilizar las variantes entregadas. Evitar sombras, contornos, estiramientos y cambios de color arbitrarios. Sobre fondos oscuros se utiliza la variante blanca; sobre fotografía, colocar primero una superficie uniforme que mantenga la lectura.')

brand.page('03  Voz y aplicaciones','Hablar con claridad<br/>también es acompañar','La comunicación debe ayudar a entender el siguiente paso. El tono es cercano y respetuoso, con frases concretas y explicaciones fáciles de seguir.')
brand.table(['Contexto','Ejemplo de mensaje'],[
 ['Presentación','Cada paso, más claro.'],
 ['Personas','Entiende qué necesitas, prepara tu visita y encuentra el servicio adecuado.'],
 ['Instituciones','Una orientación más clara para preparar mejor la atención.'],
 ['Piloto','Empezamos por un servicio y medimos juntos qué mejora.'],
 ['Estado del proyecto','Proyecto en desarrollo. Demostración con datos ficticios.']
],[103,W-189])
brand.heading('Aplicación digital')
brand.body('La landing combina una portada oscura con secciones claras, titulares grandes y vistas de producto enmarcadas. El acento verde y los pasos numerados mantienen la orientación visual. Disponible en castellano y catalán, con un ejemplo de la guía en árabe.')
c=brand.c;c.drawImage(str(ROOT/'identidad/guiatramite-social.png'),92,brand.y-215.25,width=410,height=215.25,mask='auto');brand.y-=232
brand.finish()

(ROOT/'identidad/paleta.json').write_text(json.dumps({'marca':'GuíaTrámite','lema':'Cada paso, más claro.','colors':{'verde_profundo':INK,'verde_claro':LIME,'fondo_calido':PAPER,'salvia_suave':'#EAF0E5','texto_secundario':MUTED}},ensure_ascii=False,indent=2))
(ROOT/'identidad/LEEME.md').write_text('''# GuíaTrámite

Archivos maestros en SVG con el texto convertido en trazados. Los PNG son transparentes.

- principal: uso habitual sobre fondos claros.
- blanco: uso sobre fondos oscuros.
- monocromo y negro: impresión a una tinta.
- símbolo: favicon y avatar.
- social: tarjeta de presentación para redes, 1200 x 630 px.

Mantener proporciones. Reserva mínima: un cuarto de la altura del símbolo. Consultar el manual PDF.
Tipografía web y logotipo: Montserrat. El texto de los SVG está convertido en trazados. Licencias incluidas en el proyecto.
''')
for p in OUT.glob('*.pdf'):
    pdf=fitz.open(p)
    print(p.name, len(pdf),'pages')
    for i,page in enumerate(pdf):
        target=ROOT/'tmp'/p.stem
        target.mkdir(exist_ok=True)
        page.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(target/f'page-{i+1}.png')
print('Documents ready')

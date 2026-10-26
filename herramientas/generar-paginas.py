import re
import os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
# Genera final-paginas.html con el menú y el pie de final.html. Uso: python3 herramientas/generar-paginas.py
f=open(R+'final.html').read()
style=f[f.index('<style>')+7:f.index('</style>')]
base_css=style[:style.index('/* Portada */')]
tail_css=style[style.index('/* Pie de página */'):]
header=f[f.index('<header class="top"'):f.index('<main id="inicio">')]
footer=f[f.index('<footer>'):f.index('<script src=')]
quote_css=style[style.index('/* Cotización */'):style.index('/* Pie de página */')]
quote=f[f.index('<section class="quote" id="contacto">'):f.index('</main>')].replace('id="contacto"','id="cotizar" hidden')
form_js=f[f.index('  // Formulario de cotización'):f.index('  var tabs=')]

def ctx(html):
    # En las páginas internas: anclas de la portada → final.html, páginas internas → mismo archivo, servicios → su página
    html=html.replace('href="final-paginas.html#','href="#')
    svc={'#s-mantenimiento':'#mantenimiento-preventivo','#s-reparacion':'#reparacion','#s-polizas':'#polizas','#s-emergencia':'#servicio-de-emergencia'}
    for k,v in svc.items(): html=html.replace('href="'+k+'"','href="'+v+'"')
    html=re.sub(r' data-chap="\d"','',html)
    for a in ['inicio','servicios','linea-fria','linea-caliente','preguntas-frecuentes','contacto']:
        html=html.replace('href="#'+a+'"','href="final.html#'+a+'"')
    return html
header=ctx(header).replace('href="final.html#inicio"','href="final.html"')
footer=ctx(footer)
quote=ctx(quote)

WA='https://wa.me/525646037573'
def hero(label,title,lead,img,alt,pos='50% 50%'):
    return f'''<header class="pg-hero">
    <div class="pg-copy"><span class="label">{label}</span><h1>{title}</h1><p class="lead">{lead}</p>
    <div class="acts"><a class="btn btn-blue" href="final.html#contacto">Solicitar cotización</a><a class="btn btn-ghost" href="{WA}">WhatsApp</a></div></div>
    <figure class="pg-photo"><img src="{img}" alt="{alt}" style="object-position:{pos}"></figure>
  </header>'''
def pend(t): return f'<p class="pend">{t}</p>'
def legal(pid,title,lead,items):
    toc=''.join(f'<li><a href="#" data-jump="{pid}-{i+1}">{t}</a></li>' for i,t in enumerate(items))
    secs=''.join(f'<article class="lsec" id="{pid}-{i+1}"><h2>{t}</h2>{pend("Texto pendiente: lo redacta y valida Tecnobg o su asesor legal.")}</article>' for i,t in enumerate(items))
    return f'''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Legales</span><h1>{title}</h1><p class="lead">{lead}</p></div></header>
  <div class="pg-body"><nav class="toc" aria-label="Contenido"><span class="label">Contenido</span><ol>{toc}</ol></nav><div class="lbody">{secs}</div></div>'''

# Páginas de servicios: diseño del diseñador (servicios.pdf, 22 oct 2026). Recursos en img/final/servicios/
SV='img/final/servicios/'
SVCS=[('reparacion','Reparación','t-reparacion'),('mantenimiento-preventivo','Mantenimiento<br>preventivo','t-mantenimiento'),('polizas','Pólizas','t-polizas'),('servicio-de-emergencia','Emergencia','t-emergencia')]
def svtabs(cur):
    li=''.join(f'<a href="#{i}"'+(' aria-current="page"' if i==cur else '')+f'><img src="{SV}{ic}.webp" alt="" width="40" height="40">{t}</a>' for i,t,ic in SVCS)
    return f'<nav class="sv-tabs" aria-label="Servicios"><div class="wrap">{li}</div></nav>'
def svhero(cur,label,title,lead,media,extra='',cls=''):
    return f'''{svtabs(cur)}
  <header class="sv-hero{cls}"><div class="wrap">
    <div class="pg-copy">{label}<h1>{title}</h1><p class="lead">{lead}</p>{extra}</div>
    {media}
  </div></header>'''
def photo(img,alt,w,h,pos='50% 50%'):
    return f'<figure class="pg-photo"><img src="{SV}{img}" alt="{alt}" width="{w}" height="{h}" style="object-position:{pos}"></figure>'
def incluye(title,lead,left,right,cards):
    ul=lambda xs:'<ul>'+''.join(f'<li>{x}</li>' for x in xs)+'</ul>'
    cs=''.join(f'<li><img src="{SV}{ic}.webp" alt="" width="80" height="70" loading="lazy"><span>{t}</span></li>' for ic,t in cards)
    return f'''
  <section class="sv-inc"><img class="bg" src="{SV}incluye-fondo.webp" alt="" width="1920" height="900" loading="lazy"><div class="wrap">
    <span class="label">¿Qué incluye?</span><h2>{title}</h2><p class="lead">{lead}</p>
    <div class="cols">{ul(left)}{ul(right)}</div>
    <ul class="icards">{cs}</ul>
  </div></section>'''
def campo(items):
    cs=''.join(f'<figure class="slide"><img src="{SV}{img}" alt="{alt}" width="506" height="900" loading="lazy"><figcaption><b>{lab}</b>'+(f'<span>{cap}</span>' if cap else '')+'</figcaption></figure>' for img,alt,lab,cap in items)
    return f'''
  <section class="sv-campo"><div class="wrap">
    <div class="head"><div><span class="label">Nuestro trabajo</span><h2>Así se ve un día en campo</h2></div>
    <div class="arrows"><button type="button" data-dir="-1" aria-label="Fotos anteriores"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button><button type="button" data-dir="1" aria-label="Fotos siguientes"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button></div></div>
    <div class="car-track" tabindex="0" aria-label="Fotos de trabajos en campo">{cs}</div>
    <div class="timer"><i></i></div><div class="dots" aria-label="Fotos"></div>
  </div></section>'''
COB=f'''
  <section class="sv-cob"><div class="wrap">
    <div><span class="label">Cobertura</span><h2>Operamos en CDMX y Edo Mex</h2><p>Con capacidad de atención regional, adaptándonos a las necesidades específicas de cada proyecto y cliente.</p></div>
    <img src="{SV}cobertura-mapa.webp" alt="Mapa de México con los tipos de negocio que atendemos: restaurantes, bares, cafeterías, tiendas y oficinas" width="1200" height="745" loading="lazy">
  </div></section>'''
REP_CARDS=[('i-diagnostico','Diagnóstico<br>del equipo'),('i-refacciones','Cambio de<br>refacciones'),('i-electrico','Verificación de<br>sistema eléctrico'),('i-mecanica','Verificación<br>mecánica'),('i-funcionamiento','Puesta en<br>funcionamiento')]
LEAD_INC='El principal objetivo es corregir los errores o fallas que presenten los equipos con el propósito de que vuelvan a funcionar de la forma deseada.'
SV_REP=svhero('reparacion','<span class="label">Servicios</span>','Reparación de equipos especializado en el sector HORECA en México','Atención especializada para resolver fallas con precisión y responsabilidad técnica.',
  photo('reparacion-hero.webp','Técnico de Tecnobg revisa la parte eléctrica de un refrigerador bajo barra',825,1100,'50% 40%'))+incluye('El servicio de reparación incluye',LEAD_INC,
  ['Diagnóstico ágil','Reparación especializada','Sustitución y colocación de refacciones originales y compatibles con tus equipos'],['Pruebas de funcionamiento','Garantía de 30 días'],REP_CARDS)+campo([
  ('campo-1.webp','Técnico de Tecnobg trabaja dentro de un equipo de cocina','Línea caliente','Reparación de horno de pizzas'),
  ('campo-2.webp','Dos técnicos de Tecnobg revisan el cableado de un equipo','Línea fría','Reparación de horno de pizzas'),
  ('campo-3.webp','Técnico de Tecnobg repara un equipo de cocina industrial','Línea caliente','')])+COB
SV_MANT=svhero('mantenimiento-preventivo','<span class="label">Servicios</span>','Mantenimiento preventivo especializado en el sector HORECA en México','Evita y disminuye las consecuencias de las fallas del equipo, logrando prevenir los incidentes antes de que estos ocurran.',
  photo('mantenimiento-hero.webp','Técnico de Tecnobg da mantenimiento a una vitrina refrigerada',619,1100,'50% 45%'))+incluye('El servicio de mantenimiento preventivo incluye',LEAD_INC,
  ['Inspección técnica integral','Limpieza especializada y profunda','Ajustes y calibraciones necesarias'],['Revisión de parámetros','Reporte técnico detallado con recomendaciones'],
  REP_CARDS[:2]+[('i-limpieza','Limpieza interna<br>y externa')]+REP_CARDS[2:])+campo([
  ('campo-3.webp','Técnico de Tecnobg repara un equipo de cocina industrial','Línea caliente',''),
  ('campo-4.webp','Técnico de Tecnobg ajusta la puerta de un refrigerador','Preventivo','Reparación de puerta de refrigerador'),
  ('campo-5.webp','Técnico de Tecnobg da servicio a una batidora industrial','Línea caliente','Reparación de horno de pizzas'),
  ('campo-6.webp','Técnico de Tecnobg revisa el motor de un horno de banda','Línea caliente','Reparación de horno de pizzas')])+COB
PO_CARDS=[('Mantenimiento preventivo programado','Servicios programados para evitar fallas y asegurar el buen funcionamiento.'),('Atención correctiva prioritaria','Servicio preferente para resolver incidencias en menos de 24hrs hábiles.'),('Tarifas preferenciales','Precios especiales en mano de obra y refacciones.'),('Monitoreo continuo','Seguimiento constante del estado de tus equipos para anticipar problemas.')]
PO_BEN=['Ahorro en reparaciones de hasta 30% - 40%','Operación continua y sin interrupciones','Diminuye gastos inesperados','Reducción de tiempos muertos','Mayor vida útil de tus equipos']
pcards=''.join(f'<li><span class="disc"><img src="{SV}poliza-{i+1}.webp" alt="" width="240" height="240" loading="lazy"></span><b>{t}</b><span>{d}</span></li>' for i,(t,d) in enumerate(PO_CARDS))
SV_POL=svhero('polizas','<span class="label">Pólizas</span>','Con nuestras pólizas proteges tu operación y ahorras dinero.','Evita y disminuye las consecuencias de las fallas del equipo, logrando prevenir los incidentes antes de que estos ocurran.',
  f'<figure class="pg-shield"><img src="{SV}polizas-escudos.webp" alt="Escudos de Tecnobg con las palabras confianza y seguridad" width="900" height="507"></figure>',cls=' pol')+f'''
  <section class="po-inc"><div class="wrap">
    <span class="label">¿Qué incluye?</span><h2>Nuestras pólizas incluyen</h2><p class="lead">{LEAD_INC}</p>
    <ul class="pcards">{pcards}</ul>
    <a class="btn btn-silver" href="#" data-jump="cotizar">¡Protege tus equipos ahora!</a>
  </div></section>
  <section class="po-ben">
    <figure><img src="{SV}polizas-beneficios.webp" alt="Técnico de Tecnobg trabaja en una plancha de una cocina industrial" width="1113" height="901" loading="lazy"></figure>
    <div class="txt"><h2>Beneficios de nuestras Pólizas</h2>
      <ul class="snake" style="background-image:url({SV}polizas-beneficios-linea.webp)">'''+''.join(f'<li>{b}</li>' for b in PO_BEN)+f'''</ul></div>
  </section>
  <section class="po-por">
    <figure><img src="{SV}polizas-porque.webp" alt="Refrigerador comercial con puertas de vidrio en el pasillo de un supermercado" width="1400" height="913" loading="lazy"></figure>
    <div class="txt"><h2>¿Por qué elegir una póliza con Tecnobg?</h2>
      <p>Porque entendemos que tu negocio depende de equipos funcionando al 100%.</p>
      <p>Nuestra póliza no es un gasto, es una inversión estratégica que te brinda:</p>
      <ul><li>Tranquilidad operativa</li><li>Respuesta inmediata</li><li>Ahorro real</li><li>Mayor eficiencia</li></ul></div>
  </section>'''
SV_EME=svhero('servicio-de-emergencia',f'<img class="hicon" src="{SV}i-emergencia.webp" alt="" width="44" height="52"><span class="label">Emergencia</span>','Servicio de Emergencia','Cuando la operación exige inmediatez, respondemos con eficiencia.',
  f'<figure class="pg-photo"><img src="{SV}emergencia-hero.webp" alt="Camioneta de servicio de Tecnobg circulando por la ciudad al anochecer" width="1000" height="953"></figure>',
  '<div class="acts"><a class="btn btn-warm" href="#" data-jump="em-dia">Saber más</a></div>')+f'''
  <section class="em-dia" id="em-dia">
    <figure><img src="{SV}emergencia-tecnico.webp" alt="Técnico de Tecnobg camina por la calle con su caja de herramientas" width="1200" height="1156" loading="lazy"></figure>
    <div class="txt"><h2><img src="{SV}i-pin-blanco.webp" alt="" width="24" height="36">Diagnóstico y reparación el mismo día</h2>
      <p>Enviamos a nuestro técnico más cercano a su ubicación</p><p>Exclusivo zona CDMX</p>
      <a class="btn btn-red" href="#" data-jump="em-cdmx">Ver Áreas de Servicio</a></div>
  </section>
  <section class="em-cdmx" id="em-cdmx"><div class="wrap">
    <img class="map" src="{SV}emergencia-cdmx.webp" alt="Mapa de la Ciudad de México con puntos de atención de emergencias" width="800" height="883" loading="lazy">
    <div class="txt"><h2>¿Tienes una emergencia con tus equipos?</h2>
      <ul><li><img src="{SV}i-escudo.webp" alt="" width="46" height="54">Servicio disponible los 365 días del año</li><li><img src="{SV}i-pin.webp" alt="" width="28" height="42">Exclusivo zona CDMX</li></ul>
      <a class="btn btn-red" href="{WA}">Solicitar Servicio de Emergencia</a></div>
  </div><img class="city" src="{SV}emergencia-ciudad.webp" alt="" width="2400" height="358" loading="lazy"></section>'''

V=[]
# Nosotros: diseño del diseñador (seccion nosotros.pdf, 26 oct 2026). Recursos en img/final/nosotros/
NS='img/final/nosotros/'
YT='nG2DHYtOx2g'
CONS=['Interrupciones en el servicio','Pérdida de insumos','Riesgos sanitarios','Sanciones regulatorias','Pérdida de dinero']
FEAT=[('experiencia','Experiencia en el sector'),('procesos','Procesos estandarizados<br>y profesionales'),('personal','Personal técnico capacitado'),('reportes','Reportes claros<br>y seguimiento continuo'),('preventivo','Enfoque preventivo<br>y estratégico'),('excelencia','Compromiso con la<br>excelencia operativa')]
NOS=f'''<header class="ns-hero">
    <div class="ns-video" id="nsVideo"><img src="{NS}hero-video.webp" alt="" width="1919" height="840"><div id="nsPlayer"></div></div>
    <div class="ns-shade"></div>
    <div class="ns-brand"><img class="hlogo" src="img/final/logo-tecnobg.svg" alt="Grupo Tecnobg, servicios integrales" width="272" height="85"><img class="slogan" src="img/final/slogan.webp" alt="Solución con tecnología a tu medida" width="730" height="370"></div>
    <div class="ns-intro ns-w"><h1>Nosotros</h1><p>Grupo Tecnobg es una empresa mexicana con más de 25 años de experiencia en servicios de mantenimiento técnico, especializada en la atención de restaurantes, cafeterías, corporativos, cadenas y franquicias comerciales, bares y hoteles.</p></div>
  </header>
  <section class="ns-hist" aria-label="Nuestra historia"><div class="ns-w"><div class="ns-tl">
    <img class="blob" src="{NS}linea-historia.svg" alt="" width="1438" height="1778">
    <figure class="c c1"><img src="{NS}historia-1.webp" alt="Técnico de Tecnobg revisa una tarjeta electrónica con una lámpara" width="640" height="640" loading="lazy"></figure>
    <p class="t t1">Iniciamos brindando servicios en tarjetas electrónicas, maquinaria industrial tipo CNC y robots, destacando por la efectividad de nuestras soluciones. Esto permitió posicionarnos como aliado estratégico de La Comer en la atención de fallas de alta complejidad.</p>
    <figure class="c c2"><img src="{NS}historia-2.webp" alt="Dos técnicos de mantenimiento de Tecnobg recorren un supermercado con su equipo" width="840" height="840" loading="lazy"></figure>
    <p class="t t2">A partir de estos resultados, La Comer expandió la colaboración al área de cocina, donde se identificó una oportunidad de crecimiento. Gracias a su enfoque técnico y calidad de servicio, Grupo Tecnobg comenzó a consolidarse en el sector.</p>
    <figure class="c c3"><img src="{NS}historia-3.webp" alt="Técnico de Tecnobg trabaja con guantes en un equipo de cocina" width="640" height="640" loading="lazy"></figure>
    <p class="t t3">Con el paso del tiempo nos especializamos en el mantenimiento de equipos de cocina industrial, refrigeración y sistemas de aire acondicionado, consolidando una propuesta integral orientada a la continuidad operativa de nuestros clientes.</p>
    <figure class="c c4"><img src="{NS}historia-4.webp" alt="Técnico de Tecnobg repara una vitrina refrigerada de carnes" width="520" height="520" loading="lazy"></figure>
  </div></div></section>
  <section class="ns-vis"><div class="ns-w">
    <h2>Visión Operativa</h2>
    <p>Nos anticipamos a los problemas antes de que se conviertan en costos, asegurando una operación siempre activa y rentable. Las consecuencias de no tener un plan de mantenimiento son:</p>
    <ul class="ns-cons">{''.join(f'<li>{c}</li>' for c in CONS)}</ul>
    <h2 class="prem">En Grupo Tecnobg brindamos un servicio premium y personalizado</h2>
    <p>Trabajamos bajo un enfoque estratégico que minimiza riesgos y maximiza el rendimiento de tus equipos.</p>
    <ul class="ns-feat">{''.join(f'<li><img src="{NS}i-{i}.webp" alt="" width="160" height="160" loading="lazy"><span>{t}</span></li>' for i,t in FEAT)}</ul>
  </div></section>
  <section class="ns-filo"><div class="ns-w">
    <figure class="arrow from-left"><img src="{NS}filosofia.webp" alt="Técnico de Tecnobg da servicio a una freidora industrial" width="900" height="884" loading="lazy"></figure>
    <div class="txt"><h2>Filosofía de trabajo</h2>
      <p>Creemos en un servicio donde la honestidad operativa es la prioridad. Respetamos tus instalaciones y normativas como si fueran propias.</p>
      <ul><li>La <b>prevención reduce riesgos</b></li><li>La <b>planificación reduce costos</b></li><li>La <b>constancia genera estabilidad</b></li></ul></div>
  </div></section>
  <section class="ns-anti"><div class="ns-w">
    <div class="txt"><h2>Anticipación</h2><p>No esperamos a que algo falle, actuamos para proteger tu inversión.</p>
      <button type="button" class="btn btn-blue" id="nsVideoBtn">Ver nuestro video<br>corporativo</button></div>
    <figure class="arrow from-right"><img src="{NS}anticipacion.webp" alt="Técnicos de Tecnobg caminan por un centro comercial" width="700" height="1341" loading="lazy"></figure>
  </div></section>
  <dialog class="ns-dlg" id="nsDlg" aria-label="Video corporativo de Grupo Tecnobg"><button type="button" class="x" id="nsDlgClose" aria-label="Cerrar video"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button><div class="frame"></div></dialog>'''
V.append(('nosotros','Nosotros',NOS))
V.append(('mantenimiento-preventivo','Mantenimiento preventivo',SV_MANT))
V.append(('reparacion','Reparación',SV_REP))
V.append(('polizas','Pólizas',SV_POL))
V.append(('servicio-de-emergencia','Servicio de emergencia',SV_EME))
V.append(('bolsa-de-trabajo','Bolsa de trabajo','''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Bolsa de trabajo</span><h1>Trabaja en Tecnobg</h1><p class="lead">Aquí publicaremos las vacantes de Tecnobg y la forma de postularte.</p></div></header>
  <div class="pg-body"><section class="blk"><h2>Vacantes disponibles</h2>'''+pend('Contenido pendiente: vacantes vigentes (puesto, zona, requisitos) y formulario para enviar tu solicitud.')+'''</section></div>'''))
V.append(('blog','Blog','''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Blog</span><h1>Blog</h1><p class="lead">Pronto compartiremos aquí artículos sobre el mantenimiento y cuidado de equipos para el sector HORECA.</p></div></header>
  <div class="pg-body"><section class="blk"><h2>Artículos</h2>'''+pend('Contenido pendiente: primeros artículos y temas del blog.')+'''</section></div>'''))
V.append(('aviso-de-privacidad','Aviso de privacidad',legal('ap','Aviso de privacidad','Conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.',['Identidad y domicilio del responsable','Datos personales que recabamos','Finalidades del tratamiento','Transferencias de datos','Derechos ARCO y cómo ejercerlos','Cookies y tecnologías de rastreo','Cambios a este aviso'])))
V.append(('terminos-y-condiciones','Términos y condiciones',legal('tc','Términos y condiciones','Condiciones de uso de este sitio y de los servicios de Grupo Tecnobg.',['Objeto','Uso del sitio','Cotizaciones y autorización de servicios','Garantía','Propiedad intelectual','Legislación aplicable'])))
V.append(('uso-de-cookies','Uso de cookies',legal('ck','Uso de cookies','Cómo usa este sitio las cookies y tecnologías similares.',['¿Qué son las cookies?','Herramientas que usa el sitio','Cómo desactivarlas','Cambios a esta política'])))

SVC_IDS=[i for i,_,_ in SVCS]
views=''.join(f'\n<section class="view'+(' svc' if i in SVC_IDS else ' fin' if i=='nosotros' else '')+f'" id="v-{i}" data-title="{t}" hidden>\n  {body}\n</section>' for i,t,body in V)

page_css='''
/* Páginas internas: diseño preliminar con la misma navegación y pie de la versión final */
header.top{background:rgba(25,28,55,.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.06)}
main{padding-top:calc(var(--hh) + env(safe-area-inset-top,0px))}
.prelim{position:sticky;top:calc(var(--hh) + env(safe-area-inset-top,0px));z-index:40;background:var(--g-warm);color:#2b1600;font:600 14px/1.35 var(--head)}
.prelim .wrap{display:flex;align-items:center;gap:10px;min-height:44px;padding-block:8px}
.prelim svg{flex:none}
.pg-hero{background:var(--night);padding-block:48px 56px}
.pg-hero{display:grid;gap:30px;max-width:1240px;margin:0 auto;padding-inline:16px;box-shadow:0 0 0 100vmax var(--night);clip-path:inset(0 -100vmax)}
@media (min-width:1000px){.pg-hero{grid-template-columns:1fr 1fr;align-items:center;gap:56px;padding-block:72px}.pg-hero.solo{grid-template-columns:1fr}}
.pg-copy{display:grid;gap:16px;justify-items:start}
.pg-hero h1{font:700 clamp(46px,11vw,76px)/.98 var(--cond)}
.pg-hero .lead{font-size:19px;color:#e4e8f6;max-width:46ch}
.acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.btn-ghost{background:transparent;border:1px solid rgba(255,255,255,.45)}
.pg-photo{margin:0;border-radius:22px;overflow:hidden;aspect-ratio:4/3}
.pg-photo img{width:100%;height:100%;object-fit:cover}
.view{background:var(--light);color:var(--ink-d)}
.view>.pg-hero{color:var(--ink)}
.view{padding-bottom:80px}
.pg-body{max-width:1000px;margin:0 auto;padding:48px 16px 0;display:grid;gap:36px}
.blk{display:grid;gap:12px;justify-items:start;border-top:1px solid #d9deeb;padding-top:26px}
.blk h2,.lsec h2{font:700 clamp(22px,4vw,30px)/1.2 var(--head);color:var(--ink-d)}
.blk p{max-width:65ch}
.ticks{margin:0;padding:0;list-style:none;display:grid;gap:0;width:100%}
.ticks li{padding:14px 0;border-top:1px solid #e3e7f1}
.ticks b{display:block;font:700 18px var(--head);color:var(--navy)}
.links{display:flex;flex-wrap:wrap;gap:8px 24px}
.more{color:var(--navy);font:600 16px var(--head);text-decoration:none}
.more:hover{text-decoration:underline}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:12px;width:100%}
.card{display:grid;gap:6px;padding:18px;border-radius:14px;background:#fff;border:1px solid #e3e7f1;text-decoration:none;color:var(--ink-d);transition:border-color .3s,transform .3s}
.card:hover{border-color:#219fda;transform:translateY(-2px)}
.card b{font:700 18px var(--head)}
.card span{color:var(--navy);font-size:15px}
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.stats b{display:block;font:800 clamp(40px,9vw,72px)/1 var(--head);color:var(--navy);letter-spacing:-.03em}
.stats span{font-size:16px}
.pq{margin:0;font:700 clamp(24px,4.6vw,38px)/1.2 var(--head);color:var(--ink-d);max-width:26ch}
.pend{display:inline-block;margin:0;background:#fff4cc;color:#5c4100;border-radius:10px;padding:10px 14px;font-weight:500}
.toc{background:#fff;border:1px solid #e3e7f1;border-radius:16px;padding:18px 20px}
.toc ol{margin:10px 0 0;padding-left:20px;display:grid;gap:6px}
.toc a{color:var(--navy)}
.lbody{display:grid;gap:22px}
.lsec{display:grid;gap:10px;justify-items:start;border-top:1px solid #d9deeb;padding-top:22px;scroll-margin-top:calc(var(--hh) + 20px)}
footer{padding-bottom:calc(110px + env(safe-area-inset-bottom,0px))}
@media (min-width:900px){footer{padding-bottom:40px}}
/* Páginas de servicios (diseño del diseñador, servicios.pdf) */
.view.svc{background:#fff;color:var(--ink-d);padding-bottom:0}
.btn-red{background:linear-gradient(90deg,#d8161b,#ef5a1f)}
/* Pestañas de servicios como separadores de carpeta: la línea de abajo cierra las pestañas y la activa se abre hacia la página */
.sv-tabs{padding-top:24px;box-shadow:inset 0 -2px 0 #e3e6ee}
.sv-tabs .wrap{display:flex;align-items:flex-end;gap:6px;overflow-x:auto;scrollbar-width:none}
.sv-tabs .wrap::-webkit-scrollbar{display:none}
.sv-tabs a{position:relative;flex:1 0 auto;display:flex;align-items:center;gap:10px;min-height:58px;padding:8px 18px;border:2px solid #e3e6ee;border-radius:16px 16px 0 0;background:#f3f4f7;font:600 15px/1.2 var(--head);color:#5a6a9c;text-decoration:none;transition:min-height .35s cubic-bezier(.2,.8,.2,1),background .3s,color .3s}
.sv-tabs a:hover{background:#e9ecf3;color:var(--navy)}
.sv-tabs a[aria-current="page"]{min-height:68px;background:#fff;color:var(--navy);border-bottom-color:#fff;z-index:1}
.sv-tabs a[aria-current="page"]::after{content:"";position:absolute;left:14px;right:14px;top:-2px;height:3px;border-radius:0 0 3px 3px;background:var(--g-blue)}
.sv-tabs img{width:auto;height:34px;flex:none;transition:transform .35s cubic-bezier(.2,.8,.2,1)}
.sv-tabs a:hover img{transform:scale(1.08)}
.sv-tabs a[href="#polizas"] img{height:30px}
.sv-hero .wrap{display:grid;gap:30px;padding-block:40px 56px}
@media (min-width:1000px){.sv-hero .wrap{grid-template-columns:1fr 1fr;align-items:center;gap:56px;padding-block:44px 64px}}
.sv-hero .pg-copy{display:grid;gap:12px;justify-items:start}
.sv-hero .label,.sv-inc .label,.sv-campo .label,.sv-cob .label,.po-inc .label{color:var(--navy);letter-spacing:.04em}
.sv-hero h1{font:700 clamp(38px,5.4vw,64px)/1.08 var(--cond);color:var(--navy)}
.sv-hero .lead{font-size:clamp(17px,1.7vw,21px);color:var(--navy);max-width:44ch}
.sv-hero .hicon{height:48px;width:auto;margin-bottom:-4px}
.sv-hero .acts{margin-top:14px}
.sv-hero .acts .btn{min-height:42px;min-width:170px}
.sv-hero .pg-photo{border-radius:40px;aspect-ratio:383/364}
.sv-hero.pol .pg-copy{gap:18px}
.pg-shield{margin:0}
.pg-shield img{width:100%;height:auto;mix-blend-mode:multiply}
.sv-inc{position:relative;overflow:hidden;background:var(--navy);color:#fff}
/* Fondo del diseñador (fondo servicios-51), ya viene en azul: va sin capa encima */
.sv-inc .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.sv-inc .wrap{position:relative;padding-block:56px 64px;display:grid;grid-template-columns:minmax(0,1fr);gap:14px}
.sv-inc .label,.po-inc .label{color:#fff}
.sv-inc h2,.po-inc h2{font:700 clamp(32px,4.4vw,52px)/1.08 var(--cond)}
.sv-inc .lead,.po-inc .lead{max-width:62ch;font-size:18px}
.sv-inc .cols{display:grid;gap:4px 60px;margin:22px 0 26px;font:600 clamp(17px,1.6vw,20px)/1.3 var(--cond);letter-spacing:.01em}
@media (min-width:800px){.sv-inc .cols{grid-template-columns:auto auto;justify-content:center}}
.sv-inc .cols ul{margin:0;padding-left:16px;display:grid;gap:4px;list-style:square}
.icards{list-style:none;margin:0 -16px;padding:10px 16px 6px;display:grid;grid-auto-flow:column;grid-auto-columns:minmax(150px,1fr);gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:16px;scrollbar-width:none}
.icards::-webkit-scrollbar{display:none}
/* En escritorio caben todas las tarjetas: sin scroll (el hover las levanta sin cortarse) */
@media (min-width:900px){.icards{margin:0;padding:10px 0 6px;grid-auto-flow:row;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));overflow:visible}}
.icards li{scroll-snap-align:start;display:grid;justify-items:center;align-content:start;gap:14px;padding:18px 12px 20px;border-radius:24px;background:rgba(21,33,73,.86);text-align:center;font:600 clamp(16px,1.5vw,19px)/1.2 var(--cond)}
.icards img{height:62px;width:auto}
.sv-campo .wrap{padding-block:56px 72px}
.sv-campo .head{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:24px}
.sv-campo h2{font:700 clamp(30px,3.8vw,44px)/1.1 var(--cond);color:var(--navy)}
.arrows{display:flex;gap:8px}
.arrows button{width:44px;height:44px;border-radius:50%;border:1px solid #cfd6e8;background:#fff;color:var(--navy);display:flex;align-items:center;justify-content:center}
.arrows button:hover{background:#f0f3fa}
/* Carrusel "Así se ve un día en campo": como el de la propuesta 02 (foto activa, autoplay con barra, puntos) */
.car-track{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:16px;padding:6px 16px 10px;margin-inline:-16px;scrollbar-width:none}
.car-track::-webkit-scrollbar{display:none}
.slide{position:relative;margin:0;flex:0 0 78%;max-width:360px;scroll-snap-align:center;aspect-ratio:330/450;border-radius:20px;overflow:hidden;background:#dfe4ef;transition:transform .5s cubic-bezier(.2,.8,.2,1),opacity .5s}
@media (min-width:900px){.slide{flex-basis:30%}}
.slide:not(.active){transform:scale(.92);opacity:.55}
.slide img{width:100%;height:100%;object-fit:cover;transform:scale(1.04);transition:transform 4s ease-out}
.slide.active img{transform:scale(1.12)}
.slide figcaption{position:absolute;inset:auto 0 0;padding:60px 14px 16px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.65));color:#fff;display:grid;gap:2px}
.slide b{font:700 15px/1.2 var(--head);letter-spacing:.06em;text-transform:uppercase}
.slide span{font:600 18px/1.2 var(--cond)}
.timer{height:3px;background:#e3e6ee;border-radius:3px;overflow:hidden;margin-top:14px}
.timer i{display:block;height:100%;background:var(--g-blue);transform-origin:left;transform:scaleX(0)}
.dots{display:flex;gap:6px;margin-top:12px}
.dots button{width:8px;height:8px;border-radius:999px;border:none;background:#c4cce0;padding:0;transition:width .35s,background .35s}
.dots button[aria-current="true"]{width:26px;background:var(--navy)}
/* Interacciones */
.icards li{transition:transform .3s cubic-bezier(.2,.8,.2,1),background .3s,box-shadow .3s}
.icards li:hover{transform:translateY(-6px);background:rgba(21,33,73,.97);box-shadow:0 14px 28px rgba(10,16,40,.35)}
.icards li img{transition:transform .4s cubic-bezier(.2,.8,.2,1)}
.icards li:hover img{transform:scale(1.1)}
.pcards li{transition:transform .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s}
.pcards li:hover{transform:translateY(-6px);box-shadow:0 18px 34px rgba(0,0,0,.35)}
.pcards .disc{transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.pcards li:hover .disc{transform:translateX(-50%) rotate(25deg)}
.pcards .disc img{transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.pcards li:hover .disc img{transform:rotate(-25deg)}
.btn{transition:transform .25s,filter .25s,box-shadow .25s}
.view.svc .btn:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(20,30,70,.22)}
.view.svc .btn:active{transform:scale(.97)}
.em-cdmx li img{transition:transform .4s cubic-bezier(.2,.8,.2,1)}
.em-cdmx li:hover img{transform:translateY(-3px) scale(1.08)}
@media (prefers-reduced-motion:reduce){.slide,.slide img,.sv-tabs a,.icards li,.pcards li,.pcards .disc{transition:none}}
.sv-cob{background:#0e1638;color:#fff}
.sv-cob .wrap{display:grid;gap:36px;padding-block:72px;align-items:center}
@media (min-width:900px){.sv-cob .wrap{grid-template-columns:.8fr 1.2fr;padding-block:96px}}
.sv-cob .label{color:#fff}
.sv-cob h2{font:700 clamp(34px,4.4vw,52px)/1.1 var(--cond);margin:14px 0 10px;max-width:14ch}
.sv-cob p{max-width:42ch;text-align:justify}
.sv-cob img{width:100%;height:auto}
/* Pólizas */
.po-inc{background:#1b1d3a;color:#fff}
.po-inc .wrap{display:grid;grid-template-columns:minmax(0,1fr);gap:14px;padding-block:56px 64px}
.pcards{list-style:none;margin:30px auto 10px;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:4px 16px;width:100%;max-width:860px}
.pcards li{position:relative;display:grid;justify-items:center;align-content:start;gap:8px;margin-top:70px;padding:90px 14px 22px;border-radius:12px;background:linear-gradient(90deg,#a6b0bf,#fff);color:#1b1d3a;text-align:center;font-size:15px;line-height:1.3}
.pcards .disc{position:absolute;left:50%;top:-74px;width:150px;height:150px;transform:translateX(-50%);border-radius:50%;display:flex;align-items:center;justify-content:center;background:conic-gradient(from 200deg,transparent 0 10%,#c8923d 10%,#f5d77a 30%,#c8923d 45%,transparent 45% 58%,#f0d67a 58% 60%,transparent 60%);-webkit-mask:radial-gradient(circle,#000 58px,transparent 59px 69px,#000 70px 72px,transparent 73px);mask:radial-gradient(circle,#000 58px,transparent 59px 69px,#000 70px 72px,transparent 73px)}
.pcards .disc img{position:absolute;width:118px;height:118px;border-radius:50%}
.pcards b{font:700 15px/1.25 var(--head);text-transform:uppercase;letter-spacing:.03em}
.po-inc .btn{justify-self:center;margin-top:24px;min-height:48px;padding:0 34px;font-size:16px;color:#1b1d3a;background:linear-gradient(90deg,#a6b0bf,#fff);white-space:normal;text-align:center;line-height:1.3}
.po-ben{display:grid;background:#1b1d3a;color:#fff}
@media (min-width:900px){.po-ben{grid-template-columns:1fr 1fr;align-items:center}}
.po-ben figure,.po-por figure,.em-dia figure{margin:0;min-height:320px}
.po-ben figure img,.po-por figure img,.em-dia figure img{width:100%;height:100%;object-fit:cover}
@media (min-width:900px){.po-ben figure{clip-path:polygon(0 0,92% 0,100% 100%,0 100%)}}
.po-ben .txt{padding:48px 16px 56px;display:grid;gap:28px;justify-items:center}
.po-ben h2{font:700 clamp(30px,3.4vw,42px)/1.1 var(--cond);text-align:center}
.snake{position:relative;list-style:none;margin:0;padding:0;width:min(100%,440px);aspect-ratio:2214/2160;background:no-repeat 0 0/100% 100%}
.snake li{position:absolute;transform:translateY(-50%);font:600 clamp(14px,1.5vw,18px)/1.2 var(--cond);max-width:42%}
.snake li:nth-child(1){left:17%;top:11.4%}
.snake li:nth-child(2){left:60%;top:31.1%}
.snake li:nth-child(3){left:18%;top:48.6%}
.snake li:nth-child(4){left:60%;top:68.9%}
.snake li:nth-child(5){left:20%;top:92.1%}
.po-por{display:grid;background:#f5f6fa}
@media (min-width:900px){.po-por{grid-template-columns:1.6fr 1fr}}
.po-por .txt{display:grid;gap:16px;align-content:center;padding:48px 28px;background:linear-gradient(180deg,#2db8ee,#148bcc);color:#fff;font-size:18px}
.po-por h2{font:700 clamp(30px,3.4vw,42px)/1.15 var(--cond);text-align:center}
.po-por p{text-align:justify}
.po-por ul{margin:10px 0 0;padding:0;list-style:none;text-align:center;display:grid;gap:2px}
.po-por li::before{content:"• "}
/* Emergencia */
.em-dia{display:grid;background:#1b1d3a;color:#fff}
@media (min-width:900px){.em-dia{grid-template-columns:1fr 1fr}}
.em-dia .txt{display:grid;gap:14px;align-content:center;justify-items:start;padding:48px 24px 56px;font-size:18px}
@media (min-width:900px){.em-dia .txt{padding:56px 8% 56px 8%}}
.em-dia h2{display:flex;gap:10px;align-items:flex-start;font:700 clamp(32px,3.6vw,46px)/1.1 var(--cond);margin-bottom:14px}
.em-dia h2 img{width:22px;height:auto;margin-top:6px}
.em-dia .btn,.em-cdmx .btn{margin-top:26px;min-height:46px}
.em-cdmx{background:#fff;color:#1b1d3a;padding-top:56px;scroll-margin-top:var(--hh)}
.em-dia{scroll-margin-top:var(--hh)}
.em-cdmx .wrap{position:relative;z-index:1;display:grid;gap:30px;align-items:center}
.em-cdmx .txt{padding-bottom:24px}
@media (min-width:900px){.em-cdmx .wrap{grid-template-columns:1fr 1fr}}
.em-cdmx .map{width:min(100%,330px);height:auto;justify-self:center}
.em-cdmx .txt{display:grid;justify-items:center;gap:18px;text-align:center}
.em-cdmx h2{font:700 clamp(32px,3.6vw,46px)/1.1 var(--cond)}
.em-cdmx ul{list-style:none;margin:0;padding:0;display:grid;gap:22px;justify-items:start;color:var(--ink-d);font-size:18px}
.em-cdmx li{display:flex;align-items:center;gap:12px;max-width:22ch;text-align:left}
.em-cdmx li img{width:auto;height:46px}
.em-cdmx .city{width:100%;height:auto;margin-top:-12px}
.quote{scroll-margin-top:var(--hh)}
/* Nosotros (diseño del diseñador, seccion nosotros.pdf, 26 oct 2026). Recursos en img/final/nosotros/ */
.view.fin{background:#fff;color:var(--ink-d);padding-bottom:0}
.ns-w{max-width:1000px;margin:0 auto;padding-inline:16px}
.ns-hero{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:max(560px,min(56.25vw,calc(100svh - var(--hh))));overflow:hidden;background:var(--night);color:#fff}
.ns-video{position:absolute;inset:0;overflow:hidden;container-type:size}
.ns-video>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
/* El video de YouTube cubre todo el hero como un object-fit:cover; un poco más grande para esconder la interfaz de YouTube en los bordes */
.ns-video iframe{position:absolute;top:50%;left:50%;width:max(100cqw,177.78cqh);height:max(100cqh,56.25cqw);transform:translate(-50%,-50%) scale(1.2);border:0;pointer-events:none;opacity:0;transition:opacity 1s}
.ns-video.playing iframe{opacity:1}
.ns-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(25,28,55,.35) 0%,rgba(25,28,55,.3) 45%,rgba(25,28,55,.85) 84%,var(--night) 100%)}
.ns-brand{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);display:grid;justify-items:center;gap:14px;width:100%}
.ns-brand .hlogo{width:min(56vw,320px);height:auto}
.ns-brand .slogan{width:min(56vw,260px);height:auto;filter:drop-shadow(0 2px 6px rgba(0,0,0,.35))}
.ns-intro{position:relative;width:100%;display:grid;gap:10px;padding-bottom:28px}
@media (min-width:800px){.ns-intro{grid-template-columns:29% 1fr;align-items:start;padding-bottom:36px}}
.ns-intro h1{font:700 clamp(40px,4.6vw,56px)/1 var(--cond)}
.ns-intro p{font-size:clamp(17px,1.5vw,19px);line-height:1.4;color:#eef1fa}
/* Historia: los círculos van sobre la línea con degradado del diseñador */
.ns-hist{display:flow-root;position:relative;z-index:1;background:var(--night);color:#fff;padding-top:64px;--cap:clamp(80px,18vw,240px)}
.ns-hist::after{content:"";position:absolute;left:0;right:0;top:100%;height:var(--cap);background:radial-gradient(ellipse 60% 100% at 50% 0,var(--night) 99.4%,transparent 100%);z-index:-1}
.ns-tl{position:relative;display:grid;gap:22px;justify-items:center;padding-bottom:20px}
.ns-tl .blob{display:none}
.ns-tl .c{margin:0;width:min(74vw,340px);aspect-ratio:1;border-radius:50%;box-shadow:0 0 0 10px #38a9e0}
.ns-tl .c3{box-shadow:0 0 0 10px #e84e1b}.ns-tl .c4{box-shadow:0 0 0 10px #f9b400}.ns-tl .c2{box-shadow:0 0 0 10px #2d2e82}
.ns-tl .c img{display:block;width:100%;height:100%}
.ns-tl .t{margin:0 0 18px;font-size:17px;line-height:1.45;max-width:46ch}
@media (min-width:800px){
  .ns-tl{display:block;aspect-ratio:1437.51/1778.03;margin-bottom:-41%;padding:0}
  .ns-tl .blob{display:block;position:absolute;inset:0;width:100%;height:100%}
  .ns-tl .c{position:absolute;width:auto;box-shadow:none}
  .ns-tl .c1{left:6.44%;top:3.71%;width:30.05%}
  .ns-tl .c2{left:50.33%;top:22.89%;width:41.18%}
  .ns-tl .c3{left:6.27%;top:51.38%;width:30.26%}
  .ns-tl .c4{left:58.9%;top:78.6%;width:24.35%}
  .ns-tl .t{position:absolute;margin:0;font-size:clamp(15px,1.45vw,18px);line-height:1.38;max-width:none}
  .ns-tl .t1{left:41%;width:55%;top:6%;text-align:justify}
  .ns-tl .t2{left:0;width:41.5%;top:33.8%;text-align:justify}
  .ns-tl .t3{left:52.7%;width:41.3%;top:64.4%}
}
.ns-vis{background:#fff;color:var(--ink-d);padding:calc(var(--cap,clamp(80px,18vw,240px)) + 40px) 0 72px}
.ns-vis{--cap:clamp(80px,18vw,240px)}
.ns-vis h2,.ns-filo h2{font:700 clamp(30px,3.4vw,44px)/1.15 var(--head);color:#111;letter-spacing:.01em}
.ns-vis>.ns-w>p{max-width:58ch;margin-top:26px;font-size:clamp(17px,1.4vw,19px);line-height:1.4}
.ns-vis .prem{max-width:30ch;margin-top:56px}
.ns-vis .prem+p{max-width:none;margin-top:10px}
.ns-cons{list-style:none;margin:40px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),1fr));column-gap:8%}
.ns-cons li{border-top:1px solid #8a8d99;padding:14px 4px 28px;font:700 clamp(19px,1.8vw,23px)/1.2 var(--cond);color:var(--ink-d)}
.ns-feat{list-style:none;margin:36px 0 0;padding:0;display:grid;gap:18px 40px}
@media (min-width:700px){.ns-feat{grid-template-columns:1fr 1fr;padding-inline:7%}}
.ns-feat li{display:flex;align-items:center;gap:14px;font:700 clamp(18px,1.7vw,22px)/1.25 var(--cond);color:var(--navy)}
.ns-feat img{width:clamp(62px,6vw,76px);height:auto;flex:none;filter:drop-shadow(0 4px 6px rgba(20,30,70,.18))}
.ns-filo{position:relative;z-index:1;background:#16224b;color:#fff;padding:64px 0 40px;overflow-x:clip}
.ns-filo::after{content:"";position:absolute;left:0;right:0;top:100%;height:clamp(50px,11vw,150px);background:radial-gradient(ellipse 62% 100% at 50% 0,#16224b 99.4%,transparent 100%)}
.ns-filo .ns-w,.ns-anti .ns-w{display:grid;gap:36px;align-items:center}
@media (min-width:800px){.ns-filo .ns-w{grid-template-columns:1fr 1fr;gap:4%}.ns-anti .ns-w{grid-template-columns:1.15fr .85fr}}
.ns-filo h2{color:#fff}
.ns-filo .txt{display:grid;gap:22px}
.ns-filo p{text-align:justify;font-size:clamp(17px,1.4vw,19px);line-height:1.4}
.ns-filo ul{margin:6px 0 0;padding:0;list-style:none;font-size:clamp(17px,1.4vw,19px);line-height:1.4}
.ns-filo li::before{content:"• "}
.arrow{margin:0}
.arrow img{display:block;width:100%;height:auto}
.ns-filo .arrow{max-width:520px;width:100%;justify-self:center}
.ns-anti{background:var(--night);color:#fff;padding:clamp(70px,13vw,170px) 0 80px;overflow-x:clip}
.ns-anti .txt{display:grid;justify-items:center;gap:22px;text-align:center;font-family:var(--tech)}
.ns-anti h2{font:400 clamp(20px,2vw,26px)/1.2 var(--tech)}
.ns-anti p{font:400 clamp(21px,2.3vw,30px)/1.25 var(--tech);max-width:24ch}
.ns-anti .btn{margin-top:10px;min-height:46px;padding:8px 30px;line-height:1.2;text-align:center;cursor:pointer}
.ns-anti .arrow{position:relative;z-index:2;max-width:300px;width:62%;justify-self:center}
@media (min-width:800px){.ns-anti .arrow{width:100%;margin-top:clamp(-150px,-11vw,-60px)}}
.ns-dlg{width:min(94vw,1100px);padding:0;border:0;border-radius:16px;background:#000;overflow:visible}
.ns-dlg::backdrop{background:rgba(10,12,30,.85)}
.ns-dlg .frame{aspect-ratio:16/9}
.ns-dlg iframe{display:block;width:100%;height:100%;border:0;border-radius:16px}
.ns-dlg .x{position:absolute;right:0;top:-52px;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.4);background:transparent;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer}
'''

script='''<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
(function(){
  var menu=document.getElementById('menu'),mb=document.getElementById('menuBtn');
  function openMenu(o){menu.hidden=!o;mb.setAttribute('aria-expanded',o?'true':'false');document.body.style.overflow=o?'hidden':'';if(o){document.getElementById('menuClose').focus()}else{mb.focus()}}
  mb.addEventListener('click',function(){openMenu(true)});
  document.getElementById('menuClose').addEventListener('click',function(){openMenu(false)});
  menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){openMenu(false)})});

  var sb=document.getElementById('svcBtn'),ss=document.getElementById('svcSub'),dd=sb.parentNode;
  function sub(o){ss.hidden=!o;sb.setAttribute('aria-expanded',o?'true':'false')}
  sb.addEventListener('click',function(){sub(ss.hidden)});
  dd.addEventListener('mouseenter',function(){if(matchMedia('(hover:hover)').matches)sub(true)});
  dd.addEventListener('mouseleave',function(){if(matchMedia('(hover:hover)').matches)sub(false)});
  ss.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){sub(false)})});
  document.addEventListener('click',function(e){if(!dd.contains(e.target))sub(false)});
  document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;if(!menu.hidden)openMenu(false);if(!ss.hidden){sub(false);sb.focus()}});

  [].forEach.call(document.querySelectorAll('[data-jump]'),function(a){a.addEventListener('click',function(e){e.preventDefault();var t=document.getElementById(a.dataset.jump);if(t)t.scrollIntoView({behavior:'smooth',block:'start'})})});

  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var anim=!!window.gsap&&!reduce;
  if(anim&&window.ScrollTrigger)gsap.registerPlugin(ScrollTrigger);

  // Carruseles "Así se ve un día en campo" (como la propuesta 02): una foto activa, autoplay con barra de progreso, puntos, flechas y deslizar
  [].forEach.call(document.querySelectorAll('.sv-campo'),function(c){
    var track=c.querySelector('.car-track'),slides=[].slice.call(track.children),dots=c.querySelector('.dots'),timer=c.querySelector('.timer i');
    var cur=0,auto=null,DUR=4200,paused=false,visible=false;
    slides.forEach(function(s,i){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Foto '+(i+1));b.addEventListener('click',function(){go(i,true)});dots.appendChild(b)});
    function mark(i){cur=i;slides.forEach(function(s,j){s.classList.toggle('active',j===i)});[].forEach.call(dots.children,function(d,j){d.setAttribute('aria-current',j===i?'true':'false')})}
    function go(i,user){i=(i+slides.length)%slides.length;var s=slides[i];track.scrollTo({left:s.offsetLeft-(track.clientWidth-s.clientWidth)/2,behavior:reduce?'auto':'smooth'});mark(i);if(user)restart()}
    function stop(){clearTimeout(auto);if(anim)gsap.killTweensOf(timer)}
    function restart(){stop();if(reduce||!visible)return;if(anim)gsap.fromTo(timer,{scaleX:0},{scaleX:1,duration:DUR/1000,ease:'none'});auto=setTimeout(function(){if(!paused)go(cur+1);restart()},DUR)}
    [].forEach.call(c.querySelectorAll('.arrows button'),function(b){b.addEventListener('click',function(){go(cur+ +b.dataset.dir,true)})});
    var st;track.addEventListener('scroll',function(){clearTimeout(st);st=setTimeout(function(){var m=track.scrollLeft+track.clientWidth/2,best=0,bd=1e9;slides.forEach(function(s,j){var d=Math.abs(s.offsetLeft+s.clientWidth/2-m);if(d<bd){bd=d;best=j}});if(best!==cur)mark(best)},80)},{passive:true});
    track.addEventListener('pointerdown',function(){paused=true});track.addEventListener('pointerup',function(){paused=false;restart()});
    mark(0);
    if('IntersectionObserver' in window){new IntersectionObserver(function(en){visible=en[0].isIntersecting;if(visible)restart();else stop()},{threshold:.4}).observe(track)}
  });

  // Títulos de portada de servicios: palabra por palabra
  [].forEach.call(document.querySelectorAll('.sv-hero h1'),function(h){var f=document.createDocumentFragment();h.textContent.split(/(\\s+)/).forEach(function(w){if(!w)return;if(/^\\s+$/.test(w)){f.appendChild(document.createTextNode(w))}else{var sp=document.createElement('span');sp.className='w';sp.style.display='inline-block';sp.textContent=w;f.appendChild(sp)}});h.textContent='';h.appendChild(f)});

  // Animaciones de las páginas de servicios, al estilo de la propuesta 02 (Operación primero)
  function svcAnim(v){
    var h=v.querySelector('.sv-hero');
    var tl=gsap.timeline({defaults:{ease:'power3.out'}});
    tl.from(v.querySelectorAll('.sv-tabs a'),{opacity:0,y:14,duration:.45,stagger:.05})
      .from(h.querySelectorAll('.hicon, .label'),{opacity:0,x:-14,duration:.5,stagger:.06},'-=.2')
      .from(h.querySelectorAll('h1 .w'),{opacity:0,y:'0.5em',duration:.6,stagger:.035},'-=.25')
      .from(h.querySelectorAll('.lead, .acts'),{opacity:0,y:12,duration:.5,stagger:.08},'-=.3');
    var ph=h.querySelector('.pg-photo');
    if(ph){
      tl.fromTo(ph,{clipPath:'inset(14% 14% 14% 14% round 40px)',scale:.96},{clipPath:'inset(0% 0% 0% 0% round 40px)',scale:1,duration:1.1,ease:'power3.inOut'},'-=1')
        .from(ph.querySelector('img'),{scale:1.2,duration:1.5,ease:'power2.out'},'<');
      gsap.to(ph.querySelector('img'),{yPercent:8,ease:'none',scrollTrigger:{trigger:h,start:'top top',end:'bottom top',scrub:true}});
    }
    var sh=h.querySelector('.pg-shield');
    if(sh){tl.from(sh,{opacity:0,scale:.85,y:24,duration:1,ease:'back.out(1.4)'},'-=1');gsap.to(sh.querySelector('img'),{y:-10,duration:2.8,ease:'sine.inOut',repeat:-1,yoyo:true,delay:1.8})}
    function once(el,from,trig){gsap.from(el,Object.assign({duration:.7,ease:'power3.out',scrollTrigger:{trigger:trig||el,start:'top 88%',once:true}},from))}
    gsap.utils.toArray(v.querySelectorAll('.sv-inc .wrap > :not(.icards), .sv-campo .head, .sv-cob .wrap > div, .po-inc .wrap > :not(.pcards), .po-ben h2, .po-por .txt > *, .em-dia .txt > *, .em-cdmx .txt > h2, .em-cdmx .txt > .btn')).forEach(function(el){once(el,{opacity:0,y:26})});
    gsap.utils.toArray(v.querySelectorAll('.icards, .pcards, .em-cdmx ul')).forEach(function(g){once(g.children,{opacity:0,y:28,stagger:.09},g)});
    gsap.utils.toArray(v.querySelectorAll('.pcards .disc')).forEach(function(d){once(d,{rotate:-120,duration:1.1,ease:'power3.out'},d.parentNode)});
    gsap.utils.toArray(v.querySelectorAll('.po-ben figure, .po-por figure, .em-dia figure')).forEach(function(f){
      gsap.fromTo(f,{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:1.1,ease:'power3.inOut',scrollTrigger:{trigger:f,start:'top 85%',once:true}});
      once(f.querySelector('img'),{scale:1.2,duration:1.6,ease:'power2.out'},f);
    });
    gsap.utils.toArray(v.querySelectorAll('.sv-cob img, .em-cdmx .map')).forEach(function(m){once(m,{opacity:0,scale:.9,duration:1})});
    // Beneficios de pólizas: la línea se dibuja con el scroll y cada beneficio aparece a su paso
    var sn=v.querySelector('.snake');
    if(sn){gsap.fromTo(sn,{clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0% 0)',ease:'none',scrollTrigger:{trigger:sn,start:'top 80%',end:'bottom 70%',scrub:.4}});
      gsap.utils.toArray(sn.children).forEach(function(li){gsap.from(li,{opacity:0,x:20,duration:.6,ease:'power3.out',scrollTrigger:{trigger:li,start:'top 82%',once:true}})})}
    var city=v.querySelector('.em-cdmx .city');
    if(city)once(city,{opacity:0,yPercent:30,duration:1.2},v.querySelector('.em-cdmx'));
    gsap.utils.toArray(v.querySelectorAll('.sv-campo')).forEach(function(c){
      gsap.fromTo(c.querySelector('.car-track'),{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:1.1,ease:'power3.inOut',clearProps:'clipPath',scrollTrigger:{trigger:c,start:'top 85%',once:true}});
      once(c.querySelectorAll('.slide figcaption > *'),{opacity:0,y:12,duration:.5,stagger:.04,delay:.5},c);
    });
  }

  // Nosotros: video de YouTube de fondo en bucle (silenciado); con movimiento reducido se queda la imagen fija
  var YT_ID='nG2DHYtOx2g',ytPlayer=null,ytWant=false;
  function nosVideo(on){
    ytWant=on;
    if(reduce)return;
    if(ytPlayer&&ytPlayer.playVideo){on?ytPlayer.playVideo():ytPlayer.pauseVideo();return}
    if(!on||window.YT&&window.YT.Player||document.getElementById('ytApi'))return;
    window.onYouTubeIframeAPIReady=function(){
      var box=document.getElementById('nsVideo');
      ytPlayer=new YT.Player('nsPlayer',{videoId:YT_ID,host:'https://www.youtube-nocookie.com',playerVars:{autoplay:1,mute:1,controls:0,loop:1,playlist:YT_ID,playsinline:1,rel:0,disablekb:1,fs:0,iv_load_policy:3,modestbranding:1},
        events:{onReady:function(e){e.target.mute();if(ytWant)e.target.playVideo()},
          onStateChange:function(e){if(e.data===1)box.classList.add('playing');if(e.data===0)e.target.playVideo()}}});
      var f=document.getElementById('nsPlayer');if(f)f.setAttribute('tabindex','-1'),f.setAttribute('aria-hidden','true');
    };
    var s=document.createElement('script');s.id='ytApi';s.src='https://www.youtube.com/iframe_api';document.head.appendChild(s);
  }
  // "Ver nuestro video corporativo": el mismo video con sonido y controles
  var dlg=document.getElementById('nsDlg');
  if(dlg){
    var fr=dlg.querySelector('.frame');
    document.getElementById('nsVideoBtn').addEventListener('click',function(){
      fr.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+YT_ID+'?autoplay=1&rel=0&playsinline=1" title="Video corporativo de Grupo Tecnobg" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      if(ytPlayer&&ytPlayer.pauseVideo)ytPlayer.pauseVideo();
      dlg.showModal();
    });
    document.getElementById('nsDlgClose').addEventListener('click',function(){dlg.close()});
    dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close()});
    dlg.addEventListener('close',function(){fr.innerHTML='';if(ytWant&&ytPlayer&&ytPlayer.playVideo)ytPlayer.playVideo()});
  }

  function nosAnim(v){
    var h=v.querySelector('.ns-hero');
    gsap.timeline({defaults:{ease:'power3.out'}})
      .from(h.querySelector('.hlogo'),{opacity:0,y:20,duration:.8})
      .fromTo(h.querySelector('.slogan'),{clipPath:'inset(0 0 100% 0)',y:20},{clipPath:'inset(0 0 0% 0)',y:0,duration:1.1,ease:'power4.out'},'-=.5')
      .from(h.querySelectorAll('.ns-intro > *'),{opacity:0,y:18,duration:.7,stagger:.1},'-=.7');
    function once(el,from,trig){gsap.from(el,Object.assign({duration:.7,ease:'power3.out',scrollTrigger:{trigger:trig||el,start:'top 88%',once:true}},from))}
    // Línea de la historia: se dibuja de arriba abajo con el scroll
    var blob=v.querySelector('.ns-tl .blob');
    if(blob&&getComputedStyle(blob).display!=='none')gsap.fromTo(blob,{clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0% 0)',ease:'none',scrollTrigger:{trigger:blob,start:'top 75%',end:'bottom 85%',scrub:.5}});
    // Círculos: escala 0% → 110% → 100% (pequeño rebote), como pidió el diseñador
    gsap.utils.toArray(v.querySelectorAll('.ns-tl .c')).forEach(function(c){
      gsap.timeline({scrollTrigger:{trigger:c,start:'top 82%',once:true}})
        .fromTo(c,{scale:0},{scale:1.1,duration:.4,ease:'power2.out'})
        .to(c,{scale:1,duration:.25,ease:'power1.inOut'});
    });
    gsap.utils.toArray(v.querySelectorAll('.ns-tl .t, .ns-vis h2, .ns-vis .ns-w > p, .ns-filo .txt > *, .ns-anti .txt > *')).forEach(function(el){once(el,{opacity:0,y:24})});
    gsap.utils.toArray(v.querySelectorAll('.ns-cons, .ns-feat')).forEach(function(g){once(g.children,{opacity:0,y:22,stagger:.08},g)});
    // Flechas: llegan desde el lado que marcan (Filosofía desde la izquierda, Anticipación desde la derecha)
    gsap.utils.toArray(v.querySelectorAll('.arrow')).forEach(function(a){
      var d=a.classList.contains('from-left')?-1:1;
      gsap.from(a,{x:d*Math.min(innerWidth*.45,420),opacity:0,duration:1.1,ease:'power3.out',scrollTrigger:{trigger:a,start:'top 80%',once:true}});
    });
  }

'''+form_js+'''
  // Cada página interna es una vista del mismo archivo, elegida por el #hash
  var views=[].slice.call(document.querySelectorAll('.view'));
  var ctx=null;
  function show(){
    // Las vistas usan id="v-…" para que el navegador no salte al #hash por su cuenta
    var id=(location.hash||'#nosotros').slice(1),v=document.getElementById('v-'+id);
    if(!v||!v.classList.contains('view'))return;
    views.forEach(function(x){x.hidden=x!==v});
    // Las páginas de servicios ya tienen su diseño final: sin aviso de preliminar y con el formulario de cotización
    var svc=v.classList.contains('svc');
    document.getElementById('prelim').hidden=svc||v.classList.contains('fin');
    document.getElementById('cotizar').hidden=!svc;
    document.title='Grupo Tecnobg · '+v.dataset.title;
    window.scrollTo(0,0);
    // Deja visible la pestaña activa en móvil
    var tab=v.querySelector('.sv-tabs a[aria-current]');if(tab)tab.parentNode.scrollLeft=tab.offsetLeft-16;
    if(ctx){ctx.revert();ctx=null}
    nosVideo(id==='nosotros');
    if(anim&&svc&&window.ScrollTrigger){ctx=gsap.context(function(){svcAnim(v)},v);ScrollTrigger.refresh();return}
    if(anim&&id==='nosotros'&&window.ScrollTrigger){ctx=gsap.context(function(){nosAnim(v)},v);ScrollTrigger.refresh();return}
    if(anim){
      gsap.from(v.querySelectorAll('.pg-copy > *'),{opacity:0,y:22,duration:.7,stagger:.08,ease:'power3.out'});
      var ph=v.querySelector('.pg-photo');
      if(ph){gsap.fromTo(ph,{clipPath:'inset(0 0 100% 0 round 22px)'},{clipPath:'inset(0 0 0% 0 round 22px)',duration:1.1,ease:'power3.inOut',delay:.2});gsap.from(ph.querySelector('img'),{scale:1.2,duration:1.5,ease:'power2.out',delay:.2})}
      gsap.from(v.querySelectorAll('.pg-body > *'),{opacity:0,y:24,duration:.6,stagger:.07,delay:.3,ease:'power3.out'});
    }
  }
  addEventListener('hashchange',show);
  if(!document.getElementById('v-'+(location.hash||'#nosotros').slice(1))){history.replaceState(null,'','#nosotros')}
  show();
})();
</script>'''

html=f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Grupo Tecnobg</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&family=Michroma&family=Hind:wght@400;500;600&family=Barlow+Condensed:wght@600;700&display=swap">
<style>
/* Generado por herramientas/generar-paginas.py con el menú y el pie de final.html: edita ese script y vuelve a correrlo. */
{base_css}{quote_css}{tail_css}{page_css}</style>
</head>
<body>

{header}
<main>
<div class="prelim" id="prelim" role="note"><div class="wrap"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 3 2 21h20zM12 10v5M12 18v.5"/></svg><span>Diseño preliminar: esta página sigue pendiente de su diseño final.</span></div></div>
{views}
{quote}</main>

{footer}{script}
</body>
</html>
'''
open(R+'final-paginas.html','w').write(html)
print(len(html))

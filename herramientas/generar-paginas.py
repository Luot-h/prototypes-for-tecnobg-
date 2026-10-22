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

WA='https://wa.me/525646037573'
def hero(label,title,lead,img,alt,pos='50% 50%'):
    return f'''<header class="pg-hero">
    <div class="pg-copy"><span class="label">{label}</span><h1>{title}</h1><p class="lead">{lead}</p>
    <div class="acts"><a class="btn btn-blue" href="final.html#contacto">Solicitar cotización</a><a class="btn btn-ghost" href="{WA}">WhatsApp</a></div></div>
    <figure class="pg-photo"><img src="{img}" alt="{alt}" style="object-position:{pos}"></figure>
  </header>'''
def pend(t): return f'<p class="pend">{t}</p>'
def others(cur):
    items=[('mantenimiento-preventivo','Mantenimiento preventivo'),('reparacion','Reparación'),('polizas','Pólizas'),('servicio-de-emergencia','Servicio de emergencia')]
    li=''.join(f'<a class="card" href="#{i}"><b>{t}</b><span>Ver servicio →</span></a>' for i,t in items if i!=cur)
    return f'<section class="blk"><h2>Otros servicios</h2><div class="cards">{li}</div></section>'
PROC='<section class="blk"><h2>Así atendemos tu solicitud</h2><p>Recepción inmediata, asignación rápida del servicio, diagnóstico profesional, cotización clara y ejecución final con entrega operativa.</p><a class="more" href="final.html#proceso">Ver el proceso completo →</a></section>'
def legal(pid,title,lead,items):
    toc=''.join(f'<li><a href="#" data-jump="{pid}-{i+1}">{t}</a></li>' for i,t in enumerate(items))
    secs=''.join(f'<article class="lsec" id="{pid}-{i+1}"><h2>{t}</h2>{pend("Texto pendiente: lo redacta y valida Tecnobg o su asesor legal.")}</article>' for i,t in enumerate(items))
    return f'''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Legales</span><h1>{title}</h1><p class="lead">{lead}</p></div></header>
  <div class="pg-body"><nav class="toc" aria-label="Contenido"><span class="label">Contenido</span><ol>{toc}</ol></nav><div class="lbody">{secs}</div></div>'''

V=[]
V.append(('nosotros','Nosotros',hero('Nosotros','Grupo Tecnobg','Reparación y mantenimiento preventivo especializado en el sector HORECA en México.','img/equipo-plaza.webp','Técnicos de mantenimiento de Tecnobg recorriendo una tienda')+'''
  <div class="pg-body">
    <div class="stats"><div><b>+25</b><span>Años de experiencia</span></div><div><b>+35</b><span>Marcas</span></div><div><b>+50</b><span>Soluciones</span></div></div>
    <section class="blk"><h2>Nuestros técnicos están en constante capacitación</h2><p>Nuestros técnicos están capacitándose constantemente en las últimas tecnologías para brindar a tus equipos un servicio de calidad.</p></section>
    <blockquote class="pq">“Confianza y garantía no son promesas, son el estándar con el que trabajamos”</blockquote>
    <section class="blk"><h2>Historia, misión y valores</h2>'''+pend('Contenido pendiente: historia, misión, visión, valores y equipo de Tecnobg.')+'''</section>
  </div>'''))
V.append(('mantenimiento-preventivo','Mantenimiento preventivo',hero('Servicios','Mantenimiento preventivo','Un programa estructurado que prolonga la vida útil de tus equipos y optimiza su desempeño.','img/final/mantenimiento.webp','Técnico de Tecnobg da mantenimiento a un evaporador','50% 35%')+'''
  <div class="pg-body">
    <section class="blk"><h2>Áreas que atendemos</h2><ul class="ticks">
      <li><b>Línea fría</b>Mantenimiento a sistemas de refrigeración enfocado en eficiencia térmica y conservación de su materia prima.</li>
      <li><b>Aire acondicionado</b>Mantenimiento a instalaciones de aire acondicionado para asegurar confort, eficiencia energética y funcionamiento continuo.</li>
      <li><b>Línea caliente</b>Mantenimiento preventivo y reparación de equipos de línea caliente.</li></ul>
      <p class="links"><a class="more" href="final.html#linea-fria">Equipos de línea fría →</a><a class="more" href="final.html#linea-caliente">Equipos de línea caliente →</a></p></section>
    <section class="blk"><h2>Qué incluye</h2>'''+pend('Contenido pendiente: periodicidad, actividades por visita y reporte que se entrega.')+'''</section>
    '''+PROC+others('mantenimiento-preventivo')+'</div>'))
V.append(('reparacion','Reparación',hero('Servicios','Reparación','Reparación rápida y precisa para que tu operación siga marchando.','img/final/reparacion.webp','Técnico de Tecnobg repara la tarjeta electrónica de un equipo','50% 40%')+'''
  <div class="pg-body">
    <section class="blk"><h2>Corregimos la falla con precisión</h2><p>Corregimos la falla con precisión para que tu operación no se detenga y tus equipos recuperen su rendimiento óptimo.</p></section>
    <section class="blk"><h2>Diagnóstico técnico</h2><p>Visita especializada para evaluar el equipo, identificar riesgos operativos y definir acciones preventivas o correctivas con base técnica.</p></section>
    <section class="blk"><h2>Línea fría y línea caliente</h2><p>Reparamos equipos de refrigeración, aire acondicionado, extracción y ventilación, y equipos de línea caliente, tanto comerciales como industriales.</p>
      <p class="links"><a class="more" href="final.html#linea-fria">Equipos de línea fría →</a><a class="more" href="final.html#linea-caliente">Equipos de línea caliente →</a></p></section>
    <section class="blk"><h2>Garantía</h2><p>Garantía de 30 días en cualquier reparación o mantenimiento.</p></section>
    '''+PROC+others('reparacion')+'</div>'))
V.append(('polizas','Pólizas',hero('Servicios','Pólizas','Nuestras pólizas son una solución diseñada para empresas que buscan previsión, estabilidad y control en sus equipos.','img/final/polizas.webp','Chef cocinando con fuego alto en una cocina industrial','60% 50%')+'''
  <div class="pg-body">
    <section class="blk"><h2>Previsión, estabilidad y control</h2><ul class="ticks">
      <li><b>Previsión</b>Mantenimiento preventivo programado que prolonga la vida útil de tus equipos y optimiza su desempeño.</li>
      <li><b>Respuesta</b>Respuesta a urgencias en menos de 24 horas.</li>
      <li><b>Respaldo</b>Garantía de 30 días en cualquier reparación o mantenimiento. Cumplimiento legal y REPSE vigente.</li></ul></section>
    <section class="blk"><h2>Qué incluye cada póliza</h2>'''+pend('Contenido pendiente: alcance, periodicidad de visitas, equipos cubiertos y planes disponibles.')+'''</section>
    '''+others('polizas')+'</div>'))
V.append(('servicio-de-emergencia','Servicio de emergencia',hero('Servicios','Servicios de Emergencia','Cuando la operación exige inmediatez, respondemos con eficiencia.','img/final/emergencia.webp','Camioneta de servicio de Tecnobg circulando de noche por la ciudad','62% 50%')+'''
  <div class="pg-body">
    <section class="blk"><h2>Respuesta a urgencias</h2><p>Mantenimiento correctivo rápido y preciso para restablecer la operación en el menor tiempo posible. Respuesta a urgencias en menos de 24 horas. Escríbenos por WhatsApp al 56 4603 7573, de lunes a sábado de 9:00 a 18:00.</p><a class="btn btn-blue" href="'''+WA+'''">Solicitar servicio de emergencia</a></section>
    '''+PROC+others('servicio-de-emergencia')+'</div>'))
# Blog, ofertas y bolsa de trabajo: propuesta visual del sistema administrable (contenido de ejemplo, se cargará desde el panel en Laravel)
DEMO='Propuesta visual: el contenido es de ejemplo y se administrará desde el panel de Tecnobg.'
POSTS=[
  ('Línea fría','5 señales de que tu cámara de refrigeración necesita mantenimiento','Hielo en el evaporador, puertas que no sellan o un compresor que no descansa: qué revisar antes de que falle.','img/final/equipos/camaras.webp','14 oct 2026','4 min'),
  ('Línea caliente','Cómo alargar la vida útil de tu freidora industrial','Rutinas de limpieza, cambio de aceite y revisión del termostato que evitan paros en plena operación.','img/final/equipos/freidora.webp','7 oct 2026','5 min'),
  ('Mantenimiento','Preventivo vs. correctivo: lo que cuesta no planear','Comparamos el costo de un programa de mantenimiento con el de una reparación de emergencia.','img/final/mantenimiento.webp','30 sep 2026','6 min'),
  ('Línea fría','Qué revisar en tu máquina de hielo antes de temporada alta','Filtros, sarro y ciclos de cosecha: una lista corta para llegar listo a los meses de más demanda.','img/final/equipos/maquina-hielo.webp','22 sep 2026','3 min'),
  ('Operación','Trampas de grasa: cada cuánto limpiarlas','Una guía rápida para cocinas de alto volumen y lo que pasa cuando se deja para después.','img/final/equipos/trampa-de-grasa.webp','15 sep 2026','4 min'),
  ('Línea caliente','Hornos de convección: errores comunes de operación','Carga, precalentamiento y ventilación: hábitos que dañan el equipo sin que se note.','img/final/equipos/horno-conveccion.webp','8 sep 2026','5 min'),
]
def post_card(c,t,x,img,d,m,big=False):
    return f'''<a class="post{' big' if big else ''}" href="#blog-articulo" data-cat="{c}"><figure><img src="{img}" alt="" loading="lazy"></figure><div class="pc"><span class="tag">{c}</span><h3>{t}</h3><p>{x}</p><small>{d} · {m} de lectura</small></div></a>'''
cats=['Todos','Línea fría','Línea caliente','Mantenimiento','Operación']
chips=''.join(f'<button type="button" class="chip{" on" if i==0 else ""}" data-filter="{c}">{c}</button>' for i,c in enumerate(cats))
V.append(('blog','Blog','''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Blog</span><h1>Blog Tecnobg</h1><p class="lead">Consejos de mantenimiento, cuidado de equipos y operación para cocinas, tiendas y restaurantes.</p></div></header>
  <div class="pg-body wide">
    <div class="chips" role="group" aria-label="Filtrar por categoría">'''+chips+'''</div>
    '''+post_card(*POSTS[0],big=True)+'''
    <div class="posts" id="posts">'''+''.join(post_card(*p) for p in POSTS[1:])+'''</div>
    <nav class="pager" aria-label="Paginación"><a aria-current="page" href="#blog">1</a><a href="#blog">2</a><a href="#blog">3</a><a href="#blog">Siguiente →</a></nav>
  </div>''',DEMO))

rel=''.join(post_card(*p) for p in POSTS[1:4])
V.append(('blog-articulo','Artículo','''<article>
  <header class="art-hero"><div class="wrap">
    <a class="back" href="#blog">← Volver al blog</a>
    <span class="tag">Línea fría</span>
    <h1>5 señales de que tu cámara de refrigeración necesita mantenimiento</h1>
    <p class="meta"><span class="av">TB</span>Equipo Tecnobg · 14 de octubre de 2026 · 4 min de lectura</p>
  </div></header>
  <figure class="art-cover"><img src="img/final/equipos/camaras.webp" alt="Cámara de refrigeración comercial"></figure>
  <div class="pg-body art">
    <div class="prose">
      <p class="intro">Una cámara de refrigeración rara vez falla de golpe: casi siempre avisa. Detectar esas señales a tiempo es la diferencia entre una visita programada y perder producto en plena operación.</p>
      <h2>1. Se forma hielo en el evaporador</h2>
      <p>Una capa delgada es normal, pero si el hielo cubre las aletas el aire deja de circular y el equipo trabaja de más. Puede venir de un ciclo de deshielo que no funciona o de una puerta que se queda abierta.</p>
      <h2>2. La puerta ya no sella</h2>
      <p>Empaques rotos o bisagras desajustadas dejan entrar aire caliente y humedad. Haz la prueba de la hoja: si sale sin resistencia al cerrar la puerta, el empaque necesita revisión.</p>
      <blockquote>Texto de ejemplo: el contenido real lo redactará Tecnobg desde el panel con el editor de artículos.</blockquote>
      <h2>3. El compresor no descansa</h2>
      <ul><li>Ciclos de encendido muy largos o continuos.</li><li>Ruido o vibración fuera de lo normal.</li><li>Temperatura que sube en horas de mayor uso.</li></ul>
      <h2>4. Charcos o goteo</h2>
      <p>Un drenaje tapado o una charola de condensado llena terminan en agua en el piso, un riesgo para el personal y para el equipo.</p>
      <h2>5. Facturas de luz más altas</h2>
      <p>Un condensador sucio o con poco gas hace que el equipo consuma más energía para mantener la misma temperatura.</p>
      <aside class="cta-box"><b>¿Tu equipo presenta alguna de estas señales?</b><p>Agenda una revisión con nuestros técnicos.</p><div class="acts"><a class="btn btn-blue" href="final.html#contacto">Solicitar cotización</a><a class="btn btn-ghost dark" href="'''+WA+'''">WhatsApp</a></div></aside>
      <p class="share">Compartir: <a href="#blog-articulo">Facebook</a> · <a href="#blog-articulo">LinkedIn</a> · <a href="#blog-articulo">WhatsApp</a> · <a href="#blog-articulo">Copiar enlace</a></p>
    </div>
    <section class="blk"><h2>Artículos relacionados</h2><div class="posts">'''+rel+'''</div></section>
  </div>
</article>''',DEMO))

OFFERS=[
  ('-15%','Mantenimiento preventivo de línea fría','Revisión completa de refrigeradores, mesas frías y vitrinas: limpieza de condensador, revisión de gas, empaques y termostato.','img/final/equipos/refrigeradores.webp','30 nov 2026',True),
  ('Paquete','Revisión de temporada para línea caliente','Freidoras, planchas y hornos revisados en una sola visita antes de la temporada alta.','img/final/equipos/plancha-caliente.webp','15 dic 2026',False),
  ('2×1','Diagnóstico de máquinas de hielo','Agenda el diagnóstico de dos máquinas en la misma sucursal y paga solo uno.','img/final/equipos/maquina-hielo.webp','31 oct 2026',False),
  ('Póliza','Primer mes sin costo en pólizas anuales','Contrata una póliza anual de mantenimiento y el primer mes corre por nuestra cuenta.','img/final/polizas.webp','31 dic 2026',False),
]
def offer(b,t,x,img,h,star):
    msg=('Hola, me interesa la oferta: '+t).replace(' ','%20')
    return f'''<article class="offer{' star' if star else ''}"><figure><img src="{img}" alt="" loading="lazy"><span class="badge">{b}</span>{'<span class="feat">Destacada</span>' if star else ''}</figure><div class="oc"><h3>{t}</h3><p>{x}</p><p class="valid">Válida hasta el {h}</p><div class="acts"><a class="btn btn-blue" href="{WA}?text={msg}">La quiero</a><a class="btn btn-ghost dark" href="final.html#contacto">Cotizar</a></div></div></article>'''
V.append(('ofertas','Ofertas','''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Ofertas</span><h1>Ofertas y promociones</h1><p class="lead">Promociones vigentes en mantenimiento, reparación y pólizas para tu negocio.</p></div></header>
  <div class="pg-body wide">
    <div class="offers">'''+''.join(offer(*o) for o in OFFERS)+'''</div>
    <p class="fine">Las promociones aplican en la zona de cobertura de Tecnobg, sujetas a disponibilidad y a diagnóstico previo. No son acumulables con otras promociones.</p>
  </div>''',DEMO))

JOBS=[
  ('Técnico(a) de refrigeración comercial','Operaciones','Ciudad de México','Tiempo completo','Hace 2 días'),
  ('Técnico(a) de línea caliente','Operaciones','Ciudad de México','Tiempo completo','Hace 5 días'),
  ('Auxiliar de mantenimiento','Operaciones','Estado de México','Tiempo completo','Hace 1 semana'),
  ('Ejecutivo(a) de ventas','Comercial','Ciudad de México','Tiempo completo','Hace 2 semanas'),
  ('Coordinador(a) de servicio','Administración','Ciudad de México','Tiempo completo','Hace 3 semanas'),
]
def job(t,a,z,j,h):
    return f'''<a class="job" href="#vacante" data-area="{a}"><div><span class="tag">{a}</span><h3>{t}</h3><p class="jm"><span>{z}</span><span>{j}</span></p></div><div class="jr"><small>{h}</small><span class="go">Ver vacante →</span></div></a>'''
areas=['Todas las áreas','Operaciones','Comercial','Administración']
achips=''.join(f'<button type="button" class="chip{" on" if i==0 else ""}" data-filter="{a}">{a}</button>' for i,a in enumerate(areas))
V.append(('bolsa-de-trabajo','Bolsa de trabajo',hero('Bolsa de trabajo','Trabaja en Tecnobg','Buscamos técnicos y personal administrativo que quieran crecer con nosotros atendiendo al sector HORECA.','img/equipo-plaza.webp','Técnicos de Tecnobg recorriendo una plaza comercial').replace('href="final.html#contacto">Solicitar cotización','href="#" data-jump="vacantes">Ver vacantes').replace('<a class="btn btn-ghost" href="'+WA+'">WhatsApp</a>','')+'''
  <div class="pg-body wide">
    <section class="blk" id="vacantes"><h2>Vacantes disponibles</h2>
      <div class="chips" role="group" aria-label="Filtrar por área">'''+achips+'''</div>
      <div class="jobs" id="jobs">'''+''.join(job(*j) for j in JOBS)+'''</div>
    </section>
    <section class="blk spont"><h2>¿No ves tu puesto?</h2><p>Envíanos tu CV y te tomaremos en cuenta para futuras vacantes.</p><a class="btn btn-blue" href="#vacante">Enviar mi CV</a></section>
  </div>''',DEMO))

V.append(('vacante','Vacante','''<header class="art-hero"><div class="wrap">
    <a class="back" href="#bolsa-de-trabajo">← Todas las vacantes</a>
    <span class="tag">Operaciones</span>
    <h1>Técnico(a) de refrigeración comercial</h1>
    <ul class="facts"><li>Ciudad de México</li><li>Tiempo completo</li><li>Lunes a sábado</li><li>Sueldo a tratar</li></ul>
  </div></header>
  <div class="pg-body wide job-layout">
    <div class="prose">
      <h2>Sobre el puesto</h2>
      <p>Darás servicio de mantenimiento preventivo y correctivo a equipos de refrigeración comercial en restaurantes, tiendas y cocinas industriales de nuestros clientes.</p>
      <h2>Responsabilidades</h2>
      <ul><li>Diagnóstico y reparación de cámaras, refrigeradores, mesas frías y vitrinas.</li><li>Mantenimiento preventivo según el programa de cada cliente.</li><li>Reporte de servicio con evidencia fotográfica.</li></ul>
      <h2>Requisitos</h2>
      <ul><li>Experiencia comprobable en refrigeración comercial.</li><li>Conocimientos de electricidad y manejo de herramienta.</li><li>Disponibilidad para trasladarse en la zona metropolitana.</li></ul>
      <h2>Ofrecemos</h2>
      <ul><li>Prestaciones de ley.</li><li>Capacitación constante.</li><li>Herramienta y uniforme.</li></ul>
      <p class="fine">Texto de ejemplo: cada vacante se redacta y publica desde el panel.</p>
    </div>
    <aside class="apply" id="postular">
      <form id="applyForm" novalidate>
        <h2>Postúlate</h2>
        <label>Nombre completo<input required autocomplete="name"></label>
        <label>Correo electrónico<input type="email" required autocomplete="email"></label>
        <label>Teléfono<input type="tel" required autocomplete="tel"></label>
        <label>Ciudad o alcaldía<input required></label>
        <label>Años de experiencia<select required><option value="">Elige una opción</option><option>Menos de 1 año</option><option>1 a 3 años</option><option>3 a 5 años</option><option>Más de 5 años</option></select></label>
        <label class="file">CV en PDF (máx. 5 MB)<input type="file" accept="application/pdf"><span>Arrastra tu archivo o <u>elige uno</u></span></label>
        <label>Mensaje (opcional)<textarea rows="3"></textarea></label>
        <label class="check"><input type="checkbox" required> Acepto el <a href="#aviso-de-privacidad">aviso de privacidad</a></label>
        <button class="btn btn-blue" type="submit">Enviar postulación</button>
      </form>
      <div class="sent" id="applyOk" hidden><b>¡Gracias por postularte!</b><p>Recibimos tu solicitud. Si tu perfil coincide con la vacante, el equipo de Recursos Humanos te contactará.</p><a class="more" href="#bolsa-de-trabajo">Ver otras vacantes →</a></div>
    </aside>
  </div>''',DEMO))
V.append(('aviso-de-privacidad','Aviso de privacidad',legal('ap','Aviso de privacidad','Conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.',['Identidad y domicilio del responsable','Datos personales que recabamos','Finalidades del tratamiento','Transferencias de datos','Derechos ARCO y cómo ejercerlos','Cookies y tecnologías de rastreo','Cambios a este aviso'])))
V.append(('terminos-y-condiciones','Términos y condiciones',legal('tc','Términos y condiciones','Condiciones de uso de este sitio y de los servicios de Grupo Tecnobg.',['Objeto','Uso del sitio','Cotizaciones y autorización de servicios','Garantía','Propiedad intelectual','Legislación aplicable'])))
V.append(('uso-de-cookies','Uso de cookies',legal('ck','Uso de cookies','Cómo usa este sitio las cookies y tecnologías similares.',['¿Qué son las cookies?','Herramientas que usa el sitio','Cómo desactivarlas','Cambios a esta política'])))

views=''.join(f'\n<section class="view" id="v-{v[0]}" data-title="{v[1]}"'+(f' data-note="{v[3]}"' if len(v)>3 else '')+f' hidden>\n  {v[2]}\n</section>' for v in V)

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
/* Blog, ofertas y bolsa de trabajo (propuesta del sistema administrable) */
.prelim.demo{background:linear-gradient(90deg,#4cc1f0,#219fda);color:#06243a}
.pg-body.wide{max-width:1240px}
.tag{display:inline-block;font:600 12px/1 var(--head);text-transform:uppercase;letter-spacing:.06em;color:var(--navy);background:#e6ecfa;border-radius:999px;padding:6px 10px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{min-height:40px;padding:0 16px;border-radius:999px;border:1px solid #cfd6e8;background:#fff;color:var(--ink-d);font:500 14px var(--head)}
.chip.on{background:var(--ink-d);border-color:var(--ink-d);color:#fff}
.posts{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,290px),1fr));gap:20px;width:100%}
.post{display:grid;grid-template-rows:auto 1fr;background:#fff;border:1px solid #e3e7f1;border-radius:18px;overflow:hidden;text-decoration:none;color:var(--ink-d);transition:transform .3s,box-shadow .3s}
.post:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(21,33,73,.12)}
.post figure{margin:0;aspect-ratio:16/10;overflow:hidden;background:#dfe4f0}
.post img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.post:hover img{transform:scale(1.05)}
.pc{display:grid;gap:10px;align-content:start;justify-items:start;padding:20px}
.pc h3{font:700 20px/1.25 var(--head)}
.pc p{color:#45507a;font-size:16px}
.pc small{color:#6b7493;font-size:14px}
.post.big{grid-template-rows:none}
@media (min-width:900px){.post.big{grid-template-columns:1.3fr 1fr}.post.big figure{aspect-ratio:auto;min-height:360px}.post.big .pc{padding:36px;align-content:center}.post.big h3{font-size:32px}}
.pager{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.pager a{min-width:44px;min-height:44px;padding:0 14px;display:flex;align-items:center;justify-content:center;border-radius:10px;border:1px solid #cfd6e8;background:#fff;text-decoration:none;color:var(--ink-d);font:500 15px var(--head)}
.pager a[aria-current]{background:var(--navy);border-color:var(--navy);color:#fff}
.art-hero{background:var(--night);color:var(--ink);padding-block:44px 120px}
.art-hero .wrap{max-width:860px;display:grid;gap:16px;justify-items:start}
.art-hero h1{font:700 clamp(36px,7vw,58px)/1.02 var(--cond)}
.art-hero .tag{background:rgba(255,255,255,.12);color:#fff}
.back{color:#cfd7f2;text-decoration:none;font:500 15px var(--head)}
.back:hover{color:#fff}
.meta{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:15px}
.av{width:36px;height:36px;border-radius:50%;background:var(--g-blue);display:flex;align-items:center;justify-content:center;color:#fff;font:700 13px var(--head)}
.art-cover{margin:-90px auto 0;max-width:1000px;padding-inline:16px}
.art-cover img{width:100%;aspect-ratio:16/8;object-fit:cover;border-radius:22px}
.pg-body.art{max-width:1000px}
.prose{max-width:720px;width:100%;margin:0 auto;display:grid;gap:16px;font-size:18px;line-height:1.7}
.prose h2{font:700 clamp(22px,3.6vw,28px)/1.25 var(--head);color:var(--ink-d);margin-top:14px}
.prose ul{margin:0;padding-left:22px;display:grid;gap:6px}
.prose .intro{font-size:21px;color:var(--ink-d)}
.prose blockquote{margin:0;border-left:4px solid #219fda;background:#fff;padding:14px 18px;border-radius:0 12px 12px 0;color:#45507a;font-size:16px}
.cta-box{display:grid;gap:8px;justify-items:start;background:var(--night);color:var(--ink);border-radius:18px;padding:26px;margin-top:10px}
.cta-box b{font:700 22px/1.25 var(--head)}
.btn-ghost.dark{border-color:rgba(255,255,255,.45)}
.view .pg-body .btn-ghost.dark{color:var(--ink-d);border-color:#b8c1da}
.view .cta-box .btn-ghost.dark{color:#fff;border-color:rgba(255,255,255,.45)}
.share{font-size:15px;color:#6b7493}
.share a{color:var(--navy)}
.offers{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:20px}
.offer{display:grid;grid-template-rows:auto 1fr;background:#fff;border:1px solid #e3e7f1;border-radius:18px;overflow:hidden}
.offer.star{border:2px solid #219fda}
@media (min-width:900px){.offer.star{grid-column:span 2;grid-template-rows:none;grid-template-columns:1fr 1fr}.offer.star figure{aspect-ratio:auto}}
.offer figure{margin:0;position:relative;aspect-ratio:16/10;background:#dfe4f0}
.offer img{width:100%;height:100%;object-fit:cover}
.badge{position:absolute;left:14px;top:14px;background:var(--g-warm);color:#fff;text-shadow:0 1px 3px rgba(120,30,0,.7);font:400 18px/1 var(--tech);padding:10px 14px;border-radius:10px}
.feat{position:absolute;right:14px;top:14px;background:var(--ink-d);color:#fff;font:600 12px/1 var(--head);text-transform:uppercase;letter-spacing:.06em;padding:8px 10px;border-radius:999px}
.oc{display:grid;gap:10px;align-content:start;padding:22px}
.oc h3{font:700 21px/1.25 var(--head);color:var(--ink-d)}
.oc p{color:#45507a;font-size:16px}
.oc .valid{color:var(--caliente);font:600 14px var(--head)}
.oc .btn{min-height:44px;padding:0 20px}
.fine{font-size:14px;color:#6b7493;max-width:80ch}
#vacantes{scroll-margin-top:calc(var(--hh) + 60px)}
.jobs{display:grid;gap:10px;width:100%}
.job{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:14px;padding:20px 22px;background:#fff;border:1px solid #e3e7f1;border-radius:16px;text-decoration:none;color:var(--ink-d);transition:border-color .3s,transform .3s}
.job:hover{border-color:#219fda;transform:translateX(4px)}
.job>div:first-child{display:grid;gap:8px;justify-items:start}
.job h3{font:700 20px/1.25 var(--head)}
.jm{display:flex;flex-wrap:wrap;gap:6px 16px;color:#45507a;font-size:15px}
.jm span::before{content:"• ";color:#219fda}
.jr{display:grid;gap:4px}
@media (min-width:700px){.jr{justify-items:end;text-align:right}}
.jr small{color:#6b7493}
.go{color:var(--navy);font:600 15px var(--head)}
.spont{background:#fff;border:1px dashed #b8c1da;border-radius:18px;padding:26px}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.facts li{border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:8px 14px;font-size:15px}
#v-vacante .art-hero{padding-bottom:56px}
#v-vacante .art-hero .wrap{max-width:1240px}
.job-layout{align-items:start}
@media (min-width:1000px){.job-layout{grid-template-columns:1fr 400px}.job-layout .prose{margin:0}.apply{position:sticky;top:calc(var(--hh) + 64px)}}
.apply{background:#fff;border:1px solid #e3e7f1;border-radius:20px;padding:24px;box-shadow:0 18px 40px rgba(21,33,73,.08)}
.apply form{display:grid;gap:14px}
.apply h2{font:700 24px var(--head);color:var(--ink-d)}
.apply label{display:grid;gap:6px;font:500 14px var(--head);color:var(--ink-d)}
.apply input,.apply select,.apply textarea{font:400 16px var(--body);min-height:46px;padding:10px 12px;border:1px solid #cfd6e8;border-radius:10px;background:#f9fafd;color:var(--ink-d);width:100%}
.apply textarea{resize:vertical}
.apply .file{position:relative;border:1.5px dashed #b8c1da;border-radius:12px;padding:16px;text-align:center;background:#f9fafd}
.apply .file input{position:absolute;inset:0;opacity:0;cursor:pointer;min-height:0}
.apply .file span{color:#6b7493;font:400 15px var(--body)}
.apply .check{display:flex;align-items:center;gap:10px;font:400 15px var(--body)}
.apply .check input{width:20px;height:20px;min-height:0;flex:none}
.apply .check a{color:var(--navy)}
.apply .btn{width:100%}
.sent{display:grid;gap:10px}
.sent b{font:700 22px var(--head);color:var(--ink-d)}
'''

script='''<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
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

  // Filtros de categoría (blog) y área (bolsa de trabajo)
  [].forEach.call(document.querySelectorAll('.chips'),function(g){
    var list=g.parentNode.querySelector('.posts,.jobs');
    g.addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;
      [].forEach.call(g.children,function(c){c.classList.toggle('on',c===b)});
      var f=b.dataset.filter,all=b===g.firstElementChild;
      [].forEach.call(list.children,function(it){it.hidden=!all&&(it.dataset.cat||it.dataset.area)!==f})});
  });
  // Postulación: en la propuesta solo muestra el mensaje de enviado
  var af=document.getElementById('applyForm');
  af.addEventListener('submit',function(e){e.preventDefault();if(!af.checkValidity()){af.reportValidity();return}af.hidden=true;document.getElementById('applyOk').hidden=false});
  af.querySelector('.file input').addEventListener('change',function(){var s=this.nextElementSibling;if(this.files[0])s.textContent=this.files[0].name});

  // Cada página interna es una vista del mismo archivo, elegida por el #hash
  var prelim=document.querySelector('.prelim'),prelimTxt=document.getElementById('prelimTxt'),prelimDef=prelimTxt.textContent;
  var views=[].slice.call(document.querySelectorAll('.view'));
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(){
    // Las vistas usan id="v-…" para que el navegador no salte al #hash por su cuenta
    var id=(location.hash||'#nosotros').slice(1),v=document.getElementById('v-'+id);
    if(!v||!v.classList.contains('view'))return;
    views.forEach(function(x){x.hidden=x!==v});
    prelimTxt.textContent=v.dataset.note||prelimDef;prelim.classList.toggle('demo',!!v.dataset.note);
    document.title='Grupo Tecnobg · '+v.dataset.title;
    window.scrollTo(0,0);
    if(window.gsap&&!reduce){
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
{base_css}{tail_css}{page_css}</style>
</head>
<body>

{header}
<main>
<div class="prelim" role="note"><div class="wrap"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 3 2 21h20zM12 10v5M12 18v.5"/></svg><span id="prelimTxt">Diseño preliminar: esta página sigue pendiente de su diseño final.</span></div></div>
{views}
</main>

{footer}{script}
</body>
</html>
'''
open(R+'final-paginas.html','w').write(html)
print(len(html))

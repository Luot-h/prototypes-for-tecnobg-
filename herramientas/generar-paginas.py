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
V.append(('mantenimiento-preventivo','Mantenimiento preventivo',hero('Servicios','Mantenimiento preventivo','Un programa estructurado que prolonga la vida útil de tus equipos y optimiza su desempeño.','img/final/mantenimiento.webp','Técnico de Tecnobg da mantenimiento a un evaporador','60% 40%')+'''
  <div class="pg-body">
    <section class="blk"><h2>Áreas que atendemos</h2><ul class="ticks">
      <li><b>Línea fría</b>Mantenimiento a sistemas de refrigeración enfocado en eficiencia térmica y conservación de su materia prima.</li>
      <li><b>Aire acondicionado</b>Mantenimiento a instalaciones de aire acondicionado para asegurar confort, eficiencia energética y funcionamiento continuo.</li>
      <li><b>Línea caliente</b>Mantenimiento preventivo y reparación de equipos de línea caliente.</li></ul>
      <p class="links"><a class="more" href="final.html#linea-fria">Equipos de línea fría →</a><a class="more" href="final.html#linea-caliente">Equipos de línea caliente →</a></p></section>
    <section class="blk"><h2>Qué incluye</h2>'''+pend('Contenido pendiente: periodicidad, actividades por visita y reporte que se entrega.')+'''</section>
    '''+PROC+others('mantenimiento-preventivo')+'</div>'))
V.append(('reparacion','Reparación',hero('Servicios','Reparación','Corregimos la falla con precisión para que tu operación no se detenga y tus equipos recuperen su rendimiento óptimo.','img/soldadura-compresor.webp','Técnico de Tecnobg suelda la línea de un compresor','50% 60%')+'''
  <div class="pg-body">
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
V.append(('servicio-de-emergencia','Servicio de emergencia',hero('Servicios','Servicio de emergencia','Mantenimiento correctivo rápido y preciso para restablecer la operación en el menor tiempo posible.','img/tecnico-sombra.webp','Técnico de Tecnobg atiende una falla en un espacio técnico reducido','40% 40%')+'''
  <div class="pg-body">
    <section class="blk"><h2>Respuesta a urgencias</h2><p>Respuesta a urgencias en menos de 24 horas. Escríbenos por WhatsApp al 56 4603 7573, de lunes a sábado de 9:00 a 18:00.</p><a class="btn btn-blue" href="'''+WA+'''">Solicitar servicio de emergencia</a></section>
    '''+PROC+others('servicio-de-emergencia')+'</div>'))
V.append(('bolsa-de-trabajo','Bolsa de trabajo','''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Bolsa de trabajo</span><h1>Trabaja en Tecnobg</h1><p class="lead">Aquí publicaremos las vacantes de Tecnobg y la forma de postularte.</p></div></header>
  <div class="pg-body"><section class="blk"><h2>Vacantes disponibles</h2>'''+pend('Contenido pendiente: vacantes vigentes (puesto, zona, requisitos) y formulario para enviar tu solicitud.')+'''</section></div>'''))
V.append(('blog','Blog','''<header class="pg-hero solo"><div class="pg-copy"><span class="label">Blog</span><h1>Blog</h1><p class="lead">Pronto compartiremos aquí artículos sobre el mantenimiento y cuidado de equipos para el sector HORECA.</p></div></header>
  <div class="pg-body"><section class="blk"><h2>Artículos</h2>'''+pend('Contenido pendiente: primeros artículos y temas del blog.')+'''</section></div>'''))
V.append(('aviso-de-privacidad','Aviso de privacidad',legal('ap','Aviso de privacidad','Conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.',['Identidad y domicilio del responsable','Datos personales que recabamos','Finalidades del tratamiento','Transferencias de datos','Derechos ARCO y cómo ejercerlos','Cookies y tecnologías de rastreo','Cambios a este aviso'])))
V.append(('terminos-y-condiciones','Términos y condiciones',legal('tc','Términos y condiciones','Condiciones de uso de este sitio y de los servicios de Grupo Tecnobg.',['Objeto','Uso del sitio','Cotizaciones y autorización de servicios','Garantía','Propiedad intelectual','Legislación aplicable'])))
V.append(('uso-de-cookies','Uso de cookies',legal('ck','Uso de cookies','Cómo usa este sitio las cookies y tecnologías similares.',['¿Qué son las cookies?','Herramientas que usa el sitio','Cómo desactivarlas','Cambios a esta política'])))

views=''.join(f'\n<section class="view" id="v-{i}" data-title="{t}" hidden>\n  {body}\n</section>' for i,t,body in V)

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

  // Cada página interna es una vista del mismo archivo, elegida por el #hash
  var views=[].slice.call(document.querySelectorAll('.view'));
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(){
    // Las vistas usan id="v-…" para que el navegador no salte al #hash por su cuenta
    var id=(location.hash||'#nosotros').slice(1),v=document.getElementById('v-'+id);
    if(!v||!v.classList.contains('view'))return;
    views.forEach(function(x){x.hidden=x!==v});
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
<div class="prelim" role="note"><div class="wrap"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 3 2 21h20zM12 10v5M12 18v.5"/></svg><span>Diseño preliminar: esta página sigue pendiente de su diseño final.</span></div></div>
{views}
</main>

{footer}{script}
</body>
</html>
'''
open(R+'final-paginas.html','w').write(html)
print(len(html))

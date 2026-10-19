// Función de Vercel: recibe el formulario de cotización de final.html y lo envía por correo con Resend.
// Variables de entorno (Vercel › Settings › Environment Variables):
//   RESEND_API_KEY  clave de https://resend.com (obligatoria)
//   MAIL_FROM       remitente con dominio verificado en Resend, p. ej. "Sitio Tecnobg <sitio@tecnobg.com>"
//   MAIL_TO         destinatario; por defecto ventas@tecnobg.com

const FIELDS = { nombre: 120, empresa: 120, whatsapp: 20, email: 160, mensaje: 3000 };

const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Método no permitido.' });
  }

  const body = typeof req.body === 'string' ? safeJson(req.body) : req.body || {};
  // Campo trampa para bots: si viene lleno, se responde bien sin enviar nada
  if (body.sitio) return res.status(200).json({ ok: true });

  const data = {};
  for (const [k, max] of Object.entries(FIELDS)) {
    const v = typeof body[k] === 'string' ? body[k].trim() : '';
    if (!v || v.length > max) return res.status(400).json({ error: 'Todos los campos son obligatorios.' });
    data[k] = v;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return res.status(400).json({ error: 'Revisa el correo electrónico.' });
  if (!/^[0-9 +()\-]{10,20}$/.test(data.whatsapp)) return res.status(400).json({ error: 'Revisa el número de WhatsApp.' });

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    return res.status(503).json({ error: 'El formulario aún no está conectado al correo. Escríbenos por WhatsApp al 56 4603 7573.' });
  }

  const rows = [['Nombre', data.nombre], ['Empresa', data.empresa], ['WhatsApp', data.whatsapp], ['Correo', data.email]]
    .map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0;color:#56607d">${k}</td><td style="padding:4px 0"><b>${esc(v)}</b></td></tr>`)
    .join('');
  const html = `<h2 style="font-family:sans-serif;color:#152149">Nueva solicitud de cotización</h2>
<table style="font-family:sans-serif;font-size:15px">${rows}</table>
<p style="font-family:sans-serif;font-size:15px;white-space:pre-wrap">${esc(data.mensaje)}</p>`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.MAIL_FROM || 'Sitio Tecnobg <onboarding@resend.dev>',
        to: [process.env.MAIL_TO || 'ventas@tecnobg.com'],
        reply_to: data.email,
        subject: `Cotización: ${data.empresa} (${data.nombre})`,
        html,
      }),
    });
    if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error(e);
    return res.status(502).json({ error: 'No pudimos enviar tu solicitud. Escríbenos por WhatsApp al 56 4603 7573.' });
  }
};

function safeJson(s) {
  try { return JSON.parse(s); } catch { return {}; }
}

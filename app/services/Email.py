import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings


def _construir_html(venta_id: int, total: float, detalles: list[dict]) -> str:
    filas = ""
    for d in detalles:
        filas += f"""
        <tr>
            <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;">{d['producto']}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;text-align:center;">{d['cantidad']}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;text-align:right;">${d['precio_unitario']:.2f}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;text-align:right;">${d['subtotal']:.2f}</td>
        </tr>"""
    # ✅ BUG 1 CORREGIDO: return estaba DENTRO del for (indentación incorrecta),
    #    por eso sólo procesaba la primera fila y devolvía HTML incompleto.
    return f"""
    <html><body style="font-family:sans-serif;color:#111;background:#f9f9f9;padding:24px;">
      <div style="max-width:480px;margin:auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);">
        <div style="background:#111;color:#fff;padding:24px 28px;">
          <p style="margin:0;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#aaa;">Comprobante de compra</p>
          <p style="margin:4px 0 0;font-size:22px;font-weight:700;">Folio #{venta_id}</p>
        </div>
        <div style="padding:24px 28px;">
          <table style="width:100%;border-collapse:collapse;font-size:14px;">
            <thead>
              <tr style="color:#888;font-size:11px;text-transform:uppercase;letter-spacing:.05em;">
                <th style="padding:8px 12px;text-align:left;">Producto</th>
                <th style="padding:8px 12px;text-align:center;">Cant.</th>
                <th style="padding:8px 12px;text-align:right;">Precio</th>
                <th style="padding:8px 12px;text-align:right;">Subtotal</th>
              </tr>
            </thead>
            <tbody>{filas}</tbody>
          </table>
          <div style="margin-top:16px;padding-top:16px;border-top:2px solid #111;display:flex;justify-content:space-between;">
            <span style="font-size:16px;font-weight:600;">Total</span>
            <span style="font-size:20px;font-weight:700;">${total:.2f}</span>
          </div>
        </div>
        <div style="padding:16px 28px;background:#f9f9f9;font-size:12px;color:#999;text-align:center;">
          Gracias por su compra
        </div>
      </div>
    </body></html>
    """


def enviar_ticket_correo(
    destinatario: str,
    venta_id: int,
    total: float,
    detalles: list[dict],
) -> None:
    """
    Envía el ticket de compra por correo SMTP.
    Lanza excepción si falla — el router la convierte en HTTP 500.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Tu ticket de compra — Folio #{venta_id}"
    # ✅ BUG 2 CORREGIDO: se usaban settings.SMTP_FROM / SMTP_USER / SMTP_PASSWORD
    #    que no existen en config.py. Se usan los campos reales: email_user / email_password.
    msg["From"]    = settings.email_user
    msg["To"]      = destinatario

    html = _construir_html(venta_id, total, detalles)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.email_user, settings.email_password)
        server.sendmail(settings.email_user, destinatario, msg.as_string())
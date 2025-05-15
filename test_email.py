from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Carrega variáveis do .env
load_dotenv()

# Agora sim: lê as variáveis carregadas
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Debug opcional
print("EMAIL_FROM:", EMAIL_FROM)
print("EMAIL_PASS:", EMAIL_PASS)

# Resto do código igual
msg = MIMEMultipart()
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO
msg["Subject"] = "🎉 Teste de envio do VistoBot"
body = "Funcionando perfeitamente, Mikael! 🚀"
msg.attach(MIMEText(body, "plain"))

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    print("✅ E-mail enviado com sucesso!")

except Exception as e:
    print("❌ Erro ao enviar e-mail:", e)

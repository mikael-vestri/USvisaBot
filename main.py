import os
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Load environment variables
load_dotenv()
CSRA_USER = os.getenv("CSRA_USER")
CSRA_PASS = os.getenv("CSRA_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Set up Selenium with Chrome
options = Options()
options.add_argument("--headless=new")
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Logging
LOG_FILE = "vistobot.log"
def log_event(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} {message}\n")

def send_email(matching_dates):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = "📅 Novas datas disponíveis para visto!"

    body = "Foram encontradas as seguintes datas disponíveis antes de 2 de junho de 2025:\n\n"
    body += "\n".join(matching_dates)
    body += "\n\nEntre no site e reagende manualmente se quiser aproveitar."
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    log_event("📬 E-mail enviado!")

def main():
    log_event("🚀 Iniciando VistoBot...")
    try:
        driver.get("https://ais.usvisa-info.com/pt-br/niv/users/sign_in")
        time.sleep(2)

        driver.find_element(By.ID, "user_email").send_keys(CSRA_USER)
        driver.find_element(By.ID, "user_password").send_keys(CSRA_PASS)
        # Clique no checkbox visual (não no input real)
        checkbox = driver.find_element(By.CSS_SELECTOR, "div.icheckbox")
        checkbox.click()
        log_event("☑️ Checkbox 'Li e concordo' marcado com sucesso")

        driver.find_element(By.NAME, "commit").click()
        time.sleep(3)
        log_event("🔐 Login realizado com sucesso")

        driver.get("https://ais.usvisa-info.com/pt-br/niv/schedule/67082243/continue_actions")
        time.sleep(2)
        log_event("📆 Página de reagendamento acessada")

        calendar_days = driver.find_elements(By.CSS_SELECTOR, "td.ui-datepicker-day a")
        matching_dates = []

        for day_element in calendar_days:
            try:
                day = int(day_element.text.strip())
                # Vamos assumir que o mês e ano estão visíveis em algum lugar fixo da página
                month_year_text = driver.find_element(By.CLASS_NAME, "ui-datepicker-title").text  # Ex: 'Maio 2025'
                date_str = f"{day} {month_year_text}"
                date_obj = datetime.strptime(date_str, "%d %B %Y")
                if date_obj < datetime(2025, 6, 2):
                    matching_dates.append(date_obj.strftime("%d/%m/%Y"))
            except Exception as e:
                continue

        if matching_dates:
            log_event(f"✅ Datas encontradas: {', '.join(matching_dates)}")
            send_email(matching_dates)
        else:
            log_event("🔍 Nenhuma data interessante disponível.")

    except Exception as e:
        log_event(f"❌ Erro no bot: {e}")
    finally:
        driver.quit()
        log_event("🏁 Execução finalizada")

if __name__ == "__main__":
    main()

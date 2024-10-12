import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException
from core.config import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


def send_email_verification_code(email: str, code: int):
    sender = EMAIL_HOST_USER  # Убедитесь, что вы установили эту переменную окружения
    recipient = email
    subject = "Ваш код подтверждения"
    body = f"Ваш код подтверждения: {code}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        # Настройка SMTP-сервера для Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Начинаем шифрование
            server.login(sender, EMAIL_HOST_PASSWORD)  # Убедитесь, что вы установили эту переменную окружения
            server.sendmail(sender, recipient, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки кода на почту: {e}")

import resend
from src.core.config import env_settings
# Настройки
resend.api_key = env_settings.RESEND_API_KEY
FROM_EMAIL = env_settings.MAILER_SENDER_FROM_ADDRESS

class EmailSendler:
    def send_email(to_email: str, subject: str, html_content: str, text_content: str = None):
        """
        Отправляет email через Resend.
        :param to_email: Получатель
        :param subject: Тема письма
        :param html_content: HTML-содержимое
        :param text_content: Текстовая версия (опционально)
        """
        try:
            params = {
                "from": FROM_EMAIL,
                "to": to_email,
                "subject": subject,
                "html": html_content,
            }

            if text_content:
                params["text"] = text_content

            email = resend.Emails.send(params)
            print("Письмо успешно отправлено:", email)
            return email

        except Exception as e:
            print("Ошибка при отправке письма:", e)
            return None


    # === Пример использования ===
    if __name__ == "__main__":
        send_email(
            to_email="chatplatformmailer@gmail.com",
            subject="Привет от моего проекта!",
            html_content="""
                <h1>Добро пожаловать!</h1>
                <p>Спасибо за регистрацию в нашем сервисе.</p>
                <a href="https://yourdomain.com ">Перейти на сайт</a>
            """,
            text_content="Добро пожаловать! Спасибо за регистрацию в нашем сервисе."
    )
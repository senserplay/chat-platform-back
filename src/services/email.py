import resend
from loguru import logger

from src.core.config import env_settings

# Настройки
resend.api_key = env_settings.RESEND_API_KEY
FROM_EMAIL = env_settings.MAILER_SENDER_FROM_ADDRESS


class EmailSender:
    @staticmethod
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
            logger.info(f"Письмо успешно отправлено: {email}")
            return email

        except Exception as e:
            logger.error(f"Ошибка при отправке письма: {e}")
            return None

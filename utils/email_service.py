import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import get_logger

logger = get_logger('email_service')


class EmailService:
    def __init__(self):
        # Налаштування SMTP
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_sender = "tihayanastia7@gmail.com"
        self.email_password = "wjpo kddo kcfv oniw"  # App Password для Gmail
        self.sender_name = "Щоденник вагітності"

        self.sent_codes = {}

    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))

    def send_verification_code(self, email):
        code = self.generate_verification_code()
        self.sent_codes[email] = code

        try:
            self._send_email(
                to_email=email,
                subject="Код підтвердження - Щоденник вагітності",
                html_body=self._get_verification_email_template(code)
            )
            logger.info(f"Код підтвердження надіслано на {email}: {code}")
            return code
        except Exception as e:
            logger.error(f"Помилка відправки email на {email}: {str(e)}")
            # Зберігаємо код для тестування навіть якщо email не відправився
            print(f"[EMAIL DEBUG] Код підтвердження для {email}: {code}")
            return code

    def verify_code(self, email, code):
        stored_code = self.sent_codes.get(email)
        if stored_code and stored_code == code:
            del self.sent_codes[email]
            return True
        return False

    def _send_email(self, to_email, subject, html_body):
        """Відправляє email через SMTP"""
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{self.sender_name} <{self.email_sender}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        # Додаємо HTML-версію повідомлення
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        # Відправляємо email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(msg)

    def _get_verification_email_template(self, code):
        """Шаблон email для підтвердження"""
        return f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">

              <!-- Заголовок -->
              <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #FF8C00;">
                <h1 style="color: #FF8C00; margin: 0;">Щоденник вагітності</h1>
                <p style="color: #666; margin: 5px 0;">Ваш персональний помічник під час вагітності</p>
              </div>

              <!-- Основний контент -->
              <div style="padding: 30px 0;">
                <h2 style="color: #333; margin-bottom: 20px;">Підтвердження email адреси</h2>

                <p>Привіт!</p>
                <p>Дякуємо за реєстрацію в додатку "Щоденник вагітності". Для завершення реєстрації введіть код підтвердження:</p>

                <!-- Код підтвердження -->
                <div style="text-align: center; margin: 30px 0;">
                  <div style="background-color: #f8f9fa; border: 2px dashed #FF8C00; border-radius: 10px; padding: 20px; display: inline-block;">
                    <span style="font-size: 32px; font-weight: bold; color: #FF8C00; letter-spacing: 5px;">{code}</span>
                  </div>
                </div>

                <p>Цей код дійсний протягом 10 хвилин. Якщо ви не реєструвалися в нашому додатку, просто проігноруйте цей лист.</p>

                <div style="background-color: #e8f4fd; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0;">
                  <p style="margin: 0; color: #1976D2;">
                    <strong>Про додаток:</strong><br>
                    Щоденник вагітності допоможе вам відстежувати розвиток дитини, зберігати важливі записи про здоров'я та отримувати корисні поради на кожному етапі вагітності.
                  </p>
                </div>
              </div>

              <!-- Футер -->
              <div style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>З повагою,<br>Команда "Щоденник вагітності"</p>
                <p style="margin-top: 15px;">
                  Це автоматичне повідомлення. Будь ласка, не відповідайте на цей email.
                </p>
              </div>

            </div>
          </body>
        </html>
        """

    def send_welcome_email(self, email, user_name):
        """Вітальний email після успішної реєстрації"""
        try:
            self._send_email(
                to_email=email,
                subject="Ласкаво просимо в Щоденник вагітності! 🤱",
                html_body=self._get_welcome_email_template(user_name)
            )
            logger.info(f"Вітальний email надіслано на {email}")
        except Exception as e:
            logger.error(f"Помилка відправки вітального email на {email}: {str(e)}")

    def _get_welcome_email_template(self, user_name):
        """Шаблон вітального email"""
        return f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">

              <!-- Заголовок -->
              <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #FF8C00;">
                <h1 style="color: #FF8C00; margin: 0;">🤱 Щоденник вагітності</h1>
                <p style="color: #666; margin: 5px 0;">Ваш персональний помічник під час вагітності</p>
              </div>

              <!-- Основний контент -->
              <div style="padding: 30px 0;">
                <h2 style="color: #333; margin-bottom: 20px;">Ласкаво просимо, {user_name}! 🎉</h2>

                <p>Вітаємо з успішною реєстрацією в додатку "Щоденник вагітності"!</p>

                <p>Ваша подорож материнства тепер буде ще більш організованою та інформативною. Ось що вас чекає:</p>

                <!-- Функції додатку -->
                <div style="background-color: #f8f9fa; border-radius: 10px; padding: 20px; margin: 25px 0;">
                  <h3 style="color: #FF8C00; margin-top: 0;">🌟 Можливості додатку:</h3>
                  <ul style="padding-left: 20px;">
                    <li><strong>Календар вагітності</strong> - відстежуйте тижні розвитку дитини</li>
                    <li><strong>Щоденник здоров'я</strong> - записуйте важливу медичну інформацію</li>
                    <li><strong>Нагадування</strong> - не пропустіть важливі візити та процедури</li>
                    <li><strong>Список бажань</strong> - плануйте покупки для малюка</li>
                    <li><strong>Інструменти моніторингу</strong> - контролюйте вагу, тиск та активність дитини</li>
                  </ul>
                </div>

                <div style="text-align: center; margin: 30px 0;">
                  <p style="font-size: 18px; color: #FF8C00;">
                    <strong>Бажаємо вам щасливої та здорової вагітності! 💕</strong>
                  </p>
                </div>

                <div style="background-color: #e8f4fd; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0;">
                  <p style="margin: 0; color: #1976D2;">
                    <strong>💡 Порада:</strong> Почніть з заповнення базової інформації про себе та вагітність у налаштуваннях додатку.
                  </p>
                </div>
              </div>

              <!-- Футер -->
              <div style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>З повагою та найкращими побажаннями,<br>Команда "Щоденник вагітності"</p>
                <p style="margin-top: 15px;">
                  Це автоматичне повідомлення. Будь ласка, не відповідайте на цей email.
                </p>
              </div>

            </div>
          </body>
        </html>
        """

    def send_reminder_email(self, email, user_name, reminder_title, reminder_description):
        """Відправка email нагадування"""
        try:
            self._send_email(
                to_email=email,
                subject=f"Нагадування: {reminder_title}",
                html_body=self._get_reminder_email_template(user_name, reminder_title, reminder_description)
            )
            logger.info(f"Email нагадування надіслано на {email}")
        except Exception as e:
            logger.error(f"Помилка відправки email нагадування на {email}: {str(e)}")

    def _get_reminder_email_template(self, user_name, title, description):
        """Шаблон email нагадування"""
        return f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">

              <!-- Заголовок -->
              <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #FF8C00;">
                <h1 style="color: #FF8C00; margin: 0;">⏰ Нагадування</h1>
                <p style="color: #666; margin: 5px 0;">Щоденник вагітності</p>
              </div>

              <!-- Основний контент -->
              <div style="padding: 30px 0;">
                <h2 style="color: #333; margin-bottom: 20px;">Привіт, {user_name}!</h2>

                <p>У вас є важливе нагадування:</p>

                <!-- Нагадування -->
                <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin: 25px 0;">
                  <h3 style="color: #856404; margin-top: 0;">📋 {title}</h3>
                  <p style="margin-bottom: 0; color: #856404;">{description}</p>
                </div>

                <p>Не забудьте виконати заплановану активність. Ваше здоров'я та здоров'я малюка - найважливіше!</p>
              </div>

              <!-- Футер -->
              <div style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>З турботою,<br>Команда "Щоденник вагітності"</p>
                <p style="margin-top: 15px;">
                  Це автоматичне повідомлення. Будь ласка, не відповідайте на цей email.
                </p>
              </div>

            </div>
          </body>
        </html>
        """
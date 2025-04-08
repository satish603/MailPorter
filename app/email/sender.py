# app/email/sender.py
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from app.config import SMTPConfig

# Configure logging.
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class AbstractEmailSender:
    def send_email(self, recipient: str, subject: str, context: dict):
        raise NotImplementedError("Subclasses must implement send_email method.")

class SMTPSender(AbstractEmailSender):
    def __init__(self, config: SMTPConfig):
        self.config = config
        # Set up Jinja2 to load templates from the "app/email" directory
        self.template_env = Environment(loader=FileSystemLoader(searchpath="./app/email"))
        self.template = self.template_env.get_template(config.template)

    def send_email(self, recipient: str, subject: str, context: dict):
        html_content = self.template.render(**context)
        message = MIMEMultipart("alternative")
        message["Subject"] = subject

        # If using Hostinger with brand legalvala, hardcode the From address:
        if self.config.host == "smtp.hostinger.com" and self.config.template == "legalvala_template.html":
            message["From"] = "info@legalvala.com"
        else:
            message["From"] = self.config.username

        message["To"] = recipient

        bcc = self.config.bcc_list if self.config.bcc_list else []
        all_recipients = [recipient] + bcc

        message.attach(MIMEText(html_content, "html"))  # Use "plain" or "html" as needed

        try:
            logging.debug("Connecting to SMTP server %s:%s", self.config.host, self.config.port)
            server = smtplib.SMTP(self.config.host, self.config.port)
            server.set_debuglevel(1)  # SMTP internal debug output

            logging.debug("Starting TLS...")
            if self.config.starttls:
                server.starttls()

            logging.debug("Logging in as: %s", self.config.username)
            if self.config.auth:
                server.login(self.config.username, self.config.password)

            logging.debug("Sending email to: %s; BCC: %s", recipient, self.config.bcc_list)
            server.sendmail(self.config.username, all_recipients, message.as_string())
            server.quit()

            logging.info("Email sent successfully to %s", recipient)
            return {"status": "success", "message": "Email sent successfully."}
        except Exception as e:
            logging.error("Error sending email: %s", str(e))
            return {"status": "error", "message": str(e)}

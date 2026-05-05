from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import logger
from utils.new_password import generate_password
from fastapi import HTTPException, status
import routes.auth.models as auth_models
from utils.bcrypt import hash_password


def send_email_pw_recovery(host_address, host_port, email_address, email_username, email_password, user_email, new_password):

    try:

        # inicializar servidor
        server = SMTP(host=host_address, port=host_port)

        # encriptar conexion
        server.starttls()

        server.login(user=email_username, password=email_password)

        message = MIMEMultipart('alternative')

        message['From'] = email_address
        message['To'] = user_email
        message['Subject'] = 'Recuperacion de contraseña'

        html = MIMEText(f'<h1>Nueva contraseña: {new_password} </h1>', 'html')

        message.attach(html)

        server.send_message(message)
        server.quit()

        return {
            'message':'New password sent to your email'
        }

    except Exception as e:

        logger.debug(msg=str(e))
        return None

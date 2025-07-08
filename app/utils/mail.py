from flask_mail import Mail, Message
from app import create_app

app = create_app()
mail = Mail(app)

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = f"Hello,\n\n{template} template with {kwargs}"
    msg.html = f"""
    <html>
    <body>
        <h3>Hello!</h3>
        <p>{template} template with {kwargs}</p>
    </body>
    </html>
    """
    mail.send(msg)
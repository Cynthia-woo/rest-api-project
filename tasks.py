import os
import requests
import jinja2
from dotenv import load_dotenv

load_dotenv() # background worker will import tasks.py once at the start of its lifetime, run load_dotenv() before it is requested.

DOMAIN = os.getenv("MAILGUN_DOMAIN")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_filename, **context):
    return template_env.get_template(loader=template_loader)

def send_simple_message(to, subject, body, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Your Name <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html
        },
    )

# use string is easier than use user model
def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores REST API.",
        render_template("email/action.html", username=username)
    )
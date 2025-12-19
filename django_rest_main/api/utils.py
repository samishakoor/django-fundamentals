from django.conf import settings
from mailjet_rest import Client as mailjet_client


def send_email(to_email, subject, html_content=None, plain_content=None):
    """
    Send email using Mailjet API.
    """
    try:
        MAILJET_API_KEY = getattr(settings, "MAILJET_API_KEY", "")
        MAILJET_API_SECRET = getattr(settings, "MAILJET_API_SECRET", "")
        MAILJET_SENDER_EMAIL = getattr(settings, "MAILJET_SENDER_EMAIL", "")
        MAILJET_FROM_SENDER_NAME = getattr(settings, "MAILJET_FROM_SENDER_NAME", "")

        if (
            not MAILJET_API_KEY
            or not MAILJET_API_SECRET
            or not MAILJET_SENDER_EMAIL
            or not MAILJET_FROM_SENDER_NAME
        ):
            raise Exception(
                "Missing mailjet API key or mailjet email or mailjet secret key in the .env file."
            )

        # Normalize recipient format
        if isinstance(to_email, str):
            to_list = [{"Email": to_email}]
        elif isinstance(to_email, list):
            to_list = [{"Email": email} for email in to_email if isinstance(email, str)]
        else:
            raise ValueError("to_email must be a string or list of strings")

        # Ensure at least one content type is provided
        if not html_content and not plain_content:
            raise ValueError(
                "At least one of html_content or plain_content must be provided."
            )

        # Fallbacks
        html_content = html_content or plain_content or "No content provided."
        plain_content = plain_content or html_content or "No content provided."

        mailjet = mailjet_client(
            auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version="v3.1"
        )

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": MAILJET_SENDER_EMAIL,
                        "Name": MAILJET_FROM_SENDER_NAME,
                    },
                    "To": to_list,
                    "Subject": subject,
                    "TextPart": plain_content,
                    "HTMLPart": html_content,
                }
            ]
        }

        response = mailjet.send.create(data=data)

        if response.status_code == 200:
            print(f"Email sent successfully to: {[r['Email'] for r in to_list]}")
        else:
            print(
                f"Failed to send email. Status Code: {response.status_code}, Response: {response.json()}"
            )

    except Exception as e:
        print(f"Error sending email: {e}")

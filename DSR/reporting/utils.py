from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from DSR.constants import ERROR_MSG
from DSR.utils import logger
from .models import OutgoingEmail, OutgoingEmailAttachment


class EmailManager:

    def __init__(self) -> None:
        pass

    def save_outgoing_mail(self, data) -> tuple:
        """
        Save outgoing emails in the database.

        Args:
            data (dict): A dictionary containing the email data.

        Returns:
            tuple: A boolean indicating the success of the operation and the
            created `OutgoingEmail` instance.
        """
        try:
            attachments, outgoing_email_data = self.get_outgoing_data(data)
            outgoing_email = OutgoingEmail(**outgoing_email_data)
            logger.info(f"Outgoing email saved successfully.")

            is_success, msg = self.save_attachment(attachments, outgoing_email)
            if not is_success:
                return False, msg

            return True, outgoing_email
        except Exception as e:
            logger.error(
                f"EmailManager | Error in save_outgoing_mail : {e}",
                exc_info=True,
            )
            return False, None

    def save_attachment(self, attachments, outgoing_email) -> tuple:
        try:
            for filename, file_content in attachments:
                attachment_data = {
                    "outgoing_email": outgoing_email,
                    "filename": filename,
                    "file": file_content,
                }
                _ = OutgoingEmailAttachment(**attachment_data)
            return True, "Outgoing attachments saved successfully."
        except Exception as e:
            logger.error(
                f"EmailManager | Error in save_attachment : {e}", exc_info=True
            )
            return False, ERROR_MSG

    def get_outgoing_data(self, data) -> tuple:
        """
        Extracts and organizes the necessary data from the input dictionary to
        create an OutgoingEmail instance.

        Args:
            data (dict): A dictionary containing the email data.

        Returns:
            tuple: A tuple containing the attachments list and the
            outgoing_email_data dictionary.
        """
        try:
            content = data.get("content")
            to_emails = data.get("to_emails")
            cc_emails = data.get("cc_emails")
            bcc_emails = data.get("bcc_emails")
            subject = data.get("subject")
            user_id = data.get("user_id")
            attachments = data.get("attachments", [])
            from_email = data.get("from_email")

            outgoing_email_data = {
                "from_email": from_email,
                "to_emails": to_emails,
                "cc_emails": cc_emails,
                "bcc_emails": bcc_emails,
                "subject": subject,
                "content": content,
                "status": "pending",
                "created_by": user_id,
            }
            return attachments, outgoing_email_data
        except Exception as e:
            logger.error(
                f"EmailManager | Error in get_outgoing_data : {e}",
                exc_info=True,
            )
            return None, None

    def send_mail(self, outgoing_email) -> tuple:
        """
        Sends an email using the Django EmailMessage class and updates the
        status of the outgoing email.

        Args:
            outgoing_email (OutgoingEmail): An instance of the OutgoingEmail
            model representing the email to be sent.

        Returns:
            Tuple: A tuple containing a boolean value indicating the success of
            the email sending operation (True if successful, False otherwise)
            and a string message describing the result of the operation.
        """
        try:
            email = EmailMessage(
                subject=outgoing_email.subject,
                body=outgoing_email.content,
                from_email=outgoing_email.from_email,
                to=outgoing_email.to_emails,
                cc=outgoing_email.cc_emails,
                bcc=outgoing_email.bcc_emails,
            )

            for attachment in outgoing_email.attachments:
                email.attach_file(attachment)

            email.send()
            outgoing_email.status = "success"
            outgoing_email.save()
            logger.info("Email sent successfully.")
            return True, "Email sent successfully."
        except Exception as e:
            logger.error(
                "EmailManager | Error in send_mail: {}".format(e),
                exc_info=True,
            )
            outgoing_email.status = "failed"
            outgoing_email.save()
            return False, ERROR_MSG

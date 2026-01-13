"""Email Services - Sending and receiving emails"""
import os
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime
import re


class EmailService:
    """Service for sending and receiving RFP-related emails"""

    def __init__(self):
        """Initialize email configuration"""
        self.smtp_server = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('EMAIL_PORT', '587'))
        self.imap_server = os.getenv('IMAP_SERVER', 'imap.gmail.com')
        self.imap_port = int(os.getenv('IMAP_PORT', '993'))
        self.email_address = os.getenv('EMAIL_HOST_USER', '')
        self.email_password = os.getenv('EMAIL_HOST_PASSWORD', '')
        self.from_email = os.getenv('DEFAULT_FROM_EMAIL', self.email_address)

    def send_rfp_to_vendor(self, rfp, vendor_id: str) -> bool:
        """
        Send RFP to a vendor via email.
        
        Args:
            rfp: RFP object
            vendor_id: ID of the vendor
            
        Returns:
            bool: Whether email was sent successfully
        """
        from rfp_management.apps.vendors.models import Vendor
        from rfp_management.apps.ai.services import AIService

        try:
            # Get vendor details
            vendor = Vendor.objects.get(id=vendor_id)
            
            # Generate RFP email body
            ai_service = AIService()
            email_body = ai_service.generate_rfp_email_body(rfp.title, rfp.requirements)
            
            # Create email
            subject = f"Request for Proposal: {rfp.title}"
            message = MIMEMultipart()
            message['From'] = self.from_email
            message['To'] = vendor.email
            message['Subject'] = subject
            
            message.attach(MIMEText(email_body, 'plain'))
            
            # Send email
            self._send_email(vendor.email, subject, email_body)
            
            return True

        except Exception as e:
            print(f"Error sending RFP to vendor {vendor_id}: {str(e)}")
            raise

    def _send_email(self, recipient: str, subject: str, body: str) -> None:
        """
        Send email using SMTP.
        
        Args:
            recipient: Email address of recipient
            subject: Email subject
            body: Email body content
        """
        try:
            # Create message
            message = f"Subject: {subject}\n\n{body}"
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.sendmail(self.from_email, recipient, message)
                
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

    def receive_proposal_emails(self) -> list:
        """
        Check for incoming proposal emails from vendors.
        
        Returns:
            list: List of tuples (sender_email, subject, body, message_id)
        """
        proposals = []

        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            mail.select('INBOX')

            # Search for unseen emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status == 'OK':
                message_ids = messages[0].split()
                
                for message_id in message_ids:
                    status, msg_data = mail.fetch(message_id, '(RFC822)')
                    
                    if status == 'OK':
                        msg = self._parse_email(msg_data[0][1])
                        proposals.append({
                            'sender': msg['from'],
                            'subject': msg['subject'],
                            'body': msg['body'],
                            'message_id': message_id.decode(),
                            'received_date': msg.get('date', datetime.now().isoformat())
                        })

            mail.close()
            mail.logout()
            
            return proposals

        except Exception as e:
            print(f"Error receiving proposal emails: {str(e)}")
            return []

    def _parse_email(self, email_data):
        """
        Parse email message data.
        
        Args:
            email_data: Raw email data from IMAP
            
        Returns:
            dict: Parsed email with from, subject, body
        """
        import email
        from email.header import decode_header, make_header

        msg = email.message_from_bytes(email_data)
        
        # Decode subject
        subject_header = msg.get('Subject', '')
        if isinstance(subject_header, email.header.Header):
            subject = str(subject_header)
        else:
            subject = subject_header

        # Get sender
        from_header = msg.get('From', '')
        sender = from_header

        # Get body
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')

        return {
            'from': sender,
            'subject': subject,
            'body': body,
            'date': msg.get('Date', datetime.now().isoformat())
        }

    def extract_vendor_email(self, email_address: str) -> str:
        """
        Extract clean email address from From header.
        
        Args:
            email_address: From header (may contain name)
            
        Returns:
            str: Clean email address
        """
        # Extract email from "Name <email@domain.com>" format
        match = re.search(r'<(.+?)>', email_address)
        if match:
            return match.group(1)
        return email_address.strip()

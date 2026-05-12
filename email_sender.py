#!/usr/bin/env python3
"""
Email Sender Module - Send encrypted files via email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


class EmailSender:
    """Send encrypted files via email"""
    
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_file_link(self, recipient_email, file_name, share_url, sender_email, sender_password, message=''):
        """
        Send share link via email
        
        Args:
            recipient_email: Recipient's email address
            file_name: Name of the shared file
            share_url: Share link URL
            sender_email: Sender's email (Gmail)
            sender_password: Sender's app password
            message: Optional message
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f'🔐 ملف مشفر: {file_name}'
            
            # HTML body
            html_body = f"""
            <!DOCTYPE html>
            <html dir="rtl" lang="ar">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: #f5f5f5;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        overflow: hidden;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #6c63ff, #00d4aa);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 24px;
                    }}
                    .content {{
                        padding: 30px;
                    }}
                    .file-info {{
                        background: #f8f9fa;
                        border-radius: 10px;
                        padding: 20px;
                        margin: 20px 0;
                    }}
                    .file-name {{
                        font-size: 18px;
                        font-weight: 600;
                        color: #333;
                        margin-bottom: 10px;
                    }}
                    .message {{
                        color: #666;
                        line-height: 1.6;
                        margin: 20px 0;
                    }}
                    .btn {{
                        display: inline-block;
                        background: linear-gradient(135deg, #6c63ff, #00d4aa);
                        color: white;
                        padding: 15px 40px;
                        text-decoration: none;
                        border-radius: 10px;
                        font-weight: 600;
                        margin: 20px 0;
                    }}
                    .footer {{
                        background: #f8f9fa;
                        padding: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                    }}
                    .warning {{
                        background: #fff3cd;
                        border: 1px solid #ffc107;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 20px 0;
                        color: #856404;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Secure File Vault Pro</h1>
                        <p>تم مشاركة ملف مشفر معك</p>
                    </div>
                    
                    <div class="content">
                        <div class="file-info">
                            <div class="file-name">📁 {file_name}</div>
                            <p style="color: #666; margin: 0;">ملف مشفر بأمان عالي</p>
                        </div>
                        
                        {f'<div class="message"><strong>رسالة:</strong><br>{message}</div>' if message else ''}
                        
                        <div style="text-align: center;">
                            <a href="{share_url}" class="btn">
                                🔓 تحميل الملف المشفر
                            </a>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ ملاحظة مهمة:</strong><br>
                            • الملف مشفر بأمان عالي<br>
                            • ستحتاج كلمة المرور الأصلية لفك التشفير<br>
                            • الرابط له مدة صلاحية محددة<br>
                            • لا تشارك كلمة المرور عبر نفس القناة
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>هذا البريد تم إرساله من Secure File Vault Pro</p>
                        <p>نظام تشفير ملفات آمن ومتقدم</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            return True, "تم إرسال البريد الإلكتروني بنجاح"
            
        except Exception as e:
            return False, f"فشل إرسال البريد: {str(e)}"
    
    def send_encrypted_file(self, recipient_email, file_path, file_name, sender_email, sender_password, message=''):
        """
        Send encrypted file as attachment
        
        Args:
            recipient_email: Recipient's email
            file_path: Path to encrypted file
            file_name: Original file name
            sender_email: Sender's email
            sender_password: Sender's app password
            message: Optional message
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f'🔐 ملف مشفر: {file_name}'
            
            # Body
            body = f"""
            مرحباً،
            
            تم إرسال ملف مشفر إليك: {file_name}
            
            {message if message else ''}
            
            ⚠️ ملاحظات مهمة:
            • الملف مشفر بأمان عالي
            • ستحتاج كلمة المرور لفك التشفير
            • احتفظ بكلمة المرور في مكان آمن
            
            --
            Secure File Vault Pro
            نظام تشفير ملفات آمن
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Attach file
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{file_name}.encrypted"')
                msg.attach(part)
            
            # Send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            return True, "تم إرسال الملف بنجاح"
            
        except Exception as e:
            return False, f"فشل إرسال الملف: {str(e)}"


# Test function
if __name__ == "__main__":
    sender = EmailSender()
    print("📧 Email Sender Module Ready!")
    print("\nللاستخدام:")
    print("1. استخدم Gmail App Password")
    print("2. فعّل 2FA في حساب Gmail")
    print("3. أنشئ App Password من: https://myaccount.google.com/apppasswords")

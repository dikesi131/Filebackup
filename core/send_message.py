import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from email.header import Header
from pathlib import Path
import sys
from .global_vars import get_var


class SendEmail:
    def __init__(self) -> None:
        self.email_conf = get_var('config')['email']

        # code为QQ邮箱开启SMTP服务后的授权码
        self.qq_sender_conf = {'email': get_var('config')['email'],
                               'code': get_var('config')['PassCode'],
                               'port': get_var('config')['port']}
        # from-->发件人
        # to-->收件人
        # subject:主题
        self.qq_email_content = {'from': get_var('config')['email'],
                                 'to': get_var('config')['SendTo'],
                                 'subject': 'FileBackup Status'}

    def send_qq_mail(self,
                     message=f'{Path(sys.argv[0]).name}运行完毕,文件已备份完成') -> None:
        '''
        send qq email
        param message: email content
        '''
        sender_conf = self.qq_sender_conf
        email_content = self.qq_email_content
        # 电子邮件内容设置
        msg = MIMEMultipart()
        msg['From'] = email_content['from']
        msg['To'] = email_content['to']
        msg['Subject'] = email_content['subject']

        # 添加正文
        msg.attach(MIMEText(message, 'plain'))

        # 创建 SMTP 客户端
        try:
            # 链接邮箱服务器，SMTP默认端口为25
            with smtplib.SMTP('smtp.qq.com', self.qq_sender_conf['port']) as s:
                s.starttls()
                s.login(sender_conf['email'], sender_conf['code'])
                s.send_message(msg)
            get_var('g_logger').info("[+] 邮件发送成功")
        except Exception as e:
            get_var('g_logger').error(f"[-] 邮件发送失败: {e}")

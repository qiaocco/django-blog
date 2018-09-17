from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal, receiver

comment_save_signal = Signal(providing_args=['id'])


@receiver(signal=comment_save_signal)
def comment_save_callback(sender, **kwargs):
    # TODO 使用celery发送邮件
    send_mail(
        subject='有人评论啦',
        message=f'有人评论啦:人：{kwargs.get("nickname")}, 内容:{kwargs.get("content")}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[kwargs.get('email')],
        fail_silently=False,
    )

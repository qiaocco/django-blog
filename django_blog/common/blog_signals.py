from django.dispatch import Signal, receiver

from taskapp.celery import send_mail

comment_save_signal = Signal(providing_args=['id'])


@receiver(signal=comment_save_signal)
def comment_save_callback(sender, **kwargs):
    # TODO 使用celery发送邮件
    send_mail.delay(
        subject='有人评论啦',
        body='有人评论啦！用户：{nickname}, 内容:{content}'.format(
            nickname=kwargs.get("nickname"),
            content=kwargs.get("content")),
        to=[kwargs.get('email')],
    )

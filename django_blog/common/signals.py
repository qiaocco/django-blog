import logging

from django.dispatch import Signal, receiver

from taskapp.tasks import send_mail

from .spider_notify import SpiderNotify

logger = logging.getLogger("django")

post_save_signal = Signal(providing_args=["id"])
comment_save_signal = Signal(providing_args=["id"])


@receiver(post_save_signal)
def post_save_callback(sender, **kwargs):
    from blog.models import Post

    id = kwargs.get("id")
    obj = Post.objects.filter(pk=id).first()
    if obj:
        try:
            notify_url = obj.get_full_url()
            SpiderNotify.notify_baidu(notify_url)
            # SpiderNotify.notify_google()
        except Exception as e:
            logger.error("spider notify", e)


@receiver(signal=comment_save_signal)
def comment_save_callback(sender, **kwargs):
    logger.debug(f"comment_save_callback, from:{sender}, kwargs:{kwargs}")
    send_mail.delay(
        subject="你有新评论啦",
        body=f"用户：{kwargs.get('nickname')}, 评论:{kwargs.get('content')}",
        to=[kwargs.get("email")],
    )

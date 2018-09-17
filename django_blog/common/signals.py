import logging

from django.dispatch import Signal, receiver

from .spider_notify import SpiderNotify

logger = logging.getLogger(__name__)

post_save_signal = Signal(providing_args=['id'])


@receiver(post_save_signal)
def post_save_callback(sender, **kwargs):
    from blog.models import Post

    id = kwargs.get('id')
    obj = Post.objects.filter(pk=id).first()
    if obj:
        try:
            notify_url = obj.get_full_url()
            SpiderNotify.notify_baidu(notify_url)
            # SpiderNotify.notify_google()
        except Exception as e:
            logger.error('spider notify', e)

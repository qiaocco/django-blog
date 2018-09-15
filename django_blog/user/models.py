from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    自定义用户
    替换系统默认用户，没有对做任何修改（备用）。
    """

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

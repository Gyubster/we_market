from django.db                  import models
from django.utils.translation   import ugettext_lazy as _

class Post(models.Model):
    user = models.ForeignKey(
            'user.User',
            related_name = 'users',
            on_delete = models.CASCADE,
            )
    subcategory = models.ForeignKey(
            'Subcategory',
            on_delete = models.CASCADE,
            )
    status = models.ForeignKey(
            'Status',
            on_delete = models.CASCADE,
            )
    title = models.CharField(
            verbose_name    = _('title'),
            max_length      = 64,
            )
    product = models.CharField(
            verbose_name    = _('product name'),
            max_length      = 64,
            null            = True,
            blank           = True,
            )
    introduction = models.CharField(
            verbose_name    = _('introduction'),
            max_length      = 2000,
            )
    price = models.DecimalField(
            verbose_name    = _('price'),
            max_digits      = 10,
            decimal_places  = 2,
            )
    like_count = models.IntegerField(
            verbose_name    = _('like count'),
            default         = 0,
            )
    view_count = models.IntegerField(
            verbose_name    = _('view count'),
            default         = 0,
            )
    chat_count  = models.IntegerField(
            verbose_name    = _('chat count'),
            default         = 0,
            )
    possible_discount = models.BooleanField(
            verbose_name    = _('is discount'),
            default         = False,
            )
    address = models.CharField(
            verbose_name    = _('address'),
            max_length      = 64,
            )
    created_at = models.DateTimeField(
            verbose_name    = _('created at'),
            auto_now_add    = True,
            )
    updated_at = models.DateTimeField(
            verbose_name    = _('updated_at'),
            auto_now        = True,
            )

    class Meta:
        db_table = 'posts'

    @property
    def first_image(self):
        return self.images.first()

class Subcategory(models.Model):
    category = models.ForeignKey(
            'Category',
            on_delete   = models.CASCADE,
            )
    name = models.CharField(
            verbose_name    = _('name'),
            max_length      = 64,
            )

    class Meta:
        db_table = 'subcategories'

class Category(models.Model):
    name = models.CharField(
            verbose_name    = _('name'),
            max_length      = 64,
            )

    class Meta:
        db_table = 'categories'

class Status(models.Model):
    name = models.CharField(
            verbose_name    = _('name'),
            max_length      = 64,
            )

    class Meta:
        db_table = 'statuses'

class Image(models.Model):
    post = models.ForeignKey(
            'Post',
            related_name='images',
            on_delete=models.CASCADE,
            )
    url = models.URLField(
            verbose_name    = _('url'),
            max_length      = 2000,
            null            = True,
            )

    class Meta:
        db_table = 'images'

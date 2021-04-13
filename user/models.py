from django.db                  import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils               import timezone
from django.utils.translation   import ugettext_lazy as _

class UserManager(BaseUserManager):    
    use_in_migrations = True
    
    def _create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('Phone Number must be given')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user
    
    def create_user(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, **extra_fields)

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone_number, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
            verbose_name    = _('phone number'),
            max_length      = 64,
            unique          = True,
            )
    nickname = models.CharField(
            verbose_name    = _('nickname'),
            max_length      = 64,
            default         = 'Default Nickname',
            )
    profile_image = models.URLField(
            verbose_name    = _('profile image url'),
            max_length      = 2000,
            default         = 'https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-character-default-avatar-image_2237203.jpg'
            )
    is_active = models.BooleanField(
            verbose_name    = _('is active'),
            default         = True,
            )
    is_staff = models.BooleanField(
            verbose_name    = _('is staff'),
            default         = False,
            )
    is_superuser = models.BooleanField(
            verbose_name    = _('is superuser'),
            default         = False,
            )

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()
    
    class Meta:
        db_table = 'users'

class Address(models.Model):
    user = models.ForeignKey(
            'User',
            related_name    = 'addresses',
            on_delete       = models.CASCADE,
            )
    name = models.CharField(
            verbose_name    = _('location'),
            max_length      = 64,
            null            = True,
            blank           = True,
            default         = None,
            )
    is_main = models.BooleanField(
            verbose_name    = _('is main'),
            default         = False,
            )
    
    class Meta:
        db_table = 'addresses'

class Filter(models.Model):
    user = models.ForeignKey(
            'User',
            related_name    = 'filters',
            on_delete       = models.CASCADE,
            )
    subcategory = models.ForeignKey(
            'post.Subcategory',
            on_delete       = models.CASCADE,
            )
    is_active = models.BooleanField(
            verbose_name    = _('is_main'),
            default         = True,
            )

    class Meta:
        db_table = 'filters'


from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not name:
            raise ValueError('Users must have a name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, name, email, password):

        user = self.create_user(
            name=name,
            email=email,
            password=password,
        )

        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):

        user = self.create_user(
            name=name,
            email=email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    name = models.CharField(
        verbose_name='full_name',
        max_length=255
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(blank=True,
                               null=True)

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    admin = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='owner',
                              blank=True)
    users = models.ManyToManyField(User,
                                   blank=True,
                                   related_name='member')

    def __str__(self):
        return self.name

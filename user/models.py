from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.apps import apps


class UserAppManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        username and the email are the same until the user change it. 
        """
        username = email
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        username = email
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        username = email
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class UserApp(AbstractUser):
    def user_directory_path(self, filename):
        return 'user_{0}/{1}'.format(self.id, filename)

    def user_directory_path_for_cover(self, filename):
        return 'user_{0}/cover/{1}'.format(self.id, filename)

    email = models.EmailField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },)
    photo = models.ImageField(
        _("photo"),
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    photo_cover = models.ImageField(
        _("photo_cover"),
        upload_to=user_directory_path_for_cover,
        blank=True,
        null=True,
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    bio = models.TextField(
        _("bio"),
        blank=True,
        null=True,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    more_info = models.ForeignKey("user.UserInformations", verbose_name=_(
        "more_info"), null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.email

    objects = UserAppManager()


class UserInformations(models.Model):
    NOT_DEFINE = 'NDF'

    MALE = 'ML'
    FEMALE = 'FML'

    SINGLE = 'SNG'
    IN_RELATION = 'INR'
    MARRIED = 'MRD'
    DIVORCED = 'DVR'
    COHABITING = 'CBT'

    GANDER_CHOISES = [
        (NOT_DEFINE, 'not define'),
        (MALE, 'male'),
        (FEMALE, 'female'),
    ]

    MARITAL_CHOISES = [

        (NOT_DEFINE, 'not define'),
        (SINGLE, 'single'),
        (IN_RELATION, 'in relation'),
        (MARRIED, 'married'),
        (DIVORCED, 'devorced'),
        (COHABITING, 'cohabiting'),
    ]

    gander = models.CharField(
        _("gander"), choices=GANDER_CHOISES, max_length=3, default=NOT_DEFINE)

    birth_date = models.DateField(_("birth_date"), blank=True, null=True)

    marital_state = models.CharField(
        _("marital_state"), choices=MARITAL_CHOISES, max_length=3, default=NOT_DEFINE)

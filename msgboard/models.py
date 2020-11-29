from django.conf import settings
from django.db import models


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    UNSPECIFIED = 'U', 'Unspecified'


class LookupCategories(models.Model):
    category = models.CharField(max_length=100)


class LookupValues(models.Model):
    category = models.ForeignKey(
        LookupCategories,
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=100)


class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    dob = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.UNSPECIFIED,
        blank=True, null=True
    )
    phone = models.CharField(max_length=12, blank=True, null=True)
    mothers_maiden_name = models.CharField(max_length=50, blank=True, null=True)


class Messages(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='%(class)s_author'
    )
    board = models.ForeignKey(
        LookupValues,
        limit_choices_to={'category_id': 1},
        on_delete=models.RESTRICT,
        related_name='%(class)s_board'
    )
    message_date = models.DateField()
    message = models.TextField()
    labels = models.ManyToManyField(
        LookupValues,
        limit_choices_to={'category_id': 2},
        related_name='%(class)s_label'
    )
    tags = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_tag'
    )
    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='MessageViews',
        through_fields=('message', 'user'),
        related_name='%(class)s_views'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True
    )


class MessageViews(models.Model):
    message = models.ForeignKey(
        Messages,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )
    last_view_date = models.DateField()
    reaction = models.ForeignKey(
        LookupValues,
        limit_choices_to={'category_id': 3},
        on_delete=models.RESTRICT,
        blank=True, null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['message', 'user'], name='u_msg_user'
            )
        ]

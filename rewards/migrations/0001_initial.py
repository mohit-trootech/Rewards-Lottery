# Generated by Django 5.1.1 on 2024-10-15 06:18

import django.db.models.deletion
import django_extensions.db.fields
import rewards.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Lottery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        populate_from="title",
                        verbose_name="slug",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Inactive"), (1, "Active")],
                        default=1,
                        verbose_name="status",
                    ),
                ),
                (
                    "activate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for an immediate activation",
                        null=True,
                    ),
                ),
                (
                    "deactivate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for indefinite activation",
                        null=True,
                    ),
                ),
                ("image", models.ImageField(upload_to=rewards.models._upload_to)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "buyer",
                    models.ManyToManyField(
                        related_name="lotteries", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_lotteries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Lottery",
                "verbose_name_plural": "Lotteries",
            },
        ),
        migrations.CreateModel(
            name="Winner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "lottery",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="winners",
                        to="rewards.lottery",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="won_lotteries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Winner",
                "verbose_name_plural": "Winners",
            },
        ),
    ]

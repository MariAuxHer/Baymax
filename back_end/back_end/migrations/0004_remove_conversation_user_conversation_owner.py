# Generated by Django 4.2.5 on 2023-10-04 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('back_end', '0003_remove_conversation_profile_conversation_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='user',
        ),
        migrations.AddField(
            model_name='conversation',
            name='owner',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

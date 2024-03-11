from django.db import migrations, models
from django.contrib.auth.models import User
import django.db.models.deletion


def migrate_user_data(apps, schema_editor):

    NewUserModel = apps.get_model('sustainability', 'UserProfile')  # Replace 'NewUserModel' with the name of your new user model

    for user_profile in User.objects.all():
        new_user = NewUserModel.objects.create(
            username=user_profile.username,
            password=user_profile.password,
            email=user_profile.email,
            score=0
        )
        # Transfer related data if any
        # new_user.related_model_field = user_profile.related_model_field
        new_user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sustainability', '0003_userprofile_delete_newusermodel'),  # Add dependencies as required
    ]

    operations = [

        migrations.RunPython(migrate_user_data),
    ]

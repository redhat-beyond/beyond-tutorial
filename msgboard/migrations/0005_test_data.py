from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('msgboard', '0004_usermessage'),
        ('accounts', '0002_test_data')
    ]

    def generate_data(apps, schema_editor):
        from accounts.models import Account
        from msgboard.models import UserMessage

        woman1 = Account.accounts.get(user__username='woman1')
        robot = Account.accounts.get(user__username='robot')
        zombie = Account.accounts.get(user__username='zombie')

        test_data = [
            (woman1, 'Hi!'),
            (robot, 'Beep Beep, Boop Boop!'),
            (zombie, 'Braaaiiiinz!')
        ]

        with transaction.atomic():
            for author, text in test_data:
                UserMessage(author=author, text=text).save()

    operations = [
        migrations.RunPython(generate_data),
    ]


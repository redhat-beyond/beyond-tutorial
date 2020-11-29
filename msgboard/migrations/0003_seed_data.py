from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('msgboard', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        def populate_messages(message_data, parent=None):
            for author, board, postdate, msg, labels, views, tags, replies \
                    in message_data:
                u = User.objects.get(username=author)
                brd = LookupValues.objects.get(
                    category__category='Boards', value=board)
                msg_row = Messages(author=u, board=brd, message_date=postdate,
                                   message=msg, parent=parent)
                msg_row.save()
                for label in labels:
                    lbl = LookupValues.objects.get(
                        category__category='Labels', value=label)
                    msg_row.labels.add(lbl)
                for viewer, dt, reaction in views:
                    v = User.objects.get(username=viewer)
                    r = LookupValues.objects.get(
                        category__category='Reactions', value=reaction)
                    MessageViews(message=msg_row, user=v, reaction=r,
                                 last_view_date=dt).save()
                for tag in tags:
                    t = User.objects.get(username=tag)
                    msg_row.tags.add(t)
                for reply in replies:
                    populate_messages([reply], msg_row)

        from django.contrib.auth.models import User
        from msgboard.models import LookupCategories, LookupValues, \
            UserAdditionalInfo, Messages, MessageViews

        category_data = [
            ('Boards', ['Apartment hunting', 'Buy/Sell/Swap', 'Tremping']),
            ('Labels', ['high', 'medium', 'low', 'north', 'south', 'center']),
            ('Reactions', [':-)', ':-D', ':-(']),
        ]

        user_data = [
            ('Sim', 'Zacks', 'szacks', 'my_password', '1970-03-16', 'M', '0556162223'),
            ('Liora', 'Milbaum', 'lmilbaum', 'other_password', '1979-01-18', 'F', '0523152253'),
            ('Barak', 'Korren', 'bkorren', 'wqRR%hg7hfgP', '1979-05-21', 'F', '0543282191'),
        ]

        message_data = [
            ('szacks', 'Tremping', '2020-11-26',
                'I would like a ride from Maalot to Eilat on Tuesday afternoon',
                ['north', 'medium'], [('lmilbaum', '2020-11-26', ':-D')],
                ['bkorren', 'lmilbaum'], []),
            ('lmilbaum', 'Buy/Sell/Swap', '2020-11-20', 'I am selling a pony',
                ['center'],
                [('bkorren', '2020-11-20', ':-)')], [],
                [('bkorren', 'Buy/Sell/Swap', '2020-11-20', 'How much does it cost?', [], [], [], [])])
        ]
        with transaction.atomic():
            for category, values in category_data:
                cat = LookupCategories(category=category)
                cat.save()
                for value in values:
                    LookupValues(category=cat, value=value).save()
            for fn, ln, un, pw, dob, gender, phone in user_data:
                user = User.objects.create_user(
                    first_name=fn, last_name=ln, username=un, password=pw)
                additional = UserAdditionalInfo(
                    user=user, dob=dob, gender=gender, phone=phone)
                additional.save()
            populate_messages(message_data)

    operations = [
        migrations.RunPython(generate_data),
    ]

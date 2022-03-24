# Generated by Django 4.0.2 on 2022-03-11 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('FT', 'Future'), ('OG', 'Ongoing'), ('FI', 'Finished')], default='FT', error_messages={'invalid_choice': 'Type must be between those choices: FT for future events, OG for ongoing events and FI for finished events'}, max_length=2)),
                ('attendees', models.IntegerField(blank=True)),
                ('event_date', models.DateTimeField(blank=True)),
                ('notes', models.TextField(blank=True, max_length=5000)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.client')),
                ('support_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

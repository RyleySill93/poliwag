# Generated by Django 4.0.2 on 2022-08-01 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppEvent',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('event_type', models.CharField(max_length=500)),
                ('user_id', models.CharField(blank=True, max_length=17, null=True)),
                ('payload', models.JSONField()),
                ('payload_class', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='appevent',
            index=models.Index(fields=['event_type'], name='idx_gl_event_event_type'),
        ),
    ]

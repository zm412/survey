# Generated by Django 3.2.6 on 2021-10-27 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey_instance',
            name='from_surv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_item', to='survey.survey'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_answ', to='survey.question')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_instance', to='survey.survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interwe', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
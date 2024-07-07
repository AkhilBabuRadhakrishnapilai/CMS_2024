# Generated by Django 5.0.6 on 2024-07-07 16:31

import CMSAPP.managers
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(max_length=250)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('emp_id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('address', models.CharField(max_length=250)),
                ('dob', models.DateField()),
                ('contact_number', models.CharField(blank=True, default=0, max_length=10)),
                ('date_of_joining', models.DateField()),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(default='clinics', max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genders', to='CMSAPP.gender')),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group')),
                ('qualification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='CMSAPP.qualification')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMSAPP.roles')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', CMSAPP.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('fees', models.PositiveSmallIntegerField(default=0)),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specializations', to='CMSAPP.specialization')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

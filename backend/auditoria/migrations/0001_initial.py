# Generated migration for AuditLog model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('data_hora', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('usuario_login', models.CharField(max_length=150)),
                ('id_profissional', models.IntegerField(blank=True, null=True)),
                ('perfil', models.CharField(blank=True, max_length=50, null=True)),
                ('acao', models.CharField(choices=[('LOGIN', 'Login'), ('LOGIN_FALHA', 'Login Falha'), ('LOGOUT', 'Logout'), ('CREATE', 'Criação'), ('UPDATE', 'Alteração'), ('DELETE', 'Exclusão'), ('LEITURA', 'Leitura')], max_length=20)),
                ('entidade', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('objeto_id', models.CharField(blank=True, max_length=64, null=True)),
                ('objeto_repr', models.CharField(blank=True, max_length=255, null=True)),
                ('alteracoes', models.JSONField(blank=True, null=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=255, null=True)),
                ('metodo_http', models.CharField(blank=True, max_length=10, null=True)),
                ('caminho', models.CharField(blank=True, max_length=255, null=True)),
                ('id_usuario', models.ForeignKey(blank=True, db_index=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_log_auditoria',
            },
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['data_hora'], name='auditoria_a_data_ho_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['id_usuario'], name='auditoria_a_id_user_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['entidade', 'objeto_id'], name='auditoria_a_entidad_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['acao'], name='auditoria_a_acao_idx'),
        ),
    ]

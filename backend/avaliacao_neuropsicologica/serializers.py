from rest_framework import serializers

from .models import AvaliacaoNeuropsicologica


class AvaliacaoNeuropsicologicaSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(
        source="id_paciente.nome_completo", read_only=True, default=None
    )
    psicologo_nome = serializers.CharField(
        source="id_psicologo.nome_completo", read_only=True, default=None
    )
    laudo_pdf = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = AvaliacaoNeuropsicologica
        fields = [
            "id", "id_paciente", "paciente_nome", "id_psicologo", "psicologo_nome",
            "data_avaliacao", "motivo_avaliacao", "instrumentos_utilizados",
            "valor_avaliacao", "hipoteses_diagnosticas", "resultados_principais",
            "conclusao_recomendacoes", "caminho_laudo_pdf", "laudo_pdf",
            "data_criacao", "data_atualizacao",
        ]
        read_only_fields = ["id", "data_criacao", "data_atualizacao", "caminho_laudo_pdf"]

    def create(self, validated_data):
        file = validated_data.pop("laudo_pdf", None)
        instance = super().create(validated_data)
        if file:
            self._save_file(instance, file)
        return instance

    def update(self, instance, validated_data):
        file = validated_data.pop("laudo_pdf", None)
        instance = super().update(instance, validated_data)
        if file:
            self._save_file(instance, file)
        return instance

    def _save_file(self, instance, file):
        import os
        from django.conf import settings

        upload_dir = os.path.join(settings.MEDIA_ROOT, "laudos")
        os.makedirs(upload_dir, exist_ok=True)
        filename = f"{instance.id}_{file.name}"
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        instance.caminho_laudo_pdf = f"laudos/{filename}"
        instance.save(update_fields=["caminho_laudo_pdf"])

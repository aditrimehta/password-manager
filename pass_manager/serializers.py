from rest_framework import serializers
from .models import VaultItem


class VaultItemSerializer(serializers.ModelSerializer):
    decrypted_username = serializers.SerializerMethodField()
    decrypted_password = serializers.SerializerMethodField()

    class Meta:
        model = VaultItem
        fields = ["id", "website", "decrypted_username", "decrypted_password", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_decrypted_username(self, obj):
        return obj.get_credentials()["username"]

    def get_decrypted_password(self, obj):
        return obj.get_credentials()["password"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        username = request.data.get("username")
        password = request.data.get("password")

        vault_item = VaultItem(user=user, website=validated_data["website"])
        vault_item.set_credentials(username, password)
        vault_item.save()
        return vault_item

    def update(self, instance, validated_data):
        username = self.context["request"].data.get("username")
        password = self.context["request"].data.get("password")

        instance.website = validated_data.get("website", instance.website)
        if username and password:
            instance.set_credentials(username, password)
        instance.save()
        return instance

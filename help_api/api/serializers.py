# Django imports.
from django.db import transaction

from help_api.models import *

# Rest Framework imports.
from rest_framework import serializers
from help_api.api.serializers import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityModel
        fields = ['entity_id', 'entity_name', 'entity_type']

class SOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOSModel
        fields = ['sos_id', 'sos_description', 'sos_from',
                  'sos_state', 'sos_tag', 'sos_date']

class SOSInfoSerializer(serializers.ModelSerializer):
    sos = serializers.SerializerMethodField(source='get_sos')
    address = serializers.SerializerMethodField(source='get_address')

    def get_sos(self, obj):
        qs = SOSModel.objects.filter(sos_from=obj.entity_id)
        return SOSSerializer(qs, many=True).data

    def get_address(self, obj):
        qs = AddressModel.objects.filter(entity_id=obj.entity_id)
        return AddressSerializer(qs, many=True).data

    class Meta:
        model = EntityModel
        fields = ['entity_name', 'entity_id', 'sos', 'address']


class RegisterEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityModel
        fields = ['entity_name']


class RegisterAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['entity_id', 'lane', 'town',
                  'district', 'state', 'contact_phone',
                  'contact_alternate_phone', 'email']

    def validate(self, data):
        if data['contact_phone'] is None:
            raise serializers.ValidationError("Contact cannot be empty")

        elif data['lane'] is None | data['town'] is None:
            raise serializers.ValidationError("lane and town cannot be empty")

        return data


class ToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsModel
        fields = '__all__'

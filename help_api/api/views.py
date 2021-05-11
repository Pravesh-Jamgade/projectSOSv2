
from help_api.models import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

import json

INVALID_POST_DATA = 'Failure'
VALID_POST_DATA = 'Success'


# AddressModel
# 1 get address of entity
# 2 get contact of entity
# 3 post address + contact

class AddressView(APIView):

    def get(self, request):

        data = {}
        return Response({'data': data, 'status': True})


# 2 get entity names
# 3 get entity choice

class EntityView(APIView):

    def get(self, request):
        entities = EntityModel.objects.all()
        json = []
        for entity in entities:
            data = {}
            data['entity_name'] = entity.entity_name
            data['entity_type'] = entity.entity_type

            eAddress = \
                AddressModel.objects.filter(entity_id=entity.entity_id)
            if eAddress is None:
                return Response(status=status.HTTP_404_NOT_FOUND)

            allAddresses = []
            for eAdd in eAddress:
                address = {}
                address['lane'] = eAdd.lane
                address['town'] = eAdd.town
                address['district'] = eAdd.district
                address['state'] = eAdd.state
                address['contact_phone'] = eAdd.contact_phone
                address['contact_alternate_phone'] = \
                    eAdd.contact_alternate_phone
                address['email'] = eAdd.email
                allAddresses.append(address)

            data['address'] = allAddresses
            json.append(data)
        if len(json) == 0:
            return Response({'status': False, 'message': 'No records',
                            'Response': None},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=json, status=status.HTTP_200_OK)


# ToolsModel
# 1 post tool_name, tool_from, tool_qty, tool _state
# 2 get tool_from
# 3 get tool_qty
# 4 update/put tool_state

class ToolView:

    pass


# SOSModel
# 1 post sos
# 2 get sos_from
# 3 put/update sos_state

class SOSView(APIView):
    def get(self, request):
        obj = EntityModel.objects.all()
        serialize = SOSInfoSerializer(obj, many=True)
        data = serialize.data
        return Response(data=data, status=status.HTTP_200_OK)
        # Register


class RegisterEntityView(APIView):

    def post(self, request):
        data = request.data

        # create entity

        serializer = RegisterEntitySerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'status': False,
                            'message': INVALID_POST_DATA},
                            status=status.HTTP_400_BAD_REQUEST)
        entity = serializer.save()

        # create address

        data['entity_id'] = entity.entity_id
        serializer = RegisterAddressSerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'status': False,
                            'message': INVALID_POST_DATA},
                            status=status.HTTP_400_BAD_REQUEST)
        address = serializer.save()

        return Response({'status': True, 'message': VALID_POST_DATA},
                        status=status.HTTP_200_OK)


# SortData
# 1 by SOS timestamp
# 2 by SOS location and current location
# 3 by tag requirement

class SortDataView:

    pass

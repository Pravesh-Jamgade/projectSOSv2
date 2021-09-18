
from help_api.models import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

import json

INVALID_POST_DATA = 'Failure'
VALID_POST_DATA = 'Success'


@api_view(['GET'])
def test(request):
    print("HELLLLLLLL", request.GET['name'])
    if request.method == 'GET':
        print("hello world")
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({'status': False, 'message': 'No records',
                            'Response': None},
                            status=status.HTTP_404_NOT_FOUND)


#EntityModel
#1. register entity and address - done
#2. update entity               - notdone
#3. get one entity              - done
#4. get all entity              - done

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
                        status=status.HTTP_201_CREATED)


''' creating json of entities '''
def getJsonEntityView(entities):
    json = []
    for entity in entities:
        data = {}
        data['entity_id'] = entity.entity_id
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
    return json

''' get single entity details '''
@api_view(['GET'])
def getEntityDetail(request, name):
    print("get single entity details:", name)
    res = EntityModel.objects.filter(entity_name=name)
    if res is not None:
        json = getJsonEntityView(res)
    if len(json) == 0:
        return Response({'status': False, 'message': 'No records',
                            'Response': None},
                            status=status.HTTP_404_NOT_FOUND)
    return Response(data=json, status=status.HTTP_200_OK)

''' get all entity details '''
@api_view(['GET'])
def getAllEntityDetails(request):
    print("get all entity details")
    entities = EntityModel.objects.all()
    json = getJsonEntityView(entities)
    if len(json) == 0:
        return Response({'status': False, 'message': 'No records',
                        'Response': None},
                        status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(data=json, status=status.HTTP_200_OK)


# AddressModel
# 1 get address of entity - done in entity model
# 2 get contact of entity - done in entity model
# 3 post address + contact

class AddressView(APIView):

    ''' get address of entity '''
    def get(self, request):
        pass

    def post(self, request):
        data = request.data
        serialize = AddressSerializer(data=data)
        if serialize.is_valid():
            serialize.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)



# ToolsModel
# 1 post tool_name, tool_from, tool_qty, tool _state
# 2 get tool_from
# 3 get tool_qty
# 4 update/put tool_state

class ToolsView(APIView):

    def get(self, request):
        rate = 10
        if 'rate' in request.GET:
            rate = int(request.GET['rate'])

        print(request.GET)
        objs = ToolsModel.objects.values_list()[:rate]
        if objs is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = []
        for obj in objs:
            print(obj)
            json = {}
            json['toolid'] = obj[0]
            json['tool_name'] = obj[1]
            json['tool_from'] = obj[2]
            json['tool_qty'] = obj[3]
            json['tool_state'] = obj[4]
            data.append(json)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serialize = ToolsSerializer(data=data)
        if serialize.is_valid():
            serialize.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

class ToolsUpdateView(APIView):
    pass


# SOSModel
# 1 post sos                -done 
# 2 get all sos             -done
# 3 put/update sos_state    -done
# 4 get sos based on area   -notdone

class SOSView(APIView):
    def get(self, request):
        print(request.path, " + ", request.method)
        obj = EntityModel.objects.all()
        serialize = SOSInfoSerializer(obj, many=True)
        data = serialize.data
        return Response(data=data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = SOSSerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'status': False,
                            'message': INVALID_POST_DATA},
                            status=status.HTTP_400_BAD_REQUEST)
        entity = serializer.save()
        return Response(status=status.HTTP_200_OK)

class SOSViewUpdate(APIView):

    def get(self, request, pk):
        print("SOSViewUpdate get: ", pk)
        obj = get_object_or_404(SOSModel, pk=pk)
        if obj is not None:
            print("valid sos view update ")
            serialize = SOSSerializer(obj, many=False)
            data = serialize.data
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        print("SOSViewUpdate put sos: ", pk)
        obj = get_object_or_404(SOSModel, pk=pk)
        if obj is not None:
            request.data['sos_from'] = obj.sos_from.entity_id
            serialize = SOSSerializer(obj, data=request.data)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)




# SortData
# 1 by SOS timestamp
# 2 by SOS location and current location
# 3 by tag requirement



from django.http.request import QueryDict
from rest_framework.response import Response


class SerializerMapMixin:
    serializer_class_map = {}

    def get_serializer_class(self):
        return self.serializer_class_map.get(self.action, self.serializer_class)


class PermissionMapMixin:
    permission_classes_map = {}

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.permission_classes_map.get(self.action, None):
            permission_classes = self.permission_classes_map[self.action]

        return [permission() for permission in permission_classes]


class QuerysetMapMixin:
    queryset_map = {}

    def get_queryset(self):
        return self.queryset_map.get(self.action, self.queryset)


class MappingViewSetMixin(object):
    serializer_action_map = {}
    permission_classes_map = {}
    filterset_class_map = {}

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.permission_classes_map.get(self.action, None):
            permission_classes = self.permission_classes_map[self.action]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.serializer_action_map.get(self.action, None):
            return self.serializer_action_map[self.action]
        return self.serializer_class

    def get_filterset_class(self):
        if self.filterset_class_map.get(self.action, None):
            return self.filterset_class_map[self.action]
        return getattr(self, 'filterset_class', None)

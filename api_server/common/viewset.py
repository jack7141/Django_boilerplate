from django.http.request import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
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


class MappingDjangoFilterBackend(DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        """
        Return the `FilterSet` class used to filter the queryset.
        """
        filterset_class_map = getattr(view, "filterset_class_map", {})
        filterset_class = filterset_class_map.get(view.action, None)

        if filterset_class:
            return filterset_class

        filterset_class = getattr(view, "filterset_class", None)
        filterset_fields = getattr(view, "filterset_fields", None)

        if filterset_class:
            filterset_model = filterset_class._meta.model

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                assert issubclass(
                    queryset.model, filterset_model
                ), "FilterSet model %s does not match queryset model %s" % (
                    filterset_model,
                    queryset.model,
                )

            return filterset_class

        if filterset_fields and queryset is not None:
            MetaBase = getattr(self.filterset_base, "Meta", object)

            class AutoFilterSet(self.filterset_base):
                class Meta(MetaBase):
                    model = queryset.model
                    fields = filterset_fields

            return AutoFilterSet

        return None

from django_filters.rest_framework import DjangoFilterBackend


class OrderFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user_id=request.user.id)
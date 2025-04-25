from django.urls import path
from .views import insert_request, submit_request, next_step, view_request
from .api import (
    configuration_change_request_list,
    configuration_change_request_create,
    configuration_change_request_detail,
    configuration_change_request_update,
    configuration_change_request_partial_update,
    configuration_change_request_delete,
)

urlpatterns = [
    path('request/', insert_request, name='insert_request'),
    path('request/<int:request_id>/', submit_request, name='submit_request'),
    path('request/view/<int:request_id>/', view_request, name='view_request'),
    path('request/next_step/<int:request_id>/<str:action>/', next_step, name='next_step'),
    

    path('api/configuration_change_request/v1/', configuration_change_request_list, name='configuration_change_request_list'),
    path('api/configuration_change_request/v1/create/', configuration_change_request_create, name='configuration_change_request_create'),
    path('api/configuration_change_request/v1/<int:pk>/', configuration_change_request_detail, name='configuration_change_request_detail'),
    path('api/configuration_change_request/v1/<int:pk>/update/', configuration_change_request_update, name='configuration_change_request_update'),
    path('api/configuration_change_request/v1/<int:pk>/partial-update/', configuration_change_request_partial_update, name='configuration_change_request_partial_update'),
    path('api/configuration_change_request/v1/<int:pk>/delete/', configuration_change_request_delete, name='configuration_change_request_delete'),
]

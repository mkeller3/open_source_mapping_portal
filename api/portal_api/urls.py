from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('maps/map/', views.mapView.as_view(), name='map'),
    path('maps/map_image/', views.mapImageView.as_view(), name='map_image'),
    path('maps/duplicate_map/', views.duplicateMapView.as_view(), name='duplicate_map'),
    path('maps/personal_maps/', views.personalMapsView.as_view(), name='personal_maps'),
    path('maps/all_maps/', views.allMapsView.as_view(), name='all_maps'),
    path('maps/analytics/', views.analyticsMapView.as_view(), name='map_analytics'),
    path('apps/app/', views.appView.as_view(), name='app'),
    path('apps/app_image/', views.appImageView.as_view(), name='app_image'),
    path('apps/duplicate_app/', views.duplicateAppView.as_view(), name='duplicate_app'),
    path('apps/personal_apps/', views.personalAppsView.as_view(), name='personal_apps'),
    path('apps/all_apps/', views.allAppsView.as_view(), name='all_apps'),
    path('apps/analytics/', views.analyticsAppView.as_view(), name='app_analytics'),
    path('basic/group/', views.groupView.as_view(), name='group'),
    path('basic/groups/', views.allGroupsView.as_view(), name='groups'),
    path('basic/user_search/', views.userSearchView.as_view(), name='user_search'),
    path('basic/group_search/', views.groupSearchView.as_view(), name='group_search'),
    path('import/import_geographic_file/', views.importGeographicFileView.as_view(), name='import_geographic_file'),
    path('import/import_point_file/', views.importPointFileView.as_view(), name='import_point_file'),
    path('import/esri_service/', views.importEsriUrlView.as_view(), name='esri_service'),
    path('tables/table/', views.tableView.as_view(), name='table'),
    path('tables/table_image/', views.tableImageView.as_view(), name='table_image'),
    path('tables/duplicate_table/', views.duplicateTableView.as_view(), name='duplicate_table'),
    path('tables/personal_tables/', views.personalTablesView.as_view(), name='personal_tables'),
    path('tables/all_tables/', views.allTablesView.as_view(), name='all_tables'),
    path('tables/analytics/', views.analyticsTableView.as_view(), name='table_analytics'),
    path('features/columns/', views.featureColumnsView.as_view(), name='columns'),
    path('features/query/', views.featureQueryView.as_view(), name='query'),
    path('sites/site/', views.mapView.as_view(), name='map'),
    path('sites/site_image/', views.siteImageView.as_view(), name='site_image'),
    path('sites/duplicate_site/', views.duplicateSiteView.as_view(), name='duplicate_site'),
    path('sites/personal_sites/', views.personalSitesView.as_view(), name='personal_sites'),
    path('sites/all_sites/', views.allSitesView.as_view(), name='all_sites'),
    path('sites/analytics/', views.analyticsSiteView.as_view(), name='site_analytics'),
    path('geosubscriptions/geosubscription/', views.mapView.as_view(), name='map'),
    path('geosubscriptions/geosubscription_image/', views.geosubscriptionImageView.as_view(), name='geosubscription_image'),
    path('geosubscriptions/duplicate_geosubscription/', views.duplicateGeosubscriptionView.as_view(), name='duplicate_geosubscription'),
    path('geosubscriptions/personal_geosubscriptions/', views.personalGeosubscriptionsView.as_view(), name='personal_geosubscriptions'),
    path('geosubscriptions/all_geosubscriptions/', views.allGeosubscriptionsView.as_view(), name='all_geosubscriptions'),
    path('geosubscriptions/analytics/', views.analyticsGeosubscriptionView.as_view(), name='geosubscription_analytics'),
    path('administration/map_service_congfiguration/', views.mapServiceConfigurationView.as_view(), name='map_service_congfiguration'),
    path('administration/map_service_security/', views.mapServiceSecurityConfigurationView.as_view(), name='map_service_security'),
    path('administration/blocked_user/', views.blockedUserView.as_view(), name='blocked_user'),
    path('administration/alert/', views.alertView.as_view(), name='alert'),
    path('tiles/<str:database>/<str:table_name>/<int:z>/<int:x>/<int:y>.pbf', views.tilesView.as_view(), name='tiles'),
    path('services/geocode/', views.geocodeView.as_view(), name='geocode'),
    path('services/map_query/', views.mapQueryView.as_view(), name='map_query'),
    path('services/portal_tables/', views.portalTablesView.as_view(), name='portal_tables'),
    path('services/autocomplete/', views.autocompleteView.as_view(), name='autocomplete'),
    path('services/wms_search/', views.wmsSearchView.as_view(), name='wms_search'),
    path('authentication/get_token/', obtain_auth_token, name="get_token"),
    path('register/register_user/', views.registerView.as_view(), name="register_user"),
]

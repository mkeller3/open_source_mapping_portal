from portal_api import maps, register, basic, application, administration, imports, tables, features, sites, geosubscriptions, tiles, services, remote_data

# Register API
registerView = register.registerView

# Maps API
mapView = maps.mapView
mapImageView = maps.mapImageView
personalMapsView = maps.personalMapsView
allMapsView = maps.allMapsView
analyticsMapView = maps.analyticsMapView
duplicateMapView = maps.duplicateMapView

# Apps API
appView = application.appView
appImageView = application.appImageView
personalAppsView = application.personalAppsView
allAppsView = application.allAppsView
analyticsAppView = application.analyticsAppView
duplicateAppView = application.duplicateAppView

# Basic API
userSearchView = basic.userSearchView
groupSearchView = basic.groupSearchView
groupView = basic.groupView
allGroupsView = basic.allGroupsView

# Administration API
mapServiceConfigurationView = administration.mapServiceConfigurationView
mapServiceSecurityConfigurationView = administration.mapServiceSecurityConfigurationView
blockedUserView = administration.blockedUserView
alertView = administration.alertView

# Imports API
importGeographicFileView = imports.importGeographicFileView
importPointFileView = imports.importPointFileView
importEsriUrlView = imports.importEsriUrlView

# Tables API
tableView = tables.tableView
tableImageView = tables.tableImageView
personalTablesView = tables.personalTablesView
allTablesView = tables.allTablesView
analyticsTableView = tables.analyticsTableView
duplicateTableView = tables.duplicateTableView

# Features API
featureColumnsView = features.featureColumnsView
featureQueryView = features.featureQueryView

# Sites API
siteView = sites.siteView
siteImageView = sites.siteImageView
personalSitesView = sites.personalSitesView
allSitesView = sites.allSitesView
analyticsSiteView = sites.analyticsSiteView
duplicateSiteView = sites.duplicateSiteView

# Sites API
geosubscriptionView = geosubscriptions.geosubscriptionView
geosubscriptionImageView = geosubscriptions.geosubscriptionImageView
personalGeosubscriptionsView = geosubscriptions.personalGeosubscriptionsView
allGeosubscriptionsView = geosubscriptions.allGeosubscriptionsView
analyticsGeosubscriptionView = geosubscriptions.analyticsGeosubscriptionView
duplicateGeosubscriptionView = geosubscriptions.duplicateGeosubscriptionView

# Tiles API
tilesView = tiles.tilesView

# Services API
geocodeView = services.geocodeView
mapQueryView = services.mapQueryView
portalTablesView = services.portalTablesView
autocompleteView = services.autocompleteView
wmsSearchView = services.wmsSearchView

# Remote Data API
remoteDataView = remote_data.remoteDataView
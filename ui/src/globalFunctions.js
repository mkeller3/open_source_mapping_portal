import axios from "axios";

const apiUrl = "http://0.0.0.0:8050";

export const globalFunctions = {
  httpRequest: (
    type,
    url,
    formData = undefined,
    auth = false,
    zip_file = false,
    multipart = false
  ) => {
    let parameters = {
      headers: {},
    };

    if (auth) {
      parameters.headers["Authorization"] = `Token ${localStorage.getItem(
        "mapping_portal_access_token"
      )}`;
    }

    if (zip_file) {
      parameters.responseType = "blob";
    }

    if (multipart) {
      parameters.headers["Content-Type"] = "multipart/form-data";
    }

    return new Promise((resolve) => {
      if (type === "get") {
        axios
          .get(url, parameters)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            if ("response" in error) {
              if (error.response === undefined) {
                resolve(error);
              }
              if (error.response.status != "401") {
                resolve(error.response);
              }
            } else {
              resolve(error);
            }
          });
      } else if (type === "post") {
        axios
          .post(url, formData, parameters)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            if ("response" in error) {
              if (error.response === undefined) {
                resolve(error);
              }
              if (error.response.status != "401") {
                resolve(error.response);
              }
            } else {
              resolve(error);
            }
          });
      } else if (type === "put") {
        axios
          .put(url, formData, parameters)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            if ("response" in error) {
              if (error.response === undefined) {
                resolve(error);
              }
              if (error.response.status != "401") {
                resolve(error.response);
              }
            } else {
              resolve(error);
            }
          });
      } else if (type === "delete") {
        axios
          .delete(url, { formData, ...parameters })
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            if ("response" in error) {
              if (error.response === undefined) {
                resolve(error);
              }
              if (error.response.status != "401") {
                resolve(error.response);
              }
            } else {
              resolve(error);
            }
          });
      }
    });
  },
  // Add a layer to the map
  addLayerToMap: (layer, appData, map, newLayer = true) => {
    return new Promise((resolve) => {
      layer.mapboxName = `map_service_${appData.layerCounter}`;
      if (layer.map_type === "user_data" || layer.map_type === "map_layer" ) {
        let db = 'default_maps'
        if (layer.map_type === "user_data"){
          db = 'user_data'
        }
        map.addSource(layer.mapboxName, {
          type: "vector",
          tiles: [
            `${apiUrl}/api/v1/tiles/${db}/${layer.table_id}/{z}/{x}/{y}.pbf?fields=gid`,
          ],
          minzoom: 1,
          maxzoom: 22,
        });
        if (layer.geometry_type === "polygon") {
          map.addLayer({
            id: `${layer.mapboxName}fill`,
            type: "fill",
            source: layer.mapboxName,
            'source-layer': 'default',
            // layout: layer.layout,
            paint: layer.fill_paint,
          });
          map.addLayer({
            id: `${layer.mapboxName}_line`,
            type: "line",
            source: layer.mapboxName,
            'source-layer': 'default',
            // layout: layer.layout,
            paint: layer.border_paint,
          });
        } else if (layer.geometry_type === "line") {
          map.addLayer({
            id: layer.mapboxName,
            type: "line",
            source: layer.mapboxName,
            'source-layer': 'default',
            // layout: layer.layout,
            paint: layer.paint,
          });
        } else if (layer.geometry_type === "point") {
          map.addLayer({
            id: layer.mapboxName,
            type: "circle",
            source: layer.mapboxName,
            'source-layer': 'default',
            // layout: layer.layout,
            paint: layer.paint,
          });
        }
        appData.layerCounter += 1;
        if (newLayer) {
          appData.layers.push(layer);
        }
        resolve(layer);
      }
      else if (layer.map_type === "geojson") {
        map.addSource(layer.mapboxName, {
          type: "geojson",
          data: layer.data,
        });

        if (layer.geometry_type === "polygon") {
          map.addLayer({
            id: `${layer.mapboxName}fill`,
            type: "fill",
            source: layer.mapboxName,
            layout: layer.layout,
            paint: layer.paint,
          });
          map.addLayer({
            id: `${layer.mapboxName}_line`,
            type: "line",
            source: layer.mapboxName,
            layout: layer.layout,
            paint: layer.paint,
          });
        } else if (layer.geometry_type === "line") {
          map.addLayer({
            id: layer.mapboxName,
            type: "line",
            source: layer.mapboxName,
            layout: layer.layout,
            paint: layer.paint,
          });
        } else if (layer.geometry_type === "point") {
          map.addLayer({
            id: layer.mapboxName,
            type: "circle",
            source: layer.mapboxName,
            layout: layer.layout,
            paint: layer.paint,
          });
        }
        appData.layerCounter += 1;
        if (newLayer) {
          appData.layers.push(layer);
        }
        resolve(layer);
      }
    });
  },
  // getDefaultPaint(layer){
    // if(layer.geometry_type === 'point'){
    //   return {
    //     'circle-color': '#fff'
    //   }
    // } else if(layer.geometry_type === 'line'){
    //   return {
    //     'line-color': '#fff'
    //   }
    // } if(layer.geometry_type === 'point'){
    //   return {
    //     'circle-color': '#fff'
    //   }
    // }
  // }
};

<template>
  <div id="maplibre-map">
    <alert :appData="appData"/>
  </div>
</template>

<script>
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import Alert from './Alert.vue';

export default {
  components: { Alert },
  name: "Map",
  props: {
    appData: Object,
  },
  mounted() {
    const vr = this;
    maplibregl.accessToken =
      "pk.eyJ1IjoibWtlbGxlcjMiLCJhIjoieFdYUUg5TSJ9.qzhP1v5f1elHrnTV4YpkiA";
    this.appData.map = new maplibregl.Map({
      container: "maplibre-map",
      style: `mapbox://styles/mapbox/${this.appData.basemap}-v10`,
      // style: {
      //     sources: {},
      //     layers: [],
      //     version: 8
      // },
      center: [this.appData.longitude, this.appData.latitude],
      zoom: this.appData.zoom,
      transformRequest: (url, resourceType) => {
        if (resourceType === "Tile" && url.includes("api/v1/tiles")) {
          return {
              
            url: url,
            headers: {
              Authorization: `Token ${localStorage.getItem(
                "mapping_portal_access_token"
              )}`,
            },
          };
        }
      },
    });

    this.appData.map.on("load", function () {
      vr.appData.map.addControl(new maplibregl.NavigationControl(), "top-left");
      vr.appData.map.addControl(new maplibregl.GeolocateControl(), "top-left");
      vr.appData.map.addControl(new maplibregl.ScaleControl(), "bottom-left");
      vr.appData.map.addControl(new maplibregl.FullscreenControl(), "top-left");
    });
  },
};
</script>

<style>
#maplibre-map {
  width: 100%;
  height: 100%;
}
</style>
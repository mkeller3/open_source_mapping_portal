<template>
  <div>
    <div v-if="appData.searchForLayers">
      <h2 @click="appData.searchForLayers = !appData.searchForLayers">
        Go Back
      </h2>
      <v-divider />
      <v-form @submit.prevent="searchForLayers()">
        <v-select
          label="Layer Type"
          v-model="layerType"
          outlined
          :items="layerTypes"
          item-text="text"
          item-value="value"
          @change="searchForLayers()"
        ></v-select>
        <v-text-field outlined v-model="searchTerm" label="Search for layers">
        </v-text-field>
        <v-btn
          color="success"
          :loading="loading"
          :disabled="loading"
          text
          type="submit"
        >
          Search
        </v-btn>
      </v-form>
      <div v-if="searchResults.length > 0">
        <v-divider />
        <div v-for="(result, index) in searchResults" :key="index">
          <map-builder-layer-search-card :layer="result" :appData="appData"/>
        </div>
      </div>
    </div>
    <div v-else>
      <h2>Layers</h2>
      <v-divider />
      <div v-if="appData.layers.length === 0">
        <p>No Layers</p>
      </div>
      <v-btn
        color="success"
        text
        @click="appData.searchForLayers = !appData.searchForLayers"
      >
        Add Layer
      </v-btn>
    </div>
  </div>
</template>

<script>
import MapBuilderLayerSearchCard from "./MapBuilderLayerSearchCard.vue";

export default {
  components: {
    MapBuilderLayerSearchCard,
  },
  name: "MapBuilderLayersSearchPanel",
  props: {
    appData: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    loading: false,
    searchTerm: "",
    searchResults: [],
    layerType: "personal",
    layerTypes: [
      {
        text: "Your Layers",
        value: "personal",
      },
      {
        text: "All Layers",
        value: "all",
      },
      {
        text: "Portal Layers",
        value: "portal",
      },
      {
        text: "ArcGIS Online",
        value: "esri",
      },
    ],
  }),
  methods: {
    searchForLayers() {
      this.loading = true;
      this.searchResults = [];
      if (["all", "personal"].includes(this.layerType)) {
        this.globalFunctions
          .httpRequest(
            "get",
            `${this.apiUrl}/api/v1/tables/${this.layerType}_tables/?search=${this.searchTerm}`,
            undefined,
            true
          )
          .then((res) => {
            if (res.status != 200) {
              this.appData.alert = JSON.stringify(res.data);
            }
            res.data.results.forEach((result) => {
              result.map_type = "user_data";
            });
            this.searchResults = res.data.results;
            this.loading = false;
          });
      } else if (this.layerType === "portal") {
        this.globalFunctions
          .httpRequest(
            "get",
            `${this.apiUrl}/api/v1/services/portal_tables/?search=${this.searchTerm}`,
            undefined,
            true
          )
          .then((res) => {
            if (res.status != 200) {
              this.appData.alert = JSON.stringify(res.data);
            }
            res.data.forEach((result) => {
              result.title = result.display_name;
              result.table_id = result.table_name;
              result.map_type = "map_layer";
            });
            this.searchResults = res.data;
            this.loading = false;
          });
      } else if (this.layerType === "esri") {
        let url = `https://www.arcgis.com/sharing/rest/search?num=50&start=1&sortOrder=desc&q=(${this.searchTerm}) (type:("Feature Service" OR "Hosted" OR "Tiled" OR "Map Service" OR "Image Service"))&enriched=true&f=json`;
        this.globalFunctions
          .httpRequest("get", url, undefined, false)
          .then((res) => {
            if (res.status != 200) {
              this.appData.alert = JSON.stringify(res.data);
            }
            res.data.results.forEach((result) => {
              result.map_type = "esri";
              result.image = `https://www.arcgis.com/sharing/rest/content/items/${result.id}/info/${result.thumbnail}`;
              result.description = result.snippet;
            });
            this.searchResults = res.data.results;
            this.loading = false;
          });
      }
    },
  },
};
</script>

<style>
</style>
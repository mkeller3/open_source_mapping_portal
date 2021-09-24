<template>
  <div class="p-0 m-0">
    <p>Map Search</p>
    <v-divider />
    <v-form @submit.prevent="searchForMaps()">
      <v-select
        label="Map Type"
        v-model="mapType"
        outlined
        :items="mapTypes"
        item-text="text"
        item-value="value"
        @change="searchForMaps()"
      >
      </v-select>
      <v-text-field outlined v-model="searchTerm" label="Map Name">
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
        <map-builder-map-search-card :map="result" :appData="appData" />
      </div>
    </div>
  </div>
</template>

<script>
import MapBuilderMapSearchCard from './MapBuilderMapSearchCard.vue';
export default {
  components: { 
    MapBuilderMapSearchCard 
  },
  name: "MapBuilderMapSearchPanel",
  props: {
    appData: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    loading: false,
    searchTerm: null,
    searchResults: [],
    mapType: "personal",
    mapTypes: [
      {
        text: "My Maps",
        value: "personal",
      },
      {
        text: "All Maps",
        value: "all",
      },
    ],
  }),
  methods: {
    searchForMaps() {
      this.loading = true;
      this.searchResults = [];
      this.globalFunctions
        .httpRequest(
          "get",
          `${this.apiUrl}/api/v1/maps/${this.mapType}_maps/?search=${this.searchTerm}`,
          undefined,
          true
        )
        .then((res) => {
          this.loading = false;
          if (res.status != 200) {
            this.alert = JSON.stringify(res.data);
          } else {
            console.log(res);
            this.searchResults = res.data.results;
          }
        });
    },
  },
};
</script>

<style>
</style>
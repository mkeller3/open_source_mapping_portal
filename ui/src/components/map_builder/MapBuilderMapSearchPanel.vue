<template>
  <div class="p-0 m-0">
    <p>Map Search</p>
    <v-divider/>
    <v-select
      label="Map Type"
      v-model="mapType"
      outlined
      :items="mapTypes"
      item-text="text"
      item-value="value"
    >
    </v-select>
    <v-text-field
      outlined
      v-model="searchTerm"
      label="Map Name"
    >
    </v-text-field>
    <v-btn
      color="success"
      @click="searchForMaps()"
      :loading="loading"
      :disabled="loading"
      text
    >
      Search
    </v-btn>
    <div v-if="searchResults">
      <v-card
        class="mx-auto"
        v-for="result in searchResults"
        :key="result.id"
      >
        <v-card-title>{{result.title}}</v-card-title>
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "MapBuilderMapSearchPanel",
  props: {
    appData: {
     type: Object,
      required: true
}
  },
  data: () => ({
    loading: false,
    searchTerm: null,
    searchResults: [],
    mapType: "personal",
    mapTypes: [
      {
        text: 'My Maps',
        value: 'personal'
      },
      {
        text: 'All Maps',
        value: "all"
      }
    ]
  }),
  methods: {
    searchForMaps(){
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
            console.log(res)
            this.searchResults = res.data.results;
          }
        });
    }
  }

};
</script>

<style>
</style>
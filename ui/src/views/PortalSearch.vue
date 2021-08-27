<template>
  <v-container class="pt-10">
    <v-row>
      <v-col cols="3"> filter area </v-col>
      <v-col cols="9">
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="model"
              :items="searchResults"
              :loading="loading"
              :search-input.sync="searchPortalApi"
              item-text="title"
              item-value="id"
              label="Search for maps, layers, apps, sites and more..."
              placeholder="Search for maps, layers, apps, sites and more..."
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" v-if="loading">
            <v-skeleton-loader
              v-for="n in 10"
              :key="n"
              type="article"
            ></v-skeleton-loader>
          </v-col>
          <v-col cols="12" v-if="searchResults">
            <v-card
              class="mx-auto"
              outlined
              v-for="result in searchResults"
              :key="result.id"
            >
              <search-card :result="result" />
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SearchCard from "../components/portal_search/SearchCard.vue";
export default {
  components: { SearchCard },
  name: "PortalSearch",
  data: () => ({
    loading: false,
    searchResults: [],
    model: null,
    searchPortalApi: null,
    searchTerm: null
  }),
  methods: {
    searchForData() {
      this.globalFunctions
        .httpRequest(
          "get",
          `${this.apiUrl}/api/v1/services/portal_search/?search_term=${this.searchTerm}`,
          undefined,
          true
        )
        .then((res) => {
          this.loading = false;
          if (res.status != 200) {
            this.alert = JSON.stringify(res.data);
          } else {
            this.searchResults = res.data.results;
          }
        });
    },
  },
  watch: {
    searchPortalApi(val) {
      if (val && val.length > 2) {
        this.loading = true;
        this.searchTerm = val
        this.searchForData();
      }
    },
  },
};
</script>

<style>
html {
  overflow: hidden;
}
</style>


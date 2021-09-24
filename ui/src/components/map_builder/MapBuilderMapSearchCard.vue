<template>
  <v-card class="my-2">
    <v-img
      :src="image"
      lazy-src="https://picsum.photos/id/11/100/60"
      height="150"
    >
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
    </v-img>

    <v-card-title>{{ map.title }}</v-card-title>

    <v-card-text>
      <div v-html="map.description"></div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        color="success"
        text
        @click="addToMap()"
        :disabled="loading"
        :loading="loading"
      >
        Add
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "MapBuilderLayersSearchCard",
  props: {
    map: {
      type: Object,
      required: true,
    },
    appData: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    image: "",
    loading: false,
  }),
  mounted() {
    this.globalFunctions
      .httpRequest(
        "get",
        `${this.apiUrl}/api/v1/maps/map_image/?map_id=${this.map.map_id}`,
        undefined,
        true
      )
      .then((res) => {
        this.image = res.data;
      });
  },
};
</script>

<style>
</style>
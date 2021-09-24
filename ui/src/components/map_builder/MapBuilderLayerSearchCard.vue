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

    <v-card-title>{{ layer.title }}</v-card-title>

    <v-card-text>
      <div v-html="layer.description"></div>
    </v-card-text>
    <v-card-actions>
      <v-btn color="success" text @click="addToMap()" :disabled="loading" :loading="loading"> Add </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "MapBuilderLayersSearchCard",
  props: {
    layer: {
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
    loading: false
  }),
  mounted() {
    if (this.layer.map_type === "esri") {
      this.image = this.layer.image;
    } else if (this.layer.map_type === "user_data") {
      this.globalFunctions
        .httpRequest(
          "get",
          `${this.apiUrl}/api/v1/tables/table_image/?table_id=${this.layer.table_id}`,
          undefined,
          true
        )
        .then((res) => {
          this.image = res.data;
        });
    } else if (this.layer.map_type === "map_layer") {
      this.image = `/images/maps/${this.layer.table_id}.png`;
    }
  },
  methods: {
    addToMap() {
      this.loading = true;
      if (this.layer.map_type === "user_data") {
        if (this.layer.geometry_type === "point") {
          this.layer.paint = {
            "circle-color": "#fff",
          };
        } else if (this.layer.geometry_type === "line") {
          this.layer.paint = {
            "line-color": "#fff",
          };
        } else if (this.layer.geometry_type === "polygon") {
          this.layer.border_paint = {
            "line-color": "#fff",
          };

          this.layer.fill_paint = {
            "fill-color": "#fff",
          };
        }
      } else if (this.layer.map_type === "map_layer") {
        if (this.layer.geometry_type === "point") {
          this.layer.paint = {
            "circle-color": "#fff",
          };
        } else if (this.layer.geometry_type === "line") {
          this.layer.paint = {
            "line-color": "#fff",
          };
        } else if (this.layer.geometry_type === "polygon") {
          this.layer.border_paint = {
            "line-color": "#000",
          };

          this.layer.fill_paint = {
            "fill-color": "#000",
            "fill-opacity": 0.8
          };
        }
      }
      this.globalFunctions
        .addLayerToMap(this.layer, this.appData, this.appData.map)
        .then(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style>
</style>
<template>
  <v-dialog v-model="appData.saveMapDialog" persistent max-width="1000">
    <v-card>
      <v-card-title>Save Map</v-card-title>
      <v-divider></v-divider>
      <v-form class="mt-5">
        <v-card-text>
          <v-text-field
            label="Name"
            outlined
            v-model="appData.title"
            autofocus
          ></v-text-field>
          <v-textarea
            label="Description"
            outlined
            v-model="appData.description"
            rows="2"
          >
          </v-textarea>
          <v-combobox
            label="Tags"
            outlined
            multiple
            chips
            v-model="appData.tags"
          >
          </v-combobox>
          <v-checkbox
            v-model="appData.searchable"
            label="Searchable?"
          ></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red"
            text
            @click="appData.saveMapDialog = false"
            :disabled="loading"
            :loading="loading"
          >
            Close
          </v-btn>
          <v-btn
            color="success"
            text
            :disabled="loading"
            :loading="loading"
            @click="saveMap()"
          >
            Save Map
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "MapBuilderModalSaveMap",
  props: {
    appData: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    loading: false,
  }),
  methods: {
    saveMap() {
      let formData = {
        basemap: this.appData.basemap,
        bounding_box: [],
        layers: this.appData.layers,
        notification_access_list: this.appData.notification_access_list,
        read_access_list: this.appData.read_access_list,
        write_access_list: this.appData.write_access_list,
        tags: this.appData.tags,
        title: this.appData.title,
        updated_username: this.appData.updated_username,
        username: this.appData.username,
      };
      this.alert = "";
      let httpRequest = "post";
      if (this.appData.map_id) {
        httpRequest = "put";
        formData.map_id = this.appData.map_id;
      }
      this.globalFunctions
        .httpRequest(
          httpRequest,
          `${this.apiUrl}/api/v1/maps/map/`,
          formData,
          true
        )
        .then((res) => {
          this.loading = false;
          if (res.status != 201) {
            if (res.data.non_field_errors) {
              this.alert = res.data.non_field_errors[0];
            } else {
              this.alert = JSON.stringify(res.data);
            }
          } else {
            document.title = `Mapping Portal | Map Builder - ${res.data.title}`;
            window.history.replaceState(
              null,
              null,
              `?map_id=${res.data.map_id}`
            );
            this.$set(this.appData, "alertColor", "green");
            this.$set(this.appData, "alert", "Your map has been saved!");
            this.appData.saveMapDialog = false;
          }
        });
    },
  },
};
</script>

<style>
</style>
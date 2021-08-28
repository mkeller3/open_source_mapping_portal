<template>
  <v-card class="mx-auto" outlined>
    <v-list-item three-line>
      <v-list-item-avatar tile size="100" color="grey"></v-list-item-avatar>
      <v-list-item-content>
        <a
          :href="'/portal_item/?id=' + result.id + '&type=' + result.slug"
          target="_blank"
          ><v-list-item-title class="text-h5 mb-1">
            {{ result.title }}
          </v-list-item-title></a
        >
        <v-list-item-subtitle
          >{{result.type}} by {{ result.created_by }}</v-list-item-subtitle
        >
        <div class="">{{ result.description }}</div>
        <v-list-item-subtitle
          >Updated:
          {{ result.updated_date }}</v-list-item-subtitle
        >
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>

<script>
import moment from "moment";

export default {
  name: "SearchCard",
  data: () => ({
    image: null,
  }),
  props: {
    result: Object,
  },
  mounted() {
    this.result.updated_date = moment(this.result.updated_date).format(
      "MMMM DD YYYY hh:mm a"
    );
    this.globalFunctions
      .httpRequest(
        "get",
        `${this.apiUrl}/api/v1/${this.result.slug}s/${this.result.slug}_image/?${this.result.slug}_id=${this.result.id}`,
        undefined,
        false
      )
      .then((res) => {
        if (res.status === 200) {
          this.image = res.data;
        }
      });
  },
};
</script>

<style>
</style>
<template>
<v-alert class="app-alert mx-auto" v-if="appData.alert" :color="appData.alertColor" dark dismissible>
    {{appData.alert}}
</v-alert>
</template>

<script>
export default {
  name: "Alert",
  props: {
    appData: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>

.app-alert {
    position: relative;
    z-index: 7;
    top: 20px;
    width: 80%;
}

</style>

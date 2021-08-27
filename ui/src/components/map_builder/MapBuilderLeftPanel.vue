<template>
  <div
    class="map-builder-left-panel pa-3"
    v-show="appData.openLeftPanel"
  >
    hey there
  </div>
</template>

<script>
export default {
  name: "MapBuilderLeftPanel",
  props: {
    appData: Object,
  },
};
</script>

<style>

.map-builder-left-panel{
    min-width: 20%;
    height: 100%;
    overflow-x: hidden; 
    overflow-y: auto;
}

</style>
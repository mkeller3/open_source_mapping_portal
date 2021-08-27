<template>
  <div
    class="map-builder-right-panel pa-3"
    v-show="appData.openRightPanel"
  >
    hey there
  </div>
</template>

<script>
export default {
  name: "MapBuilderRightPanel",
  props: {
    appData: Object,
  },
};
</script>

<style>

.map-builder-right-panel{
    min-width: 20%;
    height: 100%;
    overflow-x: hidden; 
    overflow-y: auto;
}

</style>
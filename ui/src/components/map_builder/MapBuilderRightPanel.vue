<template>
  <div class="map-builder-right-panel pa-3" v-show="appData.openRightPanel">
    <map-builder-layer-information-panel
      :appData="appData"
      v-if="this.appData.openRightIcon === 'information'"
    />
    <map-builder-layer-style-panel
      :appData="appData"
      v-if="this.appData.openRightIcon === 'style'"
    />
    <map-builder-layer-filter-panel
      :appData="appData"
      v-if="this.appData.openRightIcon === 'filter'"
    />
    <map-builder-layer-popups-panel
      :appData="appData"
      v-if="this.appData.openRightIcon === 'popups'"
    />
    <map-builder-layer-widgets-panel
      :appData="appData"
      v-if="this.appData.openRightIcon === 'widgets'"
    />
    <map-builder-layer-statistics-panel
      :appData="appData"
      v-if="this.appData.openRightIcon === 'statistics'"
    />
    <map-builder-layer-search-panel
      :appData="appData"
      v-if="this.appData.openRightIcon === 'search'"
    />
  </div>
</template>

<script>
import MapBuilderLayerFilterPanel from "./MapBuilderLayerFilterPanel.vue";
import MapBuilderLayerInformationPanel from "./MapBuilderLayerInformationPanel.vue";
import MapBuilderLayerPopupsPanel from "./MapBuilderLayerPopupsPanel.vue";
import MapBuilderLayerSearchPanel from "./MapBuilderLayerSearchPanel.vue";
import MapBuilderLayerStatisticsPanel from "./MapBuilderLayerStatisticsPanel.vue";
import MapBuilderLayerStylePanel from "./MapBuilderLayerStylePanel.vue";
import MapBuilderLayerWidgetsPanel from './MapBuilderLayerWidgetsPanel.vue';
export default {
  components: {
    MapBuilderLayerInformationPanel,
    MapBuilderLayerStylePanel,
    MapBuilderLayerFilterPanel,
    MapBuilderLayerPopupsPanel,
    MapBuilderLayerStatisticsPanel,
    MapBuilderLayerSearchPanel,
    MapBuilderLayerWidgetsPanel,
  },
  name: "MapBuilderRightPanel",
  props: {
    appData: {
     type: Object,
      required: true
}
  },
};
</script>

<style>
.map-builder-right-panel {
  min-width: 20%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
}
</style>
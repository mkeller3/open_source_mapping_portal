<template>
  <div class="map-builder-left-panel pa-3" v-show="appData.openLeftPanel">
    <map-builder-basemap-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'basemaps'"
    />
    <map-builder-analysis-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'analysis'"
    />
    <map-builder-draw-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'draw'"
    />
    <map-builder-help-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'help'"
    />
    <map-builder-layers-search-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'layers'"
    />
    <map-builder-legend-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'legend'"
    />
    <map-builder-map-search-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'existing_maps'"
    />
    <map-builder-query-data-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'query_data'"
    />
    <map-builder-settings-panel
      :appData="appData"
      v-if="this.appData.openLeftIcon === 'settings'"
    />
    <map-builder-modal-save-map :appData="appData"/>
  </div>
</template>

<script>
import MapBuilderAnalysisPanel from "./MapBuilderAnalysisPanel.vue";
import MapBuilderBasemapPanel from "./MapBuilderBasemapPanel.vue";
import MapBuilderDrawPanel from "./MapBuilderDrawPanel.vue";
import MapBuilderHelpPanel from "./MapBuilderHelpPanel.vue";
import MapBuilderLayersSearchPanel from "./MapBuilderLayersSearchPanel.vue";
import MapBuilderLegendPanel from "./MapBuilderLegendPanel.vue";
import MapBuilderMapSearchPanel from "./MapBuilderMapSearchPanel.vue";
import MapBuilderModalSaveMap from './MapBuilderModalSaveMap.vue';
import MapBuilderQueryDataPanel from "./MapBuilderQueryDataPanel.vue";
import MapBuilderSettingsPanel from "./MapBuilderSettingsPanel.vue";

export default {
  components: {
    MapBuilderBasemapPanel,
    MapBuilderAnalysisPanel,
    MapBuilderDrawPanel,
    MapBuilderHelpPanel,
    MapBuilderLayersSearchPanel,
    MapBuilderLegendPanel,
    MapBuilderMapSearchPanel,
    MapBuilderQueryDataPanel,
    MapBuilderSettingsPanel,
    MapBuilderModalSaveMap,
  },
  name: "MapBuilderLeftPanel",
  props: {
    appData: {
     type: Object,
      required: true
}
  },
};
</script>

<style>
.map-builder-left-panel {
  min-width: 20%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
}
</style>
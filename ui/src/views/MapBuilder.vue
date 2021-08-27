<template>
  <v-container fluid class="d-flex my-0 py-0 px-0 h-100">
    <v-navigation-drawer fluid expand-on-hover permanent>
      <v-row class="fill-height" no-gutters fluid>
        <v-navigation-drawer
          dark
          expand-on-hover
          permanent
          mini-variant
          mini-variant-width="156"
        >
          <v-list dense nav>
            <v-list-item
              v-for="item in left_nav_items"
              :key="item.title"
              link
              @click="iconClick(item, 'left')"
            >
              <v-list-item-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>

              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-row>
    </v-navigation-drawer>
    <map-builder-left-panel :appData="appData" />
    <v-col align-self="auto" class="map-panel">
      <Map :appData="appData" />
    </v-col>
    <map-builder-right-panel :appData="appData" />
    <v-navigation-drawer fluid expand-on-hover permanent right>
      <v-row class="fill-height" no-gutters fluid>
        <v-navigation-drawer
          dark
          expand-on-hover
          permanent
          mini-variant
          mini-variant-width="156"
        >
          <v-list dense nav>
            <v-list-item
              v-for="item in right_nav_items"
              :key="item.title"
              link
              @click="iconClick(item, 'right')"
            >
              <v-list-item-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>

              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-row>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import Map from "@/components/base/Map.vue";
import MapBuilderLeftPanel from "../components/map_builder/MapBuilderLeftPanel.vue";
import MapBuilderRightPanel from "../components/map_builder/MapBuilderRightPanel.vue";

export default {
  components: {
    Map,
    MapBuilderLeftPanel,
    MapBuilderRightPanel,
  },
  name: "MapBuilder",
  data: () => ({
    appData: {
      latitude: 40,
      longitude: -96,
      zoom: 3,
      basemap: "light",
      openRightIcon: undefined,
      openRightPanel: undefined,
      openLeftIcon: undefined,
      openLeftPanel: undefined,
    },
    left_nav_items: [
      {
        title: "Save Map",
        icon: "mdi-content-save",
        slug: "save_map",
        openPanel: false,
      },
      {
        title: "New Map",
        icon: "mdi-map-plus",
        slug: "new_map",
        openPanel: false,
      },
      {
        title: "Open Existing Maps",
        icon: "mdi-map-search",
        slug: "existing_maps",
        openPanel: true,
      },
      {
        title: "Import Data",
        icon: "mdi-plus-box-multiple",
        slug: "import_data",
        openPanel: false,
      },
      {
        title: "Map Layers",
        icon: "mdi-layers-triple",
        slug: "layers",
        openPanel: true,
      },
      {
        title: "Basemaps",
        icon: "mdi-earth",
        slug: "basemaps",
        openPanel: true,
      },
      {
        title: "Query Data",
        icon: "mdi-search-web",
        slug: "query_data",
        openPanel: true,
      },
      {
        title: "Analysis",
        icon: "mdi-gauge",
        slug: "analysis",
        openPanel: true,
      },
      {
        title: "Drawing",
        icon: "mdi-draw",
        slug: "draw",
        openPanel: true,
      },
      {
        title: "Legend",
        icon: "mdi-map-legend",
        slug: "legend",
        openPanel: true,
      },
      {
        title: "Address Search",
        icon: "mdi-google-street-view",
        slug: "address_search",
        openPanel: true,
      },
      {
        title: "Print",
        icon: "mdi-printer",
        slug: "print",
        openPanel: false,
      },
      {
        title: "Settings",
        icon: "mdi-cog",
        slug: "settings",
        openPanel: true,
      },
      {
        title: "Help",
        icon: "mdi-map-marker-question-outline",
        slug: "help",
        openPanel: true,
      },
    ],
    right_nav_items: [
      {
        title: "Information",
        icon: "mdi-information",
        slug: "information",
        openPanel: true,
      },
      {
        title: "Style",
        icon: "mdi-tune",
        slug: "style",
        openPanel: true,
      },
      {
        title: "Filter",
        icon: "mdi-filter",
        slug: "filter",
        openPanel: true,
      },
      {
        title: "Table",
        icon: "mdi-table",
        slug: "table",
        openPanel: false,
      },
      {
        title: "Popups",
        icon: "mdi-message-text-outline",
        slug: "popups",
        openPanel: true,
      },
      {
        title: "Search",
        icon: "mdi-layers-search",
        slug: "search",
        openPanel: true,
      },
      {
        title: "Widgets",
        icon: "mdi-chart-scatter-plot-hexbin",
        slug: "widgets",
        openPanel: true,
      },
      {
        title: "Statistics",
        icon: "mdi-android-studio",
        slug: "statistics",
        openPanel: true,
      },
    ],
    links: ["Home", "Contacts", "Settings"],
    mini: true,
    drawer: true,
  }),
  mounted(){
    document.title = 'Mapping Portal | Map Builder'
    if(this.$route.query.map_id){
        console.log('old map')
    }
  },
  methods: {
    iconClick(icon, side) {
      if (side === "left") {
        if (icon.openPanel) {
          if (this.appData.openLeftIcon === icon.slug) {
            this.$set(this.appData, "openLeftPanel", false);
          } else {
            this.$set(this.appData, "openLeftPanel", true);
          }
          this.$set(this.appData, "openLeftIcon", icon.slug);

          if (
            this.appData.openLeftIcon === icon.slug &&
            this.appData.openLeftPanel === false
          ) {
            this.$set(this.appData, "openLeftIcon", undefined);
          }
        } else {
          if (this.appData.openLeftIcon === icon.slug) {
            this.$set(this.appData, "openLeftIcon", undefined);
          } else {
            this.$set(this.appData, "openLeftIcon", icon.slug);
            this.$set(this.appData, "openLeftPanel", false);
          }
        }
      } else if (side === "right") {
        if (icon.openPanel) {
          if (this.appData.openRightIcon === icon.slug) {
            this.$set(this.appData, "openRightPanel", false);
          } else {
            this.$set(this.appData, "openRightPanel", true);
          }
          this.$set(this.appData, "openRightIcon", icon.slug);

          if (
            this.appData.openRightIcon === icon.slug &&
            this.appData.openRightPanel === false
          ) {
            this.$set(this.appData, "openRightIcon", undefined);
          }
        } else {
          if (this.appData.openRightIcon === icon.slug) {
            this.$set(this.appData, "openRightIcon", undefined);
          } else {
            this.$set(this.appData, "openRightIcon", icon.slug);
            this.$set(this.appData, "openRightPanel", false);
          }
        }
      }
    },
  },
};
</script>

<style>
.h-100 {
  height: 100%;
}

html {
  overflow: hidden;
}

.map-panel {
  padding: 0 !important;
}
</style>

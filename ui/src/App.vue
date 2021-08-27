<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="mr-3"
      ></v-app-bar-nav-icon>
      <h2>Mapping Portal</h2>
    </v-app-bar>
    <v-main>
      <router-view />
      <v-navigation-drawer v-model="drawer" absolute temporary>
        <v-list-item>
          <v-list-item-avatar>
            <v-img src="https://randomuser.me/api/portraits/men/78.jpg"></v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>Name Here</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>
        <v-list dense>
          <v-list-item
            v-for="url in urls"
            :key="url.title"
            link
            :href="url.url"
          >
            <v-list-item-icon>
              <v-icon>{{ url.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ url.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data: () => ({
    drawer: false,
    urls: [
      {
        title: "Home",
        icon: "mdi-home",
        url: "/",
      },
      {
        title: "Map Builder",
        icon: "mdi-map-outline",
        url: "/map_builder/",
      },
    ],
  }),
  methods:{
    goToUrl(link){
      window.open(link)
    }
  }
};
</script>

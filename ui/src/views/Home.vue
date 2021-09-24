<template>
<v-container fluid class="m-0 p-0">
    <section class="m-0 p-0">
      <v-parallax :src="imageLink.sub_main" height="600">
        <v-layout column align-center justify-center class="white--text">
          <h1
            class="white--text mb-2 display-1 text-xs-center"
            style="font-weight: 900; text-shadow: 1px 1px #000000"
          >
            Open Source Mapping Portal
          </h1>
          <div
            class="white--text subheading mb-3 text-xs-center"
            style="font-weight: 900; text-shadow: 1px 1px #000000"
          >
            Find the answer to where
          </div>
          <v-btn class="secondary">
            Get Started
          </v-btn>
        </v-layout>
      </v-parallax>
    </section>

    <!-- <section>
      <v-layout column wrap class="my-5" align-center>
        <v-flex xs12 sm4 class="my-3">
          <div class="text-xs-center">
            <h2 class="headline">The best way to share your amazing stuff</h2>
            <span class="subheading">
              No more restrictions, no more limits
            </span>
          </div>
        </v-flex>
        <v-flex xs12>
          <v-container grid-list-xl>
            <v-layout row wrap align-center>
              <v-flex xs12 md4>
                <v-card class="elevation-0 transparent">
                  <v-card-text class="text-center">
                    <v-icon x-large>mdi-earth</v-icon
                    >
                  </v-card-text>
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center">Reach the world</div>
                  </v-card-title>
                  <v-card-text>
                    Show your stuff to the whole community of Endorfine not only
                    to your mum or your friends. We love making good content
                    viral. In this moment Endorfine is used by artists who are
                    not famous but that want to share their works to the world.
                    Unfortunately with other social networks this is hard, slow
                    and sometime expensive.
                  </v-card-text>
                </v-card>
              </v-flex>
              <v-flex xs12 md4>
                <v-card class="elevation-0 transparent">
                  <v-card-text class="text-center">
                    <v-icon x-large>mdi-flash</v-icon
                    >
                  </v-card-text>
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline">Fast feedback</div>
                  </v-card-title>
                  <v-card-text>
                    Time is important, we don't want you to waste it. Here you
                    can get a massive feedback from real users in minutes. And
                    if your stuff is appreciated you won't only get positive
                    feedback but also lovely and sincere fans
                  </v-card-text>
                </v-card>
              </v-flex>
              <v-flex xs12 md4>
                <v-card class="elevation-0 transparent">
                  <v-card-text class="text-center">
                    <v-icon x-large>mdi-account-group</v-icon
                    >
                  </v-card-text>
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center">
                      Create new connections
                    </div>
                  </v-card-title>
                  <v-card-text>
                    Imagine if you can directly speak with the world's
                    population. Don't you think it would be easier to find nice
                    people to interact with? Endorfine is both local and global
                    and help you to connect without limitations with people from
                    your city, your state and your universe!
                  </v-card-text>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </section>

    <section>
      <v-parallax :src="imageLink.main" height="380">
        <v-layout column align-center justify-center>
          <div class="headline white--text mb-3 text-xs-center">
            Endorfine is a social network that allows everyone to reach a huge
            audience with a tap
          </div>
          <em
            >With the power of Endorfine you don't need to be famous or post
            pics of cute cats in order to get visibility</em
          >
          <v-btn class="blue lighten-2 mt-5" dark large href="/pre-made-themes">
            Get more info
          </v-btn>
        </v-layout>
      </v-parallax>
    </section>

    <section>
      <v-container grid-list-md>
        <v-layout row wrap>
          <v-flex xs12 text-xs-center class="mt-5">
            <div class="headline">Are you amazed? Stay tuned!</div>
            <br />
            <div>
              We are lunching the beta in a few time. If you want to be one of
              the first Endorfine users we will email you as soon as we're
              ready. In the beginning only few people will test before the
              launch. Let us know how Endorfine will help you!
            </div>
          </v-flex>
          <v-flex xs8 offset-xs2>
            <v-card class="elevation-0 transparent">
              <v-card-text>
                <v-flex xs12 v-if="!subscribed">
                  <v-text-field
                    box
                    label="Email address"
                    :rules="emailRules"
                    v-model="email"
                    hint="Enter your email!"
                    persistent-hint
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 v-if="!subscribed">
                  <v-text-field
                    box
                    multi-line
                    label="Bio and curiosities"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 class="text-xs-center" v-if="!subscribed">
                  <v-btn
                    class="blue lighten-2 mb-5"
                    dark
                    large
                    @click="subscribe"
                    >Get in touch</v-btn
                  >
                </v-flex>
                <v-flex xs12 class="text-xs-center" v-if="subscribed">
                  <v-btn class="green lighten-2 mb-5" dark large
                    >Welcome on board!</v-btn
                  >
                </v-flex>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </section> -->

</v-container>
</template>

<script>
export default {
  name: "Home",
  data: () => ({
    imageLink: {
      main: "/images/home.png",
      sub_main: "/images/home.png",
      social_cover: "/images/home.png",
    },
  }),
};
</script>

<style scoped>
.container{
  padding: 0;
}
</style>

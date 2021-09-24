<template>
  <v-form v-model="valid">
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary" outlinedZ>
              <v-toolbar-title>Sign In</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field
                  prepend-icon="mdi-account"
                  label="Username"
                  outlined
                  v-model="username"
                  :rules="genericRules"
                  autofocus
                ></v-text-field>
                <v-text-field
                  prepend-icon="mdi-at"
                  label="Email"
                  outlined
                  v-model="email"
                  :rules="emailRules"
                  type="email"
                ></v-text-field>
                <v-text-field
                  id="password"
                  prepend-icon="mdi-lock"
                  label="Password"
                  type="password"
                  outlined
                  v-model="password"
                  :rules="genericRules"
                ></v-text-field>
              </v-form>
              <v-alert
                v-if="alert"
                border="top"
                colored-border
                close-text="Close Alert"
                color="red"
                dismissible
              >
                {{ alert }}
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="success"
                :loading="loading"
                :disabled="loading || !valid"
                @click="login()"
                text
              >
                Login</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
export default {
  name: "Register",
  data: () => ({
    username: null,
    password: null,
    email: null,
    loading: false,
    valid: false,
    alert: "",
    emailRules: [
      (v) => !!v || "E-mail is required",
      (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
    ],
    genericRules: [(v) => !!v || "Field is required"],
  }),
  methods: {
    login() {
      this.loading = true;
      let formData = {
        username: this.username,
        password: this.password,
        email: this.email,
      };
      this.alert = "";
      this.globalFunctions
        .httpRequest(
          "post",
          `${this.apiUrl}/api/v1/register/register_user/`,
          formData
        )
        .then((res) => {
          console.log(res);
          if (res.status != 201) {
            this.loading = false;
            if (res.data.non_field_errors) {
              this.alert = res.data.non_field_errors[0];
            } else if (res.data.username) {
              this.alert = res.data.username[0];
            } else {
              this.alert = JSON.stringify(res.data);
            }
          } else {
            this.globalFunctions
              .httpRequest(
                "post",
                `${this.apiUrl}/api/v1/authentication/get_token/`,
                formData
              )
              .then((res) => {
                this.loading = false;
                if (res.status != 200) {
                  if (res.data.non_field_errors) {
                    this.alert = res.data.non_field_errors[0];
                  } else {
                    this.alert = JSON.stringify(res.data);
                  }
                } else {
                  localStorage.setItem(
                    "mapping_portal_access_token",
                    res.data.token
                  );
                }
                window.location.href = "/"
              });
          }
        });
    },
  },
};
</script>

<style>
</style>
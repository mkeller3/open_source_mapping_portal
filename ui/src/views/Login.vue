<template>
  <v-form v-model="valid">
    <v-container>
      <v-row>
        <v-col
          cols="12"
        >
          <v-text-field
            v-model="username"
            label="Username"
            autofocus
            required
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
        >
          <v-text-field
            v-model="password"
            label="Password"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12">
            <v-btn 
                color="success"
                :loading="loading"
                :disabled="loading"
                @click="login()"
            >
            Login</v-btn>
        </v-col>
        <v-alert
            v-if="alert"
            border="left"
            close-text="Close Alert"
            color="red"
            dark
            dismissible
        >
            {{alert}}
        </v-alert>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
    name: 'Login',
    data: () => ({
        username: null,
        password: null,
        loading: false,
        valid: false,
        alert: ''
    }),
    methods: {
        login(){
            this.loading = true;
            let formData = {
               username: this.username,
               password: this.password 
            }
            this.globalFunctions.httpRequest('post', `${this.apiUrl}/api/v1/authentication/get_token/`, formData).then((res) => {
                this.loading = false;
                if(res.status != 200){
                    this.alert = JSON.stringify(res.data)
                }else{
                    localStorage.setItem('mapping_portal_access_token', res.data.token)
                }
            })
        }
    }
}
</script>

<style>

</style>
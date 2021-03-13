<template>
  <v-footer id="dashboard-core-footer">
    <v-container>
      <v-row class="d-flex justify-center">
        <v-col cols="auto" class="lime--text text--darken-3">MOVLOG</v-col>
        <v-col cols="auto">Personal movie watch diary.</v-col>
        <v-col cols="auto">created by LeoPanda.</v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {
  name: "DashboardCoreFooter",
};
</script>

<style lang="sass">
#dashboard-core-footer
  a
    font-size: .825rem
    font-weight: 500
    text-decoration: none
    text-transform: uppercase
</style>

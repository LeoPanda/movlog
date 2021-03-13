<template>
  <!--メインビュー-->
  <v-main>
    <router-view />
    <DashboardCoreFooter />
  </v-main>
</template>

<script>
export default {
  name: "DashboardCoreView",

  components: {
    DashboardCoreFooter: () => import("./Footer"),
  },
};
</script>

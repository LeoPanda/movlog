<template>
  <router-view />
</template>

<script>
import { loadInitialData } from "@/js/loadControl";
import { setSortOrder } from "@/js/sort";
export default {
  name: "App",
  created() {
    loadInitialData();
    setSortOrder("dateDsc");
  },
};
</script>

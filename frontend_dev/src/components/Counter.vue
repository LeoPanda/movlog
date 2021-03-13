<template>
  <!-- ダッシュボード用統計カウンタカード -->
  <v-row justify-center>
    <div>
      <!--経過年数 -->
      <v-card-subtitle dense class="pb-0 mb-0"
        >during<v-avatar color="blue lighten-2" size="24"
          ><h4 class="mx-1">{{ getYearRange }}</h4></v-avatar
        >years,</v-card-subtitle
      >
      <!-- 鑑賞件数 -->
      <v-card-title class="my-0 py-0"
        >watched
        <h2 class="mx-1">{{ getNumOfWatchs }}</h2>
        times
      </v-card-title>
      <!-- 鑑賞劇場数 -->
      <v-card-subtitle class="d-flex align-center py-0 my-0 justify-center">
        including
        <v-avatar color="amber lighten-2" size="40"
          ><h3 class="mx-1">{{ getNumOfAtTheater }}</h3></v-avatar
        >
        at
        <v-avatar class="d-flex" color="lime lighten-2" size="32"
          ><h3 class="mx-1">{{ getNumOfTheaters }}</h3> </v-avatar
        >theaters,</v-card-subtitle
      >
      <!-- TV鑑賞数 -->
      <v-card-text class="d-flex align-center pt-0 mt-0 justify-end">
        and
        <v-avatar color="pink lighten-2" size="30"
          ><h3 class="mx-1">{{ getNumOfOnTv }}</h3></v-avatar
        >on TV.
      </v-card-text>
    </div>
  </v-row>
</template>

<script>
import { aggTheater, getYearRange } from "@/js/statistics.js";
export default {
  name: "Counter",
  props: ["events"],
  computed: {
    getNumOfWatchs() {
      return this.events.length;
    },
    getNumOfOnTv() {
      return this.events.filter((event) => event["on_tv"] == true).length;
    },
    getNumOfAtTheater() {
      return this.events.filter((event) => event["on_tv"] != true).length;
    },
    getNumOfTheaters() {
      return aggTheater(this.events).length;
    },
    getYearRange() {
      return getYearRange(this.events);
    },
  },
};
</script>
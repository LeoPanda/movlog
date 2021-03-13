<template>
  <!--ダッシュボードメイン画面-->
  <v-container id="dashboard" fluid tag="section">
    <v-row class="d-flex justify-center" v-if="!loading">
      <!--総数表示-->
      <v-col cols="auto">
        <v-card>
          <!--カウンターカード-->
          <counter :events="events" class="mx-5" />
          <!--劇場別バブルチャート-->
          <TheaterBubleChart />
        </v-card>
      </v-col>
      <!--最新映画-->
      <v-col cols="auto">
        <MovieTitleCard :event="events[0]" class="mx-5" />
      </v-col>
      <!--TVプロバイダ別円チャート-->
      <v-col cols="auto">
        <v-card>
          <BinaryBarChart />
          <TvProvidersPie />
        </v-card>
      </v-col>
      <v-col cols="auto">
        <!--ランキングチャート-->
        <v-card max-height="470px" class="mx-auto">
          <RateRanking />
        </v-card>
      </v-col>
      <v-col cols="auto">
        <!--月別鑑賞数チャート-->
        <v-card max-height="470px" class="mx-auto">
          <CounterBarChart />
        </v-card>
      </v-col>
      <v-col cols="auto">
        <!--劇場一覧-->
        <v-card max-height="470px" class="mx-auto">
          <LocationList />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Dashboard",
  computed: {
    ...mapState(["events", "loading", "searchWord"]),
  },
  mounted() {
    this.$store.commit("SET_SEARCH_WORD", "");
    this.$store.commit("SET_PAGE_START_INDEX", 0);
  },
  components: {
    Counter: () => import("@/components/Counter"),
    MovieTitleCard: () => import("@/components/MovieTitleCard"),
    CounterBarChart: () => import("@/charts/CounterBarChart.js"),
    TheaterBubleChart: () => import("@/charts/TheaterBubleChart.js"),
    TvProvidersPie: () => import("@/charts/TvProvidersPie"),
    BinaryBarChart: () => import("@/charts/BinaryBarChart"),
    LocationList: () => import("@/components/LocationList"),
    RateRanking: () => import("@/charts/RateRanking"),
  },
};
</script>
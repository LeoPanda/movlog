<template>
  <!-- 鑑賞映画一覧（カード表示）-->
  <v-container fluid>
    <div ref="top" />
    <v-row class="d-flex justify-center mb-6">
      <v-col v-for="event in displayedEvents" :key="event.id" cols="auto">
        <!-- カードコンポーネント -->
        <MovieTitleCard :event="event" />
      </v-col>
    </v-row>
    <!-- ページング -->
    <v-pagination
      v-model="pagenation.num"
      :length="pagenation.length"
      @input="paging"
    ></v-pagination>
  </v-container>
</template>

<script>
import viewmixin from "@/views/ViewMixIn.js";

export default {
  name: "Cards",
  components: {
    MovieTitleCard: () => import("@/components/MovieTitleCard"),
  },
  mixins: [viewmixin],
};
</script>
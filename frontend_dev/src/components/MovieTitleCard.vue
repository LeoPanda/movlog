<template>
  <!-- 鑑賞映画表示用カードコンポーネント -->
  <v-card class="my-4">
    <v-row class="ml-1">
      <!--テレビで鑑賞バッジ-->
      <TvBadge :isOnTv="isOnTv">
        <!-- タイトル -->
        <v-card-title
          v-text="trimedTitle"
          class="pa-0 ma-0 subtitle-2"
        ></v-card-title>
      </TvBadge>
    </v-row>
    <v-row class="ml-1">
      <!-- 鑑賞日付 -->
      <v-col class="pa-0 mx-0 mt-1">
        <v-card-subtitle class="pa-0 ma-0 caption">
          {{ getStdDate(event.start.date_time) }}
        </v-card-subtitle>
      </v-col>
      <v-col class="pa-0 ma-0">
        <!-- 劇場スクリーンのタイプ -->
        <SelectableItems
          v-if="!event['on_tv']"
          :event="event"
          :editMode="false"
          itemKey="screen_type"
          :multiple="true"
        />
      </v-col>
    </v-row>
    <v-row class="ml-1">
      <!-- 劇場名/プロバイダ名 -->
      <v-col class="pa-0 ma-0">
        <v-card-subtitle class="pa-0 ma-0 caption">
          {{ getThearter }}
        </v-card-subtitle>
      </v-col>
    </v-row>
    <v-row>
      <!-- ポスターアート -->
      <v-img
        max-width="182"
        max-height="268"
        class="white--text ml-5 mr-5 mb-0 pa-0"
        :src="getImgUrl(event['title_img'], 'middle')"
      >
        <template v-slot:default>
          <v-btn
            class="transparent"
            width="182"
            height="268"
            :to="'/pages/card/' + event.id"
          />
        </template>
      </v-img>
    </v-row>
    <v-row class="mx-0">
      <!-- レーティング -->
      <RatingBar :event="event" />
    </v-row>
  </v-card>
</template>
<script>
import { getStdDate } from "@/js/dateUtil";
import { getImgUrl } from "@/js/imgSizeControl";
export default {
  name: "MovieTitleCard",
  props: ["event"],
  components: {
    RatingBar: () => import("./parts/RatingBar"),
    SelectableItems: () => import("./parts/SelectableItems"),
    TvBadge: () => import("./parts/TvBadge"),
  },
  data() {
    return { trimedTitle: "" };
  },
  computed: {
    isOnTv() {
      return this.event["on_tv"] ? true : false;
    },
    getThearter() {
      return this.event["on_tv"]
        ? this.event["streaming_provider"]
        : this.event["location"].split(",")[0];
    },
  },
  methods: {
    getStdDate,
    getImgUrl,
  },
  mounted() {
    if (this.event.title.length > 13) {
      //長過ぎる映画タイトル名をトリミング
      this.trimedTitle = this.event.title.substring(0, 11) + "・・";
    } else {
      this.trimedTitle = this.event.title;
    }
  },
};
</script>
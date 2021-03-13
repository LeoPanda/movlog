<template>
  <v-list-item @click.stop="getLink(event.id)" class="mx-0 my-2">
    <!--ポスターイメージ-->
    <v-subheader>
      <!--テレビで鑑賞バッジ-->
      <tvBadge :isOnTv="isOnTv" :small="true">
        <!--ポスターアート-->
        <v-img
          max-height="64"
          max-width="48"
          :src="getImgUrl(event['title_img'], 'small')"
        />
      </tvBadge>
    </v-subheader>
    <v-list-item-content class="mx-0">
      <!--タイトル-->
      <v-list-item-title v-text="event.title" />
      <!--レーティングバー-->
      <RatingBar :event="event" :isNum="true" @openRate="openRate" />
    </v-list-item-content>
    <v-list-item-content v-if="getVisible">
      <!--劇場-->
      <v-list-item-title
        v-if="event['location'] && !event['on_tv']"
        v-text="event.location.split(',')[0]"
      ></v-list-item-title>
      <!---配信プロバイダ-->
      <v-list-item-title
        v-if="event['streaming_provider']"
        v-text="event.streaming_provider"
      ></v-list-item-title>
      <!--鑑賞日-->
      <v-list-item-title
        v-text="getStdDate(event.start.date_time)"
      ></v-list-item-title>
    </v-list-item-content>
    <!--削除ボタン-->
    <v-list-item-action class="mx-0">
      <v-btn icon small @click="setTrash(event.id)">
        <v-icon>mdi-trash-can</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>
<script>
import { getStdDate } from "@/js/dateUtil";
import { getImgUrl } from "@/js/imgSizeControl";
export default {
  name: "ItemLine",
  props: ["event", "onTrash"],
  components: {
    TvBadge: () => import("./parts/TvBadge"),
    RatingBar: () => import("./parts/RatingBar"),
  },
  data() {
    return {
      isRateOpened: false,
    };
  },
  computed: {
    isOnTv() {
      return this.event["on_tv"] ? true : false;
    },
    getVisible() {
      return this.$vuetify.breakpoint.name == "xs" ? false : true;
    },
  },
  methods: {
    getStdDate,
    getImgUrl,
    getLink(id) {
      //削除ボタンが押されていない、かつレート入力中でなければ該当のイベントを表示する
      if (this.onTrash == false && this.isRateOpened == false) {
        this.$router.push("../pages/card/" + id);
      }
    },
    setTrash(id) {
      //削除ボタンが押された場合、該当するeventのIDをsetOnTrashへ返す
      this.$emit("setOnTrash", id);
    },
    openRate(value) {
      //レート入力のオーバレイを操作する
      this.isRateOpened = value;
    },
  },
};
</script>
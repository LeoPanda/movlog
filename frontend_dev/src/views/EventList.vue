<template>
  <v-container fluid>
    <div ref="top" />
    <v-row class="d-flex justify-center mb-6">
      <v-list dense width="80%" height="auto">
        <!-- TIPS:keyの値に変更があると再描画される -->
        <v-list-item-group
          :v-model="null"
          color="primary"
          v-for="event in displayedEvents"
          :key="event.id"
        >
          <!-- 削除確認用オーバーレイ -->
          <v-overlay absolute v-if="event.id == onTrash">
            <v-card class="pl-5">
              このイベントを削除してよろしいですか？
              <v-btn icon @click="doTrash(event.id)"
                ><v-icon color="light-green">mdi-check-outline</v-icon></v-btn
              ><v-btn icon @click="onTrash = false"
                ><v-icon color="red">mdi-close-outline</v-icon></v-btn
              >
            </v-card>
          </v-overlay>
          <!-- イベント表示行コンポーネント -->
          <ItemLine
            :event="event"
            :onTrash="onTrash"
            @setOnTrash="setOnTrash"
          />
          <v-divider></v-divider>
        </v-list-item-group>
      </v-list>
    </v-row>
    <!--ページング-->
    <v-pagination
      v-model="pagenation.num"
      :length="pagenation.length"
      @input="paging"
    ></v-pagination>
  </v-container>
</template>

<script>
import viewmixin from "@/views/ViewMixIn.js";
import { setUploadItem } from "@/js/uploadControl";
import { ITEMS } from "@/js/serverDataItems";
export default {
  mixins: [viewmixin],
  components: {
    ItemLine: () => import("@/components/ItemLine"),
  },
  created() {
    //表示件数を増やす
    this.pageMultiple = true;
  },
  data() {
    return {
      onTrash: false,
    };
  },
  methods: {
    setOnTrash(id) {
      //ItemLineコンポーネントから返されたIDを削除予定にセットする
      this.onTrash = id;
    },
    doTrash(id) {
      //idで指定されたイベントを削除する
      this.events = this.getStoredEvent.filter((event) => event.id != id);
      this.paging(this.pagenation.num); //再描画
      this.$store.commit("SET_EVENTS", this.events);
      this.onTrash = false;
      setUploadItem(ITEMS.events);
    },
  },
};
</script>
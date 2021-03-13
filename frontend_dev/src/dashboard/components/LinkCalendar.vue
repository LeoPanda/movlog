
<template>
  <!--Google Calendarのデータリンクを制御するメニュー-->
  <v-container grid-list-xs>
    <v-row width="300" class="d-flex ml-0">
      <!--序文-->
      <v-col cols="auto">
        作品リストの最新鑑賞日以降のGoogleカレンダーを以下のキーワードで検索し、ヒットしたイベントを作品リストに反映します。
      </v-col>
    </v-row>
    <!--キーワードテーブル-->
    <v-row color="primary" width="300" class="d-flex ml-5">
      <TableList name="選択基準キーワード" table="keywords" />
    </v-row>
    <!--注意書き-->
    <v-col cols="auto">
      キーワードを変更した場合は上部バーのベルアイコンをクリックし、データを反映してからリンクを実行してください。
    </v-col>
    <!--リンク実行ボタン-->
    <v-row color="primary" width="300" class="d-flex ml-0">
      <v-col class="text-left" @click.stop="dialog = true">
        <v-btn color="accent" class="mr-0">
          googleカレンダーのデータをリンク
          <v-icon right> mdi-sync </v-icon></v-btn
        >
      </v-col>
      <!--確認ダイアログ-->
      <Confirm
        :openConfirm="dialog"
        :msgItems="[{ message: 'Googleカレンダーのデータをリンクします。' }]"
        confirmMsg="よろしいですか?"
        @do="goLink"
        @cancel="dialog = false"
      />
    </v-row>
  </v-container>
</template>

<script>
import { linkCalendar } from "@/js/loadControl";
export default {
  components: {
    TableList: () => import("@/dashboard/components/parts/TableList"),
    Confirm: () => import("@/dashboard/components/Confirm"),
  },
  data() {
    return { dialog: false };
  },
  methods: {
    goLink() {
      linkCalendar();
      this.dialog = false;
      this.$router.push("/");
    },
  },
};
</script>
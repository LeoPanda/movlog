
<template>
  <!--ローカルストレージをクリアしサーバーデータをリロードするメニュー-->
  <v-container grid-list-xs>
    <v-row width="300" class="d-flex ml-0">
      <!--序文-->
      <v-col cols="auto">
        ローカルストレージ上のデータを更新します。アイテムを選択してください。
      </v-col>
    </v-row>
    <!--Item選択-->
    <v-row color="primary" width="300" class="d-flex ml-5">
      <v-checkbox
        class="ma-2"
        v-model="storage_items"
        label="作品リスト(events)"
        value="events"
      ></v-checkbox>
      <v-checkbox
        class="ma-2"
        v-model="storage_items"
        label="劇場リスト(locations)"
        value="locations"
      ></v-checkbox>
      <v-checkbox
        class="ma-2"
        v-model="storage_items"
        label="固定値テーブル(tables)"
        value="tables"
      ></v-checkbox>
      <v-checkbox
        class="ma-2"
        v-model="storage_items"
        label="ユーザー情報(userInfo)"
        value="userInfo"
      ></v-checkbox>
    </v-row>
    <!--リンク実行ボタン-->
    <v-row color="primary" width="300" class="d-flex ml-0">
      <v-col class="text-left" @click.stop="dialog = true">
        <v-btn
          color="accent"
          class="mr-0"
          :disabled="this.storage_items.length == 0"
        >
          ローカルデータの更新
          <v-icon right> mdi-sync </v-icon></v-btn
        >
      </v-col>
      <!--確認ダイアログ-->
      <Confirm
        :openConfirm="dialog"
        :msgItems="[{ message: 'ローカルデータを更新します。' }]"
        confirmMsg="よろしいですか?"
        @do="goReload"
        @cancel="dialog = false"
      />
    </v-row>
  </v-container>
</template>

<script>
import { setMsg } from "@/js/msgSetter";
import { clearLocalStorage } from "@/js/localStorage";

export default {
  components: {
    Confirm: () => import("@/dashboard/components/Confirm"),
  },
  data() {
    return { dialog: false, storage_items: [] };
  },
  methods: {
    goReload() {
      /** サーバーデータをリロード */
      if (this.storage_items.length > 0) {
        this.storage_items.forEach((item) => {
          clearLocalStorage(item);
        });
        setMsg("ローカルデータを更新しました。", "success", "reload");
      }
      this.dialog = false;
      this.$router.push("/");
    },
  },
};
</script>
<style>
/*セレクタのチェックボックス表示 
(MovieDetailでglobalに非表示にしているため、ここで再設定)*/
.v-input--selection-controls__input {
  display: inline-flex !important;
}
</style>

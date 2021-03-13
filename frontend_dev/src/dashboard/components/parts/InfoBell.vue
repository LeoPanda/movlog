<template>
  <!--データ変更通知ベル-->
  <div>
    <!--ベルアイコン-->
    <v-btn icon fab @click.stop="openConfirm = true">
      <v-icon class="bell">mdi-bell-ring</v-icon>
    </v-btn>
    <!--アップロード確認ダイアログ -->
    <Confirm
      :openConfirm="openConfirm"
      confirmMsg="アップロードしますか？"
      :msgItems="uploadItems"
      @do="doUpload"
      @cancel="cancel"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";
import { setMsg } from "@/js/msgSetter";
import { uploadToServer } from "@/js/uploadControl";
export default {
  name: "InfoBell",
  components: {
    Confirm: () => import("@/dashboard/components/Confirm"),
  },
  data() {
    return {
      openConfirm: false,
    };
  },
  computed: {
    ...mapState(["uploadItems"]),
  },
  methods: {
    async doUpload() {
      this.openConfirm = false;
      const complete = await uploadToServer();
      if (complete) {
        setMsg("アップロードが完了しました。");
      } else {
        setMsg("エラーが発生しました。", "error");
      }
    },
    cancel() {
      this.openConfirm = false;
    },
  },
};
</script>

<style>
@import "./styles/bell.css";
</style>
<template>
  <!--メッセージ表示用ダイアログ-->
  <div class="text-center">
    <v-dialog
      v-model="display"
      persistent
      width="500px"
      transition="dialog-transition"
    >
      <v-alert :type="message.type" dense>
        <v-list color="secondary">
          <v-list-item>
            <v-list-item-content class="white--text">
              {{ message.text }}
            </v-list-item-content>
            <v-list-item-icon>
              <!--確認ボタン-->
              <v-btn icon @click="confirm">
                <v-icon color="light-green">mdi-check-outline</v-icon>
              </v-btn>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-alert>
    </v-dialog>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  computed: mapState(["message", "reload"]),
  data() {
    return { display: false };
  },
  mounted() {
    if ("text" in this.message) {
      this.display = true;
    }
  },
  methods: {
    confirm() {
      this.$store.commit("SET_MESSAGE", "");
      if (this.reload) {
        this.$router.go({ path: this.$router.currentRoute.path, force: true });
        this.$store.commit("SET_RELOAD", false);
      }
    },
  },
  watch: {
    message: {
      handler: function (value) {
        if (value["text"]) {
          this.display = true;
        } else {
          this.display = false;
        }
      },
      deep: true,
    },
  },
};
</script>
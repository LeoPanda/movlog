<template>
  <!--確認ダイアログ-->
  <v-dialog
    v-model="display"
    persistent
    max-width="500px"
    transition="dialog-transition"
  >
    <v-card>
      <v-list color="secondary">
        <v-list-item-group v-for="item in msgItems" :key="item.local">
          <v-list-item>
            <!--メッセージ-->
            <v-list-item-content class="white--text">
              <v-list-item-title v-text="item.message" />
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
        <v-spacer vertical />
        <v-list-item dense>
          <v-list-item-content class="white--text">
            {{ confirmMsg }}
          </v-list-item-content>
          <v-list-item-icon>
            <!--アップロードボタン-->
            <v-btn icon @click="msgConfirm(true)">
              <v-icon color="light-green">mdi-check-outline</v-icon>
            </v-btn>
          </v-list-item-icon>
          <v-list-item-icon>
            <!--キャンセルボタン-->
            <v-btn icon @click="msgConfirm(false)">
              <v-icon color="red">mdi-close-outline</v-icon>
            </v-btn>
          </v-list-item-icon>
        </v-list-item>
      </v-list>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["openConfirm", "msgItems", "confirmMsg"],
  data() {
    return {
      display: false,
    };
  },
  methods: {
    msgConfirm(bool) {
      this.display = false;
      if (bool) {
        this.$emit("do");
      } else {
        this.$emit("cancel");
      }
    },
  },
  watch: {
    openConfirm: function (value) {
      this.display = value;
    },
  },
};
</script>

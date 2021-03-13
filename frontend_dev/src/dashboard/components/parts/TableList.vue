<template>
  <!--テーブルメンテナンス用リスト-->
  <v-card class="ml-3" max-width="300" tile>
    <v-list dense>
      <!--テーブル名-->
      <v-list-item-title dense class="pl-5">
        {{ name }}
      </v-list-item-title>
      <v-list-item>
        <v-virtual-scroll
          :items="values"
          :item-height="40"
          height="400"
          width="200"
        >
          <template v-slot:default="{ index, item }">
            <v-list-item>
              <!--アイテム-->
              <v-list-item-content>
                <v-text-field dense v-model="values[index]" />
              </v-list-item-content>
              <!--削除ボタン-->
              <v-list-item-action>
                <v-btn icon dense color="red" @click="trash(item)">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-virtual-scroll>
      </v-list-item>
      <v-list-item>
        <!--追加ボタン-->
        <v-list-item-action class="pl-5">
          <v-btn icon @click="plus()">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-list-item-action>
        <!--確認ボタン-->
        <v-list-item-action>
          <v-btn icon color="success" @click="update()">
            <v-icon>mdi-check</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import { setUploadItem } from "@/js/uploadControl";
import { ITEMS } from "@/js/serverDataItems";
export default {
  props: ["name", "table"],
  data() {
    return {
      values: [],
    };
  },
  mounted() {
    this.values = this.$store.state.tables[this.table];
  },
  methods: {
    trash(trashItem) {
      this.values = this.values.filter((item) => item != trashItem);
      this.update();
    },
    plus() {
      this.values.push("");
    },
    update() {
      const tables = this.$store.state.tables;
      tables[this.table] = this.values.filter((value) => value != "");
      this.$store.commit("SET_TABLES", tables);
      setUploadItem(ITEMS.tables);
    },
  },
};
</script>
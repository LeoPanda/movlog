<template>
  <!--アイテムセレクターコンポーネント-->
  <v-col align-self="end" class="my-0 py-0">
    <div :v-if="event[itemKey]">
      <v-spacer></v-spacer>
    </div>
    <!--内容表示-->
    <!--muptiple表示-->
    <div v-if="multiple && event[itemKey] && !editMode">
      <v-icon
        color="info"
        class="ma-0 pa-0"
        dense
        x-small
        v-for="item in event[itemKey]"
        :key="item"
        :value="item"
        >{{ item }}
      </v-icon>
    </div>
    <!--単体表示 -->
    <CardTextDisplay
      v-if="!multiple && event[itemKey] && !editMode"
      :value="event[itemKey]"
      :label="label"
    />
    <!--選択バー-->
    <v-card width="180" flat class="ma-0 pa-0" v-if="editMode">
      <v-select
        v-if="editMode"
        :items="items"
        class="ma-0 pa-0"
        color="info"
        :label="label"
        solo
        dense
        x-small
        flex
        :rules="rules"
        :multiple="multiple"
        :value="event[itemKey]"
        @input="(value) => $emit('input', value)"
      >
      </v-select>
    </v-card>
  </v-col>
</template>
<script>
export default {
  name: "SelectableItems",
  components: {
    CardTextDisplay: () => import("./CardTextDisplay"),
  },
  props: [
    "event",
    "editMode",
    "items",
    "itemKey",
    "label",
    "multiple",
    "rules",
  ],
  data() {
    return { iaDetail: false };
  },
  mounted() {
    if (this.$route.path.match("/pages")) {
      this.isDetail = true;
    }
  },
};
</script>
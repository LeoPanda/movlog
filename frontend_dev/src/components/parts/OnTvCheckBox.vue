<template>
  <!--鑑賞メディア切替チェックボックス-->
  <div class="pa-0 ma-0">
    <!--表示用アイコン-->
    <v-icon
      class="mt-4 mx-0 px-0"
      v-if="!editMode"
      :color="getMediaIcon(onTv).color"
      >{{ getMediaIcon(onTv).icon }}</v-icon
    >
    <!--入力用チェックボックス-->
    <v-checkbox v-model="onTv" v-if="editMode">
      <template v-slot:label>
        <v-icon :color="getMediaIcon(onTv).color">{{
          getMediaIcon(onTv).icon
        }}</v-icon>
      </template>
    </v-checkbox>
  </div>
</template>
<script>
import { getMediaIcon } from "@/js/iconSetter";
export default {
  props: ["value", "editMode"],
  data() {
    return {
      onTv: false,
    };
  },
  methods: {
    getMediaIcon,
  },
  mounted() {
    this.onTv = this.value;
  },
  watch: {
    onTv: function (val) {
      this.onTv = val;
      this.$emit("input", this.onTv);
    },
  },
};
</script>
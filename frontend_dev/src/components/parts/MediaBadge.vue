<template>
  <v-row no-gutters>
    <div class="d-inline-flex">
      <!--鑑賞メディア表示バッジ-->
      <!--表示用アイコン-->
      <v-icon
        :x-small="small"
        :small="!small"
        class="mx-0 px-0"
        :color="getMediaIcon(isOnTv).color"
        >{{ getMediaIcon(isOnTv).icon }}</v-icon
      >
    </div>
    <slot></slot>
  </v-row>
</template>
<script>
import { getMediaIcon } from "@/js/iconSetter";
export default {
  props: ["isOnTv", "small"],
  methods: {
    getMediaIcon,
  },
  computed: {
    isDot() {
      return this.small && this.$vuetify.breakpoint.name == "xs" ? true : false;
    },
  },
};
</script>
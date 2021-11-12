<template>
  <!--鑑賞メディア表示バッジ-->
  <v-badge
    :offset-x="small ? '6px' : '4px'"
    :offset-y="small ? '20px' : '6px'"
    :icon="getMediaIcon(isOnTv).icon"
    :color="getMediaIcon(isOnTv).color"
    left
  >
    <slot></slot>
  </v-badge>
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
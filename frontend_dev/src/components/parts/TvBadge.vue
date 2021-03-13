<template>
  <!--テレビで鑑賞バッジ-->
  <v-badge
    :value="isOnTv"
    :offset-x="small ? '0px' : '22px'"
    :offset-y="small ? '20px' : '-1px'"
    :tile="small"
    content="TV"
    color="info"
    left
  >
    <slot></slot>
  </v-badge>
</template>
<script>
export default {
  props: ["isOnTv", "small"],
  computed: {
    isDot() {
      return this.small && this.$vuetify.breakpoint.name == "xs" ? true : false;
    },
  },
};
</script>
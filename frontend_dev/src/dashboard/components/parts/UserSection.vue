<template>
  <!--ユーザー表示パネル-->
  <v-list>
    <v-list-item dense>
      <v-avatar size="36">
        <img :src="userInfo.photo_url" />
      </v-avatar>
      <div class="mx-3 mt-5 text-caption">
        {{ userInfo.name }}
      </div></v-list-item
    >
  </v-list>
</template>
<script>
export default {
  name: "UserSection",
  data: () => ({ userInfo: [] }),
  mounted() {
    this.userInfo = this.$store.state.userInfo;
  },
};
</script>
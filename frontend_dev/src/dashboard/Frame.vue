<template>
  <!--ダッシュボード画面フレームインデックス-->
  <v-app>
    <!--機能バー-->
    <DashboardCoreAppBar />
    <!--ナビゲーションドロワー-->
    <DashboardCoreDrawer />
    <!--メインパネル-->
    <DashboardCoreMainView />
    <!--ローディング中-->
    <LoadingInfo />
    <!--メッセージ表示-->
    <Message />
  </v-app>
</template>

<script>
export default {
  name: "DashboardIndex",

  components: {
    DashboardCoreAppBar: () => import("./components/AppBar"),
    DashboardCoreDrawer: () => import("./components/Drawer"),
    DashboardCoreMainView: () => import("./components/MainView"),
    LoadingInfo: () => import("./components/LoadingInfo"),
    Message: () => import("./components/Message"),
  },
  created() {
    //夜間はダークモードに
    const date = new Date();
    const hours = date.getHours();
    if (19 < hours || hours < 6) {
      this.$vuetify.theme.dark = true;
    } else {
      this.$vuetify.theme.dark = false;
    }
    //headタイトルの設定
    document.title = "movlog";
  },
  data() {
    return { expandOnHover: false };
  },
};
</script>

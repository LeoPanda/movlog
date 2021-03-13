<template>
  <!--ダッシュボード用ナビゲーションドロワー-->
  <v-card>
    <!--ナビゲーション-->
    <v-navigation-drawer
      id="core-navigation-drawer"
      v-model="drawer"
      :right="$vuetify.rtl"
      src=""
      mobile-breakpoint="960"
      app
      width="260"
      v-bind="$attrs"
    >
      <!--ユーザー表示パネル-->
      <UserSection />
      <v-divider />
      <!--トップメニュー-->
      <MenuList :items="menuItems" />
      <!--メンテナンス用階層メニュー-->
      <v-list-group prepend-icon="mdi-tools" sub-group>
        <template v-slot:activator>
          <v-list-item-title>Mentenance</v-list-item-title>
        </template>
        <MenuList :items="mentenanceMenu" />
      </v-list-group>
      <v-spacer></v-spacer>
      <!--フッター-->
      <v-footer color="transparent">
        <v-row justify-start>
          <v-list>
            <v-list-item @click.stop="changeTheme">
              <v-list-item-icon small dense>
                <v-btn icon>
                  <v-icon v-if="!isDarkTheme">mdi-white-balance-sunny</v-icon>
                  <v-icon v-if="isDarkTheme">mdi-weather-night</v-icon>
                </v-btn>
              </v-list-item-icon>
              <v-list-item-title>Change Theme</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-row>
      </v-footer>
    </v-navigation-drawer>
  </v-card>
</template>

<script>
export default {
  name: "DashboardCoreDrawer",

  props: {
    expandOnHover: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    MenuList: () => import("./parts/MenuList"),
    UserSection: () => import("./parts/UserSection"),
  },
  data() {
    return {
      isDarkTheme: false,
      menuItems: [
        {
          //ダッシュボード
          icon: "mdi-view-dashboard",
          title: "Dashbord",
          to: "/",
        },
        {
          //カード型作品一覧
          icon: "mdi-table-large",
          title: "Movie Cards",
          to: "/views/cards",
        },
        {
          //リスト型作品一覧
          icon: "mdi-view-list",
          title: "Movie List",
          to: "/views/list",
        },
        {
          //新規作品入力画面
          icon: "mdi-pencil-plus",
          title: "Add movie",
          to: "/pages/card/new",
        },
      ],
      mentenanceMenu: [
        {
          //Link Google Calendar
          icon: "mdi-calendar-sync",
          title: "Link Google Calendar",
          to: "/maintenance/calendar",
        },
        {
          //テーブルメンテダッシュボード
          icon: "mdi-view-dashboard",
          title: "Tables",
          to: "/maintenance/tables",
        },
        {
          //リロード
          icon: "mdi-sync",
          title: "Reload",
          to: "/maintenance/reload",
        },
      ],
    };
  },
  created() {
    this.isDarkTheme = this.$vuetify.theme.dark;
  },
  computed: {
    drawer: {
      get() {
        return this.$store.state.drawer;
      },
      set(val) {
        this.$store.commit("SET_DRAWER", val);
      },
    },
  },
  methods: {
    changeTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      this.$vuetify.theme.dark = this.isDarkTheme;
    },
  },
};
</script>
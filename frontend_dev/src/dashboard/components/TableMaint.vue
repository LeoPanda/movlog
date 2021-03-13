<template>
  <!--テーブルメンテナンス ダッシュボード-->
  <v-container grid-list-xs>
    <v-row class="d-flex justify-center mb-6">
      <v-col cols="auto">
        <TableList name="スクリーンタイプ" table="screenTypes" />
      </v-col>
      <v-col cols="auto">
        <TableList name="配信プロバイダ" table="providers" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  components: {
    TableList: () => import("@/dashboard/components/parts/TableList"),
  },
};
</script>
<template>
  <!-- 編集開始・編集完了・キャンセルボタン-->
  <v-col class="ml-5 mt-0 pa-0">
    <v-col class="text-right" v-if="!editMode">
      <!--新規ボタン-->
      <v-btn
        v-if="isNew"
        color="success"
        class="mr-0"
        @click="$emit('onNew', null)"
      >
        New
        <v-icon right> mdi-pencil-plus </v-icon></v-btn
      >
      <!--編集開始ボタン-->
      <v-btn
        v-if="!isNew"
        color="accent"
        class="mr-0 ml-2"
        @click="$emit('change-mode')"
      >
        Edit
        <v-icon right> mdi-lead-pencil </v-icon></v-btn
      >
    </v-col>
    <!--編集完了ボタン-->
    <v-col class="text-right" v-if="editMode">
      <v-btn color="success" class="mr-0" @click="$emit('update')">
        Done
        <v-icon right> mdi-checkbox-marked-circle </v-icon></v-btn
      >
      <!--キャンセルボタン-->
      <v-btn color="warning" class="mr-0 ml-2" @click="$emit('cancel')">
        Cancel
        <v-icon right> mdi-close-circle-outline </v-icon></v-btn
      >
    </v-col>
  </v-col>
</template>
<script>
export default {
  name: "EditButton",
  props: ["editMode", "isNew"],
};
</script>
<template>
  <!--TV鑑賞チェックボックス-->
  <div class="pa-0 ma-0">
    <!--アイコン-->
    <v-icon
      class="mt-4 mx-0 px-0"
      v-if="!editMode"
      color="info"
      :disabled="!onTv"
      >mdi-television-box</v-icon
    >
    <!--チェックボックス-->
    <v-checkbox v-model="onTv" v-if="editMode">
      <template v-slot:label>
        <v-icon color="info" :disabled="!onTv">mdi-television-box</v-icon>
      </template>
    </v-checkbox>
  </div>
</template>
<script>
export default {
  props: ["value", "editMode"],
  data() {
    return {
      onTv: false,
    };
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
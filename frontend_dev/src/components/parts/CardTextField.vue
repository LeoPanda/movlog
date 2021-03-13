<template>
  <v-col>
    <v-text-field
      :label="label"
      :value="value"
      @input="(val) => $emit('input', val)"
      :rules="rules"
      dense
      v-bind:readonly="!editMode"
    />
  </v-col>
</template>
<script>
export default {
  name: "CardTextField",
  props: ["value", "label", "editMode", "rules"],
};
</script>
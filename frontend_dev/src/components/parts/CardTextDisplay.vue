<template>
  <v-col>
    <v-text-field :label="label" :value="value" dense readonly />
  </v-col>
</template>
<script>
export default {
  name: "CardTextDisplay",
  props: ["value", "label"],
};
</script>
<template>
  <v-expansion-panels multiple>
    <v-expansion-panel>
      <v-expansion-panel-header>{{ label }}</v-expansion-panel-header>
      <v-expansion-panel-content>
        <slot>
          {{ content }}
        </slot>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>
<script>
export default {
  name: "ExpansionPanel",
  props: ["label", "content"],
};
</script>
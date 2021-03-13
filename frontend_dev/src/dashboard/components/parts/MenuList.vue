<template>
  <!--ドロワーのメニューを表示-->
  <div>
    <v-list nav v-for="(item, i) in computedItems" :key="`item-${i}`">
      <v-list-item :to="item.to">
        <v-list-item-icon small dense>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
export default {
  props: ["items"],
  computed: {
    computedItems() {
      return this.items.map(this.mapItem);
    },
  },

  methods: {
    mapItem(item) {
      return {
        ...item,
        title: item.title,
      };
    },
  },
};
</script>
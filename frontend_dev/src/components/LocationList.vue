<template>
  <!--劇場一覧-->
  <v-list dense>
    <v-list-item>
      <v-virtual-scroll
        :items="locations"
        :item-height="50"
        height="400"
        width="350"
      >
        <template v-slot:default="{ item }">
          <v-list-item dense @click="filter(item.name)">
            <v-list-item-avatar>
              <!--画像アイコン-->
              <v-img :src="item.photo_url"></v-img>
            </v-list-item-avatar>
            <!--劇場名-->
            <v-list-item-content>
              <v-list-item-title v-text="item.name"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-list-item>
  </v-list>
</template>
<script>
import { setFilter } from "@/js/filter";
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState(["locations"]),
  },
  methods: {
    filter(name) {
      setFilter(name);
    },
  },
};
</script>
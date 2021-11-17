<template>
  <v-container fuluid>
    <div ref="top" />
    <!-- カード一覧 -->
    <v-row class="d-flex justify-left mb-6">
      <v-col
        v-for="person in people"
        :key="person.id + person.role"
        cols="auto"
      >
        <!--カードコンポーネント -->
        <v-card width="144" class="py-2">
          <!-- ポスターアート -->
          <v-row>
            <v-img
              max-width="138"
              max-height="175"
              class="white--text mx-4 mb-0 pa-0"
              :src="getImgUrl(person['img_src'], 'middle')"
            >
              <template v-slot:default>
                <v-btn
                  class="transparent"
                  width="138"
                  height="175"
                  @click="
                    openWin(
                      'https://www.themoviedb.org/person/' +
                        person.id +
                        '?language=ja'
                    )
                  "
                />
              </template>
            </v-img>
          </v-row>
          <!-- 名前 -->
          <v-row class="ml-1">
            <v-card-title
              v-text="person.name"
              class="pa-0 ma-0 body-2"
            ></v-card-title>
            <v-card-text class="caption">
              {{ person.role }}
            </v-card-text>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { getImgUrl } from "@/js/imgSizeControl";
export default {
  name: "PersonCard",
  props: ["people"],
  methods: {
    getImgUrl,
    openWin(link) {
      window.open(link, "_blank");
    },
  },
};
</script>
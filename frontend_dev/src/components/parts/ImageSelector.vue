<template>
  <!--ポスターアートイメージ選択-->
  <!--TIPS:radio-groupのv-modelとv-radioのnameを合わせることで
  checkedと同等の効果を得られる-->
  <v-radio-group row v-model="selected">
    <div v-for="(img, key) in imgs" :key="key">
      <v-radio
        name="selected"
        :key="key"
        :value="img"
        align-start
        @change="$emit('input', img)"
      >
        <template v-slot:label>
          <v-col class="pa-0 ma-0 mb-2 mx-2">
            <v-badge overlap center :content="key">
              <v-img
                width="124"
                height="184"
                class="white--text"
                :src="img"
              ></v-img>
            </v-badge>
          </v-col>
        </template>
      </v-radio>
    </div>
  </v-radio-group>
</template>
<script>
export default {
  name: "ImageSelector",
  props: ["imgSrc", "preSelected", "triger"],
  data() {
    return {
      imgs: {},
      selected: "",
    };
  },
  created() {
    this.setImgs();
  },
  mounted() {
    this.selected = this.preSelected;
  },
  methods: {
    setImgs() {
      this.$set(this.imgs, "imdb", this.imgSrc["imdb"]);
      this.$set(this.imgs, "tmdb", this.imgSrc["tmdb"]);
      this.$set(this.imgs, "eiga_db", this.imgSrc["eiga_db"]);
    },
  },

  watch: {
    triger: {
      handler: function () {
        this.setImgs();
      },
      deep: true,
    },
  },
};
</script>
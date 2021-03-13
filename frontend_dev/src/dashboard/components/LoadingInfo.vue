<template>
  <!--ローディング中表示用ダイアログ-->
  <div class="text-center">
    <v-dialog v-model="loading" width="300">
      <v-card color="primary">
        <v-card-text class="white--text">
          Now loading...
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState(["loading"]),
  },
};
</script>
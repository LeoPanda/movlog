<template>
  <!--日付フィールド-->
  <v-col>
    <!--クリック時ピッカー表示-->
    <v-menu
      ref="datePicker"
      v-model="datePicker"
      :close-on-content-click="false"
      transition="scale-transition"
      offset-y
      nudge-left="200"
      min-width="auto"
    >
      <template v-slot:activator="{ on, attrs }">
        <!--表示フィールド-->
        <v-text-field
          :value="getStdDate(date)"
          :label="label"
          dense
          readonly
          v-bind="attrs"
          v-on="on"
        ></v-text-field>
      </template>
      <!--日付ピッカー-->
      <v-date-picker
        color="primary"
        v-model="date"
        @input="
          (date) => {
            this.$emit('input', date);
            datePicker = false;
          }
        "
        no-title
        scrollable
        v-if="editMode"
      />
    </v-menu>
  </v-col>
</template>
<script>
import { getStdDate } from "@/js/dateUtil";
export default {
  props: ["label", "inDate", "editMode"],
  data() {
    return {
      date: "",
    };
  },
  mounted() {
    this.date = this.inDate;
  },
  methods: {
    getStdDate,
  },
};
</script>
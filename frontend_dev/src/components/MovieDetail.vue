<template>
  <!-- 鑑賞映画タイトルの詳細画面 -->
  <v-container id="card-detail" fluid tag="section">
    <div ref="top" />
    <v-form ref="form">
      <v-card>
        <v-container>
          <v-row>
            <div class="pl-3 pa-0 ma-0">
              <!--鑑賞メディア切替チェックボックス-->
              <OnTvCheckBox
                :value="event['on_tv']"
                :editMode="editMode"
                @input="
                  (val) => {
                    this.$set(this.event, 'on_tv', val);
                  }
                "
              />
            </div>
            <!-- 映画タイトル名 -->
            <CardTextField
              v-model="event.title"
              label="title"
              :editMode="editMode"
              :rules="required"
            />
          </v-row>
          <v-row>
            <!--ポスターアート画像 -->
            <v-col class="justify-center" ref="image">
              <v-card :width="imgWidth">
                <div @click="chgImgSize">
                  <v-img
                    :aspect-ratio="182 / 268"
                    :width="imgWidth"
                    class="white--text"
                    :src="getImgUrl(event.title_img, imgSize)"
                  ></v-img>
                </div>
                <!-- 入力 -->
                <CardTextField
                  v-if="editMode"
                  v-model="event.title_img"
                  label="image URL"
                  :editMode="editMode"
                  :rules="required"
                />
                <!-- 特殊上映スクリーンのタイプ -->
                <SelectableItems
                  v-if="!event['on_tv']"
                  :event="event"
                  :editMode="editMode"
                  :items="this.$store.state.tables['screenTypes']"
                  itemKey="screen_type"
                  label="screen type"
                  :multiple="true"
                  @input="
                    (val) => {
                      this.$set(this.event, 'screen_type', val);
                    }
                  "
                />
              </v-card>
            </v-col>

            <v-col>
              <v-card
                flat
                width="300"
                class="d-flex justify-space-around pl-1"
                v-if="visibleEnTitle"
              >
                <!-- オリジナルタイトル名 -->
                <CardTextField
                  v-model="event.en_title"
                  label="oliginal title"
                  :editMode="editMode"
                  width="300"
                />
              </v-card>

              <v-card flat class="d-flex justify-space-around ma-0" width="300">
                <!-- 劇場名-->
                <SelectableItems
                  v-if="!event['on_tv']"
                  :event="event"
                  :editMode="editMode"
                  :items="this.$store.state.locations.map((item) => item.name)"
                  itemKey="location"
                  label="theater"
                  :multiple="false"
                  :rules="required"
                  @input="
                    (val) => {
                      this.$set(this.event, 'location', val);
                    }
                  "
                />
              </v-card>
              <v-card flat class="d-flex justify-space-around ma-0">
                <!-- 配信プロバイダ -->
                <SelectableItems
                  v-if="event['on_tv']"
                  :event="event"
                  :editMode="editMode"
                  :items="this.$store.state.tables['providers']"
                  itemKey="streaming_provider"
                  label="streaming provider"
                  :multiple="false"
                  :rules="required"
                  @input="
                    (val) => {
                      this.$set(this.event, 'streaming_provider', val);
                    }
                  "
                />
              </v-card>
              <v-card flat class="d-flex justify-space-around pl-1">
                <!-- 鑑賞日付 -->
                <CardDateField
                  label="watched date"
                  :editMode="editMode"
                  :inDate="watchDate"
                  @input="setDate"
                />
              </v-card>
            </v-col>
          </v-row>
          <!-- 内容の概要説明 -->
          <v-row>
            <v-textarea
              solo
              auto-grow
              :readonly="!editMode"
              v-model="event.outline"
              label="detail"
            ></v-textarea>
          </v-row>
          <!-- 外部サイトの紐付け検索パネル -->
          <v-row v-if="editMode">
            <OuterIDSelectPanel
              :event="event"
              @input="
                (val) => {
                  setEvent(val);
                }
              "
            />
          </v-row>
          <!-- ポスターアート画像の選択パネル -->
          <v-row v-if="editMode">
            <template>
              <ImageSelector
                :imgSrc="event['img_src']"
                :preSelected="event['title_img']"
                :triger="imgChgTriger"
                @input="
                  (val) => {
                    this.$set(this.event, 'title_img', val);
                    this.checkVisible();
                  }
                "
              />
            </template>
          </v-row>
          <v-row>
            <!-- レーティング表示 -->
            <RatingBar :event="event" :isNum="true" />
            <!-- EDITボタン -->
            <EditButton
              :editMode="editMode"
              :isNew="isNew"
              @change-mode="chengeEditMode"
              @update="adaptUpdate"
              @cancel="cancelEdit"
              @onNew="
                () => {
                  this.setNew();
                  this.checkVisible();
                }
              "
            />
          </v-row>
        </v-container>
      </v-card>
      <!-- 転写元google calendarのソース表示 -->
      <ExpansionPanel label="source" :content="event" v-if="editMode" />
    </v-form>
  </v-container>
</template>

<script>
import { getYMD, getNewId, getIsoDate, compareDecDates } from "@/js/dateUtil";
import { setMsg } from "@/js/msgSetter";
import { setUploadItem } from "@/js/uploadControl";
import { ITEMS } from "@/js/serverDataItems";
import { getImgUrl } from "@/js/imgSizeControl";

export default {
  name: "MovieDetail",
  //routerからパスダイレクトで呼び出されるので引数はeventでなくid
  props: ["id"],
  components: {
    CardTextField: () => import("./parts/CardTextField"),
    CardDateField: () => import("./parts/CardDateField"),
    RatingBar: () => import("./parts/RatingBar"),
    SelectableItems: () => import("./parts/SelectableItems"),
    ImageSelector: () => import("./parts/ImageSelector"),
    OuterIDSelectPanel: () => import("./parts/OuterIDSelectPanel"),
    EditButton: () => import("./parts/EditButton"),
    ExpansionPanel: () => import("./parts/ExpansionPanel"),
    OnTvCheckBox: () => import("./parts/OnTvCheckBox"),
  },
  data() {
    return {
      event: {},
      editMode: false,
      isNew: false,
      isEventChanged: false,
      visibleEnTitle: true,
      watchDate: "",
      imgWidth: 182,
      imgSize: "middle",
      required: [(val) => !!val || "required"],
      imgChgTriger: 0,
    };
  },
  beforeRouteUpdate(to) {
    //TIPS:vue routerが同一パスのコンポーネントを再利用するため、
    //既存データ->新規と遷移させると画面表示が変わらない（createdが呼ばれない）ので、
    //新規の時は値を初期化する
    if (to.fullPath == "/pages/card/new") {
      this.setNew();
    }
  },
  created() {
    if (this.id == "new") {
      //新規入力時
      this.setNew();
    } else {
      //既存データ
      this.loadEvent();
      if (!this.event) {
        this.$router.go(-1);
        setMsg("その記録は存在しません。", "error");
      }
      this.checkVisible();
    }
    this.watchDate = getYMD(this.event.start.date_time);
    if (!this.event["img_src"]) {
      this.event["img_src"] = { imdb: "", eiga_db: "", tmdb: "" };
    } else {
      if (!this.event.img_src["eiga_db"]) {
        this.event.img_src["eiga_db"] = "";
      }
      if (!this.event.img_src["imdb"]) {
        this.event.img_src["imdb"] = "";
      }
      if (!this.event.img_src["tmdb"]) {
        this.event.img_src["tmdb"] = "";
      }
    }
  },
  mounted() {
    this.$refs.top.scrollIntoView({ block: "end" });
  },
  methods: {
    getYMD,
    getImgUrl,
    chgImgSize() {
      //イメージクリック時の拡大/縮小
      this.imgWidth = this.imgWidth == 182 ? 182 * 3 : 182;
      this.imgSize = this.imgSize == "middle" ? "large" : "middle";
    },
    setEvent(val) {
      //ID検索で得たデータをイベントにセットする
      if (val["title"]) {
        if (!this.event.title || !this.event.title.length > 0) {
          this.$set(this.event, "title", val.title);
        }
      }
      if (val["outline"]) {
        if (!this.event.outline || !this.event.outline.length > 0) {
          this.$set(this.event, "outline", val.outline);
        }
      }
      if (val["en_title"]) {
        if (!this.event.en_title || !this.event.en_title.length > 0) {
          this.$set(this.event, "en_title", val.en_title);
        }
      }
      this.$set(this.event, "img_src", val.img_src);
      this.$set(this.event, "outer_rate", val.outer_rate);
      this.$set(this.event, "outer_id", val.outer_id);
      this.checkVisible();
      this.imgChgTriger++;
    },
    setNew() {
      //新規入力用に値を初期化
      this.isNew = true;
      this.editMode = true;
      this.event = {};
      this.$set(this.event, "id", getNewId());
      this.$set(this.event, "start", { date_time: getIsoDate() });
      this.$set(this.event, "img_src", { imdb: "", eiga_db: "", tmdb: "" });
      this.$set(this.event, "on_tv", true);
    },
    loadEvent() {
      //ストアから該当IDのイベントを検索して編集メモリにセットする
      //TIPS:JSONでencode & decodeすることでdeep copyしている
      this.isNew = false;
      this.event = JSON.parse(
        JSON.stringify(
          this.$store.state.events.find((event) => event.id === this.id)
        )
      );
    },
    chengeEditMode() {
      //編集・表示モード変更
      this.editMode = !this.editMode;
      this.checkVisible();
    },
    cancelEdit() {
      //編集のキャンセル
      this.editMode = !this.editMode;
      this.$router.go(-1);
    },
    adaptUpdate() {
      //バリデーションチェック
      if (this.$refs.form.validate()) {
        this.chengeEditMode();
        //内容が変更されていたならstateに変更データをセットする。
        if (this.isEventChanged == true) {
          const repIndex = this.$store.state.events.findIndex(
            (event) => event.id === this.id
          );
          //修正/新規の判定
          if (repIndex > -1) {
            this.$store.state.events[repIndex] = this.event;
          } else {
            this.$store.state.events.push(this.event);
          }
          //イベントの降順ソート
          this.$store.state.events.sort((a, b) => {
            return compareDecDates(a.start.date_time, b.start.date_time);
          });
          //イベント変更通知
          setUploadItem(ITEMS.events);
        }
      }
    },
    checkVisible() {
      //各項目の表示・非表示設定
      this.visibleEnTitle =
        this.editMode ||
        ("en_title" in this.event &&
          this.event.en_title &&
          this.event.en_title.length > 0);
    },
    setDate(date) {
      this.$set(this.event.start, "date_time", getIsoDate(date));
    },
  },
  watch: {
    event: {
      handler: function (newVal, oldVal) {
        //event内容に変更があったかどうかチェックする
        //ただし、初期ロードによる変更は無視する
        if ("title" in oldVal) {
          this.isEventChanged = true;
        }
      },
      deep: true,
    },
  },
};
</script>
<style>
/*セレクタのチェックボックス非表示 */
.v-input--selection-controls__input {
  display: none !important;
}
.v-item--active {
  background-color: aqua;
}
</style>

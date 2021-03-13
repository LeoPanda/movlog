import { getFilteredEvents } from "@/js/filter"
import { getOrderedEvents } from "@/js/sort"
//view表示共通スクリプト
export default {
    name: "viewmixin",
    data() {
        return {
            events: [],
            displayedEvents: [],
            pagenation: { num: 1, length: 6 },
            pageMultiple: false
        };
    },
    computed: {
        //変更監視用関数
        getStoredEvent() {
            return this.$store.state.events;
        },
        getSearchWord() {
            return this.$store.state.searchWord;
        },
        getSortOrder() {
            return this.$store.state.sortOrder;
        },
        getBreakPoint() {
            return this.$vuetify.breakpoint.name;
        },
        getDrawer() {
            return this.$store.state.drawer;
        },
    },
    mounted() {
        this.events = this.getStoredEvent;
        var word = this.getSearchWord;
        if (word.length > 0) {
            this.doFilter(word);
        }
        this.paging(this.getInitPageNum(this.$store.state.pageStartIndex));
    },
    methods: {
        doFilter(word) {
            //フィルター実行
            this.events = getOrderedEvents(getFilteredEvents(word))
        },
        sortAsOrder() {
            //表示順変更
            this.events = getOrderedEvents(this.events)
        },
        getPageSizeBase() {
            //ページ表示サイズの基礎値を取得
            switch (this.$vuetify.breakpoint.name) {
                case "sm":
                    return 6;
                case "md":
                    return 6;
                case "lg":
                    return 12;
                case "xl":
                    return 14;
                default:
                    return 6;
            }
        },
        getPageSize() {
            //ページの表示サイズを取得
            return this.getPageSizeBase() * (this.pageMultiple == true ? 2 : 1)
                + (this.$store.state.drawer == true ? 0
                    : this.pageMultiple == true ? 0
                        : this.$vuetify.breakpoint.width < 960 ? 0
                            : 2);
        },
        getInitPageNum(startIndex) {
            //初期ページ番号検出処理
            this.pagenation.length =
                Math.ceil(this.events.length / this.getPageSize());
            return Math.ceil((startIndex + 1) / this.getPageSize())
        },
        paging(page) {
            //ページングボタンが押されたときの処理
            this.pagenation.num = page
            const startIndex = (page - 1) * this.getPageSize()
            this.displayedEvents =
                this.events.slice(startIndex, startIndex + this.getPageSize());
            this.$store.commit("SET_PAGE_START_INDEX", startIndex);
            this.$refs.top.scrollIntoView(true)
        },
    },
    watch: {
        getSearchWord: function (newVal) {
            //Vuex searchWord変更監視
            this.doFilter(newVal);
            this.paging(this.getInitPageNum(0));
        },
        getSortOrder: function () {
            //vuex sort order変更監視
            this.sortAsOrder()
            this.paging(this.getInitPageNum(0));
        },
        getBreakPoint: function () {
            //windowの表示幅変更監視
            this.paging(
                this.getInitPageNum(
                    this.$store.state.pageStartIndex));
        },
        getDrawer: function () {
            //ドロワーのサイドパネル表示変更監視
            this.paging(
                this.getInitPageNum(
                    this.$store.state.pageStartIndex));
        },
        events: function () {
            this.$store.commit("SET_EVENTS_NUM", this.events.length)
        }
    },
};
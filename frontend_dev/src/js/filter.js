/**
 * データフィルター関数群
 */
import store from './store'
import { getYYYYM, getYYYYMM } from "./dateUtil";


//フィルター用検索ワードをセットする
export function setFilter(word) {
    store.commit("SET_SEARCH_WORD", word);
    store.commit("SET_PAGE_START_INDEX", 0);
}
//イベントフィルタ実行処理
export function getFilteredEvents(word) {
    return store.state.events.filter(
        (event) =>
            wordFilter(event, word) || dateFilter(event, word) ||
            rateFilter(event, word) || onTvFilter(event, word) ||
            screenTypeFilter(event, word)
    );
}
//文字検索フィルター
function wordFilter(event, word) {
    const eventItems = ['title', 'en_title', 'outline', 'streaming_provider', 'location']
    return eventItems.reduce((bool, item) => {
        bool = bool || (event[item] ?
            (event[item].replace(" ", "").toUpperCase().search(word.toUpperCase()) > -1)
            : false)
        return bool
    }, false)
}
//日付フィルター
function dateFilter(event, word) {
    return (
        getYYYYM(event.start.date_time).search(word) > -1 ||
        getYYYYMM(event.start.date_time).search(word) > -1
    )
}
//レートフィルター
function rateFilter(event, word) {
    const rate = word.match(/(rate)([=<>])(\d)/)
    let bool = false;
    if (rate && event['my_rate']) {
        const num = rate[3]
        switch (rate[2]) {
            case "=": bool = event['my_rate'] == num
                break
            case "<": bool = event['my_rate'] < num
                break
            case ">": bool = event['my_rate'] > num
                break
            default:
                bool = false;
        }
    }
    return bool
}
//テレビ/劇場区分フィルター
function onTvFilter(event, word) {
    if (word.toUpperCase() == "ONTV") {
        return event['on_tv'] == true
    } else if (word.toUpperCase() == "ATTHEATER") {
        return event['on_tv'] != true
    }
    return false;
}

//スクリーンタイプフィルター
function screenTypeFilter(event, word) {
    if (event['screen_type']) {
        return event['screen_type']
            .filter(type => type == word.toUpperCase()).length > 0
    }
}
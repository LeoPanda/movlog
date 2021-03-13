/**
 * データソート関数群
 */
import store from './store'

//イベントソート処理
export function setSortOrder(order) {
    store.commit("SET_SORT_ORDER", order);
    store.commit("SET_PAGE_START_INDEX", 0);
}
//イベントソート実行処理
export function getOrderedEvents(events, order = null) {
    order = order == null ? store.state.sortOrder : order
    if (order == "dateDsc") {
        //鑑賞日付の降順
        return events.sort(
            (a, b) => new Date(b.start.date_time) - new Date(a.start.date_time)
        );
    } else if (order == "dateAsc") {
        //鑑賞日付の降順
        return events.sort(
            (a, b) => new Date(a.start.date_time) - new Date(b.start.date_time)
        );
    } else if (order == "rateDsc") {
        //my rateの降順
        return events.sort(
            (a, b) => (b.my_rate ? b.my_rate : 0) - (a.my_rate ? a.my_rate : 0)
        );
    }
    return events;
}
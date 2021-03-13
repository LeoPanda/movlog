/**
 * 統計データ算出関数
 */
import { getYYYYMM } from "./dateUtil"

//myレート別集計リスト(0件データも含む)
export function aggRate(events) {
    const array = Array.from({ length: 10 }, (_, i) => i + 1)
    const sumData = summary(getRateByTitle(events), (item) => item.rate)
    return array.reduce((result, i) => {
        const dataItem = sumData.find((item) => item.name == i)
        result.push({ name: i, count: dataItem ? dataItem.count : 0 })
        return result
    }, []).sort((a, b) => Number(b.name) - Number(a.name))
}
//タイトル別レートリスト
function getRateByTitle(events) {
    events = events.map((item) => {
        //レート未設定のアイテムを0に再設定
        return {
            title: item.title,
            rate: (item['my_rate'] ? item['my_rate'] : 0)
        }
    })
    return summary(events, (event) => event.title)
        .reduce((rateList, item) => {
            const rating = {
                name: item.name,
                rate: events.find(event => event.title == item.name).rate
            }
            rateList.push(rating)
            return rateList
        }, []).sort((a, b) => b.name - a.name)
}
//最初の鑑賞日から最後の鑑賞日までの年を四捨五入で
export function getYearRange(events) {
    return Math.round(
        (getBothEndDays(events).maxDate
            - getBothEndDays(events).miniDate)
        / (60 * 60 * 24 * 365 * 1000)
    )
}
//劇場ごとの件数サマリ(TV鑑賞は除く)
export function aggTheater(events) {
    return summary(
        events.filter(event => !('on_tv' in event)),
        (event) => event.location).sort((a, b) => b.count - a.count)
}

//映像配信プロバイダごとのサマリ
export function aggProviders(events) {
    return summary(events.filter(event => event['on_tv'] == true),
        (event) => event.streaming_provider)
        .sort((a, b) => b.count - a.count)
}

//月ごとの劇場鑑賞件数サマリ
export function MonthlyAggregate(events) {
    const monthlySummaryElements = summary(
        events.filter(event => event['on_tv'] != true),
        (event) => getYYYYMM(event.start.date_time));
    //TV視聴の件数サマリ
    const monthlyTvSummaryElements = summary(
        events.filter(event => event['on_tv'] == true),
        (event) => getYYYYMM(event.start.date_time));

    let result = []
    //0件の月も含ませる
    getEveryMonthElements(events).forEach((event) => {
        const isEventMonth = monthlySummaryElements.find(item => item.name == event.name);
        const isTvMonth = monthlyTvSummaryElements.find(item => item.name == event.name);
        event.count = isEventMonth ? isEventMonth.count : 0;
        event.tvCount = isTvMonth ? isTvMonth.count : 0;
        result.push(event)
    });
    return result;
}

//汎用サマリー関数
function summary(events, getSummaryItem) {
    //getSummaryItem :イベント情報の中の集計アイテムを指定する関数
    return events.reduce((resultDict, current) => {
        const item = getSummaryItem(current)
        const condition = resultDict.find(element => element.name == item)
        if (condition) {
            condition.count++;
        } else {
            resultDict.push({
                name: item,
                count: 1,
            })
        }
        return resultDict;
    }, []);
}

//イベントの最古日から最新日までの月ごとの初期配列を生成する
function getEveryMonthElements(events) {
    const day = new Date(getBothEndDays(events).miniDate)
    day.setMonth(day.getMonth() - 1)
    const resultElements = []
    while (day < new Date(getBothEndDays(events).maxDate)) {
        day.setMonth(day.getMonth() + 1)
        resultElements.push({ name: getYYYYMM(day), count: 0, tvCount: 0 })
    }
    return resultElements;
}

//全イベント中の最新日付と最古日付を取得する
function getBothEndDays(events) {
    const dates = events.map((event) => new Date(event.start.date_time))
    return {
        "maxDate": Math.max.apply(null, dates),
        "miniDate": Math.min.apply(null, dates)
    }
}

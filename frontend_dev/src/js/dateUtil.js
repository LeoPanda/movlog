/**
 * 日付操作関数群
 */
import moment from "moment";
export function getYYYYM(date = false) {
    //'YYYY-M'形式で日付を得る
    return getMoment(date).format("YYYY-M")
}
export function getYYYYMM(date = false) {
    //'YYYY-MM'形式で日付を得る
    //TIPS:YYYY-MはISOフォーマットと認識されない
    //chart.jsの入力でmomentが使用されているらしいので、
    //non ISOフォーマットをchart.jsの入力に使用するとwarningが出てしまう。
    return getMoment(date).format("YYYY-MM")
}
export function getYMD(date = false) {
    //'YYYY-MM-DD'形式で日付を得る
    return getMoment(date).format("YYYY-MM-DD")
}

export function getStdDate(date = false) {
    //標準表示形式（YY-MM-DD(week))で日付を得る
    return getMoment(date).format("YY-MM-DD(ddd)")
}

export function getIsoDate(date = false) {
    //日付をISOフォーマットに変換する
    return getMoment(date).format()
}

export function getNewId() {
    //ユニークなIDを生成する
    return "id" + moment().unix()
}

export function compareDecDates(a, b) {
    //日付降順ソート用比較関数
    return moment(b).unix() - moment(a).unix()
}

export function isExpired(date, expiredDays) {
    //dateがexpriredDaysで指定された期限日数を超えているかをチェックする
    return expiredDays < getMoment(date).diff(moment(), 'days')
}

function getMoment(date = false) {
    //指定された日付をmomentに変換する
    //日付が指定されなければ本日日付とみなす
    return date ? moment(new Date(date).toISOString()) : moment()
}
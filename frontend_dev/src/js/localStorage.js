/**
 * ローカルストレージ制御関数
 */
export function loadFromLocal(item) {
    //ローカルストレージからの読み込み共通処理
    let ret, ret_item
    try { ret_item = localStorage.getItem(item) } catch (e) {
        ret_item = null
    }
    if (ret_item) {
        ret = JSON.parse(ret_item)
    } else {
        ret = null
    }
    return ret
}

export function saveToLocal(item, payload) {
    //ローカルストレージへの書き込み共通処理
    try {
        localStorage.setItem(item, JSON.stringify(payload))
    } catch (e) {
        console.log("local storage is not supported.")
        return false
    }
    return true
}

export function clearLocalStorage(item) {
    //ローカルストレージアイテムのクリア
    localStorage.removeItem(item)
}
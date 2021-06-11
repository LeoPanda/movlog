/**
 * サーバーと通信してデータをロードするための関数群
 */
import { ajaxGet } from "./ajax"
import store from "./store";
import router from "./router";
import { setMsg } from "./msgSetter"
import { loadFromLocal, saveToLocal, clearLocalStorage } from "./localStorage"
import { ITEMS } from "./serverDataItems"
import { isExpired } from "./dateUtil"

/**ローカルストレージのユーザー情報の有効期限が切れている場合はそれを削除する */
/**サーバーサイドでユーザー情報はセッション変数に置かれているのでリロードしてもAPIコールは発生しない。
 */
export function checkUserInfoExpired() {
    const localName = 'userInfo'
    const userInfo = loadFromLocal(localName)
    if (userInfo) {
        //有効期限は１日
        if (isExpired(userInfo.date, 1)) {
            console.log('userInfo expired.')
            clearLocalStorage(localName)
        }
    }
}


/**googleカレンダーのデータリンクを指示する */
export async function linkCalendar() {
    store.commit("SET_LOADING", true)
    const response = await ajaxGet('/events/add')
    store.commit("SET_LOADING", false)
    if ("success" in response.data) {
        clearLocalStorage("events")
        clearLocalStorage("locations")
        loadInitialData()
        setMsg("データリンクが完了しました。", "success", "reload")
        router.push("/")
    } else {
        setMsg("データリンクでエラーが発生しました。", "error")
        console.log("データリンクでエラーが発生しました。")
        console.dir(response)
    }

}

/**初期データをStateにロードする
 * ローカルストレージにデータがある場合はこれをロードし、
 * ない場合はサーバーからデータをロードする
 * データ受信中はローディングフラグを立てる

*/
export function loadInitialData() {
    const loadItems = [ITEMS.events, ITEMS.locations, ITEMS.tables, ITEMS.userInfo]
    const fromServerItems = loadItems.filter(item => !loadLocalToStore(item))
    loadFromServer(fromServerItems);
}

/** ローカルストレージのデータをVuex Stateに転送する 
 * ローカルストレージにデータがない場合はfalseを返す
*/
function loadLocalToStore(item) {
    const localStorage = loadFromLocal(item.local)
    if (localStorage) {
        store.commit(item.state, localStorage)
        return true
    }
    return false
}

/**初期データをサーバーからロードし、ローカルストレージとvuex Stateに保存する
 */
async function loadFromServer(items) {
    store.commit("SET_LOADING", true)
    for (const item of items) {
        const response = await ajaxGet(item.loadPath)
        if (saveToLocal(item.local, response.data)) {
            loadLocalToStore(item)
        } else {
            store.commit(item.sate, response.data)
        }
    }
    store.commit("SET_LOADING", false)
}

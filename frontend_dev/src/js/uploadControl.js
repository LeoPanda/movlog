/**
 * サーバー通信データアップロード関数群
 */
import { ajaxPut } from "@/js/ajax";
import store from "./store"
import { clearLocalStorage } from "@/js/localStorage"

/**vuex stateにアップロードアイテムをセットする */
export function setUploadItem(item) {
    let uploadItems = store.state.uploadItems
    for (const uploadItem of uploadItems) {
        //重複チェック
        if (item.local == uploadItem.local) {
            return
        }
    }
    uploadItems.push({
        uploadPath: item.uploadPath,
        local: item.local,
        message: item.message
    })
    store.commit("SET_UPLAD_ITEMS", uploadItems)
}
/**stateにセットされたアイテム情報を元にデータをサーバーへアップロードする 
 * アップロードしたアイテムはローカルストレージから削除する
*/
export async function uploadToServer() {
    store.commit("SET_LOADING", true);
    const items = store.state.uploadItems
    let errItems = [...items]
    for (const item of items) {
        const response = await ajaxPut(item.uploadPath, getPayload(item))
        if ("success" in response.data) {
            clearLocalStorage(item.local)
            errItems = errItems.filter((errItem) => { errItem.local != item.local })
        }
    }
    store.commit("SET_LOADING", false)
    store.commit("SET_UPLAD_ITEMS", errItems)
    return (errItems.length == 0)
}

/** itemに応じたアップロードデータを取得する */
function getPayload(item) {
    let payload
    switch (item.local) {
        case "events":
            payload = store.state.events;
            break;
        case "locations":
            payload = store.state.locations;
            break;
        case "tables":
            payload = store.state.tables;
            break;
    }
    return payload
}

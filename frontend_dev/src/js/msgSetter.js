import store from "./store";

/**ダッシュボードのメッセージダイアログに表示される
*メッセージをセットする
*パラメータ: 
*text:表示するメッセージ
*type:メッセージのタイプ "success" "error" メッセージの表示色を規定
*postProcess:後処理 "none"：何もしない "reload":画面のリロード 
*/
export function setMsg(text, type = "success", postProcess = "none") {
    const msg = { text: "", type: "" };
    msg.text = text;
    msg.type = type;
    store.commit("SET_MESSAGE", msg)
    if (postProcess == "reload") {
        store.commit("SET_RELOAD", true)
    }
}
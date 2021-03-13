import store from "./store";

/**ダッシュボードのメッセージダイアログに表示される
 *メッセージをセットする
 */
export function setMsg(text, type = "success") {
    const msg = { text: "", type: "" };
    msg.text = text;
    msg.type = type;
    store.commit("SET_MESSAGE", msg)
}
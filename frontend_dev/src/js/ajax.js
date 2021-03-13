/**
 * Ajax関数群
 */
import axios from "axios";
import { setMsg } from "./msgSetter"

/** Ajaxでgetを発行
*/
export async function ajaxGet(url) {
    return doAjax(url, axios.get)
}
/** Ajaxでputを発行
*/
export async function ajaxPut(url, json) {
    return doAjax(url, axios.put, json)
}
/** Ajax雛形
*/
async function doAjax(url, ajaxFunc, json = null) {
    url = getDevServer() + url;
    console.log('url=' + url)
    let param = [url]
    if (json) {
        param.push(json)
    }
    const res = await ajaxFunc(...param, { withCredentials: true })
        .catch(error => { logError(error) })
    if ("auth_url" in res.data) {
        console.log('auth_url=' + res.data.auth_url)
        location.href = getDevServer() + res.data.auth_url;
    } else {
        return res
    }
}
//コンソールにエラー情報を表示する
function logError(error) {
    setMsg("通信エラーが発生しました。コンソールを確認してください。", "error")
    console.log("ajax通信でエラーが発生しました。")
    console.dir(error)
}
//ローカルで実行している場合はパスを変更する
function getDevServer() {
    if (process.env.NODE_ENV == "development") {
        return "https://localhost:5000"
    }
    return ""
}
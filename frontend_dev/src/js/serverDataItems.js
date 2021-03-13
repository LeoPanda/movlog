/**
 * サーバー通信用定数定義
 */
export const ITEMS = {
    events: {
        loadPath: "/events/list",
        uploadPath: "/events/upload",
        message: "作品情報に変更がありました。",
        state: "SET_EVENTS",
        local: "events"
    },
    locations: {
        loadPath: "/location/list",
        uploadPath: "/location/upload",
        message: "劇場情報に変更がありました。",
        state: "SET_LOCATIONS",
        local: "locations"
    },
    tables: {
        loadPath: "/tables/list",
        uploadPath: "/tables/upload",
        message: "テーブルデータに変更がありました。",
        state: "SET_TABLES",
        local: "tables"
    },
    userInfo: {
        loadPath: "/auth/getprofile",
        state: "SET_USER_INFO",
        local: "userInfo"
    },
}
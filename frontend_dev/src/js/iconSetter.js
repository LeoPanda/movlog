//劇場・TV表示バッチアイコン諸元の設定
export function getMediaIcon(isOnTv) {
    const onTv = { icon: "mdi-play-network-outline", color: "green" }
    const onTheater = { icon: "mdi-filmstrip", color: "info" }

    return {
        icon: (isOnTv ? onTv.icon : onTheater.icon),
        color: (isOnTv ? onTv.color : onTheater.color)
    }
}
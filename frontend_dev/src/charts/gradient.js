export function getGradient() {
    //カラーグラデーション
    return getGradientBase(
        { r: 0, g: 0, b: 450 },
        { r: 100, g: 0, b: 255 },
        { r: 255, g: 100, b: 100 },
        { r: 450, g: 255, b: 0 },
    )
}

export function getAltGradient() {
    //カラーグラデーション別パターン
    return getGradientBase(
        { r: 450, g: 0, b: 0 },
        { r: 100, g: 0, b: 255 },
        { r: 50, g: 0, b: 100 },
        { r: 0, g: 255, b: 450 },
    )
}

function getGradientBase(a, b, c, d) {
    //カラーグラデーションベース
    const canvas = document.querySelector('canvas');
    const gradient = canvas.getContext('2d').createLinearGradient(a.r, a.g, a.b, 0)
    gradient.addColorStop(0.0, 'rgba(' + b.r + ',' + b.g + ',' + b.b + ',' + '0.4)')
    gradient.addColorStop(0.5, 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',' + '0.6)')
    gradient.addColorStop(1, 'rgba(' + d.r + ',' + d.g + ',' + d.b + ',' + '0.8)')
    return gradient;

}




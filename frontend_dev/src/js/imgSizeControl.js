/**
 * イメージサイズのコントロール用
 */

const IMDBX_PATTERN = /(^https:\/\/m.media-amazon.com\/images\/.+_[A-Z]X)(\d+)(_CR)(\d+)(,\d+),(\d+),(\d+)(.*.jpg)/
const IMDBY_PATTERN = /(^https:\/\/m.media-amazon.com\/images\/.+_[A-Z]Y)(\d+)(_CR)(\d+)(,\d+),(\d+),(\d+)(.*.jpg)/
const AMAZON1_PATTERN = /(^https:\/\/images-na.ssl-images-amazon.com\/images\/.*_[A-Z]{2})(\d+)(_.jpg)/
const AMAZON2_PATTERN = /(^https:\/\/m.media-amazon.com\/images\/.*_[A-Z]{2})(\d+)(_.jpg)/

const SIZE = {
    imdbX: {
        small: '$164$3$4$5,64,128$8',
        middle: '$1182$3$4$5,182,268$8',
        large: '$1546$3$4$5,546,804$8',
    },
    imdbY: {
        small: '$1128$3$4$5,64,128$8',
        middle: '$1268$3$4$5,182,268$8',
        large: '$1804$3$4$5,546,804$8',
    },
    amazon: {
        small: '$164$3',
        middle: '$1268$3',
        large: '$1512$3',
    }
}

export function getImgUrl(url, size) {
    //画像のサイズ変更 'small','middle','large'で指定
    if (IMDBX_PATTERN.test(url)) {
        return url.replace(IMDBX_PATTERN, SIZE.imdbX[size])
    }
    if (IMDBY_PATTERN.test(url)) {
        return url.replace(IMDBY_PATTERN, SIZE.imdbY[size])
    }
    if (AMAZON1_PATTERN.test(url)) {
        return url.replace(AMAZON1_PATTERN, SIZE.amazon[size])
    }
    if (AMAZON2_PATTERN.test(url)) {
        return url.replace(AMAZON2_PATTERN, SIZE.amazon[size])
    }
    return url;
}

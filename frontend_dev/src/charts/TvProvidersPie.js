/**
 * 配信ストリーミングプロバイダ別円チャート
 * */
import { Doughnut } from 'vue-chartjs'
import { aggProviders } from "@/js/statistics.js";
import { setFilter } from "@/js/filter"
import { getGradient } from "./gradient"


export default {
    extends: Doughnut,
    methods: {
        handle(point, chartElement) {
            //クリック時処理
            const index = chartElement[0]._index;
            setFilter(this.getAggProviders[index].name)
        },
        setLabels(chart) {
            //ラベルを表示する
            const ctx = chart.ctx
            chart.data.datasets.forEach((dataset, i) => {
                //データの総計
                const dataSum = dataset.data.reduce((sum, element) => {
                    sum += element
                    return sum
                }, 0)
                const meta = chart.getDatasetMeta(i)
                if (!meta.hidden) {
                    meta.data.forEach(function (element, index) {
                        // フォントの設定
                        const fontSize = 12
                        const fontStyle = 'italic'
                        const fontFamily = 'Helvetica Neue'
                        // 設定を適用
                        ctx.font = fontStyle + " " + fontSize + "px " + " '" + fontFamily + "'"

                        // 5%以上のデータをラベル表示
                        const dataPersentage = (Math.round(dataset.data[index] / dataSum * 100))
                        const labelString = dataPersentage >= 5 ? chart.data.labels[index] : ""
                        const dataString = dataPersentage >= 5 ? dataset.data[index].toString() : ""

                        // positionの設定
                        ctx.textAlign = 'center'
                        ctx.textBaseline = 'middle'

                        const padding = -2
                        const position = element.tooltipPosition()
                        // ツールチップに変更内容を表示
                        ctx.fillText(labelString, position.x, position.y - (fontSize / 2) - padding) // title
                        ctx.fillText(dataString, position.x, position.y + (fontSize / 2) - padding)  // データ
                    })
                }
            })
        },
        getOptions() {
            //オプション
            return {
                plugins: {
                    labels: {
                        render: 'label',
                        position: 'outside'
                    }
                },
                tooltips: {
                    callbacks: {
                        //マウスオーバー時のホバー表示
                        label: function (tooltipItems, data) {
                            return data.labels[tooltipItems.index]
                                + ':(' +
                                data.datasets[0].data[tooltipItems.index] + ')'
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Video Streming Providers',
                },
                responsive: true,
                onClick: this.handle,
                legend: { display: false },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
            };
        },
        getDataSets() {
            //データをセット
            return this.getAggProviders.reduce((datasets, provider) => {
                datasets.push({
                    label: provider.name,
                    backgroundColor: getGradient(),
                    borderColor: getGradient(),
                    borderWidth: 0.5,
                    data: provider.count
                })
                return datasets;
            }, []);
        },
        getDataCollection() {
            return {
                labels: this.getDataSets().map(item => item.label),
                datasets: [{
                    borderColor: this.getDataSets().map(item => item.borderColor),
                    backgroundColor: this.getDataSets().map(item => item.backgroundColor),
                    borderWidth: this.getDataSets().map(item => item.borderWidth),
                    data: this.getDataSets().map(item => item.data)
                }]
            };
        }
    },
    computed: {
        getAggProviders() {
            return aggProviders(this.$store.state.events)
        }
    },
    mounted() {
        this.addPlugin({
            afterDraw: (chart) => { this.setLabels(chart) }
        })
        this.renderChart(this.getDataCollection(), this.getOptions())
    }
}

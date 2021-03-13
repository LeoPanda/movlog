/**
 * 劇場/TV チャート
 */
import { HorizontalBar } from 'vue-chartjs'
import { setFilter } from "@/js/filter"
import { getGradient, getAltGradient } from "./gradient"
export default {
    extends: HorizontalBar,
    methods: {
        onClikHandle(e, el) {
            //クリック時処理
            const item = el[0]
            if (item) {
                setFilter(item._model.datasetLabel)
            }
        },
        setLabels(chart) {
            //ラベルを表示する
            const ctx = chart.ctx
            chart.data.datasets.forEach((dataset, i) => {
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
                        const labelString = dataset.label
                        const dataString = dataset.data[index].toString()

                        // positionの設定
                        ctx.textAlign = 'right'
                        ctx.textBaseline = 'middle'

                        const padding = -6
                        const position = element.tooltipPosition()
                        // ツールチップに変更内容を表示
                        ctx.fillText(labelString, position.x + padding, position.y - (fontSize / 2) - padding) // title
                        ctx.fillText(dataString, position.x + padding, position.y + (fontSize / 2) - padding)  // データ
                    })
                }
            })
        },

        getOptions() {
            //全体オプション
            return {
                responsive: true,
                onClick: this.onClikHandle,
                legend: { display: false },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                title: {
                    display: true,
                    text: "at theater vs. on TV"
                },
                scales: {
                    xAxes: [{
                        display: false,
                        stacked: true,
                    }],
                    yAxes: [{
                        display: false,
                        stacked: true,
                    }]
                }
            };
        },
        getDataCollection() {
            //表示データセット
            return {
                labels: ["atTheater", "onTV"],
                datasets: [
                    {
                        label: "atTheater",
                        backgroundColor: getGradient(),
                        borderColor: getAltGradient(),
                        borderWidth: 0.5,
                        barThickness: 40,
                        data: [this.$store.state.events.filter(event => event['on_tv'] != true).length],
                    },
                    {
                        label: "onTV",
                        backgroundColor: getGradient(),
                        borderColor: getAltGradient(),
                        borderWidth: 0.5,
                        barThickness: 40,
                        data: [this.$store.state.events.filter(event => event['on_tv'] == true).length],
                    },
                ],
            };
        }
    },
    mounted() {
        this.$refs.canvas.height = "80"
        this.addPlugin({
            afterDraw: (chart) => { this.setLabels(chart) }
        })
        this.renderChart(this.getDataCollection(), this.getOptions())
    }
}
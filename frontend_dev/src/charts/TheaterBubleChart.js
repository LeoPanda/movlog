/**
 * 劇場別鑑賞数バブルチャート
 * */
import { Bubble } from 'vue-chartjs'
import { aggTheater } from "@/js/statistics.js";
import { setFilter } from "@/js/filter"

export default {
    extends: Bubble,
    data() {
        return {
            theaters: [],
        }
    },
    methods: {
        handle(point, event) {
            //クリック時処理
            const index = event[0]._datasetIndex;
            setFilter(this.theaters[index].name)
        },
        colorize(x, y, bold) {
            //カラーチャート
            const odx = (x % 2) != 0;
            const ody = (y % 2) != 0;
            const r = odx && ody ? 250 : odx ? 150 : ody ? 50 : 0;
            const g = odx && ody ? 0 : odx ? 50 : ody ? 150 : 250;
            const b = odx && ody ? 0 : odx && ody ? 250 : 150;
            const a = bold ? 1 : 0.4

            return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
        },
        generateBubleBase() {
            //バブルの座標とカラーをランダムに生成
            const range = 120
            const x = Math.ceil(Math.random() * range);
            const y = Math.ceil(Math.random() * range);
            return ({
                'x': x,
                'y': y,
                color: this.colorize(x, y, true),
                backgroundColor: this.colorize(x, y, false)
            })
        },
        getOptions() {
            //オプション
            return {
                tooltips: {
                    callbacks: {
                        //マウスオーバー時のホバー表示
                        label: function (tooltipItems, data) {
                            return data.datasets[tooltipItems.datasetIndex].label +
                                ': (' + data.datasets[tooltipItems.datasetIndex].title + ')';
                        }
                    }
                },
                responsive: true,
                onClick: this.handle,
                legend: { display: false },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: false,
                        gridLines:
                        {
                            display: false,
                        },
                        scaleLabel: {
                            display: false,
                        },
                    }],
                    yAxes: [{
                        display: false,
                        gridLines:
                        {
                            display: false,
                        },
                        scaleLabel: {
                            display: false,
                        },
                    }]
                }
            };
        },
        getDataSets() {
            //データセット
            return this.theaters.reduce((datasets, theater) => {
                const base = this.generateBubleBase();
                datasets.push({
                    label: [theater.name],
                    title: theater.count,
                    backgroundColor: base.backgroundColor,
                    borderColor: base.color,
                    borderWidth: 0.3,
                    data:
                        [{
                            x: base.x,
                            y: base.y,
                            r: theater.count * 3
                        }]
                })
                return datasets;
            }, []);
        },
        getDataCollection() {
            return {
                labels: "labels",
                datasets: this.getDataSets(),
            };
        }
    },
    mounted() {
        this.$refs.canvas.height = "320"
        this.theaters = aggTheater(this.$store.state.events);
        this.renderChart(this.getDataCollection(), this.getOptions())
    }
}

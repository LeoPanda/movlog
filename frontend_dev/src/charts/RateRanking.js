/**
 * レートランキング
 */
import { HorizontalBar } from 'vue-chartjs'
import { aggRate } from "@/js/statistics"
import { setFilter } from "@/js/filter"
import { getGradient } from "./gradient"
export default {
    extends: HorizontalBar,
    methods: {
        onClikHandle(e, el) {
            //クリック時処理
            const item = el[0]
            if (item) {
                setFilter('rate=' + item._model.label)
            }
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
                    text: "rate ranking"
                },
                scales: {
                    xAxes: [{
                        display: true,
                        type: 'linear',
                        distribution: 'series',
                        offset: false,
                        stacked: false,
                        ticks: {
                            stepSize: 1
                        },
                        gridLines:
                        {
                            display: false,
                        },
                        scaleLabel: {
                            display: false,
                        },
                    }],
                    yAxes: [{
                        display: true,
                        stacked: false,
                        gridLines:
                        {
                            color: 'rgba(10, 100, 10, 0.1)'
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'STAR',
                        },
                    }]
                }
            };
        },
        getDataCollection() {
            //表示データセット
            const argData = aggRate(this.$store.state.events);
            return {
                labels: argData.map((item) => item.name),
                datasets: [
                    {
                        label: "作品数",
                        backgroundColor: getGradient(),
                        borderColor: getGradient(),
                        borderWidth: 0.5,
                        data: argData.map((item) => item.count),
                    },
                ],
            };
        }
    },
    mounted() {
        this.$refs.canvas.height = "420"
        this.renderChart(this.getDataCollection(), this.getOptions())
    }
}
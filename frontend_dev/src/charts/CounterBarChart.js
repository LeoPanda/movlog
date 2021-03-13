/**
 * 月別鑑賞数チャート
 */
import { Bar } from 'vue-chartjs'
import { MonthlyAggregate } from "@/js/statistics.js";
import { setFilter } from "@/js/filter"
import { getGradient, getAltGradient } from "./gradient"
export default {
    extends: Bar,
    methods: {
        onClikHandle(e, el) {
            //クリック時処理
            const item = el[0]
            if (item) {
                setFilter(item._model.label)
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
                scales: {
                    xAxes: [{
                        display: true,
                        type: 'time',
                        distribution: 'series',
                        offset: true,
                        stacked: true,
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
                        stacked: true,
                        gridLines:
                        {
                            color: 'rgba(10, 100, 10, 0.1)'
                        },
                        scaleLabel: {
                            display: false,

                        },
                    }]
                }
            };
        },
        getDataCollection() {
            //表示データセット
            const argEvents = MonthlyAggregate(this.$store.state.events);
            return {
                labels: argEvents.map((item) => item.name),
                datasets: [
                    {
                        label: "on TV",
                        backgroundColor: getAltGradient(),
                        borderColor: getAltGradient(),
                        data: argEvents.map((item) => item.tvCount),
                    },
                    {
                        label: "at theater",
                        backgroundColor: getGradient(),
                        borderColor: getGradient(),
                        data: argEvents.map((item) => item.count)
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
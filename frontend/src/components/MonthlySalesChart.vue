<template>

<div id="chart">
  <apexchart height="400" width='100%'  type="line" :options="options" :series="series"></apexchart>
</div>

</template>
<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  props: ['categories', 'data', 'theme', 'arr_length'],
  data: function() {
    return {
/*       options: {
        theme: {
          mode: this.theme
        },
        colors: ['#fc0'],
        chart: {
          id: 'yandex-market-parser'
        },
        xaxis: {
          categories:  this.categories
        }
      },
      series: [{
        name: 'Цена на Маркете',
        data: this.data
      }] */
            series: this.data /* [
            {
              'name': "High - 2013",
              'data': this.data
            },
            {
              name: "Low - 2013",
              data: this.data
            }
          ] */,
          options: {
            theme: {
               mode: this.theme
            },
            chart: {
              height: 350,
              type: 'line',
              dropShadow: {
                enabled: true,
                color: '#000',
                top: 18,
                left: 7,
                blur: 10,
                opacity: 0.2
              },
              toolbar: {
                show: true
              }
            },
            colors: ['#fc0'],
            dataLabels: {
              enabled: true,
            },
            /* stroke: {
              curve: 'smooth'
            }, */
            title: {
              text: 'График цены на товар && Аналоги',
              align: 'left'
            },
            grid: {
              borderColor: '#e7e7e7',
              row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
              },
            },
            markers: {
              size: 1
            },
            xaxis: {
              categories: this.data[this.arr_length-1].categories,
              title: {
                text: 'Дата'
              }
            },
            yaxis: {
              title: {
                text: 'Цены'
              },
              /* min: 5,
              max: 40 */
            },
            legend: {
              position: 'top',
              horizontalAlign: 'right',
              floating: true,
              offsetY: -25,
              offsetX: -5
            }
          },
    } 
  }, 
}
</script>

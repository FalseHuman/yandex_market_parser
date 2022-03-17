<template>

<div>
  <apexchart width="525" height="300" type="line" :options="options" :series="series"></apexchart>
</div>

</template>
<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  props: ['categories', 'data', 'theme'],
  data: function() {
    return {
      options: {
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
      }]
    }
  },
}
</script>

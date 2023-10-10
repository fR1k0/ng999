// ==============================================================
// Calling the chart
// ==============================================================

   // WATER CONDITIONS - EC
  var ec_line = {
    series: [
      {
        name: "Target EC Level",
        data: [140, 140, 140, 140, 140, 140, 140],
      },
      {
        name: "EC",
        data: [10, 41, 35, 51, 49, 91, 148],
      },
    ],
    chart: {
      height: 350,
      type: "line",
      fontFamily: '"Inter",sans-serif',
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["#E44E4E","#1C77FF"],
    stroke: {
      curve: "straight",
      width: [2,2],
      dashArray: [8, 0]
    },
    legend: {
      show: true,
      showForSingleSeries: false,
      showForNullSeries: true,
      showForZeroSeries: true,
      position: 'bottom',
      horizontalAlign: 'center', 
      floating: false,
      fontSize: '12px',
      fontFamily: 'Inter, Arial',
      fontWeight: 400,
      formatter: undefined,
      inverseOrder: false,
      width: undefined,
      height: undefined,
      tooltipHoverFormatter: undefined,
      customLegendItems: [],
      offsetX: 0,
      offsetY: 0,
      labels: {
          colors: undefined,
          useSeriesColors: false
      },
      markers: {
          width: 12,
          height: 12,
          strokeWidth: 0,
          strokeColor: '#fff',
          fillColors: undefined,
          radius: 12,
          customHTML: undefined,
          onClick: undefined,
          offsetX: 0,
          offsetY: 0
      },
      itemMargin: {
          horizontal: 20
      },
      onItemClick: {
          toggleDataSeries: true
      },
      onItemHover: {
          highlightDataSeries: true
      },
    },
    xaxis: {
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
      ],
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    tooltip: {
      theme: "dark",
    },
  };




// WATER CONDITIONS - PH
  var ph_line = {
    series: [
      {
        name: "Target PH Level",
        data: [100, 100, 100, 100, 100, 100, 100],
      },
      {
        name: "PH",
        data: [30, 41, 35, 61, 79, 91, 18],
      },
    ],
    chart: {
      height: 350,
      type: "line",
      fontFamily: '"Inter",sans-serif',
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["#E44E4E","#C1840B"],
    stroke: {
      curve: "straight",
      width: [2,2],
      dashArray: [8, 0]
    },
    legend: {
      show: true,
      showForSingleSeries: false,
      showForNullSeries: true,
      showForZeroSeries: true,
      position: 'bottom',
      horizontalAlign: 'center', 
      floating: false,
      fontSize: '12px',
      fontFamily: 'Inter, Arial',
      fontWeight: 400,
      formatter: undefined,
      inverseOrder: false,
      width: undefined,
      height: undefined,
      tooltipHoverFormatter: undefined,
      customLegendItems: [],
      offsetX: 0,
      offsetY: 0,
      labels: {
          colors: undefined,
          useSeriesColors: false
      },
      markers: {
          width: 12,
          height: 12,
          strokeWidth: 0,
          strokeColor: '#fff',
          fillColors: undefined,
          radius: 12,
          customHTML: undefined,
          onClick: undefined,
          offsetX: 0,
          offsetY: 0
      },
      itemMargin: {
          horizontal: 20
      },
      onItemClick: {
          toggleDataSeries: true
      },
      onItemHover: {
          highlightDataSeries: true
      },
    },
    xaxis: {
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
      ],
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    tooltip: {
      theme: "dark",
    },
  };





// WATER CONDITIONS - EC
  var ec_line = {
    series: [
      {
        name: "Target EC Level",
        data: [140, 140, 140, 140, 140, 140, 140],
      },
      {
        name: "EC",
        data: [10, 41, 35, 51, 49, 91, 148],
      },
    ],
    chart: {
      height: 350,
      type: "line",
      fontFamily: '"Inter",sans-serif',
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["#E44E4E","#1C77FF"],
    stroke: {
      curve: "straight",
      width: [2,2],
      dashArray: [8, 0]
    },
    legend: {
      show: true,
      showForSingleSeries: false,
      showForNullSeries: true,
      showForZeroSeries: true,
      position: 'bottom',
      horizontalAlign: 'center', 
      floating: false,
      fontSize: '12px',
      fontFamily: 'Inter, Arial',
      fontWeight: 400,
      formatter: undefined,
      inverseOrder: false,
      width: undefined,
      height: undefined,
      tooltipHoverFormatter: undefined,
      customLegendItems: [],
      offsetX: 0,
      offsetY: 0,
      labels: {
          colors: undefined,
          useSeriesColors: false
      },
      markers: {
          width: 12,
          height: 12,
          strokeWidth: 0,
          strokeColor: '#fff',
          fillColors: undefined,
          radius: 12,
          customHTML: undefined,
          onClick: undefined,
          offsetX: 0,
          offsetY: 0
      },
      itemMargin: {
          horizontal: 20
      },
      onItemClick: {
          toggleDataSeries: true
      },
      onItemHover: {
          highlightDataSeries: true
      },
    },
    xaxis: {
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
      ],
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    tooltip: {
      theme: "dark",
    },
  };


// REPORT GRAPH
   var report_graph = {
      series: [{
        name: "WL_BJ1",
        data: [45, 52, 38, 24, 33, 26, 21, 20, 6, 8, 15, 10],
        color: '#405DF9'
      },
      {
        name: "WL_AB1",
        data: [35, 41, 62, 42, 13, 18, 29, 37, 36, 51, 32, 35],
        color: '#ED589D'
      },
      {
        name: 'WL_AB2',
        data: [87, 57, 74, 99, 75, 38, 62, 47, 82, 56, 45, 47],
        color: '#F2A818'
      }
      ],
      chart: {
        type: 'line',
        height: 600,
        zoom: {
          enabled: false
        },
        toolbar: {
          show: false,
        },
      },
      legend: {
        show: false,
      },
      dataLabels: {
        enabled: false
      },
      colors: ["#1C77FF","#ED589D","#8A00BA"],
      stroke: {
        curve: "straight",
        width: [2,2,2]
      },
      markers: {
        size: 0,
        hover: {
          sizeOffset: 6
        }
      },
      xaxis: {
        categories: ['01 Jan', '02 Jan', '03 Jan', '04 Jan', '05 Jan', '06 Jan', '07 Jan', '08 Jan', '09 Jan',
          '10 Jan', '11 Jan', '12 Jan'
        ],
      },
      tooltip: {
        y: [
          {
            title: {
              formatter: function (val) {
                return val;
              }
            }
          },
          {
            title: {
              formatter: function (val) {
                return val;
              }
            }
          },
          {
            title: {
              formatter: function (val) {
                return val;
              }
            }
          }
        ]
      },
      grid: {
        borderColor: '#f1f1f1',
      }
    };


if ($("body").hasClass("dashboard")) {
  var chart_wc_ec = new ApexCharts(
    document.querySelector("#chart-wc-ec"),
    ec_line
  );
  chart_wc_ec.render();

  var chart_wc_ph = new ApexCharts(
    document.querySelector("#chart-wc-ph"),
    ph_line
  );
  chart_wc_ph.render();


  var chart_wc_temp = new ApexCharts(
    document.querySelector("#chart-wc-temp"),
    temp_line
  );
  chart_wc_temp.render();
}


if ($("body").hasClass("reports")) {
  var report_graph = new ApexCharts(
    document.querySelector("#report_graph"),
    report_graph
  );
  report_graph.render();
}



/*REVENUE PAGE CHART*/

// TOTAL REVENUE
  var revenue_line = {
    series: [
      {
        name: "Total Revenue",
        data: [50, 200, 200, 160, 220, 220, 250],
      },
      {
        name: "Total Lost",
        data: [80, 110, 100, 90, 130, 130, 180],
      },
      {
        name: "Total Cost",
        data: [50, 60, 50, 45, 65, 60, 85],
      },
    ],
    chart: {
      height: 350,
      type: "line",
      fontFamily: '"Inter",sans-serif',
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["rgba(64, 93, 249, 1)","rgba(237, 88, 157, 0.5)", "rgba(242, 168, 24, 0.5)"],
    stroke: {
      curve: "straight",
      width: [2,2,2]
    },
    legend: {
      show: false,
    },
    xaxis: {
      categories: [
        "May 11",
        "May 16",
        "May 21",
        "May 26",
        "June 1",
        "June 7",
        "June 11",
      ],
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    tooltip: {
      theme: "light",
    },
  };

// TOTAL LOST
  var lost_line = {
    series: [
      {
        name: "Total Revenue",
        data: [50, 200, 200, 160, 220, 220, 250],
      },
      {
        name: "Total Lost",
        data: [80, 110, 100, 90, 130, 130, 180],
      },
      {
        name: "Total Cost",
        data: [50, 60, 50, 45, 65, 60, 85],
      },
    ],
    chart: {
      height: 350,
      type: "line",
      fontFamily: '"Inter",sans-serif',
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["rgba(64, 93, 249, 0.5)","rgba(237, 88, 157, 1)", "rgba(242, 168, 24, 0.5)"],
    stroke: {
      curve: "straight",
      width: [2,2,2]
    },
    legend: {
      show: false,
    },
    xaxis: {
      categories: [
        "May 11",
        "May 16",
        "May 21",
        "May 26",
        "June 1",
        "June 7",
        "June 11",
      ],
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    tooltip: {
      theme: "light",
    },
  };


// TOTAL COST
  var cost_line = {
    series: [
      {
        name: "Total Revenue",
        data: [50, 200, 200, 160, 220, 220, 250],
      },
      {
        name: "Total Lost",
        data: [80, 110, 100, 90, 130, 130, 180],
      },
      {
        name: "Total Cost",
        data: [50, 60, 50, 45, 65, 60, 85],
      },
    ],
    chart: {
      height: 350,
      type: "line",
      fontFamily: '"Inter",sans-serif',
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["rgba(64, 93, 249, 0.5)","rgba(237, 88, 157, 0.5)", "rgba(242, 168, 24, 1)"],
    stroke: {
      curve: "straight",
      width: [2,2,2]
    },
    legend: {
      show: false,
    },
    xaxis: {
      categories: [
        "May 11",
        "May 16",
        "May 21",
        "May 26",
        "June 1",
        "June 7",
        "June 11",
      ],
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: [
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
            "#a1aab2",
          ],
        },
      },
    },
    tooltip: {
      theme: "light",
    },
  };


if ($("body").hasClass("revenue")) {
  var chart_revenue = new ApexCharts(
    document.querySelector("#chart-revenue"),
    revenue_line
  );
  chart_revenue.render();

  var chart_lost = new ApexCharts(
    document.querySelector("#chart-lost"),
    lost_line
  );
  chart_lost.render();


  var chart_cost = new ApexCharts(
    document.querySelector("#chart-cost"),
    cost_line
  );
  chart_cost.render();
}



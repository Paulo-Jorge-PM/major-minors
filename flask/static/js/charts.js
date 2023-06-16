  // Donut Chart
  var pieChartCanvas = $('#animais-chart-canvas').get(0).getContext('2d')
  var pieData        = {
    labels: [
        'Cão', 
        'Gato',
        'Burro',
        'Camelo',
        'Galinha'
    ],
    datasets: [
      {
        data: [30,12,20,50,60],
        backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#17a2b8', '#333333'],
      }
    ]
  }
  var pieOptions = {
    legend: {
      display: true
    },
    maintainAspectRatio : false,
    responsive : true,
  }
  //Create pie or douhnut chart
  // You can switch between pie and douhnut using the method below.
  var pieChart = new Chart(pieChartCanvas, {
    type: 'doughnut',
    data: pieData,
    options: pieOptions      
  });


   var pieChartCanvas = $('#religioes-chart-canvas').get(0).getContext('2d')
  var pieData        = {
    labels: [
        'Católica', 
        'Protestante',
        'Budista'
    ],
    datasets: [
      {
        data: [20,70,10],
        backgroundColor : ['#f56954', '#00a65a', '#f39c12'],
      }
    ]
  }
  var pieOptions = {
    legend: {
      display: true
    },
    maintainAspectRatio : false,
    responsive : true,
  }
  //Create pie or douhnut chart
  // You can switch between pie and douhnut using the method below.
  var pieChart = new Chart(pieChartCanvas, {
    type: 'doughnut',
    data: pieData,
    options: pieOptions      
  });




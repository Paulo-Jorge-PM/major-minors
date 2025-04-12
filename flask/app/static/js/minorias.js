var inView = false;
var inViewRadar = false;
var inViewPizza = false;

function isScrolledIntoView(elem)
{
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemTop <= docViewBottom) && (elemBottom >= docViewTop));
}

$(window).scroll(function() {
    if (isScrolledIntoView('#yearsChart')) {
        if (inView) { return; }
        inView = true;
        var ctx = document.getElementById('yearsChart').getContext('2d');

        var myBarChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '20013', '20014', '2015', '2016', '2017', '2018'],
            datasets: [{
                label: 'Número de notícias',
                backgroundColor: 'rgb(127, 233, 235)', //received as argument
                borderColor: 'rgb(127, 233, 235)', //received as argument
                data: [0, 10, 5, 2, 20, 30, 45, 0, 10, 5, 2, 20, 30, 45, 0, 10, 5, 2] //received as argument
            }]
          },  
          options: {}
        });
    } else {
        inView = false;  
    }
});




$(window).scroll(function() {
    if (isScrolledIntoView('#sentimentRadarChart')) {
        if (inViewRadar) { return; }
        inViewRadar = true;
        var ctx = document.getElementById('sentimentRadarChart').getContext('2d');

        var myRadarChart = new Chart(ctx, {
          type: 'radar',
          data: {
            labels: ['Positivo', 'Negativo', 'Neutro'],
            datasets: [{
                label: 'Sentimento',
                backgroundColor: 'rgb(126, 224, 157)',
                data: [10, 5, 2]
            }]
          },  
          options: {}
        });
    } else {
        inViewRadar = false;  
    }
});








function sliceSize(dataNum, dataTotal) {
  return (dataNum / dataTotal) * 360;
}

function addSlice(id, sliceSize, pieElement, offset, sliceID, color) {
  $(pieElement).append("<div class='slice "+ sliceID + "'><span></span></div>");
  var offset = offset - 1;
  var sizeRotation = -179 + sliceSize;

  $(id + " ." + sliceID).css({
    "transform": "rotate(" + offset + "deg) translate3d(0,0,0)"
  });

  $(id + " ." + sliceID + " span").css({
    "transform"       : "rotate(" + sizeRotation + "deg) translate3d(0,0,0)",
    "background-color": color
  });
}

function iterateSlices(id, sliceSize, pieElement, offset, dataCount, sliceCount, color) {
  var
    maxSize = 179,
    sliceID = "s" + dataCount + "-" + sliceCount;

  if( sliceSize <= maxSize ) {
    addSlice(id, sliceSize, pieElement, offset, sliceID, color);
  } else {
    addSlice(id, maxSize, pieElement, offset, sliceID, color);
    iterateSlices(id, sliceSize-maxSize, pieElement, offset+maxSize, dataCount, sliceCount+1, color);
  }
}






function createPie(id) {
  var
    listData      = [],
    listTotal     = 0,
    offset        = 0,
    i             = 0,
    pieElement    = id + " .pie-chart__pie"
    dataElement   = id + " .pie-chart__legend"

    color         = [
      "rgb(187,228,255)",
      "rgb(2,166,209)",
      "rgb(5,116,206)",
      "rgb(239,71,111)",
      "rgb(255,209,102)",
      "rgb(6,214,160)",
      "rgb(172,78,221)",
      "rgb(255,140,62)",
      "rgb(0,188,212)",
      "rgb(194,24,91)",
      "rgb(230,74,25)",
      "rgb(103,58,183)"
    ];

  color = shuffle( color );

  $(dataElement+" span").each(function() {
    listData.push(Number($(this).html()));
  });

  for(i = 0; i < listData.length; i++) {
    listTotal += listData[i];
  }

  for(i=0; i < listData.length; i++) {
    var size = sliceSize(listData[i], listTotal);
    iterateSlices(id, size, pieElement, offset, i, 0, color[i]);
    $(dataElement + " li:nth-child(" + (i + 1) + ")").css("border-color", color[i]);
    offset += size;
  }
}

function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i--) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }

    return a;
}

function createPieCharts() {
  createPie('.pieID--region' );
  createPie('.pieID--operations' );
}





$(window).scroll(function() {
    if (isScrolledIntoView('#lol')) {
        if (inViewPizza) { return; }
        inViewPizza = true;
        createPieCharts();
    } else {
        inViewPizza = false;  
    }
});

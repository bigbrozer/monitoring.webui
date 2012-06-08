function old_createRequests(chartData) {
    "use strict";

    var chart, graph, categoryAxis, chartScrollbar;

    // CHART ////////////////////////////////////
    chart = new AmCharts.AmSerialChart();
    chart.pathToImages = "/static/js/images/";
    chart.dataProvider = chartData;
    chart.categoryField = "date";

    // CATEGORY AXIS ////////////////////////////
    categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true;
    categoryAxis.equalSpacing = true;
    categoryAxis.minPeriod = "DD";

    // GRAPH ////////////////////////////////////
    graph = new AmCharts.AmGraph();
    graph.valueField = "remained";
    graph.type = "smoothedLine";

    // SCROLLBAR ////////////////////////////////
    chartScrollbar = new AmCharts.ChartScrollbar();
    chartScrollbar.graph = graph;
    chartScrollbar.scrollbarHeight = 25;
    chart.addChartScrollbar(chartScrollbar);

    chart.addGraph(graph);
    chart.write('chartContainer2');
}

function createRequests(chartData) {
    "use strict";

    var chart, graph, dataset, categoryAxesSettings, stockPanel,
        scrollbarSettings, cursorSettings, periodSelector, panelsSettings;

    // CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";
    // chart.dataProvider = chartData;

    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

    // DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "remained",
        toField: "value"
    }];
    dataset.dataProvider = chartData;
    dataset.categoryField = "date";
    chart.dataSets = [dataset];

    // PANEL ////////////////////////////////////
    stockPanel = new AmCharts.StockPanel();
    chart.panels = [stockPanel];

    // GRAPH ////////////////////////////////////
    graph = new AmCharts.StockGraph();
    graph.valueField = "value";
    graph.type = "smoothedLine";

    stockPanel.addStockGraph(graph);

    // OTHER SETTINGS ///////////////////////////
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graph;
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

    // PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
        period: "DD",
        count: 15,
        label: "2 Weeks"
    }, {
        period: "MM",
        count: 1,
        label: "1 Month"
    }, {
        period: "MM",
        count: 6,
        label: "6 Months"
    }, {
        period: "MM",
        count: 12,
        label: "1 Year"
    }, {
        period: "MAX",
        label: "MAX"
    }];
    chart.periodSelector = periodSelector;

    // PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;

    chart.panelsSettings = panelsSettings;

    chart.write('chartContainer');
}

function deleteAmChart() {
    "use strict";
    var node, tspan, i, bad;
    tspan = document.getElementsByTagName("tspan");
    for (i = 0; i < tspan.length; i += 1) {
        if (tspan[i].textContent === "chart by amcharts.com") {
            bad = tspan[i].parentNode.parentNode;
            bad.removeChild(bad.childNodes[0]);
            bad.removeChild(bad.childNodes[0]);
        }

    }
}
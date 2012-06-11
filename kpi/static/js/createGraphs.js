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

function createRequests() {
    "use strict";

    var chart, graphRemained, dataset, dataset2, dataset3, categoryAxesSettings,
        stockPanelRemained, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings, graphOpened, stockPanelOpened, graphClosed,
        stockPanelClosed, stockLegendRemained, stockLegendOpened,
        stockLegendClosed, period_value;

    // CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";
    // chart.dataProvider = chartData;

    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

    // DATASET //////////////////////////////////
// Dataset 1 : remained  ---------------------------------------
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "remained",
        toField: "remained"
    }, {
        fromField: "opened",
        toField: "opened"
    }, {
        fromField: "closed",
        toField: "closed"
    }];
    dataset.dataProvider = chartData;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) First panel value : remained ----------------------------
    period_value = "High";

    graphRemained = new AmCharts.StockGraph();
    graphRemained.valueField = "remained";
    graphRemained.type = "smoothedLine";
    graphRemained.title = "Remained"
    graphRemained.lineThickness = 2;
    graphRemained.lineColor = "#FF0000";
    graphRemained.useDataSetColors = false;
    graphRemained.periodValue = period_value;

//  1) StockPanel options
    stockPanelRemained = new AmCharts.StockPanel();
    stockPanelRemained.title = "Requests";
    stockPanelRemained.percentHeight = 34;
    stockPanelRemained.addStockGraph(graphRemained);
    stockPanelRemained.showCategoryAxis = false;

//  1) StockLegend options
    stockLegendRemained = new AmCharts.StockLegend();
    stockPanelRemained.stockLegend = stockLegendRemained;

//  2) Second panel value : opened -----------------------------
    graphOpened = new AmCharts.StockGraph();
    graphOpened.valueField = "opened";
    graphOpened.type = "column";
    graphOpened.title = "Opened";
    graphOpened.lineThickness = 2;
    graphOpened.lineColor = "#FF9900";
    graphOpened.useDataSetColors = false;
    graphOpened.fillAlphas = 1;
    graphOpened.periodValue = period_value;
    graphOpened.cornerRadiusTop = 2;

//  2) StockPanel options
    stockPanelOpened = new AmCharts.StockPanel();
    stockPanelOpened.percentHeight = 50;
    stockPanelOpened.addStockGraph(graphOpened);

//  2) StockLegend options
    stockLegendOpened = new AmCharts.StockLegend();
    stockPanelOpened.stockLegend = stockLegendOpened;

//  3) Third panel value : closed ------------------------------
    graphClosed = new AmCharts.StockGraph();
    graphClosed.valueField = "closed";
    graphClosed.title = "Closed";
    graphClosed.lineThickness = 2;
    graphClosed.type = "smoothedLine";
    graphClosed.fillColor = "#00CC00";
    graphClosed.lineColor = "#00CC00";
    graphClosed.useDataSetColors = false;
    graphClosed.fillAlphas = 0.15;
    graphClosed.cornerRadiusTop = 2;
    graphClosed.periodValue = period_value;
    stockPanelOpened.addStockGraph(graphClosed);

    chart.panels = [stockPanelRemained, stockPanelOpened];

    // OTHER SETTINGS ///////////////////////////
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graphRemained;
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
        label: "2 Weeks",
        selected: false
    }, {
        period: "MM",
        count: 1,
        label: "1 Month",
        selected: false
    }, {
        period: "MM",
        count: 6,
        label: "6 Months",
        selected: false
    }, {
        period: "YYYY",
        count: 1,
        label: "1 Year",
        selected: false
    }, {
        period: "MAX",
        label: "MAX",
        selected: true
    }];
    chart.periodSelector = periodSelector;

    // PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;

    chart.panelsSettings = panelsSettings;

    chart.write('graphRequest');
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

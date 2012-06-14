function old_createRequests() {
    "use strict";

    var chart, graph, categoryAxis, chartScrollbar;

    // CHART ////////////////////////////////////
    chart = new AmCharts.AmSerialChart();
    chart.pathToImages = "/static/js/images/";
    chart.dataProvider = chartDataRequest;
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
    chart.write('graphRequest');
}

/////////////////// REQUESTS ///////////////////////////////////////////////////

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
    dataset.dataProvider = chartDataRequest;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) First panel value : remained ----------------------------
    period_value = "Average";

    graphRemained = new AmCharts.StockGraph();
    graphRemained.valueField = "remained";
    graphRemained.type = "smoothedLine";
    graphRemained.title = "Remained";
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
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' '};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;

    chart.write('graphRequest');
    deleteAmChart();
}


/////////////////// LIFETIME ///////////////////////////////////////////////////


function createLifetime() {
    "use strict";
    var chart, categoryAxesSettings, dataset, period_value, graphLifetimeGlobal,
        stockPanelLifetime, stockLegendLifetime, graphLifetimeNormal,
        graphLifetimeHigh, graphLifetimeUrgent, scrollbarSettings,
        cursorSettings, periodSelector, panelsSettings;

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
        fromField: "global",
        toField: "global"
    }, {
        fromField: "normal",
        toField: "normal"
    }, {
        fromField: "high",
        toField: "high"
    }, {
        fromField: "urgent",
        toField: "urgent"
    }];
    dataset.dataProvider = chartDataLifetime;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) First graph value : global ----------------------------
    period_value = "Average";

    graphLifetimeGlobal = new AmCharts.StockGraph();
    graphLifetimeGlobal.valueField = "global";
    graphLifetimeGlobal.type = "smoothedLine";
    graphLifetimeGlobal.title = "Global";
    graphLifetimeGlobal.lineThickness = 2;
    graphLifetimeGlobal.lineColor = "#000000";
    graphLifetimeGlobal.useDataSetColors = false;
    graphLifetimeGlobal.fillAlphas = 0.1;
    graphLifetimeGlobal.periodValue = period_value;
    chart.numberFormatter = {precision: 0};

//  1) StockPanel options
    stockPanelLifetime = new AmCharts.StockPanel();
    stockPanelLifetime.title = "Lifetime";
    stockPanelLifetime.percentHeight = 34;
    stockPanelLifetime.addStockGraph(graphLifetimeGlobal);

//  1) StockLegend options
    stockLegendLifetime = new AmCharts.StockLegend();
    stockPanelLifetime.stockLegend = stockLegendLifetime;

//  2) Second graph value : normal -----------------------------
    graphLifetimeNormal = new AmCharts.StockGraph();
    graphLifetimeNormal.valueField = "normal";
    graphLifetimeNormal.type = "smoothedLine";
    graphLifetimeNormal.title = "Normal";
    graphLifetimeNormal.hidden = true;
    graphLifetimeNormal.lineThickness = 2;
    graphLifetimeNormal.lineColor = "#0066FF";
    graphLifetimeNormal.useDataSetColors = false;
    graphLifetimeNormal.fillAlphas = 0.1;
    graphLifetimeNormal.periodValue = period_value;
    graphLifetimeNormal.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeNormal);

//  3) Third graph value : high ------------------------------
    graphLifetimeHigh = new AmCharts.StockGraph();
    graphLifetimeHigh.valueField = "high";
    graphLifetimeHigh.type = "smoothedLine";
    graphLifetimeHigh.title = "High";
    graphLifetimeHigh.hidden = true;
    graphLifetimeHigh.lineThickness = 2;
    graphLifetimeHigh.lineColor = "#FF9900";
    graphLifetimeHigh.useDataSetColors = false;
    graphLifetimeHigh.fillAlphas = 0.1;
    graphLifetimeHigh.periodValue = period_value;
    graphLifetimeHigh.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeHigh);

//  4) Fourth graph value : urgent ------------------------------
    graphLifetimeUrgent = new AmCharts.StockGraph();
    graphLifetimeUrgent.valueField = "urgent";
    graphLifetimeUrgent.type = "smoothedLine";
    graphLifetimeUrgent.title = "Urgent";
    graphLifetimeUrgent.hidden = true;
    graphLifetimeUrgent.lineThickness = 2;
    graphLifetimeUrgent.lineColor = "#FF0000";
    graphLifetimeUrgent.useDataSetColors = false;
    graphLifetimeUrgent.fillAlphas = 0.1;
    graphLifetimeUrgent.periodValue = period_value;
    graphLifetimeUrgent.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeUrgent);

    chart.panels = [stockPanelLifetime];

    // OTHER SETTINGS ///////////////////////////
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graphLifetimeNormal;
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
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' '};
    panelsSettings.usePrefixes = true;
    panelsSettings.prefixesOfBigNumbers = [{number: 1, prefix: " hours"}, {number: 24, prefix: " days"}];

    chart.panelsSettings = panelsSettings;

    chart.write('graphLifetime');
    deleteAmChart();

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

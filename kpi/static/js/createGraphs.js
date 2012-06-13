/*jslint plusplus: true */
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
        stockLegendClosed, period_value, graphLifetimeGlobal,
        stockPanelLifetime, stockLegendLifetime, graphLifetimeNormal,
        graphLifetimeHigh, graphLifetimeUrgent, panelsSettings2;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// DATASET //////////////////////////////////
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
    }, {
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
    dataset.dataProvider = chartDataRequest;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

// PANELS ///////////////////////////////////

//  1.1) graph Remained
    period_value = "Average";

    graphRemained = new AmCharts.StockGraph();
    graphRemained.valueField = "remained";
    graphRemained.type = "smoothedLine";
    graphRemained.title = "Remained";
    graphRemained.hideBulletsCount = 35;
    graphRemained.bullet = "bubble";
    graphRemained.lineThickness = 2;
    graphRemained.lineColor = "#FF0000";
    graphRemained.useDataSetColors = false;
    graphRemained.periodValue = "Close";

//  1.1) stockPanel Remained
    stockPanelRemained = new AmCharts.StockPanel();
    stockPanelRemained.title = "Requests";
    stockPanelRemained.percentHeight = 25;
    stockPanelRemained.addStockGraph(graphRemained);
    stockPanelRemained.showCategoryAxis = false;

//  1.1) stockLegend Remained
    stockLegendRemained = new AmCharts.StockLegend();
    stockLegendRemained.switchable = false;
    stockPanelRemained.stockLegend = stockLegendRemained;

//  1.2) graph Opened
    graphOpened = new AmCharts.StockGraph();
    graphOpened.valueField = "opened";
    graphOpened.type = "column";
    graphOpened.title = "Opened";
    // graphOpened.hideBulletsCount = 50;
    // graphOpened.bullet = "bubble";
    graphOpened.lineThickness = 2;
    graphOpened.lineColor = "#FF9900";
    graphOpened.useDataSetColors = false;
    graphOpened.fillAlphas = 1;
    graphOpened.periodValue = "Sum";
    graphOpened.cornerRadiusTop = 2;

//  1.2) stockPanel Opened (& Closed)
    stockPanelOpened = new AmCharts.StockPanel();
    stockPanelOpened.percentHeight = 25;
    stockPanelOpened.showCategoryAxis = false;
    stockPanelOpened.addStockGraph(graphOpened);

//  1.2) stockLegend Opened (& Closed)
    stockLegendOpened = new AmCharts.StockLegend();
    stockPanelOpened.stockLegend = stockLegendOpened;

//  1.3) graph Closed
    graphClosed = new AmCharts.StockGraph();
    graphClosed.valueField = "closed";
    graphClosed.title = "Closed";
    graphClosed.hideBulletsCount = 35;
    graphClosed.bullet = "bubble";
    graphClosed.lineThickness = 2;
    graphClosed.type = "smoothedLine";
    graphClosed.fillColor = "#00CC00";
    graphClosed.lineColor = "#00CC00";
    graphClosed.useDataSetColors = false;
    graphClosed.fillAlphas = 0.15;
    graphClosed.cornerRadiusTop = 2;
    graphClosed.periodValue = "Sum";
    stockPanelOpened.addStockGraph(graphClosed);

//  2.1) graph Lifetime Global
    period_value = "Average";

    graphLifetimeGlobal = new AmCharts.StockGraph();
    graphLifetimeGlobal.valueField = "global";
    graphLifetimeGlobal.type = "smoothedLine";
    graphLifetimeGlobal.title = "Global";
    graphLifetimeGlobal.hideBulletsCount = 35;
    graphLifetimeGlobal.bullet = "bubble";
    graphLifetimeGlobal.balloonText += " days";
    graphLifetimeGlobal.legendValueText += " days";
    graphLifetimeGlobal.lineThickness = 2;
    graphLifetimeGlobal.lineColor = "#000000";
    graphLifetimeGlobal.useDataSetColors = false;
    graphLifetimeGlobal.fillAlphas = 0.1;
    graphLifetimeGlobal.periodValue = period_value;

//  2.1) stockPanel Lifetime (all)
    stockPanelLifetime = new AmCharts.StockPanel();
    stockPanelLifetime.title = "Lifetime";
    stockPanelLifetime.percentHeight = 50;
    stockPanelLifetime.addStockGraph(graphLifetimeGlobal);

//  2.1) stockLegend Lifetime (all)
    stockLegendLifetime = new AmCharts.StockLegend();
    stockLegendLifetime.valueTextRegular += " days";
    stockPanelLifetime.stockLegend = stockLegendLifetime;

//  2.2) graph Lifetime Normal
    graphLifetimeNormal = new AmCharts.StockGraph();
    graphLifetimeNormal.valueField = "normal";
    graphLifetimeNormal.type = "smoothedLine";
    graphLifetimeNormal.title = "Normal";
    graphLifetimeNormal.hideBulletsCount = 35;
    graphLifetimeNormal.bullet = "bubble";
    graphLifetimeNormal.balloonText += " days";
    graphLifetimeNormal.hidden = true;
    graphLifetimeNormal.lineThickness = 2;
    graphLifetimeNormal.lineColor = "#0066FF";
    graphLifetimeNormal.useDataSetColors = false;
    graphLifetimeNormal.fillAlphas = 0.1;
    graphLifetimeNormal.periodValue = period_value;
    graphLifetimeNormal.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeNormal);

//  2.3) graph Lifetime High
    graphLifetimeHigh = new AmCharts.StockGraph();
    graphLifetimeHigh.valueField = "high";
    graphLifetimeHigh.type = "smoothedLine";
    graphLifetimeHigh.title = "High";
    graphLifetimeHigh.hideBulletsCount = 35;
    graphLifetimeHigh.bullet = "bubble";
    graphLifetimeHigh.balloonText += " days";
    graphLifetimeHigh.hidden = true;
    graphLifetimeHigh.lineThickness = 2;
    graphLifetimeHigh.lineColor = "#FF9900";
    graphLifetimeHigh.useDataSetColors = false;
    graphLifetimeHigh.fillAlphas = 0.1;
    graphLifetimeHigh.periodValue = period_value;
    graphLifetimeHigh.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeHigh);

//  2.4) graph Lifetime Urgent
    graphLifetimeUrgent = new AmCharts.StockGraph();
    graphLifetimeUrgent.valueField = "urgent";
    graphLifetimeUrgent.type = "smoothedLine";
    graphLifetimeUrgent.title = "Urgent";
    graphLifetimeUrgent.hideBulletsCount = 35;
    graphLifetimeUrgent.bullet = "bubble";
    graphLifetimeUrgent.balloonText += " days";
    graphLifetimeUrgent.hidden = true;
    graphLifetimeUrgent.lineThickness = 2;
    graphLifetimeUrgent.lineColor = "#FF0000";
    graphLifetimeUrgent.useDataSetColors = false;
    graphLifetimeUrgent.fillAlphas = 0.1;
    graphLifetimeUrgent.periodValue = period_value;
    graphLifetimeUrgent.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeUrgent);

    chart.panels = [stockPanelRemained, stockPanelOpened, stockPanelLifetime];

// OTHER SETTINGS (scrollBar & cursor)
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
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;

    chart.write('graphRequest');
    deleteAmChart();
}

function createHosts() {
    "use strict";
    var chart, categoryAxesSettings, dataset, graphHosts, stockPanelHosts,
        stockLegendHosts, graphServices, stockPanelServices,
        stockLegendServices, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "total_host",
        toField: "total_host"
    }, {
        fromField: "total_services",
        toField: "total_services"
    }];
    dataset.dataProvider = chartDataNagios;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) graph Hosts

    graphHosts = new AmCharts.StockGraph();
    graphHosts.valueField = "total_host";
    graphHosts.type = "smoothedLine";
    graphHosts.title = "Hosts";
    graphHosts.hideBulletsCount = 35;
    graphHosts.bullet = "bubble";
    graphHosts.lineThickness = 2;
    graphHosts.lineColor = "#0066FF";
    graphHosts.useDataSetColors = false;
    graphHosts.periodValue = "Average";

//  1) stockPanel Hosts
    stockPanelHosts = new AmCharts.StockPanel();
    stockPanelHosts.title = "Total Hosts";
    stockPanelHosts.percentHeight = 50;
    stockPanelHosts.addStockGraph(graphHosts);
    stockPanelHosts.showCategoryAxis = false;

//  1) stockLegend Hosts
    stockLegendHosts = new AmCharts.StockLegend();
    stockLegendHosts.switchable = false;
    stockPanelHosts.stockLegend = stockLegendHosts;

//  2) graph Services

    graphServices = new AmCharts.StockGraph();
    graphServices.valueField = "total_services";
    graphServices.type = "smoothedLine";
    graphServices.hideBulletsCount = 35;
    graphServices.bullet = "bubble";
    graphServices.title = "Services";
    graphServices.lineThickness = 2;
    graphServices.useDataSetColors = true;
    graphServices.periodValue = "Average";

//  2) stockPanel Services
    stockPanelServices = new AmCharts.StockPanel();
    stockPanelServices.title = "Total Services";
    stockPanelServices.percentHeight = 50;
    stockPanelServices.addStockGraph(graphServices);
    stockPanelServices.showCategoryAxis = false;

//  2) stockLegend Services
    stockLegendServices = new AmCharts.StockLegend();
    stockLegendServices.switchable = false;
    stockPanelServices.stockLegend = stockLegendServices;

    chart.panels = [stockPanelHosts, stockPanelServices];

// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graphServices;
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
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;

    chart.write('graphHosts');
    deleteAmChart();
}

function createWritten() {
    "use strict";
    var chart, categoryAxesSettings, dataset, graphWritten, stockPanelWritten,
        stockLegendWritten, graphMissing, scrollbarSettings, cursorSettings,
        periodSelector, panelsSettings, valueAxesSettings;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// valueAxesSettings
    valueAxesSettings = new AmCharts.ValueAxesSettings();
    chart.valueAxesSettings = valueAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "written_procedures",
        toField: "written_procedures"
    }, {
        fromField: "missing_procedures",
        toField: "missing_procedures"
    }];
    dataset.dataProvider = chartDataNagios;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

// PANELS ///////////////////////////////////

//  1) graph Written

    graphWritten = new AmCharts.StockGraph();
    graphWritten.valueField = "written_procedures";
    graphWritten.type = "smoothedLine";
    graphWritten.title = "Written procedures";
    graphWritten.balloonText += " ([[percents]]%)";
    graphWritten.lineColor = "#00CC00";
    graphWritten.lineThickness = 2;
    graphWritten.fillColor = "#00CC00";
    graphWritten.useDataSetColors = false;
    graphWritten.periodValue = "Average";
    graphWritten.fillAlphas = 0.7;
    graphWritten.stacked = true;
    graphWritten.hideBulletsCount = 35;
    graphWritten.bullet = "bubble";

//  1) stockPanel Written
    stockPanelWritten = new AmCharts.StockPanel();
    stockPanelWritten.title = "Total Written & Missing procedures";
    stockPanelWritten.percentHeight = 50;
    stockPanelWritten.addStockGraph(graphWritten);

//  1) stockLegend Written
    stockLegendWritten = new AmCharts.StockLegend();
    stockLegendWritten.valueTextRegular = "[[percents]]%";
    stockPanelWritten.stockLegend = stockLegendWritten;

//  2) graph Missing

    graphMissing = new AmCharts.StockGraph();
    graphMissing.valueField = "missing_procedures";
    graphMissing.type = "smoothedLine";
    graphMissing.title = "Missing procedures";
    graphMissing.balloonText += " ([[percents]]%)";
    graphMissing.lineColor = "#FF0000";
    graphMissing.lineThickness = 2;
    graphMissing.fillColor = "#FF0000";
    graphMissing.useDataSetColors = false;
    graphMissing.periodValue = "Average";
    graphMissing.fillAlphas = 0.7;
    graphMissing.stacked = true;
    graphMissing.hideBulletsCount = 35;
    graphMissing.bullet = "bubble";

    stockPanelWritten.addStockGraph(graphMissing);

    chart.panels = [stockPanelWritten];

// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
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
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;

    chart.write('graphWritten');
    deleteAmChart();
}

/*
    {
        fromField: "linux",
        toField: "linux"
    }, {
        fromField: "windows",
        toField: "windows"
    }, {
        fromField: "aix",
        toField: "aix"
    }, {
        fromField: "alerts_hard_warning",
        toField: "alerts_hard_warning"
    }, {
        fromField: "alerts_hard_critical",
        toField: "alerts_hard_critical"
    }, {
        fromField: "alerts_acknowledged_warning",
        toField: "alerts_acknowledged_warning"
    }, {
        fromField: "alerts_acknowledged_critical",
        toField: "alerts_acknowledged_critical"
    }
*/
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

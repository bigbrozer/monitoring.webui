/* script which generate the different charts with the parameters *
and all the options */
function oldCreateRequests() {
    /*
    example of creation for a simple serial chart, unused for now
    */
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
    graph.type = "line";

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

    var chart, graphRemained, dataset, categoryAxesSettings,
        stockPanelRemained, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings, graphOpened, stockPanelOpened, graphClosed,
        stockPanelClosed, stockLegendRemained, stockLegendOpened,
        stockLegendClosed, period_value, graphLifetimeGlobal,
        stockPanelLifetime, stockLegendLifetime, graphLifetimeNormal,
        graphLifetimeHigh, graphLifetimeUrgent;

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
    }, {
        fromField: "url",
        toField: "url"
    }];
    dataset.dataProvider = chartDataRequest;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];
    chart.balloon.showBullet = false;

// PANELS ///////////////////////////////////

//  1.1) graph Remained
    period_value = "Average";

    graphRemained = new AmCharts.StockGraph();
    graphRemained.valueField = "remained";
    graphRemained.urlField = "url";
    graphRemained.urlTarget = "_blank";
    graphRemained.type = "line";
    graphRemained.title = "Remained";
    graphRemained.hideBulletsCount = 100;
    graphRemained.bulletSize = 8;
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
    graphOpened.urlField = "url";
    graphOpened.urlTarget = "_blank";
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
    graphClosed.urlField = "url";
    graphClosed.urlTarget = "_blank";
    graphClosed.title = "Closed";
    graphClosed.hideBulletsCount = 35;
    graphClosed.bullet = "bubble";
    graphClosed.lineThickness = 2;
    graphClosed.type = "line";
    graphClosed.fillColor = "#00CC00";
    graphClosed.lineColor = "#00CC00";
    graphClosed.useDataSetColors = false;
//    graphClosed.fillAlphas = 0.15;
    graphClosed.cornerRadiusTop = 2;
    graphClosed.periodValue = "Sum";
    stockPanelOpened.addStockGraph(graphClosed);

//  2.1) graph Lifetime Global
    period_value = "Average";

    graphLifetimeGlobal = new AmCharts.StockGraph();
    graphLifetimeGlobal.valueField = "global";
    graphLifetimeGlobal.type = "line";
    graphLifetimeGlobal.title = "Low";
    graphLifetimeGlobal.hideBulletsCount = 35;
    graphLifetimeGlobal.bullet = "bubble";
//    graphLifetimeGlobal.balloonText += " days";
//    graphLifetimeGlobal.legendValueText += " days";
    graphLifetimeGlobal.lineThickness = 2;
    graphLifetimeGlobal.hidden = true;
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
//    stockLegendLifetime.valueTextRegular += " days";
    stockPanelLifetime.stockLegend = stockLegendLifetime;

//  2.2) graph Lifetime Normal
    graphLifetimeNormal = new AmCharts.StockGraph();
    graphLifetimeNormal.valueField = "normal";
    graphLifetimeNormal.type = "line";
    graphLifetimeNormal.title = "Normal";
    graphLifetimeNormal.hideBulletsCount = 35;
    graphLifetimeNormal.bullet = "bubble";
//    graphLifetimeNormal.balloonText += " days";
    graphLifetimeNormal.hidden = false;
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
    graphLifetimeHigh.type = "line";
    graphLifetimeHigh.title = "High";
    graphLifetimeHigh.hideBulletsCount = 35;
    graphLifetimeHigh.bullet = "bubble";
//    graphLifetimeHigh.balloonText += " days";
    graphLifetimeHigh.hidden = false;
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
    graphLifetimeUrgent.type = "line";
    graphLifetimeUrgent.title = "Urgent";
    graphLifetimeUrgent.hideBulletsCount = 35;
    graphLifetimeUrgent.bullet = "bubble";
//    graphLifetimeUrgent.balloonText += " days";
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
        count: 3,
        label: "3 Month",
        selected: true
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
        selected: false
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
    graphHosts.type = "line";
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
    graphServices.type = "line";
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
        count: 3,
        label: "3 Month",
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
    valueAxesSettings.stackType = "regular";
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
    graphWritten.type = "line";
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

//  1) stockLegend Written
    stockLegendWritten = new AmCharts.StockLegend();
    stockLegendWritten.valueTextRegular = "[[percents]]%";
    stockPanelWritten.stockLegend = stockLegendWritten;

//  2) graph Missing

    graphMissing = new AmCharts.StockGraph();
    graphMissing.valueField = "missing_procedures";
    graphMissing.type = "line";
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

    stockPanelWritten.addStockGraph(graphWritten);
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
        count: 3,
        label: "3 Month",
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

function createEquipements() {
    "use strict";
    var chart, categoryAxesSettings, dataset, graphLinux, stockPanelLinux,
        stockLegendLinux, graphWindows, graphAix, scrollbarSettings,
        cursorSettings, periodSelector, panelsSettings, valueAxesSettings;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// valueAxesSettings
    valueAxesSettings = new AmCharts.ValueAxesSettings();
    valueAxesSettings.stackType = "regular";
    chart.valueAxesSettings = valueAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "linux",
        toField: "linux"
    }, {
        fromField: "windows",
        toField: "windows"
    }, {
        fromField: "aix",
        toField: "aix"
    }];
    dataset.dataProvider = chartDataNagios;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

// PANELS ///////////////////////////////////

//  1) graph Linux

    graphLinux = new AmCharts.StockGraph();
    graphLinux.valueField = "linux";
    graphLinux.type = "line";
    graphLinux.title = "Linux";
    graphLinux.balloonText += " ([[percents]]%)";
    graphLinux.lineColor = "#FFCC00";
    graphLinux.lineThickness = 2;
    graphLinux.fillColor = "#FFCC00";
    graphLinux.useDataSetColors = false;
    graphLinux.periodValue = "Average";
    graphLinux.fillAlphas = 0.7;
    graphLinux.stacked = false;
    graphLinux.hideBulletsCount = 35;
    graphLinux.bullet = "bubble";

//  1) stockPanel Linux
    stockPanelLinux = new AmCharts.StockPanel();
    stockPanelLinux.title = "Number Of Equipement";
    stockPanelLinux.percentHeight = 50;

//  1) stockLegend Linux
    stockLegendLinux = new AmCharts.StockLegend();
    stockLegendLinux.valueTextRegular = "[[percents]]%";
    stockPanelLinux.stockLegend = stockLegendLinux;

//  2) graph Windows

    graphWindows = new AmCharts.StockGraph();
    graphWindows.valueField = "windows";
    graphWindows.type = "line";
    graphWindows.title = "Windows";
    graphWindows.balloonText += " ([[percents]]%)";
    graphWindows.lineColor = "#0066FF";
    graphWindows.lineThickness = 2;
    graphWindows.fillColor = "#0066FF";
    graphWindows.useDataSetColors = false;
    graphWindows.periodValue = "Average";
    graphWindows.fillAlphas = 0.7;
    graphWindows.stacked = false;
    graphWindows.hideBulletsCount = 35;
    graphWindows.bullet = "bubble";

//  3) graph Aix

    graphAix = new AmCharts.StockGraph();
    graphAix.valueField = "aix";
    graphAix.type = "line";
    graphAix.title = "Aix";
    graphAix.balloonText += " ([[percents]]%)";
    graphAix.lineColor = "#FF0000";
    graphAix.lineThickness = 2;
    graphAix.fillColor = "#FF0000";
    graphAix.useDataSetColors = false;
    graphAix.periodValue = "Average";
    graphAix.fillAlphas = 0.7;
    graphAix.stacked = false;
    graphAix.hideBulletsCount = 35;
    graphAix.bullet = "bubble";

    stockPanelLinux.addStockGraph(graphWindows);
    stockPanelLinux.addStockGraph(graphAix);
    stockPanelLinux.addStockGraph(graphLinux);


    chart.panels = [stockPanelLinux];

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
        count: 3,
        label: "3 Month",
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

    chart.write('graphEquipement');
    deleteAmChart();
}

function createAlerts() {
    "use strict";

    var chart, categoryAxesSettings, dataset, graphWarning, stockPanelWarning,
        stockLegendWarning, graphWarningAck, graphCritical, stockPanelCritical,
        stockLegendCritical, graphCriticalAck, scrollbarSettings,
        cursorSettings, periodSelector, panelsSettings, valueAxesSettings;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// valueAxesSettings
    valueAxesSettings = new AmCharts.ValueAxesSettings();
    // valueAxesSettings.stackType = "regular";
    chart.valueAxesSettings = valueAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "warning",
        toField: "warning"
    }, {
        fromField: "warning_acknowledged",
        toField: "warning_acknowledged"
    }, {
        fromField: "critical",
        toField: "critical"
    }, {
        fromField: "critical_acknowledged",
        toField: "critical_acknowledged"
    }];
    dataset.dataProvider = chartDataAlerts;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

// PANELS ///////////////////////////////////

//  1.1) graph Warning

    graphWarning = new AmCharts.StockGraph();
    graphWarning.valueField = "warning";
    graphWarning.type = "line";
    graphWarning.title = "Warning alerts";
    graphWarning.lineColor = "#FF0000";
    graphWarning.lineThickness = 2;
    graphWarning.fillColor = "#FF0000";
    graphWarning.useDataSetColors = false;
    graphWarning.periodValue = "Sum";
    graphWarning.fillAlphas = 0.7;
    graphWarning.hideBulletsCount = 35;
    graphWarning.bullet = "bubble";

//  1.1) stockPanel Warning
    stockPanelWarning = new AmCharts.StockPanel();
    stockPanelWarning.title = "Warning alerts";
    stockPanelWarning.percentHeight = 50;
    stockPanelWarning.showCategoryAxis = false;

//  1.1) stockLegend Warning
    stockLegendWarning = new AmCharts.StockLegend();
    stockPanelWarning.stockLegend = stockLegendWarning;

//  1.2) graph WarningAck

    graphWarningAck = new AmCharts.StockGraph();
    graphWarningAck.valueField = "warning_acknowledged";
    graphWarningAck.type = "line";
    graphWarningAck.title = "Warning alerts acknowledged";
    graphWarningAck.lineColor = "#00CC00";
    graphWarningAck.lineThickness = 2;
    graphWarningAck.fillColor = "#00CC00";
    graphWarningAck.useDataSetColors = false;
    graphWarningAck.periodValue = "Sum";
    graphWarningAck.fillAlphas = 0.7;
    graphWarningAck.hideBulletsCount = 35;
    graphWarningAck.bullet = "bubble";

    stockPanelWarning.addStockGraph(graphWarning);
    stockPanelWarning.addStockGraph(graphWarningAck);

//  2.1) graph Critical

    graphCritical = new AmCharts.StockGraph();
    graphCritical.valueField = "critical";
    graphCritical.type = "line";
    graphCritical.title = "Critical alerts";
    graphCritical.lineColor = "#FF0000";
    graphCritical.lineThickness = 2;
    graphCritical.fillColor = "#FF0000";
    graphCritical.useDataSetColors = false;
    graphCritical.periodValue = "Sum";
    graphCritical.fillAlphas = 0.7;
    graphCritical.hideBulletsCount = 35;
    graphCritical.bullet = "bubble";

//  2.1) stockPanel Critical
    stockPanelCritical = new AmCharts.StockPanel();
    stockPanelCritical.title = "Critical alerts";
    stockPanelCritical.percentHeight = 50;

//  2.1) stockLegend Critical
    stockLegendCritical = new AmCharts.StockLegend();
    stockPanelCritical.stockLegend = stockLegendCritical;

//  2.2) graph CriticalAck

    graphCriticalAck = new AmCharts.StockGraph();
    graphCriticalAck.valueField = "critical_acknowledged";
    graphCriticalAck.type = "line";
    graphCriticalAck.title = "Critical alerts acknowledged";
    graphCriticalAck.lineColor = "#00CC00";
    graphCriticalAck.lineThickness = 2;
    graphCriticalAck.fillColor = "#00CC00";
    graphCriticalAck.useDataSetColors = false;
    graphCriticalAck.periodValue = "Sum";
    graphCriticalAck.fillAlphas = 0.7;
    graphCriticalAck.hideBulletsCount = 35;
    graphCriticalAck.bullet = "bubble";

    stockPanelCritical.addStockGraph(graphCritical);
    stockPanelCritical.addStockGraph(graphCriticalAck);

    chart.panels = [stockPanelWarning, stockPanelCritical];

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
        count: 3,
        label: "3 Month",
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

    chart.write('graphAlerts');
    deleteAmChart();

}

function createRecurrentsAlerts() {
    "use strict";
    var chart, legend, host;

// CHART ///////////////////////////////////
    chart = new AmCharts.AmPieChart();
    chart.dataProvider = chartDataRecurrentsAlerts;
    chart.titleField = "name";
    chart.valueField = "repetitions";
    chart.balloonText = "[[title]] : [[value]]/" + other;
    chart.labelText = "[[title]] : [[value]]";
    chart.urlField = "url";
    chart.urlTarget = "_blank";
    chart.pullOutRadius = "0%";
    chart.radius = "30%";
    chart.outlineThickness = 1.2;
    chart.outlineAlpha = 1;
    chart.outlineColor = "#FFFFFF";
    chart.depth3D = 15;
    chart.angle = 30;

    chart.write('graphRecurrentsAlerts');
    deleteAmChart();
}

function createOldestsAlerts() {
    "use strict";
    var chart;

// CHART ///////////////////////////////////
    chart = new AmCharts.AmPieChart();
    chart.dataProvider = chartDataOldestsAlerts;
    chart.titleField = "name";
    chart.valueField = "days";
    chart.descriptionField = "date_error"
    chart.balloonText = "[[title]] : [[value]] days ([[description]])";
    chart.labelText = "[[title]] : [[value]] days";
    chart.pullOutRadius = "0%";
    chart.radius = "30%";
    chart.outlineThickness = 1.2;
    chart.outlineAlpha = 1;
    chart.outlineColor = "#FFFFFF";
    chart.depth3D = 15;
    chart.angle = 30;

    chart.write('graphOldestsAlerts');
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

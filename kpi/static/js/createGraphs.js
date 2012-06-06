function createRequests(chartData) {
    "use strict";

    var chart, graph, dataset;

    // CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/js/images/";
    // chart.dataProvider = chartData;

    var categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "MM";
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
    //chart.categoryField = "date";

    // PANEL ////////////////////////////////////
    var stockPanel = new AmCharts.StockPanel();
    chart.panels = [stockPanel];

    // GRAPH ////////////////////////////////////
    graph = new AmCharts.StockGraph();
    graph.valueField = "value";
    graph.type = "smoothedLine";

    stockPanel.addStockGraph(graph);

    chart.write('chartContainer');
}
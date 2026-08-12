(function (window) {
  const charts = new Map();

  function getChartConstructor() {
    if (typeof window.Chart === "undefined") {
      throw new Error("Chart.js is not available. Check if the CDN loaded successfully.");
    }
    return window.Chart;
  }

  function getCanvasElement(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
      throw new Error(`Canvas element not found: ${canvasId}`);
    }
    if (!(canvas instanceof HTMLCanvasElement)) {
      throw new Error(`Element is not a canvas: ${canvasId}`);
    }
    return canvas;
  }

  function getCanvasContext(canvas) {
    const context = canvas.getContext("2d");
    if (!context) {
      throw new Error(`Unable to get 2D drawing context for canvas: ${canvas.id}`);
    }
    return context;
  }

  function destroyChart(canvasId) {
    const existing = charts.get(canvasId);
    if (existing && typeof existing.destroy === "function") {
      existing.destroy();
    }
    charts.delete(canvasId);
  }

  function createChart(canvasId, config) {
    const ChartClass = getChartConstructor();
    const canvas = getCanvasElement(canvasId);
    const context = getCanvasContext(canvas);

    destroyChart(canvasId);
    const chart = new ChartClass(context, config);
    charts.set(canvasId, chart);
    return chart;
  }

  function hasChartLibrary() {
    return typeof window.Chart !== "undefined";
  }

  window.ChartManager = {
    createChart,
    destroyChart,
    hasChartLibrary,
  };
})(window);

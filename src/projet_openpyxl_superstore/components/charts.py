from openpyxl.chart import BarChart, Reference, DoughnutChart
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList


def build_bar_chart(ws_data, ws_visualisations):
    chart_top10 = BarChart()
    chart_top10.type = "col"
    chart_top10.title = "TOP 10 du profit en fonction des sous-catégories"
    chart_top10.width = 18
    chart_top10.height = 10

    data_ref = Reference(ws_data, min_col=30, min_row=3, max_row=12)
    cats_ref = Reference(ws_data, min_col=29, min_row=4, max_row=12)

    chart_top10.add_data(data_ref, titles_from_data=True)
    chart_top10.set_categories(cats_ref)

    chart_top10.dataLabels = DataLabelList()
    chart_top10.dataLabels.showVal = True
    chart_top10.dataLabels.numFmt = '#,##0'

    chart_top10.y_axis.title = 'Profits (en $)'
    chart_top10.x_axis.title = 'Sous-catégories'
    chart_top10.legend = None

    ws_visualisations.add_chart(chart_top10, "C7")


def build_doughnut_chart(ws_data, ws_visualisations):
    chart_percent = DoughnutChart()
    chart_percent.width = 18
    chart_percent.height = 10
    
    labels = Reference(ws_data, min_col=26, min_row=26, max_row=28)
    data = Reference(ws_data, min_col=28, min_row=25, max_row=28)
    
    chart_percent.add_data(data, titles_from_data=True)
    chart_percent.set_categories(labels)
    chart_percent.title = "Part du CA pour chaque catégorie"

    chart_percent.dataLabels = DataLabelList()
    chart_percent.dataLabels.showPercent = True

    slices = [DataPoint(idx=i) for i in range(4)]
    plain, jam, lime, chocolate = slices
    chart_percent.series[0].data_points = slices
    plain.graphicalProperties.solidFill = "A9E6EB"
    jam.graphicalProperties.solidFill = "B7A9EB"
    lime.graphicalProperties.solidFill = "EBA9D7"

    ws_visualisations.add_chart(chart_percent, "C27")


def build_all_charts(ws_data, ws_visualisations):
    build_bar_chart(ws_data, ws_visualisations)
    build_doughnut_chart(ws_data, ws_visualisations)
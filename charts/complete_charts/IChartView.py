from PyQt5.QtChart import QChartView


class IChartView(QChartView):

    def __init__(self):
        super(IChartView, self).__init__()
        self.init_ui()

    def init_ui(self):
        pass
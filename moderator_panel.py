from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView, QTableWidget, QTableWidgetItem, QHeaderView


class ModeratorPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moderator Panel")
        self.layout=QVBoxLayout(self)

        # Create table view
        # Create table widget
        self.table_widget=QTableWidget()
        self.layout.addWidget(self.table_widget)

    def set_complaints_data(self, data):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data[0])) if data else self.table_widget.setColumnCount(0)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(item)))

                # Set header titles
        header_labels=["ID", "User ID", "Water Source ID", "Description", "Status"]
        self.table_widget.setHorizontalHeaderLabels(header_labels)
        header=self.table_widget.horizontalHeader()
        for a in range(len(header_labels)):
            header.setSectionResizeMode(a, QHeaderView.ResizeMode.Stretch)
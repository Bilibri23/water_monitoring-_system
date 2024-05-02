from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QDialogButtonBox


class RoleSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Role")
        layout = QVBoxLayout()

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Administrator", "Moderator", "Customer"])
        layout.addWidget(self.role_combo)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button = QDialogButtonBox(buttons)
        button.accepted.connect(self.accept)

        button.rejected.connect(self.reject)
        layout.addWidget(button)

        self.setLayout(layout)

    def selected_role(self):
        return self.role_combo.currentText()
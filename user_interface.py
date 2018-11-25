import sys
from paint_widget import PaintWidget
from PyQt5.QtWidgets import *
from segment_tree import SegmentTree

# Class of the main application window
class SegmentTreeVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        # Initializing widgets
        self.txt_tree_data = QLineEdit()
        self.radio_min_tree = QRadioButton('Min segment tree')
        self.radio_max_tree = QRadioButton('Max segment tree')
        self.radio_sum_tree = QRadioButton('Sum segment tree')
        self.txt_change_index = QLineEdit()
        self.txt_change_value = QLineEdit()
        self.txt_range_left = QLineEdit()
        self.txt_range_right = QLineEdit()
        self.paint_image = PaintWidget(self)
        self.scroll_area = QScrollArea()
        self.txt_tree_data_dis = QLineEdit()
        self.txt_interval = QLineEdit()
        self.txt_min = QLineEdit()
        self.txt_max = QLineEdit()
        self.txt_sum = QLineEdit()
        self.init_user_interface()
        self._segment_tree = None

    def init_user_interface(self):
        # Creating and positioning widgets
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnMinimumWidth(0, 200)

        groupbox_create_tree = QGroupBox("Создать дерево")
        vbox_create_tree = QVBoxLayout()
        vbox_create_tree.addWidget(QLabel('Данные:'))
        self.txt_tree_data.setToolTip("Значения вводятся через разделитель ','\n"
                                      "Например: 1, 7, 4, 22, -10")
        vbox_create_tree.addWidget(self.txt_tree_data)
        btn_create_tree = QPushButton('Создать')
        btn_create_tree.clicked.connect(self.btn_create_tree_click)
        vbox_create_tree.addWidget(btn_create_tree)
        groupbox_create_tree.setLayout(vbox_create_tree)

        groupbox_tree_type = QGroupBox('Тип дерева отрезков')
        vbox_tree_type = QVBoxLayout()
        self.radio_min_tree.setToolTip('В узле отображаются минимальное значение для поддерева')
        self.radio_max_tree.setToolTip('В узле отображаются максимальное значение для поддерева')
        self.radio_sum_tree.setToolTip('В узле отображается сумма значений для поддерева')
        vbox_tree_type.addWidget(self.radio_min_tree)
        self.radio_min_tree.setChecked(True)
        vbox_tree_type.addWidget(self.radio_max_tree)
        vbox_tree_type.addWidget(self.radio_sum_tree)
        groupbox_tree_type.setLayout(vbox_tree_type)

        groupbox_tree_update = QGroupBox('Изменить значение')
        form_tree_update = QFormLayout()
        form_tree_update.addRow('Индекс:', self.txt_change_index)
        form_tree_update.addRow('Значение:', self.txt_change_value)
        btn_tree_update = QPushButton('Изменить')
        btn_tree_update.clicked.connect(self.btn_tree_update_click)
        form_tree_update.addRow(btn_tree_update)
        groupbox_tree_update.setLayout(form_tree_update)

        groupbox_interval_information = QGroupBox('Информация об интервале')
        form_interval_information = QFormLayout()
        form_interval_information.addRow('Начало:', self.txt_range_left)
        form_interval_information.addRow('Конец:', self.txt_range_right)
        btn_get_information = QPushButton('Получить информацию')
        btn_get_information.clicked.connect(self.btn_get_information_click)
        form_interval_information.addRow(btn_get_information)
        groupbox_interval_information.setLayout(form_interval_information)

        groupbox_result = QGroupBox('Результат')
        form_result = QFormLayout()
        self.txt_interval.setReadOnly(True)
        self.txt_min.setReadOnly(True)
        self.txt_max.setReadOnly(True)
        self.txt_sum.setReadOnly(True)
        form_result.addRow('Интервал:', self.txt_interval)
        form_result.addRow('Минимум:', self.txt_min)
        form_result.addRow('Максимум:', self.txt_max)
        form_result.addRow('Сумма:', self.txt_sum)
        groupbox_result.setLayout(form_result)

        self.scroll_area.setWidget(self.paint_image)

        grid.addWidget(groupbox_create_tree, 0, 0)
        grid.addWidget(groupbox_tree_type, 1, 0)
        grid.addWidget(groupbox_tree_update, 2, 0)
        grid.addWidget(groupbox_interval_information, 3, 0)
        grid.addWidget(groupbox_result, 4, 0)
        grid.addWidget(self.scroll_area, 0, 1, 5, 1)
        grid.addWidget(QLabel('Данные дерева: '), 6, 0)
        self.txt_tree_data_dis.setReadOnly(True)
        self.txt_tree_data_dis.setToolTip('Данные отображаются в виде: [индекс; значение]')
        grid.addWidget(self.txt_tree_data_dis, 6, 1)
        grid.setColumnStretch(1, 1)

        self.setLayout(grid)

        desktop_width = QDesktopWidget().availableGeometry().width()
        desktop_height = QDesktopWidget().availableGeometry().height()
        self.setGeometry(0, 0, desktop_width * 0.7, desktop_height * 0.85)
        self.setWindowTitle('Визуализация дерева отрезков')
        self.center()
        self.show()

    def center(self):
        # Centering window
        frame_rectangle = self.frameGeometry()
        center_screen = QDesktopWidget().availableGeometry().center()
        frame_rectangle.moveCenter(center_screen)
        self.move(frame_rectangle.topLeft())

    def btn_create_tree_click(self):
		# Creating a tree of segments

        # Load tree data from row
        text_values = self.txt_tree_data.text()
        text_values = text_values.strip()
        text_values = text_values.strip(',')
        split_values = text_values.split(',')
        split_values = map(lambda item: item.strip(), split_values)
        values = list()

       # Add data to the list
        try:
            for value in split_values:
                if value == '':
                    continue
                values.append(int(value))
        except ValueError:
            self.show_message(QMessageBox.Information, 'Введены неверные значения.', 'Ошибка')
            return

        if len(values) > 127:
            self.show_message(QMessageBox.Information, 'Превышено допустимое количество элементов.\n'
                                                      'Максимально доступно: 127.', 'Предупреждение')
            return

        # Creating a tree of segments
        self._segment_tree = SegmentTree(values)
        self.show_tree_data()
        self.paint_image.set_segment_tree(self._segment_tree)

    def btn_tree_update_click(self):
        # Update tree item by index
        if self._segment_tree is None:
            self.show_message(QMessageBox.Information, 'Сперва необходимо создать дерево.', 'Ошибка')
            return
        try:
            # Read index and new value
            index = int(self.txt_change_index.text())
            value = int(self.txt_change_value.text())
            self._segment_tree.update(index, value)
            self.show_tree_data()
            self.paint_image.set_segment_tree(self._segment_tree)
        except ValueError:
            self.show_message(QMessageBox.Warning, 'Введены неверные значения.', 'Ошибка')
        except IndexError:
            self.show_message(QMessageBox.Warning, 'Указанный индекс вне диапазона.', 'Ошибка')

    def btn_get_information_click(self):
        # Display information about the corresponding segment
        if self._segment_tree is None:
            self.show_message(QMessageBox.Information, 'Сперва необходимо создать дерево.', 'Ошибка')
            return
        try:
            # Getting the boundaries of the segment
            range_left = int(self.txt_range_left.text())
            range_right = int(self.txt_range_right.text())

            # Information output
            self.txt_min.setText(str(self._segment_tree.segment_min(range_left, range_right)))
            self.txt_max.setText(str(self._segment_tree.segment_max(range_left, range_right)))
            self.txt_sum.setText(str(self._segment_tree.segment_sum(range_left, range_right)))
            self.txt_interval.setText('[{left}; {right}]'.format(left=range_left, right=range_right))
        except ValueError:
            self.show_message(QMessageBox.Warning, 'Введены неверные значения.', 'Ошибка')
        except IndexError:
            self.show_message(QMessageBox.Warning, 'Указанный индекс вне диапазона.', 'Ошибка')

    def show_message(self, icon, text, title):
        message_box = QMessageBox()
        message_box.setIcon(icon)
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.exec()

    def show_tree_data(self):
		# Output values of all elements of the tree
        tree_data = ''
        values = self._segment_tree.values
        index = 0
        for value in values:
            tree_data += '[{index}: {value}]'.format(index=index, value=value)
            index += 1

        self.txt_tree_data_dis.setText(tree_data)

    def paintEvent(self, q_paint_event):
        self.paint_image.set_tree_mode(self.get_tree_mode())
        self.paint_image.set_size(self.scroll_area.size())

    def get_tree_mode(self):
        if self.radio_min_tree.isChecked():
            return 0
        elif self.radio_max_tree.isChecked():
            return 1
        else:
            return 2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SegmentTreeVisualizer()
    sys.exit(app.exec())

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget


class PaintWidget(QWidget):
    def __init__(self, parent, segment_tree=None, tree_mode=0):
        super().__init__(parent)
        self._segment_tree = segment_tree
        self.resize(100, 100)

        self.node_width = 46
        self.tree_mode = tree_mode
        self.view_size = None

    def set_segment_tree(self, segment_tree):
        self._segment_tree = segment_tree
        self.update()

    def set_size(self, size):
        self.view_size = QSize(size.width() - 2, size.height() - 2)
        if self.width() >= size.width() - 2 or self.height() >= size.height() - 2:
            return
        self.resize(size.width() - 2, size.height() - 2)

    def set_tree_mode(self, tree_mode):
        self.tree_mode = tree_mode
        self.update()

    def paintEvent(self, q_paint_event):
        if self._segment_tree is None or len(self._segment_tree.values) == 0:
            return

        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Расчет высоты и ширины дерева
        tree_height = self.get_tree_height(1, 0, len(self._segment_tree.values) - 1, 1)
        width = 2 ** tree_height * self.node_width - 50
        if width < self.view_size.width():
            width = self.view_size.width()

        height = 50 + tree_height * self.node_width
        self.resize(width, height)

        self.print_subtree(painter, 0, len(self._segment_tree.values) - 1, 0,
                           self.width() / 2 - self.node_width / 2, False)
        painter.end()

    def print_subtree(self, painter, subtree_left, subtree_right,
                      vertical_level, previous_horizontal_offset, is_right_child):

        tree_height = self.get_tree_height(1, subtree_left, subtree_right, 1)

        horizontal_offset = previous_horizontal_offset
        vertical_offset = 25 + vertical_level * self.node_width
        if is_right_child:
            horizontal_offset += (self.node_width - 10) * 2 ** (tree_height - 1)
        else:
            horizontal_offset -= (self.node_width - 10) * 2 ** (tree_height - 1)

        if subtree_left == subtree_right:
            painter.setPen(QColor(255, 0, 0))
        else:
            painter.setPen(QColor(0, 0, 0))

        if vertical_level == 0:
            horizontal_offset = previous_horizontal_offset
        else:
            if is_right_child:
                painter.drawLine(horizontal_offset + self.node_width / 2, vertical_offset,
                                 previous_horizontal_offset + self.node_width, vertical_offset - self.node_width / 2)
            else:
                painter.drawLine(horizontal_offset + self.node_width / 2, vertical_offset,
                                 previous_horizontal_offset, vertical_offset - self.node_width / 2)

        painter.drawEllipse(horizontal_offset, vertical_offset, self.node_width, self.node_width)
        painter.drawText(horizontal_offset + 10, vertical_offset + 57,
                         '[{left}; {right}]'.format(left=subtree_left, right=subtree_right))

        if self.tree_mode == 0:
            painter.drawText(horizontal_offset + 19, vertical_offset + 25,
                             str(self._segment_tree.segment_min(subtree_left, subtree_right)))
        elif self.tree_mode == 1:
            painter.drawText(horizontal_offset + 19, vertical_offset + 25,
                             str(self._segment_tree.segment_max(subtree_left, subtree_right)))
        else:
            painter.drawText(horizontal_offset + 19, vertical_offset + 25,
                             str(self._segment_tree.segment_sum(subtree_left, subtree_right)))

        if subtree_left == subtree_right:
            return

        middle = (subtree_right + subtree_left) >> 1
        self.print_subtree(painter, subtree_left, middle, vertical_level + 1, horizontal_offset, False)
        self.print_subtree(painter, middle + 1, subtree_right, vertical_level + 1, horizontal_offset, True)

    def get_tree_height(self, level, subtree_left, subtree_right, tree_height):
        if level > tree_height:
            tree_height = level

        if subtree_left == subtree_right:
            return tree_height

        middle = (subtree_right + subtree_left) >> 1
        tree_height = self.get_tree_height(level + 1, subtree_left, middle, tree_height)
        tree_height = self.get_tree_height(level + 1, middle + 1, subtree_right, tree_height)

        return tree_height

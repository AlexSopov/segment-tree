# Класс дерева отрезков
class SegmentTree:
    def __init__(self, values):
        self._min_values = dict()
        self._max_values = dict()
        self._sum_values = dict()

        self.values = values
        self._initialize(0, len(values) - 1)

    def segment_sum(self, segment_left, segment_right):
        self._validate_segment_range(segment_left, segment_right)
        return self._segment_sum(segment_left, segment_right, 0, len(self.values) - 1)

    def segment_max(self, segment_left, segment_right):
        self._validate_segment_range(segment_left, segment_right)
        return self._segment_max(segment_left, segment_right, 0, len(self.values) - 1)

    def segment_min(self, segment_left, segment_right):
       
        self._validate_segment_range(segment_left, segment_right)
        return self._segment_min(segment_left, segment_right, 0, len(self.values) - 1)

    def update(self, index, value):   
        self._validate_index(index)
        self._update(0, len(self.values) - 1, index, value)

    def _initialize(self, subtree_left, subtree_right):
        segment = (subtree_left, subtree_right)

		# If the left and right end of the segment coincide
		# Reached the final element
        if subtree_left == subtree_right:
            self._min_values[segment] = self.values[subtree_left]
            self._max_values[segment] = self.values[subtree_left]
            self._sum_values[segment] = self.values[subtree_left]
        else:
            middle = (subtree_right + subtree_left) >> 1
            self._initialize(subtree_left, middle)
            self._initialize(middle + 1, subtree_right)

            # Setting the minimum, maximum values and amounts
			# For the current segment
            left_segment = (subtree_left, middle)
            right_segment = (middle + 1, subtree_right)
            self._min_values[segment] = min(self._min_values[left_segment], self._min_values[right_segment])
            self._max_values[segment] = max(self._max_values[left_segment], self._max_values[right_segment])
            self._sum_values[segment] = self._sum_values[left_segment] + self._sum_values[right_segment]

    def _segment_sum(self, segment_left, segment_right, subtree_left, subtree_right):
        segment = (segment_left, segment_right)

        if subtree_left == segment_left and subtree_right == segment_right:
            return self._sum_values[segment]

		# If the right index is less than the middle of the tree - look for the result in the left half of the tree
		# If the left index is greater than the middle of the tree - look for the result in the right half of the tree.
		# Otherwise - as the sum of the results in the left and right half
        middle = (subtree_left + subtree_right) >> 1
        if segment_right <= middle:
            return self._segment_sum(segment_left, segment_right, subtree_left, middle)
        elif segment_left > middle:
            return self._segment_sum(segment_left, segment_right, middle + 1, subtree_right)
        else:
            return self._segment_sum(segment_left, middle, subtree_left, middle) + \
                   self._segment_sum(middle + 1, segment_right, middle + 1, subtree_right)

    def _segment_max(self, segment_left, segment_right, subtree_left, subtree_right):
        segment = (segment_left, segment_right)

        if subtree_left == segment_left and subtree_right == segment_right:
            return self._max_values[segment]

		# If the right index is less than the middle of the tree - look for the result in the left half of the tree
		# If the left index is greater than the middle of the tree - look for the result in the right half of the tree.
		# Otherwise - as the sum of the maximum in the left and right half
        middle = (subtree_left + subtree_right) >> 1
        if segment_right <= middle:
            return self._segment_max(segment_left, segment_right, subtree_left, middle)
        elif segment_left > middle:
            return self._segment_max(segment_left, segment_right, middle + 1, subtree_right)
        else:
            return max(self._segment_max(segment_left, middle, subtree_left, middle),
                       self._segment_max(middle + 1, segment_right, middle + 1, subtree_right))

    def _segment_min(self, segment_left, segment_right, subtree_left, subtree_right):
        segment = (segment_left, segment_right)

        if subtree_left == segment_left and subtree_right == segment_right:
            return self._min_values[segment]

        middle = (subtree_left + subtree_right) >> 1
        if segment_right <= middle:
            return self._segment_min(segment_left, segment_right, subtree_left, middle)
        elif segment_left > middle:
            return self._segment_min(segment_left, segment_right, middle + 1, subtree_right)
        else:
            return min(self._segment_min(segment_left, middle, subtree_left, middle),
                       self._segment_min(middle + 1, segment_right, middle + 1, subtree_right))

    def _update(self, subtree_left, subtree_right, index, value):
        if subtree_left == subtree_right:
            self.values[subtree_left] = value
            self._min_values[segment] = value
            self._max_values[segment] = value
            self._sum_values[segment] = value
        else:
            middle = (subtree_right + subtree_left) >> 1

            if index <= middle:
                self._update(subtree_left, middle, index, value)
            else:
                self._update(middle + 1, subtree_right, index, value)

            left_segment = (subtree_left, middle)
            right_segment = (middle + 1, subtree_right)
            self._min_values[segment] = min(self._min_values[left_segment], self._min_values[right_segment])
            self._max_values[segment] = max(self._max_values[left_segment], self._max_values[right_segment])
            self._sum_values[segment] = self._sum_values[left_segment] + self._sum_values[right_segment]

    def _validate_segment_range(self, segment_left, segment_right):
        if segment_left < 0 or segment_right >= len(self.values) or segment_left > segment_right:
            raise IndexError('Argument is out of range.')

    def _validate_index(self, index):
        if index < 0 or index >= len(self.values):
            raise IndexError('Argument is out of range.')

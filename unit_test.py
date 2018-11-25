# -*- coding: utf-8 -*-
import random
from unittest import main, TestCase
from segment_tree import SegmentTree

# Testing the segment tree
class TestSegmentTree(TestCase):
    def test(self):
        values = list()
        for i in range(1, 100000):
            values.append(random.randint(-100000, 100000))

        segment_tree = SegmentTree(values)
        self.assertEqual(segment_tree.segment_max(100, 10000), max(values[100:10000 + 1]))
        self.assertEqual(segment_tree.segment_min(100, 500), min(values[100:500 + 1]))
        self.assertEqual(segment_tree.segment_sum(9900, 99000), sum(values[9900:99000 + 1]))

if __name__ == '__main__':
    main()

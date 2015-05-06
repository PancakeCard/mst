
import unittest

from adt.graph import Graph, Vertice, Edge
from mst import kruskal, prim, split_in_groups


class TestMinimumSpanningTree(unittest.TestCase):

    def setUp(self):
        self.g = Graph()
        self.g.add_vertice(0, 0)
        self.g.add_vertice(3, 4)
        self.g.add_vertice(0, 4)
        self.g.add_vertice(3, 0)
        self.g.add_vertice(10, 40)

        self.mst = [
            Edge(Vertice(0, 0), Vertice(0, 4)),
            Edge(Vertice(3, 4), Vertice(0, 4)),
            Edge(Vertice(0, 0), Vertice(3, 0)),
            Edge(Vertice(3, 4), Vertice(10, 40)),
        ]

    def test_kruskal(self):
        mst = kruskal(self.g)
        self.assertEqual(sorted(mst), sorted(self.mst))

    def test_prim(self):
        mst = prim(self.g)
        self.assertEqual(sorted(mst), sorted(self.mst))

    def test_grouping(self):
        groups = split_in_groups(self.mst)
        self.assertEqual(len(groups), 2)
        self.assertIn(Vertice(10, 40), groups[0])
        self.assertIn(Vertice(0, 0), groups[1])
        self.assertIn(Vertice(3, 4), groups[1])
        self.assertIn(Vertice(0, 4), groups[1])
        self.assertIn(Vertice(3, 0), groups[1])

        groups = split_in_groups(self.mst, 3)
        self.assertEqual(len(groups), 3)
        self.assertIn(Vertice(10, 40), groups[0])
        self.assertIn(Vertice(0, 0), groups[1])
        self.assertIn(Vertice(3, 0), groups[1])
        self.assertIn(Vertice(3, 4), groups[2])
        self.assertIn(Vertice(0, 4), groups[2])

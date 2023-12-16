from unittest import TestCase
from utils import PointCloud, Point


class TestPointCloud(TestCase):
    def setUp(self) -> None:
        self.cloud = PointCloud(
            [
                "#........#",
                "..........",
                "....#.....",
                "..........",
                "#.........",
                ".........#",
                "..........",
                "....##....",
                "..........",
                "#........#",
            ]
        )
        self.expected_point_coords = [
            (0, 0), (9, 0),
            (4, 2),
            (0, 4),
            (9, 5),
            (4, 7), (5, 7),
            (0, 9), (9, 9)
        ]

    def test_init(self):
        for expected_point in self.expected_point_coords:
            found = self.cloud.get(*expected_point)
            self.assertEqual(len(found), 1, f"Did not find expected point {expected_point}")

    def test_add_and_remove(self):
        test_point = Point("A", 1, 1)

        self.assertEqual(len(self.expected_point_coords), len(self.cloud.points), msg="Incorrect number of points")
        self.cloud.add(test_point)
        self.assertEqual(len(self.expected_point_coords) + 1, len(self.cloud.points), msg="Incorrect number of points")
        self.cloud.remove(test_point)
        self.assertEqual(len(self.expected_point_coords), len(self.cloud.points), msg="Incorrect number of points")

    def test_get(self):
        test_point = Point("A", 1, 1)

        found = self.cloud.get(1, 1)
        self.assertEqual(0, len(found), msg=f"Expected to find no Points, found {len(found)}")

        self.cloud.add(test_point)

        found = self.cloud.get(1, 1)
        self.assertEqual(1, len(found), msg=f"Expected to find one Point, found {len(found)}")
        self.assertIs(test_point, found[0], msg=f"Found Point '{found[0]}' is not the expected Point '{test_point}'")


class TestPoint(TestCase):
    def setUp(self) -> None:
        self.cloud = PointCloud(
            [
                "#........#",
                "..........",
                "....#.....",
                "..........",
                "#.........",
                ".........#",
                "..........",
                "....##....",
                "..........",
                "#........#",
            ]
        )
        self.expected_point_coords = [
            (0, 0), (9, 0),
            (4, 2),
            (0, 4),
            (9, 5),
            (4, 7), (5, 7),
            (0, 9), (9, 9)
        ]

    def test_get_neighbours(self):
        point_1 = self.cloud.get(4, 2)[0]
        point_1_neighbours = point_1.get_neighbours("N")
        self.assertEqual(0, len(point_1_neighbours), msg=f"Did not find expected Point '{point_1}'")

        point_2 = self.cloud.get(4, 7)[0]
        for d in "NSW":
            point_2_neighbours = point_2.get_neighbours(d)
            self.assertEqual(0, len(point_2_neighbours), msg=f"Found unexpected {d} neighbours for Point '{point_2}'")
        point_2_neighbours = point_2.get_neighbours("E")
        self.assertEqual(1, len(point_2_neighbours), msg=f"Found no E neighbours for Point '{point_2}'")

        point_3 = Point("?", 0, 1)
        self.assertRaises(ValueError, point_3.get_neighbours, "N")
        self.cloud.add(point_3)
        point_3_neighbours = point_3.get_neighbours("N")
        self.assertEqual(1, len(point_3_neighbours))

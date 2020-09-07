from gphotospy.utils import batches


def test_batches():
	lst = list(range(10))
	assert list(batches(lst, 4)) == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
	assert list(batches(lst, 3)) == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
	assert list(batches(lst, 10)) == [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
	assert list(batches(lst, 11)) == [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]


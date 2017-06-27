from xml.dom import minidom
from svg.path import parse_path


class DynamicList(list):
    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __setslice__(self, i, j, seq):
        return self.__setitem__(slice(i, j), seq)

    def __delslice__(self, i, j):
        return self.__delitem__(slice(i, j))

    def _resize(self, index):
        n = len(self)
        if isinstance(index, slice):
            m = max(abs(index.start), abs(index.stop))
        else:
            m = index + 1
        if m > n:
            self.extend([self.__class__() for i in range(m - n)])

    def __getitem__(self, index):
        self._resize(index)
        return list.__getitem__(self, index)

    def __setitem__(self, index, item):
        self._resize(index)
        if isinstance(item, list):
            item = self.__class__(item)
        list.__setitem__(self, index, item)


svg_dom = minidom.parse("C:\Users\Emily\Downloads\Apple\homer-simpson.svg")
path_strings = [path.getAttribute('d') for path in svg_dom.getElementsByTagName('path')]
i = 0
z = 0
LinePos = DynamicList()
for path_string in path_strings:
    path_data = parse_path(path_string)
    for point in range(0, 1, int(1 / .001)):
        x = int(path_data.point(point).real)
        y = int(path_data.point(point).imag)
        LinePos[i] = [x, y, z]
        print(LinePos[i])
i = (i + 1)

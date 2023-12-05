from collections import namedtuple
from prior.p4 import *

# ---


class testmycode:
    def __init__(self):
        self.test_incomplete_links()

    # Tests that input list contains references with incomplete web links and the function returns a list of extracted web links with complete urls. tags: [edge case]

    def test_incomplete_links(self):
        a = namedtuple('a', ['name', 'contents'])
        a.name = 'a'
        a.contents = '<ref>{{cite web |url=https://www.bbc.com |title=BBC}}</ref>'
        b = namedtuple('b', ['name', 'contents'])
        b.name = 'b'
        b.contents = '<ref>{{cite web |url=https://www.cnn.com |title=CNN}}</ref>'
        refs = [a, b]
        expected = ['https://www.bbc.com', 'https://www.cnn.com']
        f = get_weblinks(refs, '')
        print(f)
        print('test_incomplete_links: ' + str(set(f) == set(expected)))


# ---
if __name__ == '__main__':
    testmycode()

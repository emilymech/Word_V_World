import unittest


class MyTest(unittest.TestCase):

    @staticmethod
    def test_paths():
        """
        test that paths to wiki articles are found
        """

        from word_v_world.articles import get_paths_to_articles

        paths_to_articles = []
        for p in get_paths_to_articles(param2requests=None):
            paths_to_articles.append(p)

        return paths_to_articles is not []


if __name__ == '__main__':
    unittest.main()

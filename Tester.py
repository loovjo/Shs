import unittest
from Parser import tokenize as t, parse as p, Function as F, Ordering as o

class ParserTester(unittest.TestCase):
    def test_tokenizer(self):
        self.assertEqual(t("Hello, World!"), ["Hello", ",", "World", "!"])
        self.assertEqual(t("-4312.2"), ["-4312.2"])
        self.assertEqual(t("t -4312.2 b"), ["t", "-4312.2", "b"])
        self.assertEqual(t("Hello, \"World!\""), ["Hello", ",", "\"World!\""])
        self.assertEqual(t("1 2 +"), ["1", "2", "+"])
        self.assertEqual(t("[1 2 +]"), ["[", "1", "2", "+", "]"])
        self.assertEqual(t("[\"hej\"]"), ["[", "\"hej\"", "]"])
        self.assertEqual(t("{1 +} %"), ["{", "1", "+", "}", "%"])
        self.assertEqual(t("Hello {World!}"), ["Hello", "{", "World", "!", "}"])
        self.assertEqual(t("\"Hello\" \", \" \"World\" +"), ["\"Hello\"", "\", \"", "\"World\"", "+"])
        self.assertEqual(t("(a b c1 c2-b a c2 c2)"), ["(", "a", "b", "c1", "c2", "-", "b", "a", "c2", "c2", ")"])
    def test_parser(self):
        self.assertEqual(p(t("Hello {1 2 +} ~")), ("Hello", F(("1", "2", "+")), "~"))
        self.assertEqual(p(t("[1 2] {2 /} %")), ("[", "1", "2", "]", F(("2", "/")), "%"))
        self.assertEqual(p(t("1 2 + p")), ("1", "2", "+", "p"))
        self.assertEqual(p(t("(a [b c] - [a b] c)")), (o(("a", "[", "b", "c", "]"), ("[", "a", "b", "]", "c")), ))
        self.assertEqual(p(t("(a b - b a)")), (o(("a", "b"), ("b", "a")), ))


if __name__ == '__main__':
    unittest.main()

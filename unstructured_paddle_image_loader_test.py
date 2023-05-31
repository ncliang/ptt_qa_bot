import tempfile
import unittest

import requests

from unstructured_paddle_image_loader import UnstructuredPaddleImageLoader


class UnstructredPaddleImageLoaderTest(unittest.TestCase):
    def test_basic(self):
        img_url = "https://i.imgur.com/QU8C5va.jpg"
        resp = requests.get(img_url)
        tmp_file_path = ""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as fp:
            fp.write(resp.content)
            tmp_file_path = fp.name

        self.assertNotEqual("", tmp_file_path)
        img_loader = UnstructuredPaddleImageLoader(tmp_file_path)
        documents = img_loader.load()
        self.assertEquals(1, len(documents))

from typing import List

from langchain.document_loaders import UnstructuredFileLoader
from paddleocr import PaddleOCR
from unstructured.partition.text import partition_text


class UnstructuredPaddleImageLoader(UnstructuredFileLoader):
    """Loader that uses unstructured to load image files, such as PNGs and JPGs."""

    def _get_elements(self) -> List:
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False, show_log=False)
        result = ocr.ocr(img=self.file_path)
        ocr_result = [i[1][0] for line in result for i in line]

        return partition_text(text="\n".join(ocr_result))

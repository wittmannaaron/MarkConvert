"""Convert PDF pages to images for LLM processing."""

import tempfile
from pathlib import Path
from typing import List, Union, Optional
import fitz  # PyMuPDF
from PIL import Image


class PdfToImageConverter:
    """Convert PDF pages to images."""

    def __init__(
        self,
        dpi: int = 150,
        output_format: str = "jpeg",
        jpeg_quality: int = 85,
        max_dimension: int = 2048
    ):
        """
        Initialize PDF to image converter.

        Args:
            dpi: Resolution for image conversion (default: 150 DPI - good balance)
            output_format: 'jpeg' or 'png' (jpeg is faster and uses fewer tokens)
            jpeg_quality: JPEG quality 1-100 (default: 85 - good quality, smaller files)
            max_dimension: Maximum width or height in pixels (downscale if larger)
        """
        self.dpi = dpi
        self.zoom = dpi / 72  # PDF default is 72 DPI
        self.output_format = output_format.lower()
        self.jpeg_quality = jpeg_quality
        self.max_dimension = max_dimension

    def convert_pdf_to_images(
        self,
        pdf_path: Union[str, Path],
        output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Convert all pages of PDF to images.

        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save images (defaults to temp dir)

        Returns:
            List of paths to generated images
        """
        pdf_path = Path(pdf_path)

        # Create output directory
        if output_dir is None:
            output_dir = Path(tempfile.mkdtemp(prefix="pdf_images_"))
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        image_paths = []

        # Open PDF
        doc = fitz.open(pdf_path)

        try:
            # Convert each page
            for page_num in range(len(doc)):
                page = doc[page_num]

                # Render page to pixmap (image)
                mat = fitz.Matrix(self.zoom, self.zoom)
                pix = page.get_pixmap(matrix=mat, alpha=False)

                # Convert to PIL Image for processing
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Resize if too large
                if max(img.width, img.height) > self.max_dimension:
                    ratio = self.max_dimension / max(img.width, img.height)
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                # Save with format and quality settings
                ext = "jpg" if self.output_format == "jpeg" else "png"
                image_path = output_dir / f"page_{page_num + 1:04d}.{ext}"

                if self.output_format == "jpeg":
                    img.save(str(image_path), "JPEG", quality=self.jpeg_quality, optimize=True)
                else:
                    img.save(str(image_path), "PNG", optimize=True)

                image_paths.append(image_path)

        finally:
            doc.close()

        return image_paths

    def convert_pdf_page_to_image(
        self,
        pdf_path: Union[str, Path],
        page_num: int = 0,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Convert a single PDF page to image.

        Args:
            pdf_path: Path to PDF file
            page_num: Page number (0-indexed)
            output_path: Output image path (defaults to temp file)

        Returns:
            Path to generated image
        """
        pdf_path = Path(pdf_path)

        # Create output path
        if output_path is None:
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".png",
                prefix=f"pdf_page_{page_num}_",
                delete=False
            )
            output_path = Path(temp_file.name)
            temp_file.close()
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Open PDF and convert page
        doc = fitz.open(pdf_path)

        try:
            if page_num >= len(doc):
                raise ValueError(f"Page {page_num} does not exist in PDF (total pages: {len(doc)})")

            page = doc[page_num]

            # Render page to pixmap
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)

            # Convert to PIL Image for processing
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Resize if too large
            if max(img.width, img.height) > self.max_dimension:
                ratio = self.max_dimension / max(img.width, img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Save with format and quality settings
            if self.output_format == "jpeg":
                img.save(str(output_path), "JPEG", quality=self.jpeg_quality, optimize=True)
            else:
                img.save(str(output_path), "PNG", optimize=True)

        finally:
            doc.close()

        return output_path


def get_pdf_page_count(pdf_path: Union[str, Path]) -> int:
    """
    Get number of pages in PDF.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Number of pages
    """
    doc = fitz.open(pdf_path)
    try:
        return len(doc)
    finally:
        doc.close()

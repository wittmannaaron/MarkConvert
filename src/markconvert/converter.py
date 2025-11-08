"""Document conversion using OpenAI GPT-5 for PDFs/images and Docling for office formats."""

import io
import os
import tempfile
from pathlib import Path
from typing import Union, BinaryIO, Optional

from docling.document_converter import DocumentConverter
from docx import Document
from docx.shared import Pt
import markdown
from weasyprint import HTML

from markconvert.openai_vision_client import OpenAIVisionClient


class MarkdownConverter:
    """Handle conversion between Markdown and other document formats."""

    # File extensions that are processed via LLM (vision)
    LLM_FORMATS = {'.pdf', '.png', '.jpg', '.jpeg'}

    # File extensions that are processed via Docling
    DOCLING_FORMATS = {'.docx', '.doc', '.pptx', '.ppt', '.html', '.htm'}

    # Text formats that don't need processing
    TEXT_FORMATS = {'.txt', '.md'}

    def __init__(
        self,
        openai_api_key: str = None,
        openai_model: str = "gpt-5-nano"
    ):
        """
        Initialize the converter.

        Args:
            openai_api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            openai_model: GPT-5 model ("gpt-5-nano" or "gpt-5-mini")
        """
        # Initialize OpenAI client for PDF/image processing
        self.vision_client = OpenAIVisionClient(
            api_key=openai_api_key,
            model=openai_model
        )

        # Initialize Docling for office document processing
        self.doc_converter = DocumentConverter()

    def import_document(self, file_path: str) -> str:
        """
        Import a document and convert to Markdown.

        Routing logic:
        - PDF/PNG/JPG → Ollama Vision LLM
        - DOCX/PPTX/HTML → Docling
        - TXT/MD → Direct read

        Args:
            file_path: Path to the document file

        Returns:
            Markdown text
        """
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()

        try:
            # Route 1: PDF and images → Ollama Vision
            if suffix in self.LLM_FORMATS:
                return self._import_via_llm(file_path)

            # Route 2: Office formats → Docling
            elif suffix in self.DOCLING_FORMATS:
                return self._import_via_docling(file_path)

            # Route 3: Plain text formats → Direct read
            elif suffix in self.TEXT_FORMATS:
                return file_path.read_text(encoding='utf-8')

            else:
                raise ValueError(
                    f"Unsupported file format: {suffix}. "
                    f"Supported: {', '.join(sorted(self.LLM_FORMATS | self.DOCLING_FORMATS | self.TEXT_FORMATS))}"
                )

        except Exception as e:
            raise ValueError(f"Fehler beim Importieren der Datei: {str(e)}")

    def _import_via_llm(self, file_path: Path) -> str:
        """Import PDF or image via OpenAI GPT-5."""
        import logging
        import time

        logger = logging.getLogger(__name__)
        suffix = file_path.suffix.lower()

        if suffix == '.pdf':
            # PDF: Send entire PDF to OpenAI for processing (fast!)
            start_time = time.time()
            logger.info(f"Processing PDF with OpenAI GPT-5...")
            result = self.vision_client.process_pdf(file_path)
            processing_time = time.time() - start_time
            logger.info(f"PDF processed in {processing_time:.2f}s")
            return result
        else:
            # Image: Process directly
            return self.vision_client.process_image_to_markdown(file_path)

    def _import_via_docling(self, file_path: Path) -> str:
        """Import office document via Docling."""
        result = self.doc_converter.convert(str(file_path))
        return result.document.export_to_markdown()

    def import_document_from_bytes(self, file_bytes: bytes, filename: str) -> str:
        """
        Import a document from bytes and convert to Markdown.

        Args:
            file_bytes: Document content as bytes
            filename: Original filename (for format detection)

        Returns:
            Markdown text
        """
        # Save to temporary file
        suffix = Path(filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            markdown_text = self.import_document(tmp_path)
            return markdown_text
        finally:
            # Clean up temporary file
            Path(tmp_path).unlink(missing_ok=True)

    def _clean_text(self, text: str) -> str:
        """
        Remove control characters and NULL bytes that are not XML-compatible.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        import re
        # Remove NULL bytes and control characters except newline, tab, carriage return
        # Keep only printable characters and common whitespace
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', text)
        return cleaned

    def export_to_docx(self, markdown_text: str) -> bytes:
        """
        Export Markdown to DOCX format.

        Args:
            markdown_text: Markdown content

        Returns:
            DOCX file as bytes
        """
        # Clean text from control characters
        markdown_text = self._clean_text(markdown_text)

        doc = Document()

        # Parse markdown line by line
        lines = markdown_text.split('\n')

        for line in lines:
            line = line.rstrip()

            # Headers
            if line.startswith('# '):
                p = doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                p = doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                p = doc.add_heading(line[4:], level=3)
            elif line.startswith('#### '):
                p = doc.add_heading(line[5:], level=4)
            elif line.startswith('##### '):
                p = doc.add_heading(line[6:], level=5)
            elif line.startswith('###### '):
                p = doc.add_heading(line[7:], level=6)

            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                doc.add_paragraph(line[2:], style='List Bullet')
            elif len(line) > 2 and line[0].isdigit() and line[1:3] == '. ':
                doc.add_paragraph(line[3:], style='List Number')

            # Blockquote
            elif line.startswith('> '):
                p = doc.add_paragraph(line[2:])
                p.style = 'Quote'

            # Empty line
            elif line.strip() == '':
                doc.add_paragraph()

            # Regular paragraph
            else:
                p = doc.add_paragraph()
                self._add_formatted_text(p, line)

        # Save to bytes
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.read()

    def _add_formatted_text(self, paragraph, text: str):
        """Add text with inline formatting (bold, italic, code) to paragraph."""
        import re

        # Pattern for **bold**, *italic*, `code`, [link](url)
        pattern = r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[([^\]]+)\]\(([^\)]+)\))'

        parts = re.split(pattern, text)

        for i, part in enumerate(parts):
            if not part:
                continue

            if part.startswith('**') and part.endswith('**'):
                # Bold
                run = paragraph.add_run(part[2:-2])
                run.bold = True
            elif part.startswith('*') and part.endswith('*') and not part.startswith('**'):
                # Italic
                run = paragraph.add_run(part[1:-1])
                run.italic = True
            elif part.startswith('`') and part.endswith('`'):
                # Code
                run = paragraph.add_run(part[1:-1])
                run.font.name = 'Courier New'
                run.font.size = Pt(10)
            elif part.startswith('['):
                # This is handled by the regex groups
                continue
            elif i > 0 and parts[i-1] and parts[i-1].startswith('['):
                # Link text (captured group)
                run = paragraph.add_run(part)
                run.font.color.rgb = None  # Blue color would need RGBColor
            else:
                # Regular text
                paragraph.add_run(part)

    def export_to_pdf(self, markdown_text: str) -> bytes:
        """
        Export Markdown to PDF format.

        Args:
            markdown_text: Markdown content

        Returns:
            PDF file as bytes
        """
        # Clean text from control characters
        markdown_text = self._clean_text(markdown_text)

        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_text,
            extensions=['extra', 'codehilite', 'tables', 'fenced_code']
        )

        # Wrap in HTML document with styling
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 2.5cm;
                }}
                body {{
                    font-family: 'DejaVu Sans', Arial, sans-serif;
                    font-size: 11pt;
                    line-height: 1.6;
                    color: #333;
                }}
                h1 {{
                    font-size: 24pt;
                    margin-top: 20pt;
                    margin-bottom: 12pt;
                    border-bottom: 2px solid #333;
                    padding-bottom: 6pt;
                }}
                h2 {{
                    font-size: 18pt;
                    margin-top: 16pt;
                    margin-bottom: 10pt;
                }}
                h3 {{
                    font-size: 14pt;
                    margin-top: 12pt;
                    margin-bottom: 8pt;
                }}
                p {{
                    margin-bottom: 10pt;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2pt 4pt;
                    border-radius: 3pt;
                    font-family: 'DejaVu Sans Mono', 'Courier New', monospace;
                    font-size: 10pt;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 12pt;
                    border-radius: 4pt;
                    overflow-x: auto;
                    margin: 10pt 0;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                }}
                blockquote {{
                    border-left: 4pt solid #ddd;
                    padding-left: 12pt;
                    margin-left: 0;
                    font-style: italic;
                    color: #666;
                }}
                ul, ol {{
                    margin-bottom: 10pt;
                    margin-top: 5pt;
                    padding-left: 30pt;
                    line-height: 1.8;
                }}
                li {{
                    margin-bottom: 6pt;
                    padding-left: 5pt;
                    break-inside: avoid;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 10pt 0;
                }}
                th, td {{
                    border: 1pt solid #ddd;
                    padding: 8pt;
                    text-align: left;
                }}
                th {{
                    background-color: #f4f4f4;
                    font-weight: bold;
                }}
                a {{
                    color: #0066cc;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Convert HTML to PDF
        pdf_bytes = HTML(string=full_html).write_pdf()

        return pdf_bytes

    def export_to_rtf(self, markdown_text: str) -> bytes:
        """
        Export Markdown to RTF format.

        Args:
            markdown_text: Markdown content

        Returns:
            RTF file as bytes
        """
        # Clean text from control characters
        markdown_text = self._clean_text(markdown_text)

        # RTF header with UTF-8 support
        rtf = r'{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033'
        rtf += r'{\fonttbl{\f0\fswiss\fcharset0 Arial;}{\f1\fmodern\fcharset0 Courier New;}}'
        rtf += r'{\colortbl ;\red0\green0\blue0;\red102\green102\blue102;}'
        rtf += '\n'

        lines = markdown_text.split('\n')

        for line in lines:
            line = line.rstrip()

            # Convert special characters to RTF unicode
            line = self._escape_rtf(line)

            # Headers - reduced spacing (sa100 instead of sa200)
            if line.startswith('# '):
                rtf += r'\pard\sa100\sl240\slmult1\b\fs32 ' + line[2:] + r'\b0\fs22\par' + '\n'
            elif line.startswith('## '):
                rtf += r'\pard\sa100\sl240\slmult1\b\fs28 ' + line[3:] + r'\b0\fs22\par' + '\n'
            elif line.startswith('### '):
                rtf += r'\pard\sa100\sl240\slmult1\b\fs24 ' + line[4:] + r'\b0\fs22\par' + '\n'

            # Lists - reduced spacing
            elif line.startswith('- ') or line.startswith('* '):
                rtf += r'\pard\fi-360\li720\sa80\sl240\slmult1 ' + r'\bullet\tab ' + line[2:] + r'\par' + '\n'
            elif len(line) > 2 and line[0].isdigit() and line[1:3] == '. ':
                # Numbered lists
                rtf += r'\pard\fi-360\li720\sa80\sl240\slmult1 ' + line + r'\par' + '\n'

            # Blockquote - reduced spacing
            elif line.startswith('> '):
                rtf += r'\pard\li720\sa100\sl240\slmult1\i ' + line[2:] + r'\i0\par' + '\n'

            # Empty line
            elif line.strip() == '':
                rtf += r'\par' + '\n'

            # Regular paragraph - reduced spacing
            else:
                rtf += r'\pard\sa100\sl240\slmult1 ' + line + r'\par' + '\n'

        rtf += '}'

        return rtf.encode('utf-8')

    def _escape_rtf(self, text: str) -> str:
        """Escape special characters and convert Unicode to RTF format."""
        result = []

        for char in text:
            code = ord(char)

            # ASCII special characters
            if char == '\\':
                result.append('\\\\')
            elif char == '{':
                result.append('\\{')
            elif char == '}':
                result.append('\\}')
            # Unicode characters (including emojis)
            elif code > 127:
                result.append(f'\\u{code}?')
            else:
                result.append(char)

        return ''.join(result)


# Global converter instance
# Use environment variables for configuration
# OpenAI API key from OPENAI_API_KEY env var
openai_model = os.getenv('OPENAI_MODEL', 'gpt-5-nano')

converter = MarkdownConverter(
    openai_api_key=None,  # Uses OPENAI_API_KEY env var
    openai_model=openai_model
)

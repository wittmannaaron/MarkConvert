"""Flask web application for MarkConvert."""

from flask import Flask, render_template, request, jsonify, send_file
import io
import traceback
from markconvert.converter import converter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/api/import', methods=['POST'])
def import_document():
    """
    Import a document and convert to Markdown.

    Expects: multipart/form-data with 'file' field
    Returns: JSON with 'markdown' field or 'error'
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Keine Datei hochgeladen'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Keine Datei ausgewählt'}), 400

        # Read file content
        file_bytes = file.read()

        # Check if it's a plain text file
        filename = file.filename.lower()
        if filename.endswith('.txt') or filename.endswith('.md'):
            # Just decode as text
            try:
                markdown_text = file_bytes.decode('utf-8')
            except UnicodeDecodeError:
                markdown_text = file_bytes.decode('latin-1')
        else:
            # Use docling for other formats (PDF, DOCX, etc.)
            markdown_text = converter.import_document_from_bytes(
                file_bytes,
                file.filename
            )

        return jsonify({
            'markdown': markdown_text,
            'message': f'Datei "{file.filename}" erfolgreich importiert!'
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': f'Fehler beim Importieren: {str(e)}'
        }), 500


@app.route('/api/export/markdown', methods=['POST'])
def export_markdown():
    """
    Export as Markdown file.

    Expects: JSON with 'markdown' field
    Returns: Markdown file download
    """
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')

        # Create file-like object
        buffer = io.BytesIO(markdown_text.encode('utf-8'))
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='text/markdown',
            as_attachment=True,
            download_name='dokument.md'
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': f'Fehler beim Export: {str(e)}'
        }), 500


@app.route('/api/export/docx', methods=['POST'])
def export_docx():
    """
    Export as DOCX file.

    Expects: JSON with 'markdown' field
    Returns: DOCX file download
    """
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')

        # Convert to DOCX
        docx_bytes = converter.export_to_docx(markdown_text)

        # Create file-like object
        buffer = io.BytesIO(docx_bytes)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name='dokument.docx'
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': f'Fehler beim DOCX-Export: {str(e)}'
        }), 500


@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """
    Export as PDF file.

    Expects: JSON with 'markdown' field
    Returns: PDF file download
    """
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')

        # Convert to PDF
        pdf_bytes = converter.export_to_pdf(markdown_text)

        # Create file-like object
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='dokument.pdf'
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': f'Fehler beim PDF-Export: {str(e)}'
        }), 500


@app.route('/api/export/rtf', methods=['POST'])
def export_rtf():
    """
    Export as RTF file.

    Expects: JSON with 'markdown' field
    Returns: RTF file download
    """
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')

        # Convert to RTF
        rtf_bytes = converter.export_to_rtf(markdown_text)

        # Create file-like object
        buffer = io.BytesIO(rtf_bytes)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='application/rtf',
            as_attachment=True,
            download_name='dokument.rtf'
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': f'Fehler beim RTF-Export: {str(e)}'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'MarkConvert is running'})


if __name__ == '__main__':
    app.run(debug=True)

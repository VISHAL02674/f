"""
Document Extractor with Formatting Preservation
Handles PDF, DOCX and other formats with multi-column layouts
Returns formatted markdown text preserving headings, bold, and structure
"""
import base64
import binascii
import io
import os
import re
import statistics
import traceback
from pathlib import Path
from collections import defaultdict

import docx
import docx2txt
import fitz
import pytesseract
from PIL import Image, ImageEnhance


def _strip_data_url_prefix(data: str) -> str:
    if isinstance(data, str) and data.startswith("data:"):
        return data.split(",", 1)[-1]
    return data


def _maybe_decode_base64_string(payload):
    if not isinstance(payload, str):
        return None
    cleaned = _strip_data_url_prefix(payload).strip()
    if not cleaned:
        return None
    try:
        return base64.b64decode(cleaned, validate=True)
    except (binascii.Error, ValueError):
        try:
            return base64.b64decode(cleaned)
        except (binascii.Error, ValueError):
            return None


def _detect_file_type_from_bytes(raw_bytes):
    if raw_bytes.startswith(b"%PDF"):
        return "pdf"
    if raw_bytes.startswith(b"PK\x03\x04"):
        return "docx"
    if raw_bytes.startswith(b"\xD0\xCF\x11\xE0"):
        return "doc"
    try:
        raw_bytes.decode("utf-8")
        return "txt"
    except UnicodeDecodeError:
        return None


def _ensure_docx_source(docx_source):
    if isinstance(docx_source, io.BytesIO):
        return io.BytesIO(docx_source.getvalue())
    if isinstance(docx_source, (bytes, bytearray)):
        return io.BytesIO(docx_source)
    if isinstance(docx_source, (str, os.PathLike)):
        return str(docx_source)
    return docx_source


def extract_document(doc_path, multi_column_strategy="smart", preserve_formatting=True):
    """
    Extract text from PDF, DOCX or other document formats
    Args:
        doc_path: Path or in-memory payload (str path, base64 str, bytes, BytesIO)
        multi_column_strategy:
            - "default": built in
            - "columns_first": process all left columns, then all right columns
            - "smart": auto-detect layout and use appropriate strategy (default)
        preserve_formatting: If True, preserve headings, bold, and structure as markdown

    Returns:
        Tuple: (file_type, text_raw, page, doc_object, ocr)
    """
    printable_name = "document"
    size_bytes = None
    file_ext = None
    source_payload = None

    if isinstance(doc_path, (str, os.PathLike)):
        doc_file = Path(doc_path)
        if doc_file.exists():
            printable_name = doc_file.name or printable_name
            size_bytes = doc_file.stat().st_size
            file_ext = doc_file.suffix.lower().lstrip(".")
            source_payload = str(doc_file)
        else:
            raw_bytes = _maybe_decode_base64_string(str(doc_path))
            if raw_bytes is None:
                print(f"❌ File not found: {doc_file}")
                return None
            file_ext = _detect_file_type_from_bytes(raw_bytes)
            if not file_ext:
                print("❌ Unsupported in-memory payload provided")
                return None
            printable_name = f"in-memory.{file_ext}"
            size_bytes = len(raw_bytes)
            source_payload = raw_bytes
    elif isinstance(doc_path, io.BytesIO):
        raw_bytes = doc_path.getvalue()
        file_ext = _detect_file_type_from_bytes(raw_bytes)
        if not file_ext:
            print("❌ Unsupported BytesIO payload")
            return None
        printable_name = f"bytesio.{file_ext}"
        size_bytes = len(raw_bytes)
        source_payload = raw_bytes
    elif isinstance(doc_path, (bytes, bytearray)):
        raw_bytes = bytes(doc_path)
        file_ext = _detect_file_type_from_bytes(raw_bytes)
        if not file_ext:
            print("❌ Unsupported binary payload")
            return None
        printable_name = f"bytes.{file_ext}"
        size_bytes = len(raw_bytes)
        source_payload = raw_bytes
    else:
        raise TypeError("Source must be a file path, BytesIO, bytes, or base64 string")

    print(f"✅ Opening: {printable_name}")
    if size_bytes is not None:
        print(f"   Size: {size_bytes:,} bytes")

    try:
        if file_ext == "pdf":
            return extract_pdf(
                source_payload,
                multi_column_strategy,
                preserve_formatting=preserve_formatting,
                source_name=printable_name,
                source_size=size_bytes,
            )
        if file_ext in ["docx", "doc"]:
            return extract_docx(
                _ensure_docx_source(source_payload),
                preserve_formatting=preserve_formatting,
                source_name=printable_name,
                file_ext=file_ext,
            )
        if file_ext == "txt":
            return extract_txt(source_payload, printable_name)
        print(f"❌ Unsupported file format: {file_ext}")
        print("   Supported formats: PDF, DOCX/DOC, TXT")
        return None
    except Exception as e:
        print(f"❌ Error extracting {file_ext} document: {e}")
        traceback.print_exc()
        return None


def analyze_font_sizes(doc):
    """Analyze font sizes across the document to determine heading thresholds"""
    font_sizes = []

    for page_num in range(min(5, len(doc))):  # Sample first 5 pages
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        size = span.get("size", 0)
                        if size > 0:
                            font_sizes.append(size)

    if not font_sizes:
        return {"base": 11, "h3": 12, "h2": 14, "h1": 16}

    font_sizes.sort()
    base_size = statistics.median(font_sizes)

    # Define thresholds
    return {
        "base": base_size,
        "h3": base_size + 1,
        "h2": base_size + 3,
        "h1": base_size + 5
    }


def format_text_with_style(text, size, is_bold, font_thresholds, prev_size=None):
    """Convert text to markdown based on size and style"""
    text = text.strip()
    if not text:
        return ""

    # Count words to determine if it's likely a heading
    word_count = len(text.split())
    text_length = len(text)

    # Very large text - major headings (name, main sections)
    if size >= font_thresholds["h1"]:
        # Only short text should be H1
        if text_length < 50:
            return f"**{text}**"
        else:
            return f"**{text}**"  # Long text just gets bold

    # Large text - section headers
    elif size >= font_thresholds["h2"]:
        # Only short lines (< 80 chars, < 10 words) should be H2
        if text_length < 80 and word_count < 10:
            return f"## {text}"
        else:
            return f"**{text}**"

    # Medium-large text - subsection headers
    elif size >= font_thresholds["h3"]:
        # Only short lines (< 100 chars, < 15 words) should be H3
        if text_length < 100 and word_count < 15:
            return f"### {text}"
        else:
            return f"**{text}**" if is_bold else text

    # Bold text
    elif is_bold and size > font_thresholds["base"]:
        return f"**{text}**"
    elif is_bold:
        return f"**{text}**"
    else:
        return text


def extract_formatted_blocks(page, font_thresholds):
    """Extract text blocks with formatting information"""
    blocks = page.get_text("dict")["blocks"]
    formatted_lines = []

    for block in blocks:
        if block.get("type") == 0:  # Text block
            block_x = block["bbox"][0]

            for line in block.get("lines", []):
                line_y = line["bbox"][1]

                # Collect all spans on this line
                spans = line.get("spans", [])
                if not spans:
                    continue

                # Merge all text from spans on this line
                line_text = " ".join(span.get("text", "").strip() for span in spans if span.get("text", "").strip())

                if not line_text:
                    continue

                # Get dominant font characteristics for the line
                sizes = [span.get("size", 11) for span in spans if span.get("text", "").strip()]
                fonts = [span.get("font", "") for span in spans if span.get("text", "").strip()]

                if not sizes:
                    continue

                # Use the maximum size on the line (typically the most important)
                max_size = max(sizes)
                # Check if any span is bold
                is_bold = any("bold" in font.lower() or "heavy" in font.lower() for font in fonts)

                # Format the entire line as one unit
                formatted = format_text_with_style(
                    line_text, max_size, is_bold, font_thresholds
                )

                if formatted:
                    formatted_lines.append({
                        "text": formatted,
                        "x": block_x,
                        "y": line_y,
                        "size": max_size,
                        "is_bold": is_bold
                    })

    return formatted_lines


def reorder_name_to_top(formatted_lines, font_thresholds):
    """
    Detect the candidate's name (large bold text, short) and move it to the top
    """
    if not formatted_lines:
        return formatted_lines

    name_candidates = []

    for i, line in enumerate(formatted_lines):
        text = line["text"]
        size = line.get("size", 0)
        is_bold = line.get("is_bold", False)

        # Name characteristics:
        # 1. Large font (above threshold)
        # 2. Bold (often)
        # 3. Short text (< 50 chars, typically 2-4 words)
        # 4. All caps or title case
        # 5. No special characters except spaces and common name chars

        # Remove markdown formatting for analysis
        clean_text = text.strip('*').strip('#').strip()
        word_count = len(clean_text.split())

        # Check if it looks like a name
        is_likely_name = (
            size >= font_thresholds["h1"] and  # Large font
            len(clean_text) < 50 and  # Short
            word_count >= 2 and word_count <= 4 and  # 2-4 words typical for names
            clean_text.isupper() and  # All caps (common for names in resumes)
            not any(char in clean_text for char in ['@', ':', '|', '•', '(', ')'])  # No special chars
        )

        if is_likely_name:
            name_candidates.append((i, line, size))

    if not name_candidates:
        return formatted_lines

    # If multiple candidates, choose the one with largest font
    name_candidates.sort(key=lambda x: x[2], reverse=True)
    name_index, name_line, _ = name_candidates[0]

    # Remove from current position and insert at top
    formatted_lines_copy = formatted_lines[:]
    formatted_lines_copy.pop(name_index)
    formatted_lines_copy.insert(0, name_line)

    return formatted_lines_copy


def extract_pdf(pdf_source, multi_column_strategy="smart", preserve_formatting=True,
                source_name=None, source_size=None):
    """Extract PDF with optional formatting preservation"""
    display_name = source_name or "document.pdf"
    try:
        if isinstance(pdf_source, (str, os.PathLike)):
            doc = fitz.open(pdf_source)
        else:
            doc = fitz.open(stream=pdf_source, filetype="pdf")

        if len(doc) == 0:
            print("❌ PDF has 0 pages!")
            doc.close()
            return None

        print(f"   Pages: {len(doc)}")

        if multi_column_strategy == "smart":
            is_multi_column = detect_multi_column_layout(doc)
            strategy = "columns_first" if is_multi_column else "default"
            print(f"   Detected {'multi-column' if is_multi_column else 'single-column'} layout")
        else:
            strategy = multi_column_strategy

        if preserve_formatting:
            print("   Preserving formatting (headings, bold, structure)")
            font_thresholds = analyze_font_sizes(doc)
            all_text, stats = extract_with_formatting(doc, strategy, font_thresholds)
        else:
            if strategy == "default":
                all_text, stats = extract_with_default_strategy(doc)
            else:
                all_text, stats = extract_with_columns_first_strategy(doc)

        text_raw = "\n\n".join(all_text)

        print(f"\n✅ Extraction complete for {display_name}!")
        print(f"   Total characters: {len(text_raw):,}")

        return (
            "pdf",
            text_raw,
            stats["total_pages"],
            doc,
            stats["ocr_pages"] > 0,
        )

    except Exception as e:
        print(f"❌ Error in PDF extraction: {e}")
        traceback.print_exc()
        return None


def extract_with_formatting(doc, strategy, font_thresholds):
    """Extract text preserving formatting"""
    stats = {
        "total_pages": len(doc),
        "text_pages": 0,
        "ocr_pages": 0,
        "total_chars": 0,
    }

    if strategy == "default":
        all_text = []
        extracted_name = None

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")

            if len(text.strip()) < 50:
                print(f"   Page {page_num + 1}: ⚠️  Image-based - trying OCR")
                stats["ocr_pages"] += 1
                ocr_text = perform_ocr(page)
                all_text.append(clean_text(ocr_text))
                continue

            formatted_blocks = extract_formatted_blocks(page, font_thresholds)

            # Extract name from first page only
            if page_num == 0 and formatted_blocks:
                extracted_name, formatted_blocks = find_and_extract_name(formatted_blocks, font_thresholds)
                if extracted_name:
                    print(f"   🎯 Name detected and extracted: {extracted_name.strip('*')}")

            page_text = "\n".join([block["text"] for block in formatted_blocks])

            print(f"   Page {page_num + 1}: ✓  Text extracted with formatting ({len(page_text):,} chars)")
            stats["text_pages"] += 1
            all_text.append(clean_markdown(page_text))

        # Prepend name at the very beginning
        if extracted_name:
            all_text.insert(0, extracted_name)

        stats["total_chars"] = sum(len(t) for t in all_text)
        return all_text, stats

    else:  # columns_first strategy
        return extract_with_columns_first_formatting(doc, font_thresholds, stats)


def find_and_extract_name(formatted_blocks, font_thresholds):
    """
    Find the candidate's name in blocks, extract it, and return both the name and cleaned blocks
    Returns: (name_text or None, blocks_without_name)
    """
    if not formatted_blocks:
        return None, formatted_blocks

    name_candidates = []

    for i, line in enumerate(formatted_blocks):
        text = line["text"]
        size = line.get("size", 0)
        is_bold = line.get("is_bold", False)

        # Remove markdown formatting for analysis
        clean_text = text.strip('*').strip('#').strip()
        word_count = len(clean_text.split())

        # Name characteristics:
        # 1. Large font (above h1 threshold)
        # 2. Short text (< 50 chars, typically 2-4 words)
        # 3. All caps or title case
        # 4. No special characters except spaces and common name chars

        is_likely_name = (
            size >= font_thresholds["h1"] and  # Large font
            len(clean_text) < 50 and  # Short
            word_count >= 2 and word_count <= 5 and  # 2-5 words typical for names
            clean_text.isupper() and  # All caps (common for names in resumes)
            not any(char in clean_text for char in ['@', ':', '|', '•', '(', ')', '+', '#'])  # No special chars
        )

        if is_likely_name:
            name_candidates.append((i, line, size, clean_text))

    if not name_candidates:
        return None, formatted_blocks

    # If multiple candidates, choose the one with largest font
    name_candidates.sort(key=lambda x: x[2], reverse=True)
    name_index, name_line, _, name_text = name_candidates[0]

    # Remove name from blocks
    blocks_without_name = [b for i, b in enumerate(formatted_blocks) if i != name_index]

    return name_line["text"], blocks_without_name


def extract_with_columns_first_formatting(doc, font_thresholds, stats):
    """Extract multi-column text with formatting"""
    ocr_text_pages = []
    all_pages_blocks = []
    extracted_name = None

    # First pass: Extract all formatted blocks from all pages
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        if len(text.strip()) < 50:
            print(f"   Page {page_num + 1}: ⚠️  Image-based - trying OCR")
            stats["ocr_pages"] += 1
            ocr_text = clean_text(perform_ocr(page))
            ocr_text_pages.append(ocr_text)
            all_pages_blocks.append(([], 0, page_num))
            continue

        print(f"   Page {page_num + 1}: ✓  Text extracted with formatting")
        stats["text_pages"] += 1

        formatted_blocks = extract_formatted_blocks(page, font_thresholds)

        # Extract name from first page only
        if page_num == 0 and formatted_blocks:
            extracted_name, formatted_blocks = find_and_extract_name(formatted_blocks, font_thresholds)
            if extracted_name:
                print(f"   🎯 Name detected and extracted: {extracted_name.strip('*')}")

        if formatted_blocks:
            x_coords = [block["x"] for block in formatted_blocks]
            boundary = detect_column_boundary(x_coords)
        else:
            boundary = 0

        all_pages_blocks.append((formatted_blocks, boundary, page_num))

    # Second pass: Separate into columns and build text
    left_column_text = []
    right_column_text = []

    for formatted_blocks, boundary, page_num in all_pages_blocks:
        if not formatted_blocks:
            continue

        left_blocks = [b for b in formatted_blocks if b["x"] < boundary]
        left_blocks.sort(key=lambda b: b["y"])
        left_text = "\n".join([block["text"] for block in left_blocks])
        left_column_text.append(clean_markdown(left_text))

    for formatted_blocks, boundary, page_num in all_pages_blocks:
        if not formatted_blocks:
            continue

        right_blocks = [b for b in formatted_blocks if b["x"] >= boundary]
        right_blocks.sort(key=lambda b: b["y"])
        right_text = "\n".join([block["text"] for block in right_blocks])
        right_column_text.append(clean_markdown(right_text))

    column_text = ""
    if left_column_text or right_column_text:
        column_parts = []
        if left_column_text:
            column_parts.append("\n\n".join(left_column_text))
        if right_column_text:
            column_parts.append("\n\n".join(right_column_text))
        column_text = "\n\n".join(column_parts)

    # Prepend name to the very beginning if found
    final_parts = []
    if extracted_name:
        final_parts.append(extracted_name)

    final_parts.extend(ocr_text_pages)

    if column_text.strip():
        final_parts.append(column_text)

    stats["total_chars"] = sum(len(text_part) for text_part in final_parts)

    if not final_parts:
        final_parts.append("")

    return final_parts, stats


def extract_docx(docx_source, preserve_formatting=True, source_name="document.docx", file_ext="docx"):
    """Extract text from DOCX/DOC with optional formatting and table support"""
    try:
        doc_obj = docx.Document(_ensure_docx_source(docx_source))

        if preserve_formatting:
            # Extract both paragraphs and tables in document order
            formatted_parts = []

            # Get all elements in order (paragraphs and tables)
            # We need to iterate through the document body elements
            from docx.oxml.text.paragraph import CT_P
            from docx.oxml.table import CT_Tbl

            for element in doc_obj.element.body:
                if isinstance(element, CT_P):
                    # It's a paragraph
                    para = docx.text.paragraph.Paragraph(element, doc_obj)
                    if not para.text.strip():
                        continue

                    # Check paragraph style
                    style_name = para.style.name.lower() if para.style else ""

                    if "heading 1" in style_name or "title" in style_name:
                        formatted_parts.append(f"**{para.text.strip()}**")
                    elif "heading 2" in style_name:
                        formatted_parts.append(f"## {para.text.strip()}")
                    elif "heading 3" in style_name:
                        formatted_parts.append(f"### {para.text.strip()}")
                    else:
                        # Check for bold runs
                        has_bold = any(run.bold for run in para.runs if run.text.strip())
                        all_bold = all(run.bold for run in para.runs if run.text.strip())

                        if all_bold and len(para.text.strip()) < 100:
                            formatted_parts.append(f"**{para.text.strip()}**")
                        elif has_bold:
                            # Mix of bold and normal - reconstruct carefully
                            line_parts = []
                            for run in para.runs:
                                text = run.text
                                if not text:
                                    continue

                                # Remove any existing bold markers to avoid duplication
                                text = text.replace('**', '')

                                if run.bold and text.strip():
                                    line_parts.append(f"**{text}**")
                                else:
                                    line_parts.append(text)

                            result = "".join(line_parts)
                            # Clean up any double bold markers
                            result = result.replace('****', '** **')
                            formatted_parts.append(result)
                        else:
                            formatted_parts.append(para.text.strip())

                elif isinstance(element, CT_Tbl):
                    # It's a table
                    table = docx.table.Table(element, doc_obj)
                    table_text = extract_table_formatted(table)
                    if table_text:
                        formatted_parts.append("\n" + table_text + "\n")

            text = "\n".join(formatted_parts)
            method = "python-docx (formatted with tables)"
        else:
            # Plain text extraction with tables
            all_text = []

            from docx.oxml.text.paragraph import CT_P
            from docx.oxml.table import CT_Tbl

            for element in doc_obj.element.body:
                if isinstance(element, CT_P):
                    para = docx.text.paragraph.Paragraph(element, doc_obj)
                    if para.text.strip():
                        all_text.append(para.text.strip())
                elif isinstance(element, CT_Tbl):
                    table = docx.table.Table(element, doc_obj)
                    table_text = extract_table_plain(table)
                    if table_text:
                        all_text.append(table_text)

            text = "\n\n".join(all_text)
            method = "python-docx (with tables)"

        text = clean_markdown(text) if preserve_formatting else clean_text(text)

        print(f"\n✅ {file_ext.upper()} extraction complete for {source_name} using {method}!")
        print(f"   Total characters: {len(text):,}")

        normalized_type = "docx" if file_ext in ["docx", "doc"] else file_ext
        return (
            normalized_type,
            text,
            1,
            "",
            False,
        )

    except Exception as e:
        print(f"❌ Error in {file_ext.upper()} extraction: {e}")
        traceback.print_exc()
        return None


def extract_table_formatted(table):
    """Extract table content with markdown formatting"""
    if not table.rows:
        return ""

    rows_text = []

    for row in table.rows:
        cells_text = []
        for cell in row.cells:
            cell_text = cell.text.strip()
            if cell_text:
                cells_text.append(cell_text)

        if cells_text:
            # Format as markdown table if 2+ columns, otherwise as list
            if len(cells_text) >= 2:
                rows_text.append(f"| {' | '.join(cells_text)} |")
            else:
                rows_text.append(cells_text[0])

    if not rows_text:
        return ""

    # If it looks like a markdown table, add header separator
    if len(rows_text) > 0 and '|' in rows_text[0]:
        # Count columns from first row
        col_count = rows_text[0].count('|') - 1
        separator = '| ' + ' | '.join(['---'] * col_count) + ' |'
        # Insert separator after first row
        rows_text.insert(1, separator)

    return "\n".join(rows_text)


def extract_table_plain(table):
    """Extract table content as plain text"""
    if not table.rows:
        return ""

    rows_text = []

    for row in table.rows:
        cells_text = []
        for cell in row.cells:
            cell_text = cell.text.strip()
            if cell_text:
                cells_text.append(cell_text)

        if cells_text:
            rows_text.append(" | ".join(cells_text))

    return "\n".join(rows_text)


def extract_txt(txt_source, source_name="document.txt"):
    """Extract text from plain text files"""
    try:
        if isinstance(txt_source, (str, os.PathLike)):
            txt_file = Path(txt_source)
            try:
                text = txt_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = txt_file.read_text(encoding="latin-1")
        elif isinstance(txt_source, io.BytesIO):
            txt_source.seek(0)
            text = txt_source.read().decode("utf-8", errors="replace")
        elif isinstance(txt_source, (bytes, bytearray)):
            text = bytes(txt_source).decode("utf-8", errors="replace")
        else:
            raise TypeError("Unsupported text source type")

        text = clean_text(text)

        print(f"\n✅ TXT extraction complete from {source_name}!")
        print(f"   Total characters: {len(text):,}")

        return (
            "txt",
            text,
            1,
            "",
            False,
        )

    except Exception as e:
        print(f"❌ Error in TXT extraction: {e}")
        traceback.print_exc()
        return None


def detect_multi_column_layout(doc):
    """Detect if the document has a multi-column layout"""
    pages_to_check = min(3, len(doc))
    multi_column_votes = 0

    for page_num in range(pages_to_check):
        page = doc[page_num]
        text = page.get_text("text")

        if len(text.strip()) < 50:
            continue

        blocks = page.get_text("blocks")

        if len(blocks) < 5:
            continue

        x_coords = [block[0] for block in blocks]
        x_coords.sort()
        gaps = [x_coords[i + 1] - x_coords[i] for i in range(len(x_coords) - 1)]

        if not gaps:
            continue

        max_gap = max(gaps)
        mean_gap = statistics.mean(gaps)

        if max_gap > 2 * mean_gap and max_gap > 50:
            multi_column_votes += 1

    return multi_column_votes >= pages_to_check / 2


def extract_with_default_strategy(doc):
    """Extract text using PyMuPDF's default text extraction"""
    all_text = []
    stats = {
        "total_pages": len(doc),
        "text_pages": 0,
        "ocr_pages": 0,
        "total_chars": 0,
    }

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        if len(text.strip()) < 50:
            print(f"   Page {page_num + 1}: ⚠️  Image-based ({len(text)} chars) - trying OCR")
            stats["ocr_pages"] += 1
            text = perform_ocr(page)
        elif len(text.strip()) < 100:
            print(f"   Page {page_num + 1}: ⚠️  Low content ({len(text)} chars)")
            stats["text_pages"] += 1
        else:
            print(f"   Page {page_num + 1}: ✓  Text extracted ({len(text):,} chars)")
            stats["text_pages"] += 1

        text = clean_text(text)
        all_text.append(text)
        stats["total_chars"] += len(text)

    return all_text, stats


def extract_with_columns_first_strategy(doc):
    """Extract text using column-first strategy"""
    stats = {
        "total_pages": len(doc),
        "text_pages": 0,
        "ocr_pages": 0,
        "total_chars": 0,
    }

    ocr_text_pages = []
    text_pages_info = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        if len(text.strip()) < 50:
            print(f"   Page {page_num + 1}: ⚠️  Image-based ({len(text)} chars) - trying OCR")
            stats["ocr_pages"] += 1
            ocr_text = clean_text(perform_ocr(page))
            ocr_text_pages.append(ocr_text)
            continue

        if len(text.strip()) < 100:
            print(f"   Page {page_num + 1}: ⚠️  Low content ({len(text)} chars)")
        else:
            print(f"   Page {page_num + 1}: ✓  Text extracted ({len(text):,} chars)")

        stats["text_pages"] += 1
        blocks = page.get_text("blocks")
        if blocks:
            boundary = detect_column_boundary([block[0] for block in blocks])
        else:
            boundary = 0
        text_pages_info.append((blocks, boundary))

    left_column_text = []
    right_column_text = []

    for blocks, boundary in text_pages_info:
        if not blocks:
            continue
        left_blocks = [b for b in blocks if b[0] < boundary]
        left_blocks.sort(key=lambda b: b[1])
        left_text = "\n".join([block[4] for block in left_blocks])
        left_column_text.append(clean_text(left_text))

    for blocks, boundary in text_pages_info:
        if not blocks:
            continue
        right_blocks = [b for b in blocks if b[0] >= boundary]
        right_blocks.sort(key=lambda b: b[1])
        right_text = "\n".join([block[4] for block in right_blocks])
        right_column_text.append(clean_text(right_text))

    column_text = ""
    if left_column_text or right_column_text:
        column_parts = []
        if left_column_text:
            column_parts.append("\n\n".join(left_column_text))
        if right_column_text:
            column_parts.append("\n\n".join(right_column_text))
        column_text = "\n\n".join(column_parts)

    composed_text_parts = ocr_text_pages[:]
    if column_text.strip():
        composed_text_parts.append(column_text)

    stats["total_chars"] = sum(len(text_part) for text_part in composed_text_parts)

    if not composed_text_parts:
        composed_text_parts.append("")

    return composed_text_parts, stats


def detect_column_boundary(x_positions):
    """Detect the boundary between columns"""
    if not x_positions:
        return 0

    x_sorted = sorted(x_positions)
    max_gap = 0
    boundary = 0

    for i in range(1, len(x_sorted)):
        gap = x_sorted[i] - x_sorted[i - 1]
        if gap > max_gap:
            max_gap = gap
            boundary = (x_sorted[i] + x_sorted[i - 1]) / 2

    if max_gap < 50:
        boundary = sum(x_positions) / len(x_positions)

    return boundary


def preprocess_image(img):
    """Preprocess image for better OCR"""
    try:
        img = img.convert('L')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
        return img
    except Exception as e:
        print(f"              ⚠️  Preprocessing failed: {e}")
        return img


def perform_ocr(page):
    """Perform OCR on a page"""
    try:
        pix = page.get_pixmap(matrix=fitz.Matrix(400 / 72, 400 / 72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = preprocess_image(img)
        ocr_text = pytesseract.image_to_string(img, lang="eng", config="--psm 3")
        print(f"              ✓ OCR extracted {len(ocr_text)} chars")
        return ocr_text
    except ImportError:
        print("              ⚠️  pytesseract not installed")
        return page.get_text("text")
    except Exception as e:
        print(f"              ❌ OCR failed: {e}")
        return page.get_text("text")


def clean_text(text):
    """Clean extracted text"""
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if line and not re.match(r"^[^\w\s]+$", line):
            cleaned.append(line)
    return "\n".join(cleaned)


def clean_markdown(text):
    """Clean markdown text while preserving formatting"""
    # Remove excessive whitespace
    text = re.sub(r" +", " ", text)

    # Normalize line breaks (max 2 consecutive)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # Remove lines with only special characters
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Keep markdown headers and bold text
        if stripped and not re.match(r"^[^\w\s#*]+$", stripped):
            cleaned.append(line.rstrip())

    return "\n".join(cleaned)


def process_document(doc_path, multi_column_strategy="smart", preserve_formatting=True):
    """
    Main function to process a document
    Args:
        doc_path: Path or in-memory payload
        multi_column_strategy: Strategy for multi-column layouts
        preserve_formatting: If True, preserve headings, bold, etc. as markdown

    Returns:
        Tuple: (file_type, text_raw, page, doc_object, ocr)
        or None if extraction fails
    """
    result = extract_document(doc_path, multi_column_strategy, preserve_formatting)
    if result:
        return result
    print("\n" + "=" * 80)
    print("❌ FAILED!")
    return None

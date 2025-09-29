#!/usr/bin/env python3
"""
Markdown to PDF Converter (Alternative using reportlab)
Converts the Team Task Delegation Framework markdown to PDF format using reportlab.
"""

import os
import sys
from pathlib import Path
import markdown2
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas with page numbers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        canvas.Canvas.showPage(self)

    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, page_state) in enumerate(self._saved_page_states):
            self.__dict__.update(page_state)
            self.draw_page_number(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_num, total_pages):
        self.setFont("Helvetica", 9)
        self.drawString(letter[0] / 2.0 - 50, 0.5 * inch,
                       f"Page {page_num} of {total_pages}")
        self.drawString(letter[0] / 2.0 - 100, letter[1] - 0.5 * inch,
                       "Smart India Hackathon: Autonomous Lunar Habitat Robot")


def create_custom_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()

    # Custom styles
    custom_styles = {
        'CustomTitle': ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=22,
            textColor=HexColor('#003366'),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        ),
        'CustomHeading1': ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#0066cc'),
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ),
        'CustomHeading2': ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#336699'),
            spaceAfter=12,
            spaceBefore=18,
            fontName='Helvetica-Bold'
        ),
        'CustomHeading3': ParagraphStyle(
            'CustomHeading3',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=HexColor('#4d79a4'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ),
        'CustomNormal': ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            textColor=HexColor('#333333'),
            fontName='Helvetica'
        ),
        'CustomBullet': ParagraphStyle(
            'CustomBullet',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=6,
            textColor=HexColor('#333333'),
            fontName='Helvetica'
        ),
        'TeamMember': ParagraphStyle(
            'TeamMember',
            parent=styles['Normal'],
            fontSize=12,
            textColor=HexColor('#003366'),
            fontName='Helvetica-Bold',
            spaceAfter=8,
            leftIndent=10
        )
    }

    # Add custom styles to the existing stylesheet
    for name, style in custom_styles.items():
        styles.add(style)

    return styles


def clean_text(text):
    """Clean markdown formatting from text"""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Italic
    text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)  # Code
    text = re.sub(r'#{1,6}\s*', '', text)  # Remove hash symbols
    return text.strip()


def process_markdown_to_paragraphs(content, styles):
    """Process markdown content and convert to reportlab paragraphs"""
    elements = []
    lines = content.split('\n')

    # Add title
    elements.append(Paragraph("Smart India Hackathon: Autonomous Lunar Habitat Robot", styles['CustomTitle']))
    elements.append(Paragraph("Team Task Delegation Framework (16-Week Research Program)", styles['CustomHeading1']))
    elements.append(Spacer(1, 20))

    current_paragraph_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            # Empty line - finish current paragraph if any
            if current_paragraph_lines:
                para_text = ' '.join(current_paragraph_lines)
                para_text = clean_text(para_text)
                if para_text:
                    elements.append(Paragraph(para_text, styles['CustomNormal']))
                current_paragraph_lines = []
            continue

        # Handle headers
        if line.startswith('# '):
            if current_paragraph_lines:
                para_text = ' '.join(current_paragraph_lines)
                para_text = clean_text(para_text)
                if para_text:
                    elements.append(Paragraph(para_text, styles['CustomNormal']))
                current_paragraph_lines = []

            header_text = clean_text(line[2:])
            elements.append(Spacer(1, 15))
            elements.append(Paragraph(header_text, styles['CustomHeading1']))

        elif line.startswith('## '):
            if current_paragraph_lines:
                para_text = ' '.join(current_paragraph_lines)
                para_text = clean_text(para_text)
                if para_text:
                    elements.append(Paragraph(para_text, styles['CustomNormal']))
                current_paragraph_lines = []

            header_text = clean_text(line[3:])
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(header_text, styles['CustomHeading2']))

        elif line.startswith('### '):
            if current_paragraph_lines:
                para_text = ' '.join(current_paragraph_lines)
                para_text = clean_text(para_text)
                if para_text:
                    elements.append(Paragraph(para_text, styles['CustomNormal']))
                current_paragraph_lines = []

            header_text = clean_text(line[4:])
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(header_text, styles['CustomHeading3']))

        elif line.startswith('#### '):
            if current_paragraph_lines:
                para_text = ' '.join(current_paragraph_lines)
                para_text = clean_text(para_text)
                if para_text:
                    elements.append(Paragraph(para_text, styles['CustomNormal']))
                current_paragraph_lines = []

            header_text = clean_text(line[5:])
            elements.append(Spacer(1, 8))
            elements.append(Paragraph(header_text, styles['TeamMember']))

        # Handle bullet points
        elif line.startswith('- ') or line.startswith('* '):
            if current_paragraph_lines:
                para_text = ' '.join(current_paragraph_lines)
                para_text = clean_text(para_text)
                if para_text:
                    elements.append(Paragraph(para_text, styles['CustomNormal']))
                current_paragraph_lines = []

            bullet_text = clean_text(line[2:])
            elements.append(Paragraph(f"• {bullet_text}", styles['CustomBullet']))

        # Handle horizontal rules
        elif line.startswith('---'):
            if current_paragraph_lines:
                para_text = ' '.join(current_paragraph_lines)
                para_text = clean_text(para_text)
                if para_text:
                    elements.append(Paragraph(para_text, styles['CustomNormal']))
                current_paragraph_lines = []
            elements.append(Spacer(1, 15))

        # Regular text
        else:
            current_paragraph_lines.append(line)

    # Don't forget the last paragraph
    if current_paragraph_lines:
        para_text = ' '.join(current_paragraph_lines)
        para_text = clean_text(para_text)
        if para_text:
            elements.append(Paragraph(para_text, styles['CustomNormal']))

    return elements


def convert_markdown_to_pdf_reportlab(input_file, output_file):
    """Convert markdown file to PDF using reportlab"""
    try:
        # Read markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            canvasmaker=NumberedCanvas
        )

        # Get styles
        styles = create_custom_styles()

        # Process content
        elements = process_markdown_to_paragraphs(content, styles)

        # Build PDF
        doc.build(elements)

        print(f"✅ Successfully converted {input_file} to {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error converting to PDF: {str(e)}")
        return False


def main():
    """Main function"""
    # Set file paths
    script_dir = Path(__file__).parent
    input_file = script_dir / "Team_Task_Delegation_Framework.md"
    output_file = script_dir / "Team_Task_Delegation_Framework.pdf"

    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        print("Available files:")
        for file in script_dir.glob("*.md"):
            print(f"  - {file.name}")
        return False

    print(f"🚀 Converting {input_file.name} to PDF format using ReportLab...")
    print(f"📁 Input: {input_file}")
    print(f"📄 Output: {output_file}")

    success = convert_markdown_to_pdf_reportlab(input_file, output_file)

    if success:
        print(f"\n🎉 Conversion completed successfully!")
        print(f"📋 PDF file created: {output_file}")
        print(f"📊 File size: {output_file.stat().st_size / 1024:.1f} KB")
    else:
        print(f"\n💥 Conversion failed!")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

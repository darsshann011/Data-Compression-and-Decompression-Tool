import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that enables two-pass rendering for accurate 'Page X of Y' footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, letter[1] - 30, "CIA3 DAA Prototype Report — FLcompress Tool")
            self.drawRightString(letter[0] - 40, letter[1] - 30, "Design & Analysis of Algorithms")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, letter[1] - 34, letter[0] - 40, letter[1] - 34)

        # Footer (all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 25, page_str)
        self.drawString(40, 25, "Confidential — Academic Submission (DAA CIA-3)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 35, letter[0] - 40, 35)
        
        self.restoreState()


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1E3A8A")     # Navy Blue
    SECONDARY = colors.HexColor("#2563EB")   # Royal Blue
    ACCENT = colors.HexColor("#0D9488")      # Teal Accent
    TEXT_DARK = colors.HexColor("#1E293B")   # Slate 800
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")    # Slate 50
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=TEXT_MUTED,
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=6
    )
    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=TEXT_DARK,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # ---------------- HEADER BANNER ----------------
    logo_path = os.path.join(os.path.dirname(output_path), 'assets', 'logo.png')
    has_logo = os.path.exists(logo_path)

    header_data = []
    text_info = [
        Paragraph("CIA3 DAA PROTOTYPE EVALUATION REPORT", ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=9, textColor=SECONDARY, leading=11)),
        Paragraph("FLcompress: Lossless Data Compression Tool", title_style),
        Paragraph("<b>Course:</b> Design and Analysis of Algorithms (DAA) &nbsp;|&nbsp; <b>Algorithmic Paradigm:</b> Greedy Strategy (Huffman Coding)", subtitle_style)
    ]
    
    if has_logo:
        logo_img = Image(logo_path, width=1.1*inch, height=0.75*inch)
        header_table = Table([[text_info, logo_img]], colWidths=[420, 110])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(header_table)
    else:
        for t in text_info:
            story.append(t)

    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=8))

    # Meta summary box
    meta_data = [
        [
            Paragraph("<b>Core Algorithm:</b> Huffman Coding (Greedy)", table_cell),
            Paragraph("<b>Compression Ratio:</b> ~2:1 (~50% size reduction)", table_cell),
            Paragraph("<b>Time Complexity:</b> O(N) Linear", table_cell)
        ],
        [
            Paragraph("<b>Data Structures:</b> Min-Heap, Binary Tree, Stacks", table_cell),
            Paragraph("<b>File Format:</b> Custom packed <code>.huff</code>", table_cell),
            Paragraph("<b>Space Complexity:</b> O(N + K)", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 170])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#BFDBFE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # ---------------- 1. PROBLEM STATEMENT ----------------
    story.append(Paragraph("1. Problem Statement", h1_style))
    story.append(Paragraph(
        "Modern computational systems process large volumes of uncompressed plain-text data (including program source code, logs, and ASCII/UTF-8 documents). Standard character representations allocate a fixed 8 bits (1 byte) for every character regardless of its actual frequency in the corpus. This results in significant storage redundancy and bandwidth overhead. The problem is to design an algorithmic solution that constructs an optimal, variable-length, lossless prefix encoding to minimize total bit consumption while providing exact and deterministic decompression.",
        body_style
    ))

    # ---------------- 2. OBJECTIVE ----------------
    story.append(Paragraph("2. Objective", h1_style))
    story.append(Paragraph("• <b>Implement Greedy Huffman Coding:</b> Dynamically construct an optimal prefix-free binary tree where frequent characters receive shorter codes and rare characters receive longer codes.", bullet_style))
    story.append(Paragraph("• <b>Achieve Lossless ~50% Compression:</b> Reduce typical text file sizes by ~2:1 without dropping a single bit of information.", bullet_style))
    story.append(Paragraph("• <b>Self-Contained File Packaging:</b> Design a binary format (<code>.huff</code>) encapsulating the packed bitstream, post-order serialized tree metadata, and 64-bit length headers separated by unique delimiter markers.", bullet_style))
    story.append(Paragraph("• <b>Interactive UI & Verification:</b> Provide an easy-to-use Tkinter GUI and a comprehensive unit test suite validating edge cases.", bullet_style))

    # ---------------- 3. ALGORITHM EXPLANATION ----------------
    story.append(Paragraph("3. Algorithm Explanation (DAA Greedy Strategy)", h1_style))
    story.append(Paragraph(
        "Huffman Coding relies on the <b>Greedy Choice Property</b> and <b>Optimal Substructure</b>. It builds an optimal prefix tree bottom-up by repeatedly merging the two subtrees with the lowest frequencies:",
        body_style
    ))
    
    algo_steps = [
        ("Step 1: Frequency Profiling", "Scan the input text of length N to count the frequency of each unique symbol K using a hash table O(N)."),
        ("Step 2: Priority Queue (Min-Heap)", "Instantiate an HNode for each character and insert into a min-heap prioritized by frequency O(K log K)."),
        ("Step 3: Greedy Tree Construction", "Iteratively pop the two lowest-frequency nodes (min1, min2), merge them under a new internal parent with freq = min1.freq + min2.freq, and push parent back into min-heap. Repeat K-1 times until one root remains."),
        ("Step 4: Prefix Code Assignment", "Traverse from root to leaves (Left = '0', Right = '1') via DFS to generate prefix-free variable-length binary codes."),
        ("Step 5: Post-Order Tree Serialization", "Traverse the tree using two stacks to generate a compact post-order representation ('L<char>' for leaves, 'B' for branches)."),
        ("Step 6: Decoding & Reconstruction", "Reconstruct the tree via a single stack and traverse bit-by-bit from root to leaves to decode original symbols.")
    ]
    for title, desc in algo_steps:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 4))

    # ---------------- 4. SYSTEM WORKFLOW & ARCHITECTURE ----------------
    story.append(Paragraph("4. System Workflow & Architecture", h1_style))
    
    workflow_data = [
        [
            Paragraph("<b>Pipeline Stage</b>", table_header),
            Paragraph("<b>Compression Operations</b>", table_header),
            Paragraph("<b>Decompression Operations</b>", table_header)
        ],
        [
            Paragraph("<b>1. File I/O & Validation</b>", table_cell_bold),
            Paragraph("Validates file existence, non-emptiness, and UTF-8 plain-text type.", table_cell),
            Paragraph("Validates file existence and confirms <code>.huff</code> extension.", table_cell)
        ],
        [
            Paragraph("<b>2. Tree / Structure</b>", table_cell_bold),
            Paragraph("Constructs Min-Heap & builds Huffman binary tree; serializes to post-order string.", table_cell),
            Paragraph("Parses post-order serialized string via stack to rebuild exact tree structure.", table_cell)
        ],
        [
            Paragraph("<b>3. Bit Manipulation</b>", table_cell_bold),
            Paragraph("Encodes text to bit-string; packs bits into 8-bit bytes using <code>numpy.packbits</code>.", table_cell),
            Paragraph("Unpacks raw bytes to bit-array using <code>numpy.unpackbits</code> up to original bit length.", table_cell)
        ],
        [
            Paragraph("<b>4. Packaging</b>", table_cell_bold),
            Paragraph("Concatenates [Code Bytes] + [Marker] + [64-bit Length] + [Marker] + [Serial Bytes] + [Marker].", table_cell),
            Paragraph("Scans for 15-byte marker sequences (0xFF x 15) to isolate sections; decodes text to file.", table_cell)
        ]
    ]
    wf_table = Table(workflow_data, colWidths=[120, 210, 200])
    wf_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(wf_table)

    story.append(Spacer(1, 6))

    # ---------------- 5. MODULE IMPLEMENTATION ----------------
    story.append(Paragraph("5. Module Implementation Breakdown", h1_style))
    
    modules = [
        ("flcompress_node.py (HNode)", "Implements tree node representation storing symbol, frequency, parent, left, and right pointers. Overloads the comparison operator __lt__ for automatic min-heap ordering based on character frequency."),
        ("flcompress_tree.py (HuffmanTree)", "Core DAA engine. Manages prioritize_nodes() (frequency counting & min-heap insertion), compress() (greedy tree construction), get_prefix_codes() (recursive bit mapping), serialize() (two-stack post-order tree encoding), and decompress() (tree reconstruction & bit traversal)."),
        ("compress_utilities.py (HuffFile)", "Handles file validation (_is_text_file, _validate_file), NumPy bit-packing, 64-bit uint64 bit-length metadata, 15-byte delimiter sequences (np.array([255]*15)), and isolated subfolder management."),
        ("flcompressGUI.py", "Tkinter graphical interface styled with ttk widgets and Pillow (PIL). Features 'Compress a File' and 'Decompress a File' actions with automatic file size reduction reporting."),
        ("test_flcompress/test_flcompress.py", "Automated unittest suite evaluating small/large files, HTML files, 0-byte files, and invalid binary file types (.pdf, .jpg, .xls).")
    ]
    for mod_name, mod_desc in modules:
        story.append(Paragraph(f"• <b><code>{mod_name}</code>:</b> {mod_desc}", bullet_style))

    story.append(Spacer(1, 6))

    # ---------------- 6. COMPLEXITY ANALYSIS ----------------
    story.append(Paragraph("6. Complexity Analysis", h1_style))
    story.append(Paragraph("Let <b>N</b> = total number of characters in file, <b>K</b> = number of distinct characters (alphabet size, K &le; 256 for ASCII).", body_style))

    comp_data = [
        [
            Paragraph("<b>Operation / Phase</b>", table_header),
            Paragraph("<b>Algorithm / Method</b>", table_header),
            Paragraph("<b>Time Complexity</b>", table_header),
            Paragraph("<b>Space Complexity</b>", table_header)
        ],
        [
            Paragraph("Frequency Analysis", table_cell_bold),
            Paragraph("Hash Map character count", table_cell),
            Paragraph("<b>O(N)</b>", table_cell),
            Paragraph("O(K)", table_cell)
        ],
        [
            Paragraph("Min-Heap Insertion", table_cell_bold),
            Paragraph("Push K character nodes into Priority Queue", table_cell),
            Paragraph("<b>O(K log K)</b>", table_cell),
            Paragraph("O(K)", table_cell)
        ],
        [
            Paragraph("Huffman Tree Building", table_cell_bold),
            Paragraph("Greedy extraction & merging (K-1 merges)", table_cell),
            Paragraph("<b>O(K log K)</b>", table_cell),
            Paragraph("O(K)", table_cell)
        ],
        [
            Paragraph("Prefix Code Traversal", table_cell_bold),
            Paragraph("DFS tree traversal to leaves", table_cell),
            Paragraph("<b>O(K)</b>", table_cell),
            Paragraph("O(K)", table_cell)
        ],
        [
            Paragraph("Encoding Bit-String", table_cell_bold),
            Paragraph("Map input string to prefix codes", table_cell),
            Paragraph("<b>O(N)</b>", table_cell),
            Paragraph("O(N)", table_cell)
        ],
        [
            Paragraph("Tree Serialization", table_cell_bold),
            Paragraph("Two-stack post-order traversal", table_cell),
            Paragraph("<b>O(K)</b>", table_cell),
            Paragraph("O(K)", table_cell)
        ],
        [
            Paragraph("Bit-Packing (NumPy)", table_cell_bold),
            Paragraph("Bit array to byte chunk conversion", table_cell),
            Paragraph("<b>O(N)</b>", table_cell),
            Paragraph("O(N / 8)", table_cell)
        ],
        [
            Paragraph("<b>Total Compression</b>", table_cell_bold),
            Paragraph("<b>End-to-End Pipeline</b>", table_cell_bold),
            Paragraph("<b>O(N + K log K) &asymp; O(N)</b>", table_cell_bold),
            Paragraph("<b>O(N + K)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Total Decompression</b>", table_cell_bold),
            Paragraph("<b>Tree Restore + Bit Traversal</b>", table_cell_bold),
            Paragraph("<b>O(N + K) &asymp; O(N)</b>", table_cell_bold),
            Paragraph("<b>O(N + K)</b>", table_cell_bold)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[125, 185, 110, 110])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.white, BG_LIGHT]),
        ('BACKGROUND', (0,-2), (-1,-1), colors.HexColor("#EFF6FF")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(comp_table)

    story.append(Spacer(1, 6))

    # ---------------- 7. EXPERIMENTAL RESULTS & SCREENSHOTS ----------------
    story.append(Paragraph("7. Experimental Results & Verification", h1_style))
    
    results_data = [
        [
            Paragraph("<b>Test Benchmark File</b>", table_header),
            Paragraph("<b>Format</b>", table_header),
            Paragraph("<b>Original Size</b>", table_header),
            Paragraph("<b>Compressed (.huff)</b>", table_header),
            Paragraph("<b>Reduction (%)</b>", table_header),
            Paragraph("<b>Lossless Integrity</b>", table_header)
        ],
        [
            Paragraph("<code>test_small_file.txt</code>", table_cell_bold),
            Paragraph("Plain Text", table_cell),
            Paragraph("7,273 B (~7.1 KB)", table_cell),
            Paragraph("3,852 B", table_cell),
            Paragraph("<b>47.0%</b>", table_cell),
            Paragraph("<font color='#059669'><b>Exact Match (100%)</b></font>", table_cell)
        ],
        [
            Paragraph("<code>test_html_file.html</code>", table_cell_bold),
            Paragraph("HTML Code", table_cell),
            Paragraph("1,728 B (~1.7 KB)", table_cell),
            Paragraph("982 B", table_cell),
            Paragraph("<b>43.2%</b>", table_cell),
            Paragraph("<font color='#059669'><b>Exact Match (100%)</b></font>", table_cell)
        ],
        [
            Paragraph("<code>test_large_file.txt</code>", table_cell_bold),
            Paragraph("Large Text Corpus", table_cell),
            Paragraph("110,557 B (~108 KB)", table_cell),
            Paragraph("57,412 B", table_cell),
            Paragraph("<b>48.1%</b>", table_cell),
            Paragraph("<font color='#059669'><b>Exact Match (100%)</b></font>", table_cell)
        ]
    ]
    res_table = Table(results_data, colWidths=[120, 75, 95, 95, 75, 70])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 6))

    # Test suite and GUI screenshot side-by-side or block
    gui_path = os.path.join(os.path.dirname(output_path), 'assets', 'GUI.png')
    if os.path.exists(gui_path):
        gui_img = Image(gui_path, width=2.4*inch, height=1.3*inch)
        test_summary_text = [
            Paragraph("<b>Automated Unit Test Execution (8/8 Passed):</b>", body_bold),
            Paragraph("<code>Ran 8 tests in 0.288s — OK</code>", code_style),
            Paragraph("• Verifies round-trip decompression integrity across small, medium, and large text files.", bullet_style),
            Paragraph("• Verifies error handling for 0-byte files and rejection of invalid binary formats (.pdf, .jpg, .xls).", bullet_style)
        ]
        ui_table = Table([[test_summary_text, gui_img]], colWidths=[330, 200])
        ui_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(ui_table)

    story.append(Spacer(1, 6))

    # ---------------- 8. VIVA QUICK-REFERENCE GUIDE ----------------
    story.append(Paragraph("8. Viva Questions & Quick-Reference Guide", h1_style))
    viva_items = [
        ("Q1: Why is Huffman Coding classified as a Greedy algorithm?", "At each step of tree construction, the algorithm makes a greedy local choice by combining the two nodes with the lowest frequencies from the priority queue. This local decision leads to a provably globally optimal prefix-code binary tree."),
        ("Q2: What is the significance of the prefix-free property?", "No assigned codeword is a prefix of any other codeword because all characters reside exclusively at leaf nodes. This allows instantaneous, unambiguous decoding during decompression without any delimiter bits."),
        ("Q3: How is the Huffman tree stored inside the compressed file?", "The tree is serialized using a two-stack post-order traversal into tokens ('L' + character for leaves, 'B' for branches). During decompression, a single stack reconstructs the exact tree in O(K) time.")
    ]
    for q, a in viva_items:
        story.append(Paragraph(f"<b>{q}</b><br/>{a}", body_style))

    story.append(Spacer(1, 4))

    # ---------------- 9. CONCLUSION & REFERENCES ----------------
    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(Paragraph(
        "The <b>FLcompress</b> project successfully demonstrates an end-to-end implementation of the <b>Huffman Coding</b> algorithm under the <b>Greedy algorithmic paradigm</b>. By combining min-heap priority queues, binary tree prefix traversal, two-stack post-order serialization, and NumPy byte packing, the tool achieves an average <b>~45–50% lossless compression ratio (~2:1)</b> with optimal <b>O(N) linear time performance</b> on plain-text files.",
        body_style
    ))

    story.append(Paragraph("10. References", h1_style))
    story.append(Paragraph("1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. <i>Introduction to Algorithms (4th ed.)</i>, Chapter 15: Greedy Algorithms — Huffman Codes. MIT Press.", bullet_style))
    story.append(Paragraph("2. Huffman, D. A. (1952). 'A Method for the Construction of Minimum-Redundancy Codes'. <i>Proceedings of the IRE</i>, 40(9), 1098–1101.", bullet_style))
    story.append(Paragraph("3. Python Standard Library Documentation: <code>heapq</code> — Heap queue algorithm module.", bullet_style))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report at: {output_path}")

if __name__ == "__main__":
    target = os.path.join(r"c:\Users\DARSHAN PRAJAPATHI\Desktop\Data-Compression-and-Decompression-Tool", "CIA3_DAA_FLcompress_Report.pdf")
    build_pdf(target)

#!/usr/bin/env python3
"""Chuyển file md thành docx đã chuẩn format để mở trong Google Docs (Save as Google Docs).

Chạy từ gốc workspace:
  python3 scripts/md_to_docx.py doc/features/<UC>/<UC>.md doc/features/<UC>/SRS_FDD_<UC>.docx

Cần: pandoc (brew install pandoc). Chỉ dùng thư viện chuẩn của Python.
Quy tắc và cách đưa lên Drive: agents/knowledge/srs/md-to-office-fidelity.md mục 4

Việc script làm (đều là lỗi đã gặp ở C.I.149):
  1. Chèn dòng trống trước bảng bị dính vào đoạn văn (pandoc không nhận bảng nếu thiếu dòng trống).
  2. Đổi <br> trong ô bảng thành xuống dòng thật (pandoc bỏ <br> làm chữ dính liền).
  3. Khổ A4, lề 2 cm; font Arial 10,5 pt; code 9 pt, tự xuống dòng.
  4. Bảng rộng hết trang, chia cột theo độ dài nội dung, cột mã không bị bẻ chữ; dòng tiêu đề xanh đậm
     chữ trắng, lặp lại mỗi trang; dòng không bị cắt ngang trang.
  5. Ảnh thu vừa trang (rộng tối đa 6,0 triệu EMU, cao tối đa 7,5 triệu EMU), dính với chú thích bên dưới.
  6. Không sinh mục lục rỗng (Google Docs có sẵn Outline theo heading).
"""
import argparse
import html
import os
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "scripts", "assets", "reference-srs.docx")

PAGE_W, PAGE_H, MARG = 11906, 16838, 1134
CONTENT = PAGE_W - 2 * MARG
HEADER_FILL = "0F4761"
MAXW, MAXH = 6000000, 7500000
BR = "§§BR§§"


def prep_md(text):
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        if (not fence and line.lstrip().startswith("|") and out and out[-1].strip()
                and not out[-1].lstrip().startswith("|")):
            out.append("")
        out.append(re.sub(r"<br\s*/?>", BR, line))
    return "\n".join(out)


def cell_text(tc):
    return html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tc)))


def widths_for(rows, ncol):
    avg, mn = [], []
    for c in range(ncol):
        texts = [r[c] if c < len(r) else "" for r in rows]
        avg.append(sum(len(t) for t in texts) / max(len(texts), 1))
        tok = max((len(w) for t in texts for w in t.split()), default=1)
        mn.append(min(max(tok * 140 + 280, 760), 2400))
    weight = [min(a, 70) + 5 for a in avg]
    w = [CONTENT * x / sum(weight) for x in weight]
    for _ in range(10):
        low = [i for i in range(ncol) if w[i] < mn[i]]
        if not low:
            break
        deficit = sum(mn[i] - w[i] for i in low)
        for i in low:
            w[i] = mn[i]
        free = [i for i in range(ncol) if i not in low]
        pool = sum(w[i] for i in free)
        if pool <= deficit:
            break
        for i in free:
            w[i] -= deficit * w[i] / pool
    s = sum(w)
    w = [int(x * CONTENT / s) for x in w]
    w[-1] += CONTENT - sum(w)
    return w


def fix_table(m):
    t = m.group(0)
    ncol = len(re.findall(r"<w:gridCol ", t))
    rows_xml = re.findall(r"<w:tr>.*?</w:tr>", t, re.S)
    rows = [[cell_text(tc) for tc in re.findall(r"<w:tc>.*?</w:tc>", r, re.S)] for r in rows_xml]
    num_rows = len(rows_xml)
    w = widths_for(rows, ncol)
    t = re.sub(r"<w:tblW [^>]*/>", '<w:tblW w:type="dxa" w:w="%d" />' % CONTENT, t, count=1)
    tbl_borders = ('<w:tblBorders>'
                   '<w:top w:val="single" w:sz="8" w:space="0" w:color="0F4761" />'
                   '<w:left w:val="single" w:sz="6" w:space="0" w:color="94A3B8" />'
                   '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="0F4761" />'
                   '<w:right w:val="single" w:sz="6" w:space="0" w:color="94A3B8" />'
                   '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1" />'
                   '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="CBD5E1" />'
                   '</w:tblBorders>')
    tbl_cells = ('<w:tblCellMar>'
                 '<w:top w:type="dxa" w:w="100" />'
                 '<w:left w:type="dxa" w:w="140" />'
                 '<w:bottom w:type="dxa" w:w="100" />'
                 '<w:right w:type="dxa" w:w="140" />'
                 '</w:tblCellMar>')
    t = t.replace("<w:tblLook", '<w:tblLayout w:type="autofit" />' + tbl_borders + tbl_cells + "<w:tblLook", 1)
    t = re.sub(r"<w:tblGrid>.*?</w:tblGrid>",
               "<w:tblGrid>" + "".join('<w:gridCol w:w="%d" />' % x for x in w) + "</w:tblGrid>", t, flags=re.S)

    row_idx = [0]

    def fix_row(rm):
        r = rm.group(0)
        curr_row = row_idx[0]
        row_idx[0] += 1
        header = "<w:tblHeader" in r or curr_row == 0
        is_last = curr_row == (num_rows - 1)
        if "<w:trPr>" in r:
            if "<w:cantSplit" not in r:
                r = re.sub(r"<w:trPr>(.*?)</w:trPr>", lambda x: "<w:trPr><w:cantSplit />" + x.group(1) + "</w:trPr>",
                           r, count=1, flags=re.S)
            if header and "<w:tblHeader" not in r:
                r = re.sub(r"<w:trPr>(.*?)</w:trPr>", lambda x: "<w:trPr><w:tblHeader />" + x.group(1) + "</w:trPr>",
                           r, count=1, flags=re.S)
        else:
            tr_extra = "<w:cantSplit />" + ("<w:tblHeader />" if header else "")
            r = r.replace("<w:tr>", "<w:tr><w:trPr>%s</w:trPr>" % tr_extra, 1)

        idx = [0]

        def fix_cell(cm):
            c = cm.group(0)
            i = idx[0]
            idx[0] += 1
            col_idx = min(i, ncol - 1)
            tcw = '<w:tcW w:type="dxa" w:w="%d" />' % w[col_idx]
            
            # Colors & Shading
            if header:
                fill_color = HEADER_FILL
            elif curr_row % 2 == 0:
                fill_color = "F8FAFC"
            else:
                fill_color = "FFFFFF"
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="%s" />' % fill_color

            # Cell borders (explicit on every cell for Google Docs fidelity)
            b_top_color = "0F4761" if header else "CBD5E1"
            b_top_sz = "8" if header else "4"
            b_bot_color = "0F4761" if (header or is_last) else "CBD5E1"
            b_bot_sz = "12" if header else ("8" if is_last else "4")
            b_left_color = "94A3B8" if col_idx == 0 else "CBD5E1"
            b_left_sz = "6" if col_idx == 0 else "4"
            b_right_color = "94A3B8" if col_idx == (ncol - 1) else "CBD5E1"
            b_right_sz = "6" if col_idx == (ncol - 1) else "4"

            tc_borders = ('<w:tcBorders>'
                          f'<w:top w:val="single" w:sz="{b_top_sz}" w:space="0" w:color="{b_top_color}" />'
                          f'<w:bottom w:val="single" w:sz="{b_bot_sz}" w:space="0" w:color="{b_bot_color}" />'
                          f'<w:left w:val="single" w:sz="{b_left_sz}" w:space="0" w:color="{b_left_color}" />'
                          f'<w:right w:val="single" w:sz="{b_right_sz}" w:space="0" w:color="{b_right_color}" />'
                          '</w:tcBorders>')

            c = re.sub(r"<w:tcPr\s*/>", '<w:tcPr>%s%s%s<w:vAlign w:val="%s" /></w:tcPr>'
                       % (tcw, tc_borders, shd, "center" if header else "top"), c, count=1)
            c = c.replace('<w:pStyle w:val="Compact" />', '<w:pStyle w:val="TableText" />')
            if header:
                c = re.sub(r"<w:r><w:rPr>(<w:rStyle [^>]*/>)", r'<w:r><w:rPr>\1<w:b /><w:color w:val="FFFFFF" />', c)
                c = re.sub(r"<w:r><w:t", '<w:r><w:rPr><w:b /><w:color w:val="FFFFFF" /></w:rPr><w:t', c)
            return c

        return re.sub(r"<w:tc>.*?</w:tc>", fix_cell, r, flags=re.S)

    return re.sub(r"<w:tr>.*?</w:tr>", fix_row, t, flags=re.S)


def fix_inline(m):
    s = m.group(0)
    e = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', s)
    cx, cy = int(e.group(1)), int(e.group(2))
    k = min(MAXW / cx, MAXH / cy, 1.15)
    ncx, ncy = int(cx * k), int(cy * k)
    s = re.sub(r'(<wp:extent cx=")\d+(" cy=")\d+', r"\g<1>%d\g<2>%d" % (ncx, ncy), s)
    return re.sub(r'(<a:ext cx=")\d+(" cy=")\d+', r"\g<1>%d\g<2>%d" % (ncx, ncy), s)


def post(src, dst):
    zin = zipfile.ZipFile(src)
    doc = zin.read("word/document.xml").decode("utf8")
    sty = zin.read("word/styles.xml").decode("utf8")

    arial = '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Arial" />'
    sty = re.sub(r"<w:rFonts [^>]*Theme[^>]*/>", arial, sty)
    sty = re.sub(r'(<w:docDefaults>.*?<w:sz w:val=")\d+(" />\s*<w:szCs w:val=")\d+', r"\g<1>21\g<2>21", sty, flags=re.S)
    sty = re.sub(r"(<w:pPrDefault>\s*<w:pPr>\s*)<w:spacing [^>]*/>",
                 r'\1<w:spacing w:after="100" w:line="276" w:lineRule="auto" />', sty)
    sty = sty.replace('<w:wordWrap w:val="off" />', "")
    sty = re.sub(r'(w:styleId="BodyText".*?<w:spacing )w:after="\d+" w:before="\d+"',
                 r'\1w:after="100" w:before="100"', sty, count=1, flags=re.S)
    sty = re.sub(r'(w:styleId="VerbatimChar".*?<w:sz w:val=")\d+', r"\g<1>19", sty, count=1, flags=re.S)

    source_code_style = ('<w:style w:type="paragraph" w:customStyle="1" w:styleId="SourceCode">'
                         '<w:name w:val="Source Code" />'
                         '<w:basedOn w:val="Normal" />'
                         '<w:link w:val="VerbatimChar" />'
                         '<w:pPr>'
                         '<w:pBdr><w:left w:val="single" w:sz="18" w:space="12" w:color="3B82F6" /></w:pBdr>'
                         '<w:shd w:val="clear" w:color="auto" w:fill="F1F5F9" />'
                         '<w:ind w:left="240" w:right="240" />'
                         '<w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto" />'
                         '</w:pPr>'
                         '<w:rPr>'
                         '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" />'
                         '<w:color w:val="0F172A" />'
                         '<w:sz w:val="18" /><w:szCs w:val="18" />'
                         '</w:rPr>'
                         '</w:style>')
    sty = re.sub(r'<w:style[^>]*w:styleId="SourceCode".*?</w:style>', source_code_style, sty, flags=re.S)

    sty = sty.replace("</w:styles>",
                      '<w:style w:customStyle="1" w:styleId="TableText" w:type="paragraph"><w:name w:val="Table Text" />'
                      '<w:basedOn w:val="Normal" /><w:qFormat /><w:pPr><w:spacing w:after="30" w:before="30" '
                      'w:line="252" w:lineRule="auto" /></w:pPr><w:rPr><w:sz w:val="19" /><w:szCs w:val="19" /></w:rPr>'
                      "</w:style></w:styles>")

    pat = re.compile(r'<w:t xml:space="preserve">([^<]*?)%s([^<]*)</w:t>' % BR)
    while True:
        new = pat.sub(lambda m: '<w:t xml:space="preserve">%s</w:t><w:br /><w:t xml:space="preserve">%s</w:t>'
                      % (m.group(1), m.group(2)), doc)
        if new == doc:
            break
        doc = new

    doc = re.sub(r'(<w:pStyle w:val="Heading1" />)',
                 r'\1<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="6" w:color="0F4761" /></w:pBdr>', doc)
    doc = re.sub(r"<w:tbl>.*?</w:tbl>", fix_table, doc, flags=re.S)
    doc = re.sub(r"<wp:inline>.*?</wp:inline>", fix_inline, doc, flags=re.S)
    doc = re.sub(r'(<w:p><w:pPr><w:pStyle w:val="[^"]+" />)(</w:pPr><w:r><w:drawing>)', r"\1<w:keepNext />\2", doc)
    if "</w:footnotePr>" in doc:
        doc = doc.replace("</w:footnotePr>",
                          '</w:footnotePr><w:pgSz w:w="%d" w:h="%d" /><w:pgMar w:top="%d" w:right="%d" w:bottom="%d" '
                          'w:left="%d" w:header="567" w:footer="567" w:gutter="0" />'
                          % (PAGE_W, PAGE_H, MARG, MARG, MARG, MARG), 1)
    else:
        doc = re.sub(r"<w:sectPr[^>]*/>|<w:sectPr[^>]*>.*?</w:sectPr>",
                     '<w:sectPr><w:pgSz w:w="%d" w:h="%d" /><w:pgMar w:top="%d" w:right="%d" w:bottom="%d" '
                     'w:left="%d" w:header="567" w:footer="567" w:gutter="0" /></w:sectPr>'
                     % (PAGE_W, PAGE_H, MARG, MARG, MARG, MARG), doc, count=1, flags=re.S)

    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == "word/document.xml":
            data = doc.encode("utf8")
        elif it.filename == "word/styles.xml":
            data = sty.encode("utf8")
        zout.writestr(it, data)
    zout.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md")
    ap.add_argument("docx")
    a = ap.parse_args()
    md = os.path.abspath(a.md)
    out = os.path.abspath(a.docx)
    with tempfile.TemporaryDirectory() as tmp:
        prep = os.path.join(tmp, "prep.md")
        raw = os.path.join(tmp, "raw.docx")
        open(prep, "w", encoding="utf8").write(prep_md(open(md, encoding="utf8").read()))
        cmd = ["pandoc", "-f", "gfm", "-t", "docx", "--resource-path=" + os.path.dirname(md), "-o", raw, prep]
        if os.path.exists(REF):
            cmd.insert(5, "--reference-doc=" + REF)
        subprocess.run(cmd, check=True)
        post(raw, out)
    size = os.path.getsize(out) / 1048576
    print("Đã ghi %s (%.1f MB)" % (out, size))
    if size > 9.5:
        print("CẢNH BÁO: trên 9,5 MB. Google giới hạn xuất 10 MB và công cụ tải lên Chrome giới hạn 10 MB; "
              "nén ảnh PNG trước khi chuyển.")


if __name__ == "__main__":
    sys.exit(main())

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_receipt_pdf(
    invoice_number: str,
    issue_date: str,
    seller_name: str,
    seller_address: str,
    seller_nip: str | None,
    description: str,
    amount: float,
) -> bytes:
    """Generate a PDF receipt and return bytes."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    y = height - 20 * mm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, y, seller_name)
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, y - 6 * mm, seller_address)
    if seller_nip:
        c.drawString(20 * mm, y - 10 * mm, f"NIP: {seller_nip}")

    # Receipt number
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y - 20 * mm, f"Paragon: {invoice_number}")
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, y - 24 * mm, f"data wystawienia: {issue_date}")

    # Divider
    c.line(20 * mm, y - 30 * mm, width - 20 * mm, y - 30 * mm)

    # Item
    item_y = y - 36 * mm
    c.drawString(20 * mm, item_y, description)
    c.drawString(60 * mm, item_y, "1 szt.")
    c.drawRightString(width - 20 * mm, item_y, f"{amount:.2f} PLN")

    # Divider
    c.line(20 * mm, item_y - 6 * mm, width - 20 * mm, item_y - 6 * mm)

    # Total
    total_y = item_y - 14 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, total_y, "RAZEM:")
    c.drawRightString(width - 20 * mm, total_y, f"{amount:.2f} PLN")

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(20 * mm, 20 * mm, "Sprzedaż nierejestrowana — paragon bez NIP nabywcy")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

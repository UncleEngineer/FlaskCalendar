from flask import Flask, render_template, request, send_file
import calendar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# Function to generate calendar PDF

def generate_calendar_pdf(year, month):
    # Ensure directory exists
    save_dir = os.path.join(os.getcwd(), "generated_pdfs")
    os.makedirs(save_dir, exist_ok=True)

    # Define full path
    filename = f"calendar_{year}_{month}.pdf"
    file_path = os.path.join(save_dir, filename)

    # Page settings
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter  # 8.5 x 11 inches (612 x 792 pixels)

    # Title
    title = f"{calendar.month_name[month]} {year}"
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, title)

    # Calendar data
    cal = calendar.monthcalendar(year, month)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Full-page table settings
    margin_x = 50
    margin_y = 80  # Space for title
    table_width = width - (2 * margin_x)
    table_height = height - (margin_y + 50)  # 50px bottom margin

    rows = len(cal) + 1  # Number of rows (weeks + header)
    cols = 7  # 7 days in a week

    cell_width = table_width / cols
    cell_height = table_height / rows

    # Draw table border
    c.rect(margin_x, height - margin_y - table_height, table_width, table_height)

    # Draw vertical lines (columns)
    for i in range(cols + 1):
        x_pos = margin_x + (i * cell_width)
        c.line(x_pos, height - margin_y, x_pos, height - margin_y - table_height)

    # Draw horizontal lines (rows)
    for i in range(rows + 1):
        y_pos = height - margin_y - (i * cell_height)
        c.line(margin_x, y_pos, margin_x + table_width, y_pos)

    # Set font for table headers
    c.setFont("Helvetica-Bold", 14)

    # Draw the day headers
    for i, day in enumerate(days):
        c.drawCentredString(margin_x + (i * cell_width) + (cell_width / 2), 
                            height - margin_y - (cell_height / 2) + 5, day)

    # Set font for numbers
    c.setFont("Helvetica", 12)

    # Fill in the calendar days (Top-Right Corner)
    y_offset = height - margin_y - cell_height * 1.1  # Start below headers
    for week in cal:
        for i, day in enumerate(week):
            if day != 0:
                c.drawString(margin_x + ((i + 1) * cell_width) - 15,  # Right-aligned
                             y_offset - 15,  # Top padding
                             str(day))
        y_offset -= cell_height

    # Save the PDF
    c.save()

    return file_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        year = int(request.form["year"])
        month = int(request.form["month"])

        # Generate calendar PDF and get the correct path
        file_path = generate_calendar_pdf(year, month)

        # Return file as an attachment
        return send_file(file_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
import os
from datetime import datetime

def create_yearly_pdf(filename, details, dasha_data):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph(f"<b><font size=16>Yearly Prediction Report</font></b><br/><font size=10>Based on Vimshottari Dasha</font>", styles['Normal'])
    story.append(title)
    story.append(Spacer(1, 0.3*inch))
    
    # Birth Details
    story.append(Paragraph("<b>Birth Details</b>", styles['Heading2']))
    birth_details = [
        ["Name", details.get("name", "User")],
        ["Birth Date", details.get("dob")],
        ["Birth Time", details.get("time")],
        ["Birth Place", f"{details.get('lat')}, {details.get('lon')}"],
        ["Report Year", datetime.now().strftime("%Y")]
    ]
    t = Table(birth_details, colWidths=[2*inch, 3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*inch))
    
    # Active Dasha Periods
    story.append(Paragraph("<b>Active Dasha Periods (Next 12 Months)</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    dasha_table_data = [
        ["Maha Dasha", "Antar Dasha", "Start Date", "End Date"]
    ]
    
    # We expect dasha_data to be a list of periods active within the next year.
    for period in dasha_data:
        dasha_table_data.append([
            period.get("maha_dasha", ""),
            period.get("antar_dasha", ""),
            period.get("start_date", ""),
            period.get("end_date", "")
        ])
        
    if len(dasha_table_data) == 1:
        dasha_table_data.append(["No data available", "", "", ""])
        
    t2 = Table(dasha_table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.beige),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.4*inch))
    
    # General Predictions based on Dasha
    story.append(Paragraph("<b>Yearly Outlook</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    # We will pick the main Maha Dasha from the first element
    if dasha_data:
        current_maha = dasha_data[0].get("maha_dasha", "")
        current_antar = dasha_data[0].get("antar_dasha", "")
        
        outlook_text = f"The year begins under the major influence (Maha Dasha) of <b>{current_maha}</b> and the minor influence (Antar Dasha) of <b>{current_antar}</b>. "
        
        # Simple generic mapping for demonstration. Real astrology logic would be complex.
        planet_traits = {
            "Sun": "This period brings focus on career, authority, and health.",
            "Moon": "This period emphasizes emotional well-being, travel, and family.",
            "Mars": "Expect high energy, ambition, and potential conflicts. Drive towards your goals.",
            "Rahu": "Sudden changes, material desires, and foreign connections are highlighted.",
            "Jupiter": "A time of growth, wisdom, financial expansion, and spiritual learning.",
            "Saturn": "Hard work, discipline, delays, and long-term achievements are the theme.",
            "Mercury": "Focus on communication, learning, business, and intellect.",
            "Ketu": "Spiritual growth, detachment, and resolving past karmas.",
            "Venus": "Romance, luxury, arts, and relationship harmony are favored."
        }
        
        outlook_text += planet_traits.get(current_maha, "This is a transformative period.")
        
        story.append(Paragraph(outlook_text, styles['Normal']))
    else:
        story.append(Paragraph("Dasha information not available.", styles['Normal']))
    
    doc.build(story)

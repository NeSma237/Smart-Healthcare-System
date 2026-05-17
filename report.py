from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
def build_report(plot_path, results_summary, output="report.pdf"):
    doc    = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()
    story  = []
    # Title
    story.append(Paragraph("Game Theory — Smart Healthcare System",
                            styles["Title"]))
    story.append(Spacer(1, 12))
    # Section 1
    story.append(Paragraph("1. Introduction", styles["Heading1"]))
    story.append(Paragraph(
        "This project applies game theory to model strategic interaction "
        "between a Hospital and Insurance Company...",
        styles["Normal"]))
    # Insert plots
    story.append(Paragraph("5. Simulation Results", styles["Heading1"]))
    story.append(Image(plot_path, width=450, height=270))
    # Build
    doc.build(story)
    print(f"Report saved -> {output}")
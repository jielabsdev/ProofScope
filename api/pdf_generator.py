from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_audit_pdf(data: dict, output_path: str) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    c = canvas.Canvas(output_path, pagesize=letter)
    
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.rect(50, 730, 512, 40, fill=True, stroke=False)
    
    c.setFillColorRGB(1.0, 1.0, 1.0)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(70, 742, "ProofScope Certificate of Verification")
    
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, 690, "Audit Telemetry Profile Summary")
    
    c.setFont("Helvetica", 10)
    line_y = 670
    metrics_map = [
        ("Report Reference ID:", str(data.get("id"))),
        ("Timestamp (UTC):", str(data.get("timestamp"))),
        ("Verification Outcome:", str(data.get("status"))),
        ("Diagnostic Tracker Code:", str(data.get("error_code", "SUCCESS"))),
        ("Model Version Target:", str(data.get("model_version", "unknown"))),
        ("Confidence Score Weight:", f"{(float(data.get('confidence_score', 0.0)) * 100):.2f}%"),
        ("Circuit Constraint Load:", f"{(float(data.get('constraint_utilization', 0.0)) * 100):.2f}%"),
        ("Engine Latency Duration:", f"{float(data.get('execution_time_ms', 0.0)):.2f} ms"),
        ("Circuit Complexity:", f"{int(data.get('gate_count', 0)):,} gates (Depth: {int(data.get('circuit_depth', 0))})"),
    ]
    
    for label, val in metrics_map:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(70, line_y, label)
        c.setFont("Helvetica", 10)
        c.drawString(240, line_y, val)
        line_y -= 18
        
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(0.5)
    c.line(50, line_y - 10, 562, line_y - 10)
    
    line_y -= 30
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, line_y, "Cryptographic Append-Only Ledger Anchors")
    
    line_y -= 20
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(70, line_y, "Parent Block (Prev Record Hash):")
    c.setFont("Courier", 9)
    c.drawString(70, line_y - 12, str(data.get("prev_record_hash")))
    
    line_y -= 35
    c.setFont("Helvetica-Bold", 10)
    c.drawString(70, line_y, "Current Block Signature (Record Hash):")
    c.setFont("Courier", 9)
    c.drawString(70, line_y - 12, str(data.get("record_hash")))
    
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawRightString(562, 40, "Generated automatically via pybind11 C++ Engine & ProofScope Trust-Layer.")
    
    c.save()
    return output_path

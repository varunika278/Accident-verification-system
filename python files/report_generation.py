from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import textwrap

def read_status_report(filename="status_report.txt"):
    drowsy = False
    cause = "unknown"
    accident = False
    
    # Create a dictionary to store the latest values
    latest_values = {}
    
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
                
            # Check if the line contains the expected delimiter
            if ": " not in line:
                continue
                
            parts = line.split(": ", 1)  # Split only on the first occurrence of ": "
            if len(parts) < 2:
                continue
                
            key, value = parts
            
            # Store the latest value for each key
            if key in ["Drowsiness", "Cause of drowsiness", "Accident"]:
                latest_values[key] = value
    
    # Now extract the values we need from the latest values
    if "Drowsiness" in latest_values:
        drowsy = (latest_values["Drowsiness"] == "drowsy")
        
    if "Cause of drowsiness" in latest_values:
        cause = latest_values["Cause of drowsiness"].lower()
        
    if "Accident" in latest_values:
        accident = (latest_values["Accident"] == "accident")
    
    return drowsy, cause, accident

def update_status_report(filename, claim_status):
    with open(filename, "a") as file:
        file.write(f"Insurance Status: {claim_status}\n")

def wrap_text(text, width=80):
    return textwrap.wrap(text, width)

def generate_insurance_report(drowsy, cause, accident, output_filename="insurance_report.pdf"):
    print("Generating report.......")
    
    # Determine claim eligibility
    if cause == "alcohol":
        claim_status = "Rejected"
        reason = "The driver was under the influence of alcohol, which violates insurance policies."
    elif cause == "both":
        claim_status = "Rejected"
        reason = "The insurance claim is rejected because, although drowsiness was influenced by the car’s internal environment, the driver had also consumed alcohol. Driving under the influence of alcohol is a direct violation of insurance policies, regardless of other contributing factors. Insurance policies do not cover accidents where alcohol consumption is involved, as it is considered negligent and preventable behavior."
    elif cause == "environment":
        claim_status = "Approved"
        reason = "The driver was naturally fatigued or affected by environmental factors beyond their control."
    else:
        claim_status = "Approved"
        reason = "No signs of intoxication were detected, and the accident was unavoidable."
    
    # Create PDF
    c = canvas.Canvas(output_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Insurance Claim Report")
    c.setFont("Helvetica", 12)
    
    if cause == "both":
        cause_text = "Consumption of alcohol and Car Internal Environment/Medical condition"
    elif cause == "environment":
        cause_text = "Car Internal Environment/Medical condition"
    elif cause == "alcohol":
        cause_text = "Consumption of alcohol"
    elif cause == "none":
        cause_text = "Medical condition"

    # Add text with proper spacing
    y_position = 700  # Start Y position
    line_spacing = 20  # Spacing between lines

    c.drawString(50, y_position, f"Drowsiness Detected: {'Yes' if drowsy else 'No'}")
    y_position -= line_spacing

    c.drawString(50, y_position, "Cause of Drowsiness:")
    y_position -= line_spacing

    # Wrap and write cause text
    wrapped_cause = wrap_text(cause_text, 60)
    for line in wrapped_cause:
        c.drawString(70, y_position, line)
        y_position -= line_spacing

    c.drawString(50, y_position, f"Accident Occurred: {'Yes' if accident else 'No'}")
    y_position -= line_spacing * 2

    # Claim Status
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, f"Claim Status: {claim_status}")
    y_position -= line_spacing

    c.setFont("Helvetica", 12)
    c.drawString(50, y_position, "Reason:")
    y_position -= line_spacing

    # Wrap and write the reason text
    wrapped_reason = wrap_text(reason, 80)
    for line in wrapped_reason:
        c.drawString(70, y_position, line)
        y_position -= line_spacing

    # Save PDF
    c.save()
    
    # Update status_report.txt
    update_status_report("status_report.txt", claim_status)
    print("\nReport generated")

# Read values from status_report.txt
drowsy, cause, accident = read_status_report()

# Generate report using extracted values
generate_insurance_report(drowsy, cause, accident)

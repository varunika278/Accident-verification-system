# Accident Verification System

This project is an integrated system for detecting driver drowsiness, accident events, and air quality, with automated reporting and insurance claim management.

## Project Structure

```
accident detection/
    accident_model_architecture.json
    accident_model_weights.weights.h5
    accident_model.h5
accident frames/
dataset/
    dataset.docx
    final_dataset.csv
    Gas_Sensors_Measurements.csv
    iot_telemetry_data.csv
drowsiness detection/
    drowsiness_model_architecture.json
    drowsiness_model_weights.weights.h5
    drowsiness_model.h5
drowsiness frames/
python files/
    accident_demo.py
    air_check.py
    app.ipynb
    drowsy_demo.py
    drowsyV2I.py
    insurance.py
    report_generation.py
    run.bat
sample videos/
```

## Main Components

- **Drowsiness Detection:** Uses a trained model to detect driver drowsiness from video frames ([drowsy_demo.py](python%20files/drowsy_demo.py)).
- **Accident Detection:** Detects accidents using a separate model ([accident_demo.py](python%20files/accident_demo.py)).
- **Air Quality Check:** Monitors air quality data ([air_check.py](python%20files/air_check.py)).
- **Insurance Claim Management:** Handles insurance claim logic and database storage ([insurance.py](python%20files/insurance.py)).
- **Report Generation:** Generates PDF reports based on detection results ([report_generation.py](python%20files/report_generation.py)).
- **Batch Execution:** The [run.bat](python%20files/run.bat) script runs all main modules in sequence.

## How to Run

1. Ensure you have Python and required dependencies installed.
2. Place your input data (frames, sensor data) in the appropriate folders.
3. Run the batch script:

    ```sh
    cd "python files"
    run.bat
    ```

   This will execute all detection modules and generate reports.

## Requirements

- Python 3.x
- TensorFlow/Keras (for model loading)
- MySQL (for insurance claim database)
- reportlab (for PDF generation)
- Other dependencies as required by the scripts

## Outputs

- **status_report.txt:** Logs detection results.
- **insurance_report.pdf:** Generated insurance report.
- **Database:** Stores insurance claim data.

## Notes

- Update email credentials and database settings in the scripts as needed.
- Models and data files must be present in their respective folders.

---

*For more details, refer to the code in the [python files/](python%20files/)

# Urine Test Analysis Feature

## Overview
The Medical Report Analyzer now supports comprehensive urine test (urinalysis) analysis in addition to blood tests. This feature can extract, analyze, and provide insights on various urine parameters from uploaded medical reports.

## Supported Urine Test Parameters

### Physical Properties
- **pH** (4.5-8.0): Measures acidity/alkalinity of urine
- **Specific Gravity** (1.005-1.030): Indicates urine concentration

### Chemical Analysis
- **Protein** (Negative): Detects kidney damage or disease
- **Glucose** (Negative): Screens for diabetes
- **Ketones** (Negative): Indicates metabolic state
- **Blood** (Negative): Detects kidney stones, infection, or disease
- **Bilirubin** (Negative): Indicates liver function
- **Urobilinogen** (0.1-1.0 mg/dL): Liver and hemolysis marker
- **Nitrite** (Negative): Bacterial infection indicator
- **Leukocyte Esterase** (Negative): White blood cell indicator

### Microscopic Examination
- **WBC/Pus Cells** (0-5 cells/hpf): Infection indicator
- **RBC** (0-3 cells/hpf): Blood in urine
- **Epithelial Cells** (0-5 cells/hpf): Contamination or infection
- **Bacteria** (Negative): Infection indicator
- **Crystals** (Negative): Kidney stone risk
- **Casts** (Negative): Kidney disease indicator

## How to Use

### 1. Upload Urine Test Report
- Upload a clear image (PNG, JPG) or PDF of your urine test report
- The OCR system will automatically extract the values
- Supported formats: Lab reports, hospital reports, home test results

### 2. View Analysis
The system will provide:
- **Comparison with normal ranges**: Each parameter is compared to reference values
- **Status indicators**: Normal (green), High (red), Low (blue)
- **Visual charts**: Interactive graphs showing your results
- **Health insights**: Personalized recommendations based on your results

### 3. Ask the AI Chatbot
You can ask questions like:
- "What is a urine test?"
- "What does protein in urine mean?"
- "Why is there blood in my urine?"
- "What causes a urinary tract infection?"
- "How to improve urinary health?"
- "What is normal urine pH?"

## Common Conditions Detected

### Urinary Tract Infection (UTI)
**Indicators:**
- Elevated WBC/pus cells
- Bacteria present
- Positive nitrite
- Positive leukocyte esterase
- May have blood

**Recommendations:**
- Consult doctor for antibiotics
- Drink plenty of water
- Cranberry juice may help
- Complete full antibiotic course

### Kidney Disease
**Indicators:**
- Protein in urine (proteinuria)
- Blood in urine (hematuria)
- Abnormal pH
- Casts present
- Elevated creatinine (blood test)

**Recommendations:**
- Immediate medical consultation
- Kidney function tests
- Monitor blood pressure
- Control blood sugar if diabetic

### Diabetes
**Indicators:**
- Glucose in urine
- Ketones in urine
- High blood glucose (blood test)

**Recommendations:**
- Blood sugar monitoring
- HbA1c test
- Dietary changes
- Medical consultation

### Kidney Stones
**Indicators:**
- Blood in urine
- Crystals present
- Abnormal pH
- Severe pain (clinical symptom)

**Recommendations:**
- Drink plenty of water (8-10 glasses daily)
- Limit sodium and protein
- Medical imaging may be needed
- Pain management

### Dehydration
**Indicators:**
- High specific gravity (>1.030)
- Concentrated urine
- Dark color (clinical observation)

**Recommendations:**
- Increase water intake immediately
- Drink 8-10 glasses daily
- Monitor urine color (should be pale yellow)

## Health Tips for Urinary System

### Prevention
- Drink 8-10 glasses of water daily
- Urinate when you feel the urge
- Urinate after sexual activity
- Maintain good hygiene
- Wear breathable cotton underwear
- Avoid holding urine for long periods

### Foods for Urinary Health
- **Good:** Water, cranberries, blueberries, watermelon, celery, parsley, garlic, probiotics
- **Limit:** Caffeine, alcohol, spicy foods, artificial sweeteners, high-sodium foods

### When to See a Doctor
- Blood in urine
- Painful urination
- Frequent urination with little output
- Fever with urinary symptoms
- Back or side pain
- Cloudy or foul-smelling urine
- Protein or glucose in urine

## Technical Details

### OCR Recognition
The system uses enhanced OCR patterns to recognize urine test parameters even with:
- Messy handwriting
- Poor image quality
- Various report formats
- Different terminology (e.g., "pus cells" vs "WBC")

### Reference Data
All urine test parameters are stored in `reference_data.csv` with:
- Normal ranges
- Units of measurement
- Descriptions
- Clinical significance

### AI Chatbot Knowledge
The chatbot has comprehensive knowledge about:
- Urine test basics
- Protein in urine (proteinuria)
- Blood in urine (hematuria)
- Urinary tract infections
- pH balance
- Kidney health
- Prevention and treatment

## Example Questions for the Chatbot

### General Information
- "What is a urine test?"
- "What does urinalysis check for?"
- "How often should I get a urine test?"

### Specific Parameters
- "What does protein in urine mean?"
- "Why is there blood in my urine?"
- "What is normal urine pH?"
- "What is specific gravity?"

### Health Concerns
- "Do I have a urinary tract infection?"
- "What causes kidney stones?"
- "How to prevent UTIs?"
- "What foods are good for kidney health?"

### Results Interpretation
- "Tell me about my urine test results"
- "Why is my urine pH high?"
- "What does it mean if I have WBC in urine?"
- "Should I be worried about my results?"

## Visualization Features

The system provides multiple chart types for urine test results:
1. **Bar Chart**: Overview of all parameters
2. **Gauge Charts**: Individual parameter status
3. **Status Distribution**: Pie chart of normal vs abnormal
4. **Radar Chart**: Multi-parameter comparison
5. **Trend Analysis**: Historical comparison (simulated)

## Integration with Blood Tests

The system can analyze both blood and urine tests simultaneously:
- Upload multiple reports
- Get comprehensive health overview
- Correlate findings (e.g., glucose in blood and urine)
- Holistic health insights

## Notes

- Always consult a healthcare professional for medical advice
- This tool is for educational and informational purposes
- Abnormal results should be discussed with your doctor
- Follow-up testing may be needed for confirmation
- Keep track of your test results over time

## Future Enhancements

Planned features:
- Stool test analysis
- Hormone panel analysis
- Thyroid function tests
- Liver function tests
- Kidney function panel
- Complete metabolic panel

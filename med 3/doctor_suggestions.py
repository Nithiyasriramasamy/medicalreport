"""
Doctor Suggestion System
Provides specialist recommendations based on test results
"""

def get_specialist_recommendations(comparison_results):
    """
    Analyze test results and recommend appropriate medical specialists
    """
    recommendations = {
        'specialists': [],
        'urgency': 'routine',
        'reasons': [],
        'next_steps': []
    }
    
    # Track which specialists are needed
    specialist_scores = {}
    urgent_conditions = []
    
    for result in comparison_results:
        test = result['test']
        status = result['status']
        value = result['value']
        
        if status == 'Normal':
            continue
            
        # Cardiologist - Heart conditions
        if test in ['Troponin', 'BNP', 'NT_proBNP', 'CK_MB', 'Cholesterol', 'LDL', 'HDL', 'Triglycerides']:
            specialist_scores['Cardiologist'] = specialist_scores.get('Cardiologist', 0) + 1
            if test == 'Troponin' and status == 'High':
                urgent_conditions.append('Possible heart attack - EMERGENCY')
                recommendations['urgency'] = 'emergency'
            elif test in ['BNP', 'NT_proBNP'] and status == 'High':
                recommendations['reasons'].append('Elevated heart failure markers')
            elif test in ['Cholesterol', 'LDL', 'Triglycerides'] and status == 'High':
                recommendations['reasons'].append('High cardiovascular risk factors')
        
        # Nephrologist - Kidney specialist
        if test in ['Creatinine', 'BUN', 'Urea', 'Urine_Protein', 'Urine_Blood', 'Potassium']:
            specialist_scores['Nephrologist'] = specialist_scores.get('Nephrologist', 0) + 1
            if test == 'Urine_Protein' and status == 'High':
                recommendations['reasons'].append('Protein in urine - possible kidney disease')
            elif test in ['Creatinine', 'BUN'] and status == 'High':
                recommendations['reasons'].append('Elevated kidney function markers')
        
        # Endocrinologist - Hormones and metabolism
        if test in ['TSH', 'T3', 'T4', 'Free_T3', 'Free_T4', 'HbA1c', 'Glucose', 'Insulin', 
                    'Testosterone_Total', 'Estradiol', 'Cortisol', 'DHEA_S']:
            specialist_scores['Endocrinologist'] = specialist_scores.get('Endocrinologist', 0) + 1
            if test == 'HbA1c' and value > 6.5:
                recommendations['reasons'].append('Diabetes diagnosis - needs management')
            elif test in ['TSH', 'T3', 'T4'] and status != 'Normal':
                recommendations['reasons'].append('Thyroid dysfunction detected')
            elif test in ['Testosterone_Total', 'Estradiol'] and status != 'Normal':
                recommendations['reasons'].append('Hormonal imbalance detected')
        
        # Hepatologist/Gastroenterologist - Liver specialist
        if test in ['ALT', 'AST', 'Alkaline_Phosphatase', 'GGT', 'Total_Bilirubin', 
                    'Direct_Bilirubin', 'Albumin', 'Total_Protein']:
            specialist_scores['Hepatologist'] = specialist_scores.get('Hepatologist', 0) + 1
            if test in ['ALT', 'AST'] and value > 100:
                recommendations['reasons'].append('Significantly elevated liver enzymes')
            elif test == 'Total_Bilirubin' and status == 'High':
                recommendations['reasons'].append('Elevated bilirubin - possible liver/bile duct issue')
        
        # Hematologist - Blood disorders
        if test in ['Hemoglobin', 'WBC', 'RBC', 'Platelets', 'Ferritin', 'Iron', 'TIBC',
                    'MCV', 'MCH', 'MCHC', 'RDW']:
            if status != 'Normal':
                specialist_scores['Hematologist'] = specialist_scores.get('Hematologist', 0) + 1
                if test == 'Hemoglobin' and value < 8:
                    recommendations['reasons'].append('Severe anemia - needs urgent evaluation')
                    recommendations['urgency'] = 'urgent'
                elif test == 'WBC' and (value < 2000 or value > 20000):
                    recommendations['reasons'].append('Abnormal white blood cell count')
                elif test == 'Platelets' and value < 50000:
                    recommendations['reasons'].append('Low platelet count - bleeding risk')
                    recommendations['urgency'] = 'urgent'
        
        # Urologist - Urinary system
        if test in ['PSA', 'Urine_WBC', 'Urine_RBC', 'Urine_Bacteria', 'Urine_Nitrite']:
            specialist_scores['Urologist'] = specialist_scores.get('Urologist', 0) + 1
            if test == 'PSA' and value > 4:
                recommendations['reasons'].append('Elevated PSA - prostate evaluation needed')
            elif test in ['Urine_WBC', 'Urine_Bacteria'] and status == 'High':
                recommendations['reasons'].append('Urinary tract infection detected')
        
        # Rheumatologist - Inflammation and autoimmune
        if test in ['CRP', 'ESR', 'Uric_Acid']:
            if status == 'High':
                specialist_scores['Rheumatologist'] = specialist_scores.get('Rheumatologist', 0) + 1
                if test == 'Uric_Acid' and value > 8:
                    recommendations['reasons'].append('High uric acid - gout risk')
                elif test in ['CRP', 'ESR']:
                    recommendations['reasons'].append('Elevated inflammation markers')
        
        # Oncologist - Cancer markers
        if test in ['CEA', 'CA_125', 'CA_19_9', 'AFP', 'PSA']:
            if status == 'High':
                specialist_scores['Oncologist'] = specialist_scores.get('Oncologist', 0) + 1
                recommendations['reasons'].append(f'Elevated tumor marker: {test}')
                recommendations['urgency'] = 'urgent'
    
    # Sort specialists by score and add top recommendations
    sorted_specialists = sorted(specialist_scores.items(), key=lambda x: x[1], reverse=True)
    
    for specialist, score in sorted_specialists[:3]:  # Top 3 specialists
        recommendations['specialists'].append({
            'name': specialist,
            'priority': 'High' if score >= 3 else 'Medium' if score >= 2 else 'Low',
            'reason_count': score
        })
    
    # Add next steps based on urgency
    if recommendations['urgency'] == 'emergency':
        recommendations['next_steps'] = [
            '🚨 SEEK EMERGENCY MEDICAL CARE IMMEDIATELY',
            'Call emergency services or go to nearest ER',
            'Do not wait for an appointment',
            'Bring all test results with you'
        ]
    elif recommendations['urgency'] == 'urgent':
        recommendations['next_steps'] = [
            '⚠️ Schedule appointment within 24-48 hours',
            'Contact your primary care physician immediately',
            'Explain your test results',
            'Request urgent specialist referral if needed'
        ]
    else:
        recommendations['next_steps'] = [
            '📅 Schedule appointment within 1-2 weeks',
            'Discuss results with your doctor',
            'Get specialist referral if recommended',
            'Follow up on any abnormal findings'
        ]
    
    # Add general recommendations
    if not recommendations['specialists']:
        recommendations['specialists'].append({
            'name': 'Primary Care Physician',
            'priority': 'Medium',
            'reason_count': 1
        })
        recommendations['reasons'].append('General health consultation recommended')
    
    # Add urgent conditions to reasons
    if urgent_conditions:
        recommendations['reasons'] = urgent_conditions + recommendations['reasons']
    
    return recommendations


def get_doctor_search_keywords(specialists):
    """
    Generate search keywords for finding doctors
    """
    keywords = []
    
    specialist_keywords = {
        'Cardiologist': ['cardiologist', 'heart doctor', 'cardiovascular specialist'],
        'Nephrologist': ['nephrologist', 'kidney specialist', 'renal doctor'],
        'Endocrinologist': ['endocrinologist', 'diabetes doctor', 'hormone specialist', 'thyroid doctor'],
        'Hepatologist': ['hepatologist', 'liver specialist', 'gastroenterologist'],
        'Hematologist': ['hematologist', 'blood specialist', 'blood disorder doctor'],
        'Urologist': ['urologist', 'urinary specialist', 'prostate doctor'],
        'Rheumatologist': ['rheumatologist', 'arthritis doctor', 'autoimmune specialist'],
        'Oncologist': ['oncologist', 'cancer specialist', 'cancer doctor'],
        'Primary Care Physician': ['primary care', 'general practitioner', 'family doctor', 'GP']
    }
    
    for specialist_info in specialists:
        specialist_name = specialist_info['name']
        if specialist_name in specialist_keywords:
            keywords.extend(specialist_keywords[specialist_name])
    
    return list(set(keywords))  # Remove duplicates


def generate_doctor_finder_url(specialist_name, location=''):
    """
    Generate URLs for finding doctors online
    """
    urls = {
        'google': f"https://www.google.com/search?q={specialist_name}+near+{location}",
        'healthgrades': f"https://www.healthgrades.com/search?what={specialist_name}&where={location}",
        'zocdoc': f"https://www.zocdoc.com/search/?dr_specialty=&insurance_carrier=&search_query={specialist_name}&address={location}",
        'vitals': f"https://www.vitals.com/search?type=specialty&q={specialist_name}&loc={location}"
    }
    
    return urls


def get_health_tips_by_condition(test_results):
    """
    Provide health tips based on specific conditions detected
    """
    tips = []
    
    conditions_detected = set()
    
    for result in test_results:
        test = result['test']
        status = result['status']
        
        if status == 'Normal':
            continue
        
        # Detect conditions
        if test in ['Cholesterol', 'LDL', 'Triglycerides'] and status == 'High':
            conditions_detected.add('high_cholesterol')
        
        if test in ['Glucose', 'HbA1c'] and status == 'High':
            conditions_detected.add('diabetes')
        
        if test in ['Creatinine', 'BUN', 'Urine_Protein'] and status == 'High':
            conditions_detected.add('kidney_issues')
        
        if test in ['ALT', 'AST', 'GGT'] and status == 'High':
            conditions_detected.add('liver_issues')
        
        if test == 'Hemoglobin' and status == 'Low':
            conditions_detected.add('anemia')
        
        if test in ['TSH', 'T4'] and status != 'Normal':
            conditions_detected.add('thyroid_issues')
        
        if test in ['Urine_WBC', 'Urine_Bacteria'] and status == 'High':
            conditions_detected.add('uti')
    
    # Generate tips for each condition
    condition_tips = {
        'high_cholesterol': {
            'title': '💛 Managing High Cholesterol',
            'tips': [
                'Eat more fiber: oats, beans, fruits, vegetables',
                'Choose healthy fats: olive oil, avocados, nuts',
                'Limit saturated fats: red meat, butter, cheese',
                'Exercise 30 minutes daily',
                'Maintain healthy weight',
                'Consider plant sterols supplements',
                'Quit smoking if applicable'
            ]
        },
        'diabetes': {
            'title': '🍬 Managing Blood Sugar',
            'tips': [
                'Monitor blood sugar regularly',
                'Eat low glycemic index foods',
                'Control portion sizes',
                'Exercise regularly (150 min/week)',
                'Stay hydrated with water',
                'Avoid sugary drinks and processed foods',
                'Take medications as prescribed',
                'Check feet daily for wounds'
            ]
        },
        'kidney_issues': {
            'title': '🫘 Protecting Your Kidneys',
            'tips': [
                'Drink plenty of water (8-10 glasses daily)',
                'Limit sodium intake (<2,300mg/day)',
                'Control blood pressure',
                'Manage blood sugar if diabetic',
                'Avoid NSAIDs (ibuprofen, aspirin)',
                'Limit protein if advised by doctor',
                'Monitor kidney function regularly'
            ]
        },
        'liver_issues': {
            'title': '🧪 Supporting Liver Health',
            'tips': [
                'Avoid alcohol completely',
                'Maintain healthy weight',
                'Eat liver-friendly foods: leafy greens, berries',
                'Avoid processed foods and excess sugar',
                'Stay hydrated',
                'Avoid unnecessary medications',
                'Get vaccinated for hepatitis A & B',
                'Exercise regularly'
            ]
        },
        'anemia': {
            'title': '🔴 Treating Anemia',
            'tips': [
                'Eat iron-rich foods: red meat, spinach, beans',
                'Take vitamin C with iron for better absorption',
                'Avoid tea/coffee with meals',
                'Consider iron supplements (consult doctor)',
                'Eat vitamin B12: eggs, dairy, fish',
                'Include folate: leafy greens, citrus',
                'Cook in cast iron cookware'
            ]
        },
        'thyroid_issues': {
            'title': '🦋 Managing Thyroid Health',
            'tips': [
                'Take thyroid medication as prescribed',
                'Take medication on empty stomach',
                'Avoid soy products near medication time',
                'Get adequate iodine (but not excessive)',
                'Manage stress levels',
                'Get regular thyroid function tests',
                'Maintain healthy weight'
            ]
        },
        'uti': {
            'title': '💧 Treating UTI',
            'tips': [
                'Drink plenty of water (flush bacteria)',
                'Urinate frequently, don\'t hold it',
                'Take full course of antibiotics',
                'Drink cranberry juice (unsweetened)',
                'Avoid irritants: caffeine, alcohol, spicy foods',
                'Wipe front to back (women)',
                'Urinate after sexual activity',
                'Wear cotton underwear'
            ]
        }
    }
    
    for condition in conditions_detected:
        if condition in condition_tips:
            tips.append(condition_tips[condition])
    
    return tips

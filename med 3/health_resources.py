"""
Health Resources and Information
Provides health tips, news, and educational content
"""

import requests
from datetime import datetime

def get_health_news():
    """
    Get latest health news (simulated - can be replaced with real API)
    """
    # In production, you would use a real news API like NewsAPI
    # For now, providing curated health news topics
    
    health_news = [
        {
            'title': 'New Study Shows Benefits of Mediterranean Diet for Heart Health',
            'summary': 'Recent research confirms that Mediterranean diet reduces cardiovascular disease risk by 30%.',
            'category': 'Nutrition',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Medical Journal',
            'relevance': ['Cholesterol', 'Heart Health', 'Triglycerides']
        },
        {
            'title': 'Vitamin D Deficiency Linked to Immune Function',
            'summary': 'Studies show adequate vitamin D levels are crucial for immune system health.',
            'category': 'Vitamins',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Health Research',
            'relevance': ['Vitamin D', 'Immunity', 'Bone Health']
        },
        {
            'title': 'Early Detection of Kidney Disease Through Regular Testing',
            'summary': 'Regular monitoring of creatinine and protein levels can detect kidney disease early.',
            'category': 'Kidney Health',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Nephrology Today',
            'relevance': ['Creatinine', 'Kidney Function', 'Urine Protein']
        },
        {
            'title': 'Managing Diabetes: Latest Guidelines for HbA1c Targets',
            'summary': 'New recommendations suggest personalized HbA1c targets based on individual factors.',
            'category': 'Diabetes',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Diabetes Association',
            'relevance': ['HbA1c', 'Glucose', 'Diabetes']
        },
        {
            'title': 'Thyroid Health: Understanding TSH Levels',
            'summary': 'Comprehensive guide to interpreting thyroid function tests and when to seek treatment.',
            'category': 'Endocrinology',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Endocrine Society',
            'relevance': ['TSH', 'Thyroid', 'T3', 'T4']
        }
    ]
    
    return health_news


def get_relevant_news(test_results):
    """
    Filter health news based on user's test results
    """
    all_news = get_health_news()
    relevant_news = []
    
    # Get list of abnormal tests
    abnormal_tests = [result['test'] for result in test_results if result['status'] != 'Normal']
    
    for news in all_news:
        # Check if news is relevant to any abnormal test
        for test in abnormal_tests:
            if any(keyword.lower() in test.lower() or test.lower() in keyword.lower() 
                   for keyword in news['relevance']):
                relevant_news.append(news)
                break
    
    return relevant_news if relevant_news else all_news[:3]


def get_preventive_health_tips():
    """
    General preventive health tips
    """
    tips = {
        'daily_habits': {
            'title': '🌟 Daily Health Habits',
            'tips': [
                'Drink 8-10 glasses of water daily',
                'Get 7-9 hours of quality sleep',
                'Exercise for 30 minutes daily',
                'Eat 5 servings of fruits and vegetables',
                'Practice stress management (meditation, yoga)',
                'Limit screen time before bed',
                'Take breaks from sitting every hour'
            ]
        },
        'nutrition': {
            'title': '🥗 Nutrition Guidelines',
            'tips': [
                'Eat a rainbow of colorful vegetables',
                'Choose whole grains over refined',
                'Include lean proteins in every meal',
                'Limit processed and packaged foods',
                'Reduce added sugar intake',
                'Use healthy fats (olive oil, avocados, nuts)',
                'Practice portion control'
            ]
        },
        'exercise': {
            'title': '🏃 Exercise Recommendations',
            'tips': [
                '150 minutes moderate aerobic activity per week',
                'Strength training 2 days per week',
                'Include flexibility exercises (stretching, yoga)',
                'Start slowly and gradually increase intensity',
                'Find activities you enjoy',
                'Mix cardio and strength training',
                'Stay consistent - make it a habit'
            ]
        },
        'mental_health': {
            'title': '🧠 Mental Wellness',
            'tips': [
                'Practice mindfulness or meditation daily',
                'Maintain social connections',
                'Set realistic goals and priorities',
                'Take breaks and practice self-care',
                'Seek help when feeling overwhelmed',
                'Limit negative news consumption',
                'Express gratitude daily'
            ]
        },
        'preventive_care': {
            'title': '🏥 Preventive Healthcare',
            'tips': [
                'Get annual physical examinations',
                'Stay up-to-date with vaccinations',
                'Schedule age-appropriate screenings',
                'Monitor blood pressure regularly',
                'Check cholesterol levels annually',
                'Get dental checkups twice yearly',
                'Perform self-examinations (breast, testicular)'
            ]
        }
    }
    
    return tips


def get_food_recommendations(test_name, status):
    """
    Get specific food recommendations based on test results
    """
    recommendations = {
        'Cholesterol': {
            'High': {
                'eat_more': ['Oats', 'Barley', 'Beans', 'Lentils', 'Nuts', 'Fatty fish', 'Olive oil', 'Avocados', 'Fruits', 'Vegetables'],
                'eat_less': ['Red meat', 'Butter', 'Cheese', 'Fried foods', 'Processed meats', 'Baked goods', 'Fast food'],
                'supplements': ['Fish oil (Omega-3)', 'Plant sterols', 'Psyllium fiber', 'Red yeast rice']
            }
        },
        'Glucose': {
            'High': {
                'eat_more': ['Non-starchy vegetables', 'Whole grains', 'Legumes', 'Nuts', 'Seeds', 'Lean proteins', 'Berries'],
                'eat_less': ['White bread', 'White rice', 'Sugary drinks', 'Candy', 'Pastries', 'Processed snacks'],
                'supplements': ['Chromium', 'Alpha-lipoic acid', 'Berberine', 'Cinnamon extract']
            }
        },
        'Hemoglobin': {
            'Low': {
                'eat_more': ['Red meat', 'Liver', 'Spinach', 'Lentils', 'Beans', 'Fortified cereals', 'Pumpkin seeds', 'Quinoa'],
                'eat_less': ['Tea with meals', 'Coffee with meals', 'Excessive dairy'],
                'supplements': ['Iron supplements', 'Vitamin C (enhances iron absorption)', 'Vitamin B12', 'Folate']
            }
        },
        'Vitamin_D': {
            'Low': {
                'eat_more': ['Fatty fish', 'Egg yolks', 'Fortified milk', 'Fortified cereals', 'Mushrooms'],
                'eat_less': [],
                'supplements': ['Vitamin D3 (2000-4000 IU daily)', 'Get 15-30 minutes sun exposure daily']
            }
        },
        'Calcium': {
            'Low': {
                'eat_more': ['Dairy products', 'Leafy greens', 'Sardines', 'Tofu', 'Almonds', 'Fortified foods'],
                'eat_less': ['Excessive salt', 'Caffeine'],
                'supplements': ['Calcium citrate or carbonate', 'Vitamin D (helps absorption)']
            }
        },
        'Iron': {
            'Low': {
                'eat_more': ['Red meat', 'Poultry', 'Fish', 'Beans', 'Dark leafy greens', 'Dried fruits'],
                'eat_less': ['Tea', 'Coffee', 'Calcium-rich foods with iron meals'],
                'supplements': ['Ferrous sulfate', 'Vitamin C']
            }
        },
        'Uric_Acid': {
            'High': {
                'eat_more': ['Water (8-10 glasses)', 'Cherries', 'Coffee', 'Low-fat dairy', 'Vegetables', 'Whole grains'],
                'eat_less': ['Red meat', 'Organ meats', 'Seafood', 'Alcohol', 'Sugary drinks', 'High-fructose corn syrup'],
                'supplements': ['Vitamin C', 'Cherry extract']
            }
        }
    }
    
    return recommendations.get(test_name, {}).get(status, {
        'eat_more': [],
        'eat_less': [],
        'supplements': []
    })


def get_lifestyle_modifications(conditions):
    """
    Get lifestyle modification recommendations based on conditions
    """
    modifications = []
    
    if 'high_cholesterol' in conditions:
        modifications.append({
            'condition': 'High Cholesterol',
            'modifications': [
                'Exercise 30 minutes daily (walking, swimming, cycling)',
                'Lose 5-10% of body weight if overweight',
                'Quit smoking (raises HDL by 10%)',
                'Limit alcohol to 1 drink/day (women) or 2/day (men)',
                'Manage stress through meditation or yoga',
                'Get 7-9 hours of sleep nightly'
            ]
        })
    
    if 'diabetes' in conditions:
        modifications.append({
            'condition': 'Diabetes/High Blood Sugar',
            'modifications': [
                'Monitor blood sugar regularly',
                'Exercise 150 minutes per week',
                'Lose weight if overweight (even 5-7% helps)',
                'Eat smaller, frequent meals',
                'Manage stress (raises blood sugar)',
                'Get adequate sleep (affects insulin sensitivity)',
                'Stay hydrated with water'
            ]
        })
    
    if 'hypertension' in conditions:
        modifications.append({
            'condition': 'High Blood Pressure',
            'modifications': [
                'Reduce sodium to <2,300mg daily',
                'Follow DASH diet (fruits, vegetables, whole grains)',
                'Exercise regularly (lowers BP by 5-8 mmHg)',
                'Limit alcohol consumption',
                'Maintain healthy weight',
                'Manage stress',
                'Quit smoking'
            ]
        })
    
    return modifications


def get_medical_resources():
    """
    Provide links to trusted medical resources
    """
    resources = {
        'general': [
            {
                'name': 'Mayo Clinic',
                'url': 'https://www.mayoclinic.org',
                'description': 'Comprehensive medical information and health resources'
            },
            {
                'name': 'WebMD',
                'url': 'https://www.webmd.com',
                'description': 'Health information, symptom checker, and medical news'
            },
            {
                'name': 'MedlinePlus',
                'url': 'https://medlineplus.gov',
                'description': 'Trusted health information from the National Library of Medicine'
            }
        ],
        'specific': {
            'diabetes': [
                {
                    'name': 'American Diabetes Association',
                    'url': 'https://www.diabetes.org',
                    'description': 'Diabetes education, research, and advocacy'
                }
            ],
            'heart': [
                {
                    'name': 'American Heart Association',
                    'url': 'https://www.heart.org',
                    'description': 'Heart health information and resources'
                }
            ],
            'kidney': [
                {
                    'name': 'National Kidney Foundation',
                    'url': 'https://www.kidney.org',
                    'description': 'Kidney disease information and support'
                }
            ],
            'thyroid': [
                {
                    'name': 'American Thyroid Association',
                    'url': 'https://www.thyroid.org',
                    'description': 'Thyroid health information and resources'
                }
            ]
        }
    }
    
    return resources


def get_emergency_signs():
    """
    Warning signs that require immediate medical attention
    """
    emergency_signs = {
        'cardiac': {
            'title': '🚨 Heart Attack Warning Signs',
            'signs': [
                'Chest pain or pressure',
                'Pain radiating to arm, jaw, or back',
                'Shortness of breath',
                'Cold sweat, nausea',
                'Lightheadedness or dizziness',
                '➡️ CALL 911 IMMEDIATELY'
            ]
        },
        'stroke': {
            'title': '🚨 Stroke Warning Signs (FAST)',
            'signs': [
                'Face drooping on one side',
                'Arm weakness or numbness',
                'Speech difficulty or slurred speech',
                'Time to call 911 immediately',
                'Sudden severe headache',
                'Vision problems in one or both eyes'
            ]
        },
        'diabetic': {
            'title': '🚨 Diabetic Emergency',
            'signs': [
                'Blood sugar <70 or >300 mg/dL',
                'Confusion or loss of consciousness',
                'Rapid breathing',
                'Fruity breath odor',
                'Severe dehydration',
                '➡️ Seek immediate medical care'
            ]
        },
        'kidney': {
            'title': '🚨 Kidney Emergency',
            'signs': [
                'Little or no urine output',
                'Blood in urine (large amounts)',
                'Severe back or side pain',
                'High fever with urinary symptoms',
                'Severe swelling',
                '➡️ Go to emergency room'
            ]
        }
    }
    
    return emergency_signs

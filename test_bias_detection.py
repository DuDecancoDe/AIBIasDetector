#!/usr/bin/env python3
"""
Test script for AI Bias Detection functionality
This script demonstrates how the bias detection works without needing the full Django server
"""

import sys
import os

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Import Django and setup
import django
django.setup()

# Now import our views
from main.views import perform_ai_bias_analysis, advanced_keyword_analysis

def test_bias_detection():
    """Test the bias detection with sample texts"""
    
    print("🤖 AI Bias Detector - Test Mode")
    print("=" * 50)
    
    # Test texts with different levels of bias
    test_texts = [
        {
            "title": "Neutral News Article",
            "text": "The government announced new policies today. The changes will affect approximately 2 million people. Officials stated that the measures are necessary for economic stability. Experts have mixed opinions on the impact.",
            "expected_bias": "Low"
        },
        {
            "title": "Moderately Biased Article",
            "text": "The government's outrageous new policies are clearly designed to hurt ordinary citizens. These terrible changes will devastate millions of hardworking people. Officials claim the measures are necessary, but everyone knows they're lying.",
            "expected_bias": "Moderate"
        },
        {
            "title": "Highly Biased Article",
            "text": "The radical left-wing government has launched a socialist attack on our freedoms! These absolutely terrible policies will completely destroy our capitalist economy. Every single conservative knows this is a disaster. The liberal media is obviously covering up the truth.",
            "expected_bias": "High"
        }
    ]
    
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n📰 Test {i}: {test_case['title']}")
        print("-" * 40)
        print(f"Expected Bias Level: {test_case['expected_bias']}")
        print(f"Text: {test_case['text'][:100]}...")
        
        # Perform analysis
        try:
            analysis = perform_ai_bias_analysis(test_case['text'])
            
            print(f"\n🔍 Analysis Results:")
            print(f"  Overall Bias Score: {analysis['overall_score']:.1f}%")
            print(f"  Bias Level: {analysis['bias_level']}")
            print(f"  AI Confidence: {analysis['confidence']:.1f}")
            print(f"  Models Used: {', '.join(analysis['models_used'])}")
            
            # Show detailed analysis
            if 'sentiment' in analysis['detailed_analysis']:
                sent = analysis['detailed_analysis']['sentiment']
                print(f"  📊 TextBlob Analysis:")
                print(f"    - Polarity: {sent['polarity']:.2f}")
                print(f"    - Subjectivity: {sent['subjectivity']:.2f}")
                print(f"    - Bias Score: {sent['bias_score']:.1f}%")
            
            if 'keyword_analysis' in analysis['detailed_analysis']:
                kw = analysis['detailed_analysis']['keyword_analysis']
                print(f"  🔍 Keyword Analysis:")
                print(f"    - Bias Score: {kw['bias_score']:.1f}%")
            
            # Show recommendations
            if analysis['recommendations']:
                print(f"  💡 AI Recommendations:")
                for rec in analysis['recommendations']:
                    print(f"    - {rec}")
            
        except Exception as e:
            print(f"  ❌ Error during analysis: {str(e)}")
        
        print("\n" + "="*50)

def test_keyword_analysis():
    """Test just the keyword analysis function"""
    
    print("\n🔍 Testing Keyword Analysis Function")
    print("=" * 50)
    
    sample_text = "This is an absolutely amazing and wonderful article that everyone should read. It's clearly the best piece of journalism ever written."
    
    try:
        score = advanced_keyword_analysis(sample_text)
        print(f"Sample text: {sample_text}")
        print(f"Keyword bias score: {score:.1f}%")
        
        # Analyze the categories
        text_lower = sample_text.lower()
        bias_words = {
            'emotional': ['amazing', 'wonderful'],
            'loaded': ['clearly', 'everyone'],
            'subjective': ['best', 'ever']
        }
        
        print("\nDetected bias words:")
        for category, words in bias_words.items():
            found = [word for word in words if word in text_lower]
            if found:
                print(f"  {category.title()}: {', '.join(found)}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting AI Bias Detection Tests...")
    
    try:
        test_bias_detection()
        test_keyword_analysis()
        
        print("\n✅ All tests completed!")
        print("\n💡 To use the full website:")
        print("   1. Make sure Django server is running: python manage.py runserver")
        print("   2. Open http://127.0.0.1:8000 in your browser")
        print("   3. Go to the Analyze page to test with real URLs")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()






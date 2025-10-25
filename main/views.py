from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
import re
import json
import os
from textblob import TextBlob
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import AI libraries (they might not be installed yet)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not available. Install with: pip install openai")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers library not available. Install with: pip install transformers")


class HomeView(TemplateView):
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AI Bias Detector'
        context['description'] = 'Advanced AI-powered analysis to detect bias in articles using multiple AI models'
        return context


def about(request):
    return render(request, 'main/about.html', {
        'title': 'About AI Bias Detector',
        'description': 'Learn how our advanced AI models analyze articles for bias using cutting-edge NLP techniques'
    })


def analyze_article(request):
    if request.method == 'POST':
        try:
            text_content = request.POST.get('text_content', '').strip()
            if not text_content:
                return render(request, 'main/analyze.html', {
                    'error': 'Please provide article text to analyze',
                    'title': 'Analyze Article'
                })
            
            # Perform AI-powered bias analysis
            bias_analysis = perform_ai_bias_analysis(text_content)
            
            return render(request, 'main/analyze.html', {
                'title': 'AI Analysis Results',
                'bias_analysis': bias_analysis,
                'text_preview': text_content[:500] + '...' if len(text_content) > 500 else text_content,
                'ai_models_used': bias_analysis.get('models_used', [])
            })
            
        except Exception as e:
            logger.error(f"Error in analyze_article: {str(e)}")
            return render(request, 'main/analyze.html', {
                'error': f'An error occurred during analysis: {str(e)}',
                'title': 'Analyze Article'
            })
    
    return render(request, 'main/analyze.html', {
        'title': 'AI Article Analysis'
    })





def perform_ai_bias_analysis(text):
    """Perform comprehensive AI-powered bias analysis using multiple approaches"""
    analysis_results = {
        'overall_score': 0,
        'bias_level': 'Unknown',
        'confidence': 0,
        'detailed_analysis': {},
        'models_used': [],
        'recommendations': []
    }
    
    scores = []
    confidences = []
    
    # 1. TextBlob Sentiment Analysis
    try:
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity
        
        # Convert to bias score (higher subjectivity = more bias)
        bias_score = (subjectivity_score + abs(sentiment_score)) / 2 * 100
        scores.append(bias_score)
        confidences.append(0.7)
        
        analysis_results['detailed_analysis']['sentiment'] = {
            'polarity': sentiment_score,
            'subjectivity': subjectivity_score,
            'bias_score': bias_score,
            'description': f"Sentiment analysis shows {'positive' if sentiment_score > 0 else 'negative' if sentiment_score < 0 else 'neutral'} tone with {subjectivity_score:.2f} subjectivity"
        }
        analysis_results['models_used'].append('TextBlob Sentiment Analysis')
        
    except Exception as e:
        logger.error(f"TextBlob analysis error: {str(e)}")
    
    # 2. Advanced Keyword Analysis
    try:
        keyword_score = advanced_keyword_analysis(text)
        scores.append(keyword_score)
        confidences.append(0.8)
        
        analysis_results['detailed_analysis']['keyword_analysis'] = {
            'bias_score': keyword_score,
            'description': "Advanced keyword analysis for bias indicators"
        }
        analysis_results['models_used'].append('Advanced Keyword Analysis')
        
    except Exception as e:
        logger.error(f"Keyword analysis error: {str(e)}")
    
    # 3. OpenAI GPT Analysis (if available)
    if OPENAI_AVAILABLE:
        try:
            openai_score, openai_analysis = openai_bias_analysis(text)
            if openai_score is not None:
                scores.append(openai_score)
                confidences.append(0.9)
                
                analysis_results['detailed_analysis']['openai_analysis'] = {
                    'bias_score': openai_score,
                    'analysis': openai_analysis,
                    'description': "OpenAI GPT-powered bias analysis"
                }
                analysis_results['models_used'].append('OpenAI GPT-4')
                
        except Exception as e:
            logger.error(f"OpenAI analysis error: {str(e)}")
    
    # 4. Transformers-based Analysis (if available)
    if TRANSFORMERS_AVAILABLE:
        try:
            transformers_score, transformers_analysis = transformers_bias_analysis(text)
            if transformers_score is not None:
                scores.append(transformers_score)
                confidences.append(0.85)
                
                analysis_results['detailed_analysis']['transformers_analysis'] = {
                    'bias_score': transformers_score,
                    'analysis': transformers_analysis,
                    'description': "Hugging Face Transformers analysis"
                }
                analysis_results['models_used'].append('Hugging Face Transformers')
                
        except Exception as e:
            logger.error(f"Transformers analysis error: {str(e)}")
    
    # Calculate weighted average score
    if scores and confidences:
        weighted_score = sum(score * conf for score, conf in zip(scores, confidences)) / sum(confidences)
        analysis_results['overall_score'] = min(100, max(0, weighted_score))
        analysis_results['confidence'] = sum(confidences) / len(confidences)
        
        # Determine bias level
        if weighted_score < 20:
            analysis_results['bias_level'] = "Low Bias"
            analysis_results['recommendations'].append("This article appears relatively objective and balanced.")
        elif weighted_score < 40:
            analysis_results['bias_level'] = "Moderate Bias"
            analysis_results['recommendations'].append("Some bias detected. Read with critical awareness.")
        elif weighted_score < 60:
            analysis_results['bias_level'] = "High Bias"
            analysis_results['recommendations'].append("Significant bias detected. Verify facts from multiple sources.")
        else:
            analysis_results['bias_level'] = "Very High Bias"
            analysis_results['recommendations'].append("Strong bias detected. Approach with extreme caution.")
    
    return analysis_results


def advanced_keyword_analysis(text):
    """Advanced keyword-based bias analysis"""
    text_lower = text.lower()
    
    # Comprehensive bias indicators
    bias_categories = {
        'emotional_language': {
            'words': ['outrageous', 'shocking', 'scandalous', 'terrible', 'amazing', 'incredible',
                     'horrible', 'wonderful', 'disgusting', 'beautiful', 'awful', 'fantastic',
                     'devastating', 'miraculous', 'catastrophic', 'brilliant', 'disastrous'],
            'weight': 1.2
        },
        'loaded_words': {
            'words': ['clearly', 'obviously', 'undoubtedly', 'certainly', 'definitely',
                     'absolutely', 'never', 'always', 'everyone', 'nobody', 'everybody',
                     'completely', 'totally', 'utterly', 'entirely'],
            'weight': 1.0
        },
        'subjective_qualifiers': {
            'words': ['best', 'worst', 'greatest', 'terrible', 'excellent', 'poor',
                     'superior', 'inferior', 'amazing', 'awful', 'outstanding', 'horrible'],
            'weight': 1.1
        },
        'political_indicators': {
            'words': ['liberal', 'conservative', 'progressive', 'republican', 'democrat',
                     'left-wing', 'right-wing', 'socialist', 'capitalist', 'radical',
                     'extremist', 'moderate', 'centrist'],
            'weight': 1.3
        },
        'exaggeration': {
            'words': ['huge', 'massive', 'enormous', 'tiny', 'miniscule', 'gigantic',
                     'colossal', 'monumental', 'insignificant', 'trivial'],
            'weight': 1.1
        }
    }
    
    total_score = 0
    max_possible = 0
    
    for category, data in bias_categories.items():
        count = sum(1 for word in data['words'] if word in text_lower)
        weighted_count = count * data['weight']
        total_score += weighted_count
        max_possible += len(data['words']) * data['weight']
    
    # Normalize to 0-100 scale
    if max_possible > 0:
        normalized_score = min(100, (total_score / max_possible) * 100)
    else:
        normalized_score = 0
    
    return normalized_score


def openai_bias_analysis(text):
    """Use OpenAI GPT to analyze bias (requires API key)"""
    try:
        # Check if OpenAI API key is configured
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OpenAI API key not configured")
            return None, "OpenAI API key not configured"
        
        # Truncate text if too long (OpenAI has token limits)
        max_tokens = 4000
        if len(text) > max_tokens:
            text = text[:max_tokens] + "..."
        
        prompt = f"""
        Analyze the following article text for bias. Consider:
        1. Emotional language and sensationalism
        2. Loaded words and subjective qualifiers
        3. Political or ideological slant
        4. Factual vs. opinion-based content
        5. Balance and fairness
        
        Provide a bias score from 0-100 (0 = completely neutral, 100 = extremely biased) and a brief explanation.
        
        Article text:
        {text}
        
        Respond in this exact format:
        Score: [0-100]
        Explanation: [your analysis]
        """
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        
        # Parse the response
        try:
            score_match = re.search(r'Score:\s*(\d+)', result)
            explanation_match = re.search(r'Explanation:\s*(.+)', result, re.DOTALL)
            
            if score_match and explanation_match:
                score = int(score_match.group(1))
                explanation = explanation_match.group(1).strip()
                return score, explanation
            else:
                return None, result
                
        except Exception as e:
            logger.error(f"Error parsing OpenAI response: {str(e)}")
            return None, result
            
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return None, f"OpenAI API error: {str(e)}"


def transformers_bias_analysis(text):
    """Use Hugging Face transformers for bias analysis"""
    try:
        # Use a sentiment analysis pipeline
        sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        
        # Analyze text in chunks if too long
        max_length = 500
        chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        
        scores = []
        for chunk in chunks:
            if chunk.strip():
                result = sentiment_analyzer(chunk)
                # Convert sentiment to bias score
                if result[0]['label'] == 'POSITIVE':
                    score = 30 + (result[0]['score'] * 40)  # 30-70 range
                elif result[0]['label'] == 'NEGATIVE':
                    score = 30 + (result[0]['score'] * 40)  # 30-70 range
                else:  # NEUTRAL
                    score = 20 + (result[0]['score'] * 20)  # 20-40 range
                scores.append(score)
        
        if scores:
            avg_score = sum(scores) / len(scores)
            analysis = f"Transformers analysis across {len(chunks)} text chunks"
            return avg_score, analysis
        
        return None, "No valid text chunks for analysis"
        
    except Exception as e:
        logger.error(f"Transformers analysis error: {str(e)}")
        return None, f"Transformers error: {str(e)}"


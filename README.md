# AI Bias Detector

An advanced Django-based website that uses multiple AI models to analyze articles for potential bias. The system combines natural language processing, machine learning, and large language models to provide comprehensive bias analysis.

## Features

- **Multi-AI Analysis**: Combines TextBlob, advanced keyword analysis, OpenAI GPT, and Hugging Face Transformers
- **Web Scraping**: Automatically extracts article content from URLs
- **Comprehensive Scoring**: Provides detailed bias scores with confidence levels
- **Multiple Bias Categories**: Detects emotional language, loaded words, political indicators, and more
- **Beautiful UI**: Modern, responsive interface built with Bootstrap 5

## AI Models Used

1. **TextBlob NLP**: Sentiment and subjectivity analysis
2. **Advanced Keyword Analysis**: Pattern recognition for bias indicators
3. **OpenAI GPT**: Large language model analysis (requires API key)
4. **Hugging Face Transformers**: Pre-trained sentiment analysis models

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mysite
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   # Django Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # AI Configuration
   OPENAI_API_KEY=your-openai-api-key-here
   AI_ANALYSIS_ENABLED=True
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## Configuration

### OpenAI API Key (Optional)

To use OpenAI GPT analysis:
1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Add it to your `.env` file: `OPENAI_API_KEY=your-key-here`

### AI Models

The system will automatically detect available AI libraries:
- **TextBlob**: Always available (included in requirements)
- **OpenAI**: Available if API key is configured
- **Transformers**: Available if the library is installed

## Usage

1. **Home Page**: Overview of the bias detection system
2. **Analyze Page**: Paste any article URL for analysis
3. **Results**: View comprehensive bias analysis from multiple AI models

## How It Works

1. **URL Input**: User provides an article URL
2. **Content Extraction**: Web scraping extracts clean text content
3. **AI Analysis**: Multiple AI models analyze the text simultaneously
4. **Score Calculation**: Weighted average of all model scores
5. **Results Display**: Comprehensive breakdown with recommendations

## Bias Detection Categories

- **Emotional Language**: Detects sensationalist and emotional words
- **Loaded Words**: Identifies words with strong connotations
- **Subjective Qualifiers**: Spots subjective judgments and opinions
- **Political Indicators**: Recognizes politically charged terminology
- **Exaggeration**: Finds hyperbolic language patterns

## API Endpoints

- `GET /`: Home page
- `GET /analyze/`: Analysis form
- `POST /analyze/`: Submit article for analysis
- `GET /about/`: About page
- `GET /contact/`: Contact page

## Development

### Project Structure
```
mysite/
├── main/                 # Main app
│   ├── views.py         # AI analysis logic
│   ├── urls.py          # URL routing
│   └── apps.py          # App configuration
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   └── main/            # App-specific templates
├── static/              # CSS, JS, images
├── mysite/              # Project settings
│   ├── settings.py      # Django settings
│   └── urls.py          # Main URL configuration
└── requirements.txt      # Python dependencies
```

### Adding New AI Models

To add a new AI model:

1. **Install the library** and add to `requirements.txt`
2. **Import the library** in `views.py`
3. **Create analysis function** following the existing pattern
4. **Add to `perform_ai_bias_analysis`** function
5. **Update templates** to display results

### Customizing Bias Detection

Modify the `advanced_keyword_analysis` function in `views.py` to:
- Add new bias categories
- Adjust word weights
- Change scoring algorithms

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all requirements are installed
2. **OpenAI API Errors**: Check API key configuration
3. **Web Scraping Issues**: Some sites may block automated requests
4. **Memory Issues**: Large articles may cause memory problems

### Performance Optimization

- **Text Truncation**: Long articles are automatically truncated for AI models
- **Caching**: Consider implementing result caching for repeated analyses
- **Async Processing**: For production, consider async processing for large articles

## Security Considerations

- **API Keys**: Never commit API keys to version control
- **Input Validation**: URLs are validated before processing
- **Rate Limiting**: Consider implementing rate limiting for production
- **Content Privacy**: Article content is not stored permanently

## Production Deployment

1. **Set `DEBUG=False`** in production
2. **Use environment variables** for all sensitive settings
3. **Implement proper logging** and monitoring
4. **Add rate limiting** and user authentication if needed
5. **Use HTTPS** for secure communication
6. **Monitor API usage** and costs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review Django and AI library documentation

## Acknowledgments

- Django framework
- TextBlob for NLP analysis
- OpenAI for GPT models
- Hugging Face for transformers
- Bootstrap for UI components

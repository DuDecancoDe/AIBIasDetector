
// ===== Gemini 1.5 Flash API Key Placeholder =====
// Insert your Gemini API key below. For security, do NOT use a real key in production static sites.
const GEMINI_API_KEY = "AIzaSyAAOFJgiDV3n8tljnQ49W7zDNIpyoHRxOg";

// Simple JavaScript bias and sentiment analysis for static site
// This is a basic implementation. For more advanced analysis, consider integrating open-source JS NLP libraries.

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzeForm');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const text = document.getElementById('text_content').value.trim();
        if (!text) return;
        resultsDiv.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-danger" role="status"></div><p class="mt-3">Analyzing with Gemini...</p></div>';
        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
        let geminiResult = null;
        try {
            geminiResult = await analyzeWithGemini(text);
        } catch (err) {
            geminiResult = { error: 'Gemini API error: ' + (err.message || err) };
        }
        const localAnalysis = analyzeText(text);
        resultsDiv.innerHTML = renderResults(text, localAnalysis, geminiResult);
    });
});

// Gemini 1.5 Flash API integration
async function analyzeWithGemini(text) {
    const url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY;
    const prompt = `Analyze the following article for bias. Give a summary of bias indicators, a bias score (0-100), and a short explanation.\n\nArticle:\n"""${text}"""`;
    const body = {
        contents: [{ parts: [{ text: prompt }] }]
    };
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    if (!response.ok) throw new Error('Gemini API error: ' + response.status);
    const data = await response.json();
    // Try to extract the model's text response
    let geminiText = '';
    try {
        geminiText = data.candidates[0].content.parts[0].text;
    } catch {
        geminiText = JSON.stringify(data);
    }
    return { geminiText };
}

function analyzeText(text) {
    // Simple sentiment analysis (polarity, subjectivity)
    const positiveWords = ['good','great','excellent','positive','fortunate','correct','superior','happy','joy','love','success'];
    const negativeWords = ['bad','poor','negative','unfortunate','wrong','inferior','sad','anger','hate','failure'];
    const biasWords = ['always','never','everyone','nobody','obviously','clearly','undoubtedly','certainly','must','should'];
    const emotionalWords = ['amazing','horrible','disaster','fantastic','terrible','shocking','unbelievable','incredible'];

    let pos = 0, neg = 0, bias = 0, emotional = 0;
    const words = text.toLowerCase().split(/\W+/);
    words.forEach(word => {
        if (positiveWords.includes(word)) pos++;
        if (negativeWords.includes(word)) neg++;
        if (biasWords.includes(word)) bias++;
        if (emotionalWords.includes(word)) emotional++;
    });
    const total = words.length || 1;
    const polarity = (pos - neg) / total;
    const subjectivity = (bias + emotional) / total;
    // Bias score: weighted sum
    const biasScore = Math.min(100, Math.round((Math.abs(polarity) + subjectivity) * 100));
    let biasLevel = 'Low';
    if (biasScore > 60) biasLevel = 'High';
    else if (biasScore > 30) biasLevel = 'Medium';
    return {
        polarity: polarity.toFixed(2),
        subjectivity: subjectivity.toFixed(2),
        biasScore,
        biasLevel,
        pos,
        neg,
        bias,
        emotional
    };
}

function renderResults(text, analysis, geminiResult) {
    let geminiSection = '';
    if (geminiResult && geminiResult.geminiText) {
        geminiSection = `
        <div class="mb-4">
            <h5>Analysis:</h5>
            <div class="alert alert-danger" style="white-space: pre-line;">${geminiResult.geminiText.replace(/</g, '&lt;')}</div>
        </div>
        `;
    } else if (geminiResult && geminiResult.error) {
        geminiSection = `<div class="alert alert-warning">${geminiResult.error}</div>`;
    }
    return `
    <div class="card shadow-lg border-0">
        <div class="card-header bg-primary text-white">
            <h3 class="mb-0">
                <i class="fas fa-chart-line me-2"></i>
                AI Bias Analysis Results
            </h3>
        </div>
        <div class="card-body p-5">
            <div class="mb-4">
                <h5>Analyzed Text:</h5>
                <div class="bg-light p-3 rounded">
                    <p class="mb-0">${text.replace(/</g, '&lt;')}</p>
                </div>
            </div>
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="text-center p-4 bg-light rounded">
                        <h2 class="display-4 fw-bold text-primary">${analysis.biasScore}%</h2>
                        <p class="text-muted mb-0">Overall Bias Score</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="text-center p-4 bg-light rounded">
                        <h4 class="fw-bold text-dark">${analysis.biasLevel}</h4>
                        <p class="text-muted mb-0">Bias Level</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="text-center p-4 bg-light rounded">
                        <h4 class="fw-bold text-dark">${analysis.polarity}</h4>
                        <p class="text-muted mb-0">Polarity</p>
                    </div>
                </div>
            </div>
            <div class="mb-4">
                <h5>Details:</h5>
                <ul>
                    <li>Positive words: ${analysis.pos}</li>
                    <li>Negative words: ${analysis.neg}</li>
                    <li>Bias words: ${analysis.bias}</li>
                    <li>Emotional words: ${analysis.emotional}</li>
                    <li>Subjectivity: ${analysis.subjectivity}</li>
                </ul>
            </div>
            ${geminiSection}
            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                <a href="analyze.html" class="btn btn-primary btn-lg">
                    <i class="fas fa-plus me-2"></i>
                    Analyze Another Article
                </a>
                <a href="index.html" class="btn btn-outline-secondary btn-lg">
                    <i class="fas fa-home me-2"></i>
                    Back to Home
                </a>
            </div>
        </div>
    </div>
    `;
}

    function extractGeminiAnalysis(geminiText) {
        // Extract bias score
        let biasScore = null;
        let polarity = null;
        let biasLevel = null;
        // Bias Score
        const scoreMatch = geminiText && geminiText.match(/bias score\D{0,10}(\d{1,3})/i);
        if (scoreMatch) {
            const score = parseInt(scoreMatch[1], 10);
            if (!isNaN(score) && score >= 0 && score <= 100) biasScore = score;
        }
        // Polarity (look for e.g. "Polarity: -0.23" or "Polarity: 0.5")
        const polarityMatch = geminiText && geminiText.match(/polarity\D{0,10}(-?\d+\.\d+)/i);
        if (polarityMatch) {
            polarity = parseFloat(polarityMatch[1]).toFixed(2);
        }
        // Bias Level (look for "Bias Level: High/Medium/Low")
        const levelMatch = geminiText && geminiText.match(/bias level\D{0,10}(high|medium|low)/i);
        if (levelMatch) {
            biasLevel = levelMatch[1].charAt(0).toUpperCase() + levelMatch[1].slice(1).toLowerCase();
        } else if (biasScore !== null) {
            if (biasScore > 60) biasLevel = 'High';
            else if (biasScore > 30) biasLevel = 'Medium';
            else biasLevel = 'Low';
        }
        // Extract details (summary/explanation)
        let details = null;
        const detailsMatch = geminiText && geminiText.match(/(explanation|summary|details)\s*[:\-]?\s*([\s\S]{0,300})/i);
        if (detailsMatch) {
            details = detailsMatch[2].trim();
        }
        return { biasScore, polarity, biasLevel, details };
    }

    function renderResults(text, analysis, geminiResult) {
        let geminiSection = '';
        let biasScore = analysis.biasScore;
        let biasLevel = analysis.biasLevel;
        let polarity = analysis.polarity;
        let detailsList = `<ul>
            <li>Positive words: ${analysis.pos}</li>
            <li>Negative words: ${analysis.neg}</li>
            <li>Bias words: ${analysis.bias}</li>
            <li>Emotional words: ${analysis.emotional}</li>
            <li>Subjectivity: ${analysis.subjectivity}</li>
        </ul>`;
        if (geminiResult && geminiResult.geminiText) {
            // Try to extract Gemini bias score, polarity, bias level, and details
            const gemini = extractGeminiAnalysis(geminiResult.geminiText);
            if (gemini.biasScore !== null) biasScore = gemini.biasScore;
            if (gemini.biasLevel) biasLevel = gemini.biasLevel;
            if (gemini.polarity !== null) polarity = gemini.polarity;
            if (gemini.details) {
                detailsList = `<div class="mb-2"><strong>AI Details:</strong> ${gemini.details}</div>` + detailsList;
            }
            geminiSection = `
            <div class="mb-4">
                <h5>Gemini 1.5 Flash Analysis:</h5>
                <div class="alert alert-danger" style="white-space: pre-line;">${geminiResult.geminiText.replace(/</g, '&lt;')}</div>
            </div>
            `;
        } else if (geminiResult && geminiResult.error) {
            geminiSection = `<div class="alert alert-warning">${geminiResult.error}</div>`;
        }
        return `
        <div class="card shadow-lg border-0">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0">
                    <i class="fas fa-chart-line me-2"></i>
                    AI Bias Analysis Results
                </h3>
            </div>
            <div class="card-body p-5">
                <div class="mb-4">
                    <h5>Analyzed Text:</h5>
                    <div class="bg-light p-3 rounded">
                        <p class="mb-0">${text.replace(/</g, '&lt;')}</p>
                    </div>
                </div>
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="text-center p-4 bg-light rounded">
                            <h2 class="display-4 fw-bold text-primary">${biasScore}%</h2>
                            <p class="text-muted mb-0">Overall Bias Score</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-4 bg-light rounded">
                            <h4 class="fw-bold text-dark">${biasLevel}</h4>
                            <p class="text-muted mb-0">Bias Level</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-4 bg-light rounded">
                            <h4 class="fw-bold text-dark">${polarity}</h4>
                            <p class="text-muted mb-0">Polarity</p>
                        </div>
                    </div>
                </div>
                <div class="mb-4">
                    <h5>Details:</h5>
                    ${detailsList}
                </div>
                ${geminiSection}
                <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                    <a href="analyze.html" class="btn btn-primary btn-lg">
                        <i class="fas fa-plus me-2"></i>
                        Analyze Another Article
                    </a>
                    <a href="index.html" class="btn btn-outline-secondary btn-lg">
                        <i class="fas fa-home me-2"></i>
                        Back to Home
                    </a>
                </div>
            </div>
        </div>
        `;
    }

let currentTab = 'text';
let analysisInProgress = false;

// Initialize dashboard
async function loadDashboard() {
  try {
    const response = await fetch('http://127.0.0.1:8010/dashboard/');
    const data = await response.json();

    document.getElementById('totalAnalyses').textContent = data.total_analyses || 0;
    document.getElementById('fakeDetectionRate').textContent = Math.round((data.fake_detection_rate || 0) * 100) + '%';
    document.getElementById('communityReports').textContent = data.community_reports || 0;
    document.getElementById('verifiedSources').textContent = data.verified_sources || 0;
  } catch (error) {
    console.error('Failed to load dashboard:', error);
  }
}

// Analyze content
async function analyzeContent() {
  if (analysisInProgress) return;

  analysisInProgress = true;
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultsContainer = document.getElementById('resultsContainer');

  // Show loading state
  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

  resultsContainer.innerHTML = `
    <div class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Running comprehensive analysis...</p>
      <p style="font-size: 0.9rem; color: #718096;">This may take a few moments</p>
    </div>
  `;
  // Auto-scroll to results area (start of analysis)
  const resultsSection = document.querySelector('.results-section');
  if (resultsSection && resultsSection.scrollIntoView) {
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  try {
    let formData = new FormData();
    let endpoint = 'http://127.0.0.1:8010/analyze_auto/';

    // Collect inputs based on the active tab, but allow auto-detection on backend
    if (currentTab === 'text') {
      const text = document.getElementById('textInput').value;
      const language = document.getElementById('textLanguage').value;
      const source = document.getElementById('textSource').value;

      if (!text.trim() && !source.trim()) {
        throw new Error('Please enter text or provide a source URL');
      }

      if (text.trim()) formData.append('text', text);
      if (language) formData.append('lang', language);
      if (source) formData.append('source_url', source);
    } else {
      const fileInput = document.getElementById(currentTab + 'File');
      const sourceInput = document.getElementById(currentTab + 'Source');
      const hasFile = fileInput && fileInput.files && fileInput.files[0];
      const hasUrl = sourceInput && sourceInput.value && sourceInput.value.trim().length > 0;

      if (!hasFile && !hasUrl) {
        throw new Error('Please select a file or provide a source URL to analyze');
      }

      if (hasFile) formData.append('file', fileInput.files[0]);
      if (hasUrl) formData.append('source_url', sourceInput.value.trim());
    }

    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    const result = await response.json();
    displayResults(result);

  } catch (error) {
    resultsContainer.innerHTML = `
      <div class="error-message">
        <i class="fas fa-exclamation-triangle"></i>
        ${error.message}
      </div>
    `;
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Content';
    analysisInProgress = false;
  }
}

// Display analysis results
function displayResults(result) {
  const resultsContainer = document.getElementById('resultsContainer');

  // Determine risk level and colors
  let riskLevel, riskIcon, riskText, cardColor, textColor;

  // If flagged as adult content (18+), force high-risk styling
  if (result.adult_content === true) {
    riskLevel = 'high-risk';
    riskIcon = '🚨';
    riskText = '18+ CONTENT DETECTED';
    cardColor = '#fee2e2';
    textColor = '#dc2626';
  } else if (result.fake_score >= 0.7) {
    // High Risk - Red
    riskLevel = 'high-risk';
    riskIcon = '🚨';
    riskText = 'FAKE DETECTED';
    cardColor = '#fee2e2';
    textColor = '#dc2626';
  } else if (result.fake_score >= 0.4) {
    // Medium Risk - Orange
    riskLevel = 'medium-risk';
    riskIcon = '⚠️';
    riskText = 'SUSPICIOUS';
    cardColor = '#fef3c7';
    textColor = '#d97706';
  } else {
    // Low Risk - Green
    riskLevel = 'low-risk';
    riskIcon = '✅';
    riskText = 'AUTHENTIC';
    cardColor = '#d1fae5';
    textColor = '#059669';
  }

  resultsContainer.innerHTML = `
    <div class="result-card" style="background: ${cardColor}; border-left-color: ${textColor};">
      <div class="result-header">
        <div class="result-title" style="color: ${textColor}; font-weight: bold; font-size: 1.4rem;">
          ${riskIcon} ${riskText}
        </div>
        <div class="confidence-score ${riskLevel}" style="background: ${textColor}; color: white; font-weight: bold;">
          ${Math.round(result.fake_score * 100)}%
        </div>
      </div>

      <div class="result-details">
        <div class="detail-item">
          <span class="detail-label">Analysis Type:</span>
          <span class="detail-value">${result.analysis_type || currentTab}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Confidence:</span>
          <span class="detail-value">${Math.round((result.confidence || result.fake_score) * 100)}%</span>
        </div>
        ${result.adult_content === true ? `
        <div class="detail-item">
          <span class="detail-label">Content Rating:</span>
          <span class="detail-value" style="color: ${textColor}; font-weight: 600;">18+ (Adult)</span>
        </div>
        ` : ''}
        ${result.credibility_score ? `
        <div class="detail-item">
          <span class="detail-label">Source Credibility:</span>
          <span class="detail-value">${Math.round(result.credibility_score * 100)}%</span>
        </div>
        ` : ''}
        ${result.blockchain_hash ? `
        <div class="detail-item">
          <span class="detail-label">Blockchain Hash:</span>
          <span class="detail-value" style="font-family: monospace; font-size: 0.9rem;">${result.blockchain_hash}</span>
        </div>
        ` : ''}
      </div>

      ${result.explanation ? `
      <div class="result-details" style="margin-top: 20px;">
        <h4 style="color: #2d3748; margin-bottom: 15px;">📊 Detailed Analysis</h4>
        <div style="background: #f7fafc; padding: 15px; border-radius: 10px; border-left: 4px solid ${textColor};">
          <p style="color: ${textColor}; font-weight: bold;"><strong>Summary:</strong> ${result.explanation.summary || 'Analysis completed'}</p>
          ${result.explanation.detailed_analysis ? `
            <div style="margin-top: 15px;">
              <p><strong>Technical Indicators:</strong></p>
              <ul style="margin-left: 20px; margin-top: 5px;">
                ${result.explanation.detailed_analysis.technical_indicators ?
                  result.explanation.detailed_analysis.technical_indicators.map(indicator =>
                    `<li>${indicator}</li>`
                  ).join('') : '<li>No specific indicators</li>'}
              </ul>
            </div>
          ` : ''}
          ${result.explanation && result.explanation.metrics && (typeof result.explanation.metrics.visual_score === 'number' || typeof result.explanation.metrics.audio_score === 'number') ? `
            <div style="margin-top: 15px;">
              <p><strong>Component Scores:</strong></p>
              <ul style="margin-left: 20px; margin-top: 5px;">
                ${typeof result.explanation.metrics.visual_score === 'number' ? `<li>Visual Score: ${Math.round(result.explanation.metrics.visual_score * 100)}%</li>` : ''}
                ${typeof result.explanation.metrics.audio_score === 'number' ? `<li>Audio Score: ${Math.round(result.explanation.metrics.audio_score * 100)}%</li>` : ''}
              </ul>
            </div>
          ` : ''}
        </div>
      </div>
      ` : ''}

      ${result.explanation && result.explanation.recommendations ? `
      <div class="recommendations" style="background: ${cardColor}; border-left: 4px solid ${textColor};">
        <h3 style="color: ${textColor};">💡 Recommendations</h3>
        ${result.explanation.recommendations.map(rec => `
          <div class="recommendation-item">
            <span class="recommendation-icon">${rec.includes('⚠️') ? '⚠️' : rec.includes('🔍') ? '🔍' : rec.includes('📚') ? '📚' : rec.includes('✅') ? '✅' : '💡'}</span>
            <span class="recommendation-text" style="color: ${textColor}; font-weight: 500;">${rec}</span>
          </div>
        `).join('')}
      </div>
      ` : ''}
    </div>

    ${(result.cultural_context || result.psychological_impact || result.traceability) ? `
    <details style="margin-top: 15px;">
      <summary style="cursor: pointer; color: ${textColor}; font-weight: 600;">Advanced details</summary>
      <div style="margin-top: 10px;">
        ${result.cultural_context ? `<p><strong>Cultural Context:</strong> ${JSON.stringify(result.cultural_context)}</p>` : ''}
        ${result.psychological_impact ? `<p><strong>Psychological Impact:</strong> ${JSON.stringify(result.psychological_impact)}</p>` : ''}
        ${result.traceability ? `<p><strong>Traceability:</strong> ${JSON.stringify(result.traceability)}</p>` : ''}
      </div>
    </details>
    ` : ''}
  `;

  // Auto-scroll to results area (after analysis)
  const resultsSection = document.querySelector('.results-section');
  if (resultsSection && resultsSection.scrollIntoView) {
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// Basic drag & drop handlers for file-upload areas
function setupDragDrop(areaId, inputId) {
  const area = document.getElementById(areaId);
  const input = document.getElementById(inputId);
  if (!area || !input) return;
  area.addEventListener('click', () => input.click());
  ['dragenter','dragover'].forEach(evt => area.addEventListener(evt, (e) => { e.preventDefault(); area.classList.add('dragover'); }));
  ;['dragleave','drop'].forEach(evt => area.addEventListener(evt, (e) => { e.preventDefault(); area.classList.remove('dragover'); }));
  area.addEventListener('drop', (e) => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length) {
      input.files = e.dataTransfer.files;
    }
  });
}

// DOMContentLoaded initialization
document.addEventListener('DOMContentLoaded', () => {
  loadDashboard();

  setupDragDrop('imageUploadArea', 'imageFile');
  setupDragDrop('videoUploadArea', 'videoFile');
  setupDragDrop('audioUploadArea', 'audioFile');

  // Tabs click handling (no inline handlers)
  document.querySelectorAll('.upload-tabs .tab').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const tabName = btn.getAttribute('data-tab');
      if (!tabName) return;
      // Update currentTab and active classes
      currentTab = tabName;
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      const pane = document.getElementById(tabName + 'Tab');
      if (pane) pane.classList.add('active');
    });
  });

  // Analyze button handler
  const analyzeBtn = document.getElementById('analyzeBtn');
  if (analyzeBtn) analyzeBtn.addEventListener('click', analyzeContent);
});

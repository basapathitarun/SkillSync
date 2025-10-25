import React, { useState } from 'react';
import { Upload, FileText, Zap, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import './App.css';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // Update this URL to your Render backend URL after deployment
  const API_URL = 'https://skillsync-vkn0.onrender.com';

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && (file.type === 'application/pdf' || 
        file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      setResumeFile(file);
      setError('');
    } else {
      setError('Please upload a PDF or DOCX file');
      setResumeFile(null);
    }
  };

  const handleSubmit = async () => {
    if (!resumeFile || !jobDescription.trim()) {
      setError('Please provide both resume and job description');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch(`${API_URL}/api/match`, {

        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze resume');
      }

      const data = await response.json();
      
      // Handle different response formats
      let processedData = data;
      
      // Process suggestions based on their structure
      if (data.suggestions) {
        let allSuggestions = [];
        
        if (Array.isArray(data.suggestions)) {
          // Handle array of suggestions
          allSuggestions = data.suggestions.map(suggestion => {
            if (typeof suggestion === 'string') {
              return suggestion;
            } else if (typeof suggestion === 'object') {
              // Handle object suggestions with original_text and improvements
              if (suggestion.improvements) {
                return suggestion.improvements;
              } else if (suggestion.original_text) {
                return suggestion.original_text;
              }
            }
            return JSON.stringify(suggestion);
          });
        } else if (typeof data.suggestions === 'object') {
          // Handle nested object structure
          Object.keys(data.suggestions).forEach(key => {
            const suggestionValue = data.suggestions[key];
            if (Array.isArray(suggestionValue)) {
              suggestionValue.forEach(item => {
                if (typeof item === 'string') {
                  allSuggestions.push(item);
                } else if (typeof item === 'object' && item.improvements) {
                  allSuggestions.push(item.improvements);
                } else if (typeof item === 'object' && item.original_text) {
                  allSuggestions.push(item.original_text);
                }
              });
            } else if (typeof suggestionValue === 'string') {
              allSuggestions.push(suggestionValue);
            } else if (typeof suggestionValue === 'object' && suggestionValue.improvements) {
              allSuggestions.push(suggestionValue.improvements);
            }
          });
        }
        
        processedData = {
          ...data,
          suggestions: allSuggestions
        };
      }
      
      setResult(processedData);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing the resume');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'score-excellent';
    if (score >= 60) return 'score-good';
    return 'score-poor';
  };

  const getScoreBackground = (score) => {
    if (score >= 80) return 'score-bg-excellent';
    if (score >= 60) return 'score-bg-good';
    return 'score-bg-poor';
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <Zap className="logo-icon" />
            <div>
              <h1 className="title">SkillSync</h1>
              <p className="subtitle">AI-Powered Resume Screening</p>
            </div>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="container">
          <div className="hero">
            <h2 className="hero-title">
              Match Your Resume to Your Dream Job
            </h2>
            <p className="hero-description">
              Get instant AI-powered analysis of how well your resume matches a job description, 
              plus actionable suggestions to improve your chances.
            </p>
          </div>

          <div className="content-grid">
            {/* Input Section */}
            <div className="card">
              <h3 className="card-title">Upload & Analyze</h3>
              
              <div className="form-container">
                <div className="form-group">
                  <label className="label">Resume (PDF or DOCX)</label>
                  <div className="upload-container">
                    <input
                      type="file"
                      accept=".pdf,.docx"
                      onChange={handleFileChange}
                      className="file-input"
                      id="resume-upload"
                    />
                    <label htmlFor="resume-upload" className="upload-label">
                      <div className="upload-content">
                        <Upload className="upload-icon" />
                        <p className="upload-text">
                          {resumeFile ? resumeFile.name : 'Click to upload resume'}
                        </p>
                        <p className="upload-hint">PDF or DOCX, max 10MB</p>
                      </div>
                    </label>
                  </div>
                </div>

                <div className="form-group">
                  <label className="label">Job Description</label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here..."
                    rows={10}
                    className="textarea"
                  />
                </div>

                {error && (
                  <div className="error-box">
                    <AlertCircle className="error-icon" />
                    <p className="error-text">{error}</p>
                  </div>
                )}

                <button
                  onClick={handleSubmit}
                  disabled={loading || !resumeFile || !jobDescription.trim()}
                  className="submit-button"
                >
                  {loading ? (
                    <>
                      <Loader className="button-icon spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Zap className="button-icon" />
                      Analyze Resume
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Results Section */}
            <div className="card">
              <h3 className="card-title">Analysis Results</h3>
              
              {!result && !loading && (
                <div className="empty-state">
                  <FileText className="empty-icon" />
                  <p className="empty-text">Your analysis will appear here</p>
                </div>
              )}

              {loading && (
                <div className="loading-state">
                  <Loader className="loading-icon spin" />
                  <p className="loading-text">Analyzing your resume...</p>
                </div>
              )}

              {result && (
                <div className="results-container">
                  <div className={`score-card ${getScoreBackground(result.match_percentage)}`}>
                    <p className="score-label">Match Score</p>
                    <p className={`score-value ${getScoreColor(result.match_percentage)}`}>
                      {result.match_percentage}%
                    </p>
                    <p className="score-description">
                      {result.match_percentage >= 80 ? 'Excellent Match!' : 
                       result.match_percentage >= 60 ? 'Good Match' : 
                       'Needs Improvement'}
                    </p>
                  </div>

                  <div className="suggestions-section">
                    <h4 className="suggestions-title">
                      <CheckCircle className="suggestions-icon" />
                      Suggestions for Improvement
                    </h4>
                    <div className="suggestions-list">
                      {result.suggestions && result.suggestions.length > 0 ? (
                        result.suggestions.map((suggestion, index) => (
                          <div key={index} className="suggestion-item">
                            <p className="suggestion-text">{suggestion}</p>
                          </div>
                        ))
                      ) : (
                        <p className="no-suggestions">No suggestions available</p>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Features Section */}
          <div className="features-grid">
            <div className="feature">
              <div className="feature-icon-wrapper icon-blue">
                <Zap className="feature-icon" />
              </div>
              <h4 className="feature-title">AI-Powered Analysis</h4>
              <p className="feature-description">
                Advanced language models analyze your resume against job requirements
              </p>
            </div>
            
            <div className="feature">
              <div className="feature-icon-wrapper icon-purple">
                <CheckCircle className="feature-icon" />
              </div>
              <h4 className="feature-title">Actionable Feedback</h4>
              <p className="feature-description">
                Get specific, targeted suggestions to improve your resume
              </p>
            </div>
            
            <div className="feature">
              <div className="feature-icon-wrapper icon-green">
                <FileText className="feature-icon" />
              </div>
              <h4 className="feature-title">Multi-Format Support</h4>
              <p className="feature-description">
                Upload resumes in PDF or DOCX format for instant analysis
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <p className="footer-text">
            © 2025 SkillSync. Powered by AI to help you land your dream job.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
import { useState } from "react";
import { analyzeResume } from "./api";

function App() {
  const [file, setFile] = useState(null);
  const [jobTitle, setJobTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showRawText, setShowRawText] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== "application/pdf") {
        setError("Please select a PDF file");
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError(null);
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a PDF file to analyze");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const analysisResult = await analyzeResume(file, jobTitle);
      setResult(analysisResult);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  const getCategoryColor = (score, max) => {
    const percentage = (score / max) * 100;
    if (percentage >= 80) return "bg-green-500";
    if (percentage >= 60) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          AI Resume Analyzer
        </h1>
        <p className="text-white text-opacity-90">
          Upload your resume and get instant AI-powered insights
        </p>
      </div>

      {/* Upload Card */}
      <div className="bg-white rounded-lg shadow-xl p-8 mb-6">
        <div className="space-y-6">
          {/* Job Title Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Job Title (Optional)
            </label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              placeholder="e.g., Software Engineer, Data Scientist"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
              disabled={loading}
            />
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Resume (PDF only)
            </label>
            <div className="flex items-center justify-center w-full">
              <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <svg
                    className="w-10 h-10 mb-3 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                  <p className="mb-2 text-sm text-gray-500">
                    <span className="font-semibold">Click to upload</span> or
                    drag and drop
                  </p>
                  <p className="text-xs text-gray-500">PDF files only</p>
                </div>
                <input
                  type="file"
                  className="hidden"
                  accept=".pdf"
                  onChange={handleFileChange}
                  disabled={loading}
                />
              </label>
            </div>
            {file && (
              <p className="mt-2 text-sm text-green-600">
                Selected: {file.name}
              </p>
            )}
          </div>

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition ${
              !file || loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-lg"
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Analyzing...
              </span>
            ) : (
              "Analyze Resume"
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 fade-in">
          <p className="font-semibold">Error</p>
          <p>{error}</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6 fade-in">
          {/* Score Card */}
          <div className="bg-white rounded-lg shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Overall Score
            </h2>
            <div className="text-center">
              <div
                className={`text-6xl font-bold ${getScoreColor(result.score)}`}
              >
                {result.score}
                <span className="text-3xl">/100</span>
              </div>
              <p className="text-gray-600 mt-2">
                {result.score >= 80
                  ? "Excellent resume!"
                  : result.score >= 60
                  ? "Good resume with room for improvement"
                  : "Needs significant improvement"}
              </p>
            </div>

            {/* Breakdown */}
            <div className="mt-8 space-y-4">
              <h3 className="text-lg font-semibold text-gray-800">
                Score Breakdown
              </h3>

              {Object.entries(result.breakdown).map(([category, score]) => {
                const maxScores = {
                  experience: 30,
                  skills: 35,
                  education: 15,
                  format: 10,
                  keywords: 10,
                };
                const max = maxScores[category];
                const percentage = (score / max) * 100;

                return (
                  <div key={category}>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700 capitalize">
                        {category}
                      </span>
                      <span className="text-sm font-medium text-gray-700">
                        {score.toFixed(1)} / {max}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div
                        className={`h-2.5 rounded-full ${getCategoryColor(
                          score,
                          max
                        )}`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Skills & Experience */}
          <div className="bg-white rounded-lg shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Detected Information
            </h2>

            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Years of Experience
              </h3>
              <p className="text-3xl font-bold text-purple-600">
                {result.years_experience}{" "}
                {result.years_experience === 1 ? "year" : "years"}
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Skills Found ({result.skills.length})
              </h3>
              {result.skills.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {result.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 italic">No skills detected</p>
              )}
            </div>
          </div>

          {/* AI Suggestions */}
          <div className="bg-white rounded-lg shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              AI-Powered Suggestions
            </h2>

            {/* Improvement Suggestions */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-3">
                Recommendations
              </h3>
              <ul className="space-y-2">
                {result.suggestions.suggestions?.map((suggestion, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-purple-600 mr-2 mt-1">•</span>
                    <span className="text-gray-700">{suggestion}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Rewritten Bullet */}
            {result.suggestions.rewritten_bullet && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                  Example: Stronger Bullet Point
                </h3>
                <div className="bg-green-50 border-l-4 border-green-500 p-4">
                  <p className="text-gray-800">
                    {result.suggestions.rewritten_bullet}
                  </p>
                </div>
              </div>
            )}

            {/* Suggested Title */}
            {result.suggestions.title && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                  Suggested Resume Title
                </h3>
                <p className="text-xl font-semibold text-purple-600">
                  {result.suggestions.title}
                </p>
              </div>
            )}

            {/* ATS Keywords */}
            {result.suggestions.ats_keywords?.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                  Recommended ATS Keywords
                </h3>
                <div className="flex flex-wrap gap-2">
                  {result.suggestions.ats_keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Error from AI (if any) */}
            {result.suggestions.error && (
              <div className="mt-4 bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded">
                <p className="text-sm">{result.suggestions.error}</p>
              </div>
            )}
          </div>

          {/* Raw Text Preview (Collapsible) */}
          <div className="bg-white rounded-lg shadow-xl p-8">
            <button
              onClick={() => setShowRawText(!showRawText)}
              className="w-full flex items-center justify-between text-left"
            >
              <h2 className="text-2xl font-bold text-gray-800">
                Raw Text Preview
              </h2>
              <svg
                className={`w-6 h-6 transition-transform ${
                  showRawText ? "transform rotate-180" : ""
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            {showRawText && (
              <div className="mt-4">
                <pre className="bg-gray-50 p-4 rounded text-sm text-gray-700 overflow-x-auto whitespace-pre-wrap">
                  {result.raw_text_preview}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="text-center mt-8 text-white text-opacity-75 text-sm">
        <p>Your resume is processed securely and not stored.</p>
        <p className="mt-1">Powered by OpenAI GPT</p>
      </div>
    </div>
  );
}

export default App;

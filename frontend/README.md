# AI Resume Analyzer - Frontend

React frontend for the AI Resume Analyzer application.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Backend URL (Optional)

The frontend is configured to connect to the backend at `http://localhost:8000` by default.

If your backend runs on a different URL, update the `API_BASE_URL` in `src/api.js`.

### 3. Run Development Server

```bash
npm run dev
```

The application will open automatically in your browser at `http://localhost:5173`

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

To preview the production build:

```bash
npm run preview
```

## Features

- **File Upload**: Upload PDF resumes for analysis
- **Job Title Input**: Optional job title for targeted suggestions
- **Real-time Analysis**: Get instant feedback on resume quality
- **Score Breakdown**: See detailed scoring by category
- **Skills Detection**: View all detected skills
- **AI Suggestions**: Get actionable improvement recommendations
- **ATS Keywords**: Discover important keywords for applicant tracking systems

## Technology Stack

- React 18
- Vite (build tool)
- Tailwind CSS (styling)
- Native Fetch API (HTTP requests)

## Troubleshooting

### Backend Connection Errors

Make sure the backend is running on `http://localhost:8000`. Check the browser console for detailed error messages.

### CORS Issues

The backend must allow requests from `http://localhost:5173`. This is configured by default in the backend's CORS middleware.

### File Upload Issues

- Only PDF files are accepted
- Maximum file size depends on your backend configuration
- Ensure the PDF contains extractable text (not scanned images)

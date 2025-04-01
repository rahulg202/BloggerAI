# BloggerAI - Content Calendar Generator

BloggerAI is a Streamlit-based application that leverages Google's Gemini AI to automatically generate blog content calendars and full blog posts based on your keywords, SEO insights, and ideal customer profiles.


## Features

- **Automated Content Calendar Generation:** Create a customized content calendar for up to 12 months with your specified posting frequency
- **SEO-Optimized Blog Topics:** Generate blog topics that incorporate your target keywords
- **ICP-Targeted Content:** Tailor content to your Ideal Customer Profile
- **Full Blog Post Generation:** Create complete, well-structured blog posts with a single click
- **Easy Export:** Download your content calendar as CSV and blog posts as Markdown files

## Installation

### Prerequisites

- Python 3.7+
- Pip package manager

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bloggerai.git
   cd bloggerai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

The application will be accessible at `http://localhost:8501` in your web browser.

## Usage

### 1. Setup

In the "Setup" tab:

- Upload your JSON file containing target keywords (required format below)
- Upload your text file with SEO recommendations
- Upload your JSON file with Ideal Customer Profile data
- Configure your calendar settings:
  - Start date for the content calendar
  - Duration in months (1-12)
  - Number of blog posts per week (1-7)
- Click "Load Data & Generate Calendar" to create your content calendar

### 2. Content Calendar

In the "Calendar" tab:

- View your generated content calendar
- Download the calendar as a CSV file

### 3. Generate Blog Posts

In the "Generate Blog" tab:

- Select a blog topic from the dropdown menu
- Click "Generate Blog Post" to create a full blog post
- View the generated blog content
- Download the blog post as a Markdown file

## File Formats

### Keywords JSON Format

```json
{
  "all_keywords": [
    "content marketing",
    "SEO strategy",
    "blog optimization",
    "content calendar",
    "keyword research"
  ]
}
```

Alternatively, you can provide a simple array of keywords:

```json
[
  "content marketing",
  "SEO strategy",
  "blog optimization",
  "content calendar",
  "keyword research"
]
```

### SEO Recommendations Format

A plain text file containing your SEO insights and recommendations.

### ICP (Ideal Customer Profile) JSON Format

```json
{
  "industries": ["SaaS", "E-commerce", "Digital Marketing"],
  "company_size": "Small to Medium Business",
  "roles": ["Marketing Manager", "Content Strategist", "Digital Marketing Specialist"],
  "challenges": [
    "Maintaining consistent content publication",
    "Creating SEO-optimized content",
    "Generating engaging blog topics"
  ],
  "goals": [
    "Increase organic traffic",
    "Improve content quality",
    "Save time on content planning"
  ]
}
```

## Deployment

The application can be deployed using various methods:

### Streamlit Sharing

Deploy directly through [Streamlit Sharing](https://streamlit.io/sharing) for a quick setup.

### Docker

Build and run with Docker:

```bash
docker build -t bloggerai .
docker run -p 8501:8501 bloggerai
```

### Google Cloud Run

Deploy to Google Cloud Run using the included app.yaml:

```bash
gcloud app deploy
```

## Technical Details

BloggerAI is built with:

- **Streamlit**: For the web interface
- **Google Generative AI (Gemini)**: For content generation
- **Pandas**: For data handling and CSV export

## Limitations

- Requires proper JSON formatting for input files
- Content generation quality depends on the specificity of your input data
- API rate limits may apply based on your Gemini API usage

## Future Improvements

- Content templates customization
- Image generation for blog posts
- Direct publishing to WordPress, Medium, etc.
- Analytics to track content performance

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Google Generative AI](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)

---

Made with ❤️ by Rahul Gupta

import streamlit as st
import json
import os
import datetime
import time
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import pandas as pd
import tempfile

class BlogCalendarGenerator:
    def __init__(self):
        self.api_key = "AIzaSyA4D8zZIEh3Olm8GCoRz6Mde4Eq-fS93no" 
        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.keywords = []
        self.seo_insights = ""
        self.icp_data = {}
        self.blog_calendar = []
        self.current_blog_index = 0
        self.blogs = []

    def load_data(self, keywords_data, seo_data, icp_data) -> None:
        """Load all required data files."""
        
        try:
            if isinstance(keywords_data, dict) and "all_keywords" in keywords_data:
                self.keywords = keywords_data["all_keywords"]
            else:
                self.keywords = keywords_data
            st.success("✅ Successfully loaded keywords")
        except Exception as e:
            st.error(f"❌ Error loading keywords: {str(e)}")
            raise

        try:
            self.seo_insights = seo_data
            st.success("✅ Successfully loaded SEO insights")
        except Exception as e:
            st.error(f"❌ Error loading SEO insights: {str(e)}")
            raise

        try:
            self.icp_data = icp_data
            st.success("✅ Successfully loaded ICP data")
        except Exception as e:
            st.error(f"❌ Error loading ICP data: {str(e)}")
            raise

    def generate_calendar(self, start_date: datetime.date, duration_months: int = 6, blogs_per_week: int = 2) -> List[Dict[str, Any]]:
        """Generate a blog calendar for the specified duration."""
        with st.status("🔄 Generating blog calendar..."):
            
            prompt = f"""
            Create a {duration_months}-month blog content calendar with {blogs_per_week} blog posts per week starting from {start_date.strftime('%Y-%m-%d')}.

            Here are the important keywords that must be incorporated into the blog topics:
            {json.dumps(self.keywords, indent=2)}

            Here are the SEO insights to consider:
            {self.seo_insights}

            Here is the Ideal Customer Profile information:
            {json.dumps(self.icp_data, indent=2)}

            For each blog post, provide:
            1. Publishing date (starting from {start_date.strftime('%Y-%m-%d')}, typically on working days)
            2. Blog title
            3. Primary target keyword
            4. Brief description (2-3 sentences)

            Return the information as a valid JSON array with objects containing these fields:
            "date", "title", "primary_keyword", "description"
            """

            try:
                response = self.model.generate_content(prompt)
                response_text = response.text

                json_start = response_text.find('[')
                json_end = response_text.rfind(']') + 1

                if json_start == -1 or json_end == 0:
                    raise ValueError("Failed to parse JSON response from LLM")

                json_str = response_text[json_start:json_end]
                self.blog_calendar = json.loads(json_str)

                st.success(f"✅ Successfully generated a blog calendar with {len(self.blog_calendar)} topics")
                return self.blog_calendar

            except Exception as e:
                st.error(f"❌ Error generating blog calendar: {str(e)}")
                raise

    def display_calendar(self) -> pd.DataFrame:
        """Display the generated blog calendar in a tabular format."""
        if not self.blog_calendar:
            st.warning("⚠ No blog calendar generated yet.")
            return pd.DataFrame()

        df = pd.DataFrame(self.blog_calendar)
        return df

    def generate_blog(self, blog_index: int) -> Dict[str, Any]:
        """Generate a full blog post based on a topic from the calendar."""
        if not self.blog_calendar:
            st.warning("⚠ No blog calendar generated yet.")
            return {}

        if blog_index >= len(self.blog_calendar):
            st.warning("⚠ No more blog topics in the calendar.")
            return {}

        blog_topic = self.blog_calendar[blog_index]
        
        with st.status(f"🔄 Generating blog: {blog_topic['title']}..."):
            
            prompt = f"""
            Write a complete blog post based on the following information:

            Blog title: {blog_topic['title']}
            Primary keyword: {blog_topic['primary_keyword']}
            Description: {blog_topic['description']}
            Publishing date: {blog_topic['date']}

            Consider these SEO insights:
            {self.seo_insights}

            Consider this Ideal Customer Profile:
            {json.dumps(self.icp_data, indent=2)}

            Additional keywords to incorporate:
            {json.dumps([k for k in self.keywords if k != blog_topic['primary_keyword']][:5], indent=2)}

            Create a comprehensive blog post with:
            1. Engaging introduction
            2. 4-6 structured sections with subheadings (H2s and H3s)
            3. Actionable tips or insights
            4. Conclusion with call-to-action
            5. Total word count: 1200-1500 words

            Format the blog post in Markdown.
            """

            try:
                response = self.model.generate_content(prompt)
                blog_content = response.text

                blog = {
                    "index": blog_index,
                    "date": blog_topic['date'],
                    "title": blog_topic['title'],
                    "primary_keyword": blog_topic['primary_keyword'],
                    "content": blog_content
                }

                self.blogs.append(blog)
                
                return blog

            except Exception as e:
                st.error(f"❌ Error generating blog: {str(e)}")
                raise

def main():
    st.set_page_config(page_title="BloggerAI - Content Calendar Generator", layout="wide")
    
    st.title("BloggerAI - Content Calendar Generator")
    st.markdown("""
    This application helps you generate a content calendar and write blog posts using AI.
    Upload your keyword data, SEO insights, and ICP (Ideal Customer Profile) data to get started.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Setup", "Calendar", "Generate Blog"])
    
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'calendar_df' not in st.session_state:
        st.session_state.calendar_df = None
    if 'blog_content' not in st.session_state:
        st.session_state.blog_content = None
    
    with tab1:
        st.header("1. Setup")
        
        keywords_file = st.file_uploader("Upload Keywords JSON File", type=['json'], 
                                       help="JSON file containing keywords to target in blog posts.")
        
        seo_file = st.file_uploader("Upload SEO Recommendations File", type=['txt'], 
                                   help="Text file containing SEO insights and recommendations.")
        
        icp_file = st.file_uploader("Upload ICP Data JSON File", type=['json'], 
                                  help="JSON file containing Ideal Customer Profile data.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start Date", 
                                      value=datetime.date.today() + datetime.timedelta(days=(7 - datetime.date.today().weekday()) % 7),
                                      help="Date to start the content calendar (defaults to next Monday)")
        with col2:
            duration_months = st.number_input("Duration (Months)", min_value=1, max_value=12, value=6,
                                            help="Number of months to generate the calendar for")
        with col3:
            blogs_per_week = st.number_input("Blogs Per Week", min_value=1, max_value=7, value=2,
                                           help="Number of blog posts to generate per week")
        
        if st.button("Load Data & Generate Calendar"):
            if not keywords_file or not seo_file or not icp_file:
                st.error("Please upload all required files")
            else:
                try:
                    keywords_data = json.load(keywords_file)
                    seo_data = seo_file.read().decode()
                    icp_data = json.load(icp_file)
                    
                    # Initialize generator with hard-coded API key
                    generator = BlogCalendarGenerator()
                    generator.load_data(keywords_data, seo_data, icp_data)
                    
                    generator.generate_calendar(start_date, duration_months, blogs_per_week)
                    
                    st.session_state.generator = generator
                    st.session_state.calendar_df = generator.display_calendar()
                    
                    st.success("Calendar generated successfully! Go to the Calendar tab to view it.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.header("2. Content Calendar")
        
        if st.session_state.calendar_df is not None:
            st.dataframe(st.session_state.calendar_df, use_container_width=True)
            
            csv = st.session_state.calendar_df.to_csv(index=False)
            st.download_button(
                label="Download Calendar as CSV",
                data=csv,
                file_name=f"blog_calendar_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No calendar generated yet. Go to the Setup tab to generate one.")
    
    with tab3:
        st.header("3. Generate Blog Post")
        
        if st.session_state.generator is not None and st.session_state.calendar_df is not None:
            blog_options = [f"{i+1}: {row['title']}" for i, row in st.session_state.calendar_df.iterrows()]
            selected_blog = st.selectbox("Select blog to generate", blog_options)
            
            if st.button("Generate Blog Post"):
                try:
                    blog_index = int(selected_blog.split(":")[0]) - 1
                    blog = st.session_state.generator.generate_blog(blog_index)
                    st.session_state.blog_content = blog
                    st.success("Blog generated successfully!")
                except Exception as e:
                    st.error(f"Error generating blog: {str(e)}")
            
            if st.session_state.blog_content:
                st.subheader(st.session_state.blog_content["title"])
                st.markdown(f"*Date:* {st.session_state.blog_content['date']}")
                st.markdown(f"*Primary Keyword:* {st.session_state.blog_content['primary_keyword']}")
                
                with st.expander("View Blog Content", expanded=True):
                    st.markdown(st.session_state.blog_content["content"])
                
                st.download_button(
                    label="Download Blog as Markdown",
                    data=f"# {st.session_state.blog_content['title']}\n\nDate: {st.session_state.blog_content['date']}\n\n{st.session_state.blog_content['content']}",
                    file_name=f"blog_{st.session_state.blog_content['index'] + 1}{st.session_state.blog_content['title'].replace(' ', '')[:30]}.md",
                    mime="text/markdown"
                )
        else:
            st.info("No calendar generated yet. Go to the Setup tab to generate one.")

if __name__ == "__main__":
    main()
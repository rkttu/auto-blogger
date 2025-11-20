"""Blog post generator using LangChain."""

from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .config import Config
from .mcp_client import run_async_research, ResearchHelper


class BlogGenerator:
    """Generate blog posts using LangChain and OpenAI."""
    
    LENGTH_GUIDELINES = {
        "short": "300-500 words",
        "medium": "800-1200 words",
        "long": "1500-2500 words"
    }
    
    def __init__(self, config: Config):
        """Initialize the blog generator with configuration."""
        self.config = config
        
        # Initialize ChatOpenAI with optional custom base URL
        llm_kwargs = {
            "model": config.model,
            "temperature": config.temperature,
            "api_key": config.openai_api_key,
        }
        
        if config.openai_api_base:
            llm_kwargs["base_url"] = config.openai_api_base
        
        self.llm = ChatOpenAI(**llm_kwargs)
    
    def generate(
        self,
        topic: str,
        language: str = "Korean",
        tone: str = "professional",
        length: str = "medium",
        use_research: bool = False,
        use_front_matter: bool = False,
        author: str = "Auto-Blogger"
    ) -> str:
        """Generate a blog post on the given topic."""
        
        length_guideline = self.LENGTH_GUIDELINES.get(length, self.LENGTH_GUIDELINES["medium"])
        
        # Gather research materials if enabled and MCP servers are configured
        research_context = ""
        if use_research and self.config.mcp_servers:
            try:
                references = run_async_research(self.config.mcp_servers, topic)
                if references:
                    helper = ResearchHelper(self.config.mcp_servers)
                    research_context = helper.format_references(references)
            except Exception as e:
                print(f"Warning: Could not gather research materials: {e}")
        
        system_message = """You are an expert blog writer who creates engaging, well-structured, and informative blog posts.
Your writing is clear, compelling, and tailored to the specified tone and audience.

IMPORTANT FORMATTING RULES:
- Write in clean Markdown format that passes markdown linters
- DO NOT use numbered prefixes in headings (e.g., avoid "1.1 Title", "2.3 Section")
- Use plain heading text only (e.g., "## Introduction" not "## 1. Introduction")
- DO NOT add date, author signature, or metadata at the end of the article
- Start the article with a blockquote (using >) containing an AI attribution notice in the target language
- The attribution should state that this article was written with partial assistance from generative AI
- Ensure proper spacing: blank lines before and after headings, lists, and code blocks
- Use consistent list markers (- for unordered, 1. 2. 3. for ordered)
- Properly indent nested lists with 2 or 4 spaces
- Add language identifiers to code blocks (e.g., ```python, ```bash, ```csharp)
- Avoid trailing spaces at end of lines
- Use proper link and image syntax
- Ensure proper table formatting with aligned columns

CONTENT STRUCTURE:
- AI attribution notice in blockquote format at the very beginning
- An attention-grabbing introduction
- Well-organized main content with clear sections
- Relevant examples or insights
- A strong conclusion
- Natural flow and readability"""

        if research_context:
            system_message += "\n\nYou have access to reference materials that you should use to enrich your content with accurate information and insights."
        
        user_message = """Write a blog post with the following specifications:

Topic: {topic}
Language: {language}
Tone: {tone}
Target Length: {length_guideline}"""

        if research_context:
            user_message += "\n{research_context}"
        
        user_message += """

Please write a complete blog post in {language} that:
1. Starts with an AI attribution notice in a blockquote (>) stating this was written with AI assistance
2. Has an engaging title (without numbering)
3. Includes a compelling introduction
4. Covers the topic thoroughly with well-structured sections (use clean headings without numbers)
5. Uses the specified {tone} tone consistently
6. Ends with a memorable conclusion
7. Targets approximately {length_guideline}
8. Follows markdown best practices (proper spacing, code block languages, clean formatting)
9. Does NOT include author signature, date, or metadata at the end"""

        if research_context:
            user_message += "\n10. Incorporates insights from the provided reference materials naturally"
        
        user_message += "\n\nFormat the output in Markdown."
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", user_message)
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        invoke_params = {
            "topic": topic,
            "language": language,
            "tone": tone,
            "length_guideline": length_guideline
        }
        
        if research_context:
            invoke_params["research_context"] = research_context
        
        result = chain.invoke(invoke_params)
        
        # Add YAML front matter if requested (AI already added attribution in content)
        if use_front_matter:
            result = self._add_front_matter(result, topic, author, language, tone)
        
        return result
    
    def _add_front_matter(self, content: str, topic: str, author: str, language: str, tone: str) -> str:
        """Add YAML front matter to the blog post."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        front_matter = f"""---
title: "{topic}"
date: {today}
author: {author}
language: {language}
tone: {tone}
---

"""
        return front_matter + content

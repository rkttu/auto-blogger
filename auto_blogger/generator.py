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
        author: str = "Auto-Blogger"
    ) -> str:
        """Generate a blog post on the given topic with SEO-optimized front matter.
        
        This uses a two-phase approach:
        Phase 1: Generate main content
        Phase 2: Analyze content and generate front matter (title, keywords, abstract)
        """
        
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
        
        # Phase 1: Generate main content
        content = chain.invoke(invoke_params)
        
        # Phase 2: Generate SEO-optimized front matter with keywords and abstract
        result = self._add_front_matter_with_metadata(content, topic, author, language)
        
        return result
    
    def _add_front_matter_with_metadata(self, content: str, topic: str, author: str, language: str) -> str:
        """Add SEO-optimized YAML front matter with auto-generated keywords and abstract.
        
        This analyzes the content to generate:
        - Relevant SEO keywords (5-8 keywords)
        - Marketing-friendly abstract (2-3 sentences)
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Generate keywords and abstract using LLM
        metadata = self._generate_metadata(content, language)
        
        # Build front matter with all metadata
        front_matter = f"""---
title: "{topic}"
date: {today}
author: {author}
language: {language}
keywords:
"""
        
        for keyword in metadata["keywords"]:
            front_matter += f"  - {keyword}\n"
        
        front_matter += f"""abstract: |
  {metadata["abstract"]}
---

"""
        return front_matter + content
    
    def _generate_metadata(self, content: str, language: str) -> dict:
        """Generate SEO keywords and abstract from the content."""
        
        metadata_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an SEO and content marketing expert. 
Analyze the provided blog post content and generate:
1. 5-8 relevant SEO keywords/phrases that would help this article rank well
2. A compelling 2-3 sentence abstract that summarizes the article in a marketing-friendly way

Respond in JSON format with 'keywords' (array of strings) and 'abstract' (single string) fields.
Use the same language as the article."""),
            ("user", """Analyze this blog post and generate SEO metadata:

{content}

Generate keywords and abstract in {language}.""")
        ])
        
        chain = metadata_prompt | self.llm | StrOutputParser()
        
        result = chain.invoke({
            "content": content[:3000],  # Limit content length for efficiency
            "language": language
        })
        
        # Parse JSON response
        import json
        try:
            metadata = json.loads(result)
            # Ensure we have the expected structure
            if "keywords" not in metadata or "abstract" not in metadata:
                raise ValueError("Missing required metadata fields")
            return metadata
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback to basic metadata if parsing fails
            print(f"Warning: Could not parse metadata, using defaults: {e}")
            return {
                "keywords": ["blog", "article", "content"],
                "abstract": "An informative article generated by Auto-Blogger."
            }

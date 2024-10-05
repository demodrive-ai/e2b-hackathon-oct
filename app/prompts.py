from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser



extract_is_blog_post_technical_prompt = ChatPromptTemplate.from_template("""
You are a software engineer. Given a blog post, you are going to answer the following questions:
                                                                         
1. Is this blog post technical?
2. Does this blog post have a code recipe/how-to guide you can follow to use some tool or achieve some outcome?
                                                                                                                                                  
## Blog post: 

{blog_post}
""")


extract_code_metadata_prompt = ChatPromptTemplate.from_template("""
You are a software engineer. Given a blog post, you are going to answer the following questions:
                                                                         
Find all the self-contained code examples/recipes given in this blog. Make sure each code file content is end to end runnable.

## Blog post: 

{blog_post}
""")
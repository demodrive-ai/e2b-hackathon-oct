from langchain_core.prompts import ChatPromptTemplate


extract_is_blog_post_technical_prompt = ChatPromptTemplate.from_template("""
You are a software engineer. Given a blog post, you are going to answer the following questions:

1. Is this blog post technical?
2. Does this blog post have a code recipe/how-to guide you can follow to use some tool or achieve some outcome?

## Blog post:

{blog_post}
""")


extract_all_code_recipes_prompt = ChatPromptTemplate.from_template("""
You are a software engineer. Given a blog post, you are going to answer the following questions:

What are all the code recipes/how-to guides in this blog post?

## Guidelines:

1. All variations of doing something is considered a different recipe.
2. If there is no code related details of the recipe then ignore it.
3. Each recipe description should have end to end meaning. Prefer complete meaningful recipes over things that could be part of a bigger recipe.
4. If same recipe is show in different languages then its a different recipe for every language.


## Blog post:

{blog_post}
""")


extract_code_metadata_prompt = ChatPromptTemplate.from_template("""
You are a software engineer. Given the following blog post, you are going to extract the details of the code project from the blog post.

Look at the description of the code recipe you need to extract below.

## Code Recipe Description:

{code_recipe_description}

## Guidelines for good code recipe:

1. The code should be self-contained and run end to end in the same file. You may have to intelligently piece things together here.
3. The code file should not have anything but code. No commands like pip install, npm install, etc.
4. .env files should have all the important keys in it. Sometimes the keys are implicit in the code and not mentioned explicitly. If you think it will be helpful to have a env variable then add it. better safe than sorry.
5. For all python recipes it should have requirements.txt, .env for environment variables, main.py for all the self-contained code and command to run the project. Carefully make sure the requirements.txt and .env are complete. Somethings this can be tricky.
6. If it is a javascript/typescript project then it should have package.json, .env for environment variables, index.js for all the self-contained code and command to run the project.
7. Review all the code files in the recipes to make sure nothing is missing wholistically.

# Blog post:

{blog_post}
""")

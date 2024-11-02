import os
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Set up paths and Jinja2 environment
CONTENT_DIR = 'content/blog'
OUTPUT_DIR = 'output/blog'
TEMPLATE_DIR = 'templates'
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def parse_markdown(file_path):
    """Convert Markdown file to HTML and extract metadata."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract metadata and content
    meta, content = {}, []
    for line in lines:
        if line.startswith('Title:'):
            meta['title'] = line[len('Title:'):].strip()
        elif line.startswith('Date:'):
            meta['date'] = line[len('Date:'):].strip()
        else:
            content.append(line)
    
    meta['content'] = markdown.markdown(''.join(content))
    return meta

def generate_blog_index(posts):
    """Render the blog index page."""
    template = env.get_template('blog_index.html')
    rendered_html = template.render(posts=posts)
    with open(os.path.join('output', 'blog', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def generate_blog_post(post, filename):
    """Render an individual blog post page."""
    template = env.get_template('blog_post.html')
    rendered_html = template.render(
        title=post['title'], date=post['date'], content=post['content']
    )
    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def build_site():
    """Main function to generate the site."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Parse each markdown file in content/blog
    posts = []
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            file_path = os.path.join(CONTENT_DIR, filename)
            post = parse_markdown(file_path)
            post_url = f"{filename[:-3]}.html"
            post['url'] = os.path.join('blog', post_url)
            posts.append(post)
            
            # Generate individual blog post page
            generate_blog_post(post, post_url)
    
    # Sort posts by date (assuming format 'YYYY-MM-DD')
    posts.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    
    # Generate the blog index page
    generate_blog_index(posts)

if __name__ == '__main__':
    build_site()


# Lain Is Real Blog

A neural interface for digital consciousness - a Django-powered blog platform with markdown editing, real-time preview, and cyberpunk aesthetics. Present in the Wired as a fusion of content management and visual expression. Let's all love Lain.

## Features

- User authentication and authorization
- Markdown content editor with live preview
- Rich taxonomy with categories and tags
- Image uploads and gallery management
- Comment and reply system
- Search functionality
- Responsive design for all devices
- Admin dashboard with content management
- Post scheduling and draft saving
- Cyberpunk-inspired UI with Lain aesthetics

## Tech Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **Markdown**: markdown-deux
- **Styling**: Custom CSS with cyberpunk-inspired design
- **Icons**: Font Awesome
- **Development Tools**: Django Debug Toolbar

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
   ```
   git clone https://github.com/glitchidea/lain-blog.git
   cd lain-blog
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```
   python manage.py migrate
   ```

5. Create a superuser
   ```
   python manage.py createsuperuser
   ```

6. Run the development server
   ```
   python manage.py runserver
   ```

7. Access the blog at http://127.0.0.1:8000/

## Project Structure

- `apps/` - Django applications
  - `accounts/` - User profiles and account management
  - `blog/` - Blog posts, categories, tags
  - `comments/` - Comment functionality
  - `media/` - Media file management
- `static/` - Static files (CSS, JS, images)
- `templates/` - HTML templates
- `media/` - User-uploaded content
- `blogger/` - Project settings

## Usage

### Creating Blog Posts

1. Log in as a superuser or staff member
2. Click on "New Post" in the navigation menu
3. Use the markdown editor to write content
4. Add categories and tags
5. Save as draft or publish immediately

### Managing Categories

1. Log in to the admin dashboard
2. Navigate to the Blog > Categories section
3. Create, edit or delete categories

### Uploading Images

1. While editing a post, click on the image button
2. Upload a new image or select from the gallery
3. Images can be inserted anywhere in your content

## Customization

### Themes

The blog comes with a cyberpunk-inspired design featuring Lain aesthetics. You can customize the appearance by editing the CSS files in the `static/css/` directory.

### Settings

Key settings can be modified in `blogger/settings.py`:

- `BLOG_POSTS_PER_PAGE`: Number of posts to display per page
- `BLOG_ALLOW_COMMENTS`: Enable/disable comments globally
- `BLOG_AUTO_EXCERPT_LENGTH`: Length of auto-generated excerpts

## Production Deployment

For production deployment:

1. Update `SECRET_KEY` in settings
2. Set `DEBUG = False`
3. Configure PostgreSQL database
4. Set up a proper web server (Nginx, Apache)
5. Configure static files with Whitenoise
6. Use a production-ready email backend

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django
- Django AllAuth
- Markdown Deux
- Font Awesome
- Serial Experiments Lain

*Present day... Present time! HAHAHAHA!* 
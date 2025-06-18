from datetime import datetime
import math
import os
from flask import current_app, flash, render_template, request, send_from_directory
from flask_smorest import Blueprint
from flask_login import login_required
import requests
from iSaksham.app.models.chapters import Chapters
from iSaksham.app.models.modules import Modules
from flask_login import login_required
from iSaksham.app.models.feedback import Feedback
from iSaksham.app.models.user import User  # Importing User model
# Importing login_required decorator

blp = Blueprint("learning","learning","Routes to LMS")
CAPTCHA_SECRET_KEY = os.getenv('CAPTCHA_SECRET_KEY',' ')


# Route for the home page
@blp.route('/')
@blp.route('/home')
def home():
    return render_template('home.html')  # Rendering home.html template

# Route for the FAQ page, accessible only to logged-in users
@blp.route('/faq')
# @login_required
def faq():
    return render_template('faq.html')  # Rendering faq.html template

# Route for the user manual page, accessible only to logged-in users

@blp.route('/user_manual')
# @login_required
def user_manual():
    return render_template('user_manual.html')  # Rendering user_manual.html template

# Route for the contact page
@blp.route('/contact')
def contact():
    return render_template('contact.html')  # Rendering contact.html template

# Route for the important links page
@blp.route('/important_links')
def important_links():
    return render_template('important_links.html')  # Rendering important_links.html template

# Route for the credits page
@blp.route('/credits')
def credits():
    return render_template('credits.html')  # Rendering credits.html template

@blp.route('/course_2018')
@login_required
def course_2018():
    modules = Modules.get_all()
    chapters = Chapters.get_all()
    
    accordion_title = []
    accordion_content = []
    
    for module in modules:
        content = []
        accordion_title.append({"id":module.id,"name":module.name})
        for chapter in chapters:
            if module.id == chapter.module_id:
                json = {"id":chapter.id,"module_id": chapter.module_id,"link": chapter.link,"length":chapter.length, "title":chapter.title}
                content.append(json)
        accordion_content.append(content)
        
    # Get count of feedback for category 'course'
    review = Feedback.query.filter_by(message_category='course').count()
    registered = User.query.count()
    return render_template('course_2018.html',accordion_content = accordion_content,accordion_title= accordion_title,registered=registered,review=review)

# Route for the course page, accessible only to logged-in users
@blp.route('/course_2024')
@login_required
def course_2024():
    
    return render_template('course_2024.html')  # Rendering course.html template

@blp.route('/play_chapter/<string:uuid>')
@login_required
def play_chapter(uuid):
    modules = Modules.get_all()
    chapters = Chapters.get_all()
    accordion_title = []
    accordion_content = []
    
    for module in modules:
        content = []
        accordion_title.append({"id":module.id,"name":module.name})
        for chapter in chapters:
            if module.id == chapter.module_id:
                json = {"id":chapter.id,"uuid":chapter.uuid,"module_id": chapter.module_id,"link": chapter.link,"length":chapter.length, "title":chapter.title}
                content.append(json)
        accordion_content.append(content)
        
    chapter_db = Chapters.get_chapters_by_uuid(uuid)
    if chapter_db:
        if chapter_db['link']:
            iframe = True
        else:
            iframe = False
    else:
        return render_template('developer/error.html', 
                            error_code=404, 
                            error_message="Page Not Found", 
                            description="The page you are looking for does not exist."), 404
    id = chapter_db['id']
    next_chapter = Chapters.get_chapters_by_id(id+1)
    if id != 0:
        previous_chapter=Chapters.get_chapters_by_id(id-1)
    else:
        previous_chapter = 0
    return render_template('play_chapter.html',iframe=iframe,accordion_content = accordion_content,accordion_title= accordion_title,chapter_db=chapter_db,next_chapter=next_chapter,previous_chapter=previous_chapter)

# Route for the feedback submission page
@blp.route('/feedback', methods=['POST', 'GET'])
@login_required
def feedback():
    if request.method == "POST":
        # Extracting form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_category = request.form.get('message_type')
        rating = request.form.get('rating')
        recaptcha_response = request.form.get('g-recaptcha-response')
        
        # If no response was provided, reject the submission
        if not recaptcha_response:
            flash('Please check the reCAPTCHA box.')
            return render_template('feedback.html')
        
        # Verify the reCAPTCHA response
        verification_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': CAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        )
        
        verification_result = verification_response.json()
        if not verification_result.get('success'):
            flash('reCAPTCHA verification failed. Please try again.')
            return render_template('feedback.html')
        
        if not rating:
            rating = request.form.get('rating-mobile')
        
        message = request.form.get('message')
        
        # Handle file upload
        image_filename = None
        if 'feedback_image' in request.files:
            file = request.files['feedback_image']
            if file and file.filename:
                # Ensure the filename is secure
                from werkzeug.utils import secure_filename
                import os
                
                # Define allowed file extensions
                ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
                
                # Function to check if file extension is allowed
                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
                
                if allowed_file(file.filename):
                    # Create a unique filename
                    filename = secure_filename(file.filename)
                    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                    
                    # Define upload folder
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    
                    # Create directory if it doesn't exist
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Save the file
                    file_path = os.path.join(upload_folder, unique_filename)
                    file.save(file_path)
                    
                    # Set the image filename to be stored in the database
                    image_filename = unique_filename
                else:
                    flash("Invalid file format. Please upload an image file (PNG, JPG, JPEG, GIF).")
                    return render_template('feedback.html')
        
        # Creating Feedback object and saving to database
        feedback = Feedback(name, email, subject, message_category, message, rating, image_filename)
        feedback.save_to_db()

        flash("Thank You for sharing your feedback")  # Flashing a message to indicate successful feedback submission
        return render_template('feedback.html')  # Rendering feedback.html template
    
    return render_template('feedback.html')  # Rendering feedback.html template for GET requests

@blp.route('/reviews')
def reviews():
    # Get page number from query parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of reviews per page
    
    # Get all feedback entries with message_category 'course'
    query = Feedback.query.filter_by(message_category='course')
    
    # Count total entries for pagination
    total_reviews = query.count()
    total_pages = math.ceil(total_reviews / per_page)
    
    # Get reviews for current page
    reviews = query.order_by(Feedback.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False).items
    
    return render_template('reviews.html', 
                          reviews=reviews,
                          current_page=page,
                          total_pages=total_pages)
    
@blp.route("/robots.txt")
def robots():
    static_folder = os.path.join(current_app.root_path, 'static')
    return send_from_directory(static_folder, "robots.txt")
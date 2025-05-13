from flask import render_template, request, jsonify, abort
from app import db
from jinja2 import TemplateNotFound
from app.models import ContactSubmission

def init_routes(app):

    @app.route('/')
    @app.route('/home')
    @app.route('/index')
    def home():
        return render_template('home/Home.html')

    @app.route('/services')
    def services_main():
        return render_template('services/services.html')

    @app.route('/services/<animal>')
    def services_page(animal):
        try:
            return render_template(f'services/{animal}.html', animal=animal)
        except TemplateNotFound:
            abort(404)

    @app.route('/about')
    def about():
        return render_template('about/about.html')

    @app.route('/about/process')
    def process():
        return render_template('about/process.html')

    @app.route('/contact')
    def contact():
        return render_template('contact/contact.html')

    @app.route('/api/contact', methods=["POST"])
    def contact_form_submission():
        data = request.get_json()   # Get JSON data from request
        print("\nReceived:", data, "\n")

        # Save to the database
        new_message = ContactSubmission(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            message=data.get("message"),
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({"message": "Message received and saved!"}), 200

    @app.route('/location')
    def location():
        return render_template('location/location.html')

    @app.route('/blog')
    def blog():
        return render_template('blog/blog.html')
    

    # @app.route('/submission_list')
    # def submission_list():
    #     # Query all submissions, ordered by newest first
    #     submissions = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).all()
        
    #     return render_template("submission/submission.html", submissions=submissions)


    # @app.route('/base')
    # def base():
    #     return render_template('base.html')
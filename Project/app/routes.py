from flask import render_template, request, jsonify, abort
from jinja2 import TemplateNotFound
from flask_mail import Message

from app.models import ContactSubmission
from app import db, mail

# debug
import logging


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
        FormData = request.form  # Make sure this is here before using `data`
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'message']
        if not all(FormData.get(field) for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        app.logger.debug("Form data received: %s", FormData)

        
        try:
            # Save to database
            new_message = ContactSubmission(
                first_name=FormData["first_name"],
                last_name=FormData["last_name"],
                email=FormData["email"],
                message=FormData["message"]
            )
            db.session.add(new_message)
            db.session.commit()

            # Send email to your team
            team_msg = Message(
                subject=f"New Contact: {FormData['first_name']} {FormData['last_name']}",
                recipients=["info@pestshieldgta.ca"]  # Your team's email
            )
            team_msg.body = f"""
            New contact form submission:
            
            Name: {FormData['first_name']} {FormData['last_name']}
            Email: {FormData['email']}
            Message: {FormData['message']}
            """
            mail.send(team_msg)

            # Send confirmation to client
            client_msg = Message(
                subject="Thank you for contacting PestShield GTA",
                recipients=[FormData['email']]
            )
            client_msg.body = f"""
            Dear {FormData['first_name']},
            
            Thank you for your message. We'll respond as soon as possible.
            
            Your message:
            {FormData['message']}
            
            Best regards,
            Pest Shield GTA Team
            """
            mail.send(client_msg)

            return jsonify({"message": "Message received and saved!"}), 200

        # except Exception as error:
        #     db.session.rollback()
        #     return jsonify({"error": str(error)}), 500
        
        except Exception as error:
            db.session.rollback()
            app.logger.error(f"Email error: {str(error)}")
            app.logger.error(f"Mail settings: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
            app.logger.error(f"Using auth: {app.config['MAIL_USERNAME']}")
            return jsonify({"error": str(error)}), 500


    @app.route('/location')
    def location():
        return render_template('location/location.html')

    @app.route('/blog')
    def blog():
        return render_template('blog/blog.html')
    

    # @app.route('/admin/submission_list')
    # def submission_list():
    #     # Query all submissions, ordered by newest first
    #     submissions = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).all()
        
    #     return render_template("submission/submission.html", submissions=submissions)


    # @app.route('/base')
    # def base():
    #     return render_template('base.html')


    # @app.route('/force-test-email')
    # def force_test_email():
    #     try:
    #         msg = Message(
    #             "FORCED Test Email", 
    #             recipients=["PestShieldGTA@gmail.com"],
    #             body="Manual test email from VPS"
    #         )
    #         mail.send(msg)
    #         app.logger.debug("✅ FORCED email sent successfully")
    #         return "Email forced successfully"
    #     except Exception as e:
    #         app.logger.error("❌ FORCED email failed", exc_info=True)
    #         return f"Email failed: {str(e)}"
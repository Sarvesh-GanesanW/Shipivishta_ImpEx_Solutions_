# routes.py
from flask import render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from forms import ContactForm  # Importing the ContactForm
from db import save_user_query, get_db_connection
import logging
import os
import openai

# Initialize logging
logging.basicConfig(level=logging.INFO)

def init_routes(app):
    @app.route('/')
    def home():
        try:
            logging.info("Accessed the home page")
            return render_template('index.html')
        except Exception as e:
            logging.error("Error accessing the home page: %s", e, exc_info=True)
            return jsonify({"error": "An error occurred accessing the home page"}), 500

    @app.route('/dgft')
    def dgft_services():
        try:
            logging.info("Accessed the DGFT Services page")
            return render_template('dgft_services.html')
        except Exception as e:
            logging.error("Error accessing the DGFT Services page: %s", e, exc_info=True)
            return jsonify({"error": "An error occurred accessing the DGFT Services page"}), 500

    @app.route('/customs')
    def customs_services():
        try:
            logging.info("Accessed the Customs Services page")
            return render_template('customs_services.html')
        except Exception as e:
            logging.error("Error accessing the Customs Services page: %s", e, exc_info=True)
            return jsonify({"error": "An error occurred accessing the Customs Services page"}), 500

    @app.route('/taxation')
    def taxation_services():
        try:
            logging.info("Accessed the Taxation Services page")
            return render_template('taxation_services.html')
        except Exception as e:
            logging.error("Error accessing the Taxation Services page: %s", e, exc_info=True)
            return jsonify({"error": "An error occurred accessing the Taxation Services page"}), 500

    @app.route('/regulatory-permits')
    def regulatory_permits():
        try:
            logging.info("Accessed the Regulatory Permits page")
            return render_template('regulatory_permits.html')
        except Exception as e:
            logging.error("Error accessing the Regulatory Permits page: %s", e, exc_info=True)
            return jsonify({"error": "An error occurred accessing the Regulatory Permits page"}), 500

    @app.route('/services/<category>')
    def services(category):
        form = ContactForm(request.form)
        try:
            logging.info(f"Accessed the {category} Services page")
            return render_template('service_template.html', category=category, form=form)
        except Exception as e:
            logging.error(f"Error accessing the {category} Services page: %s", e, exc_info=True)
            return jsonify({"error": f"An error occurred accessing the {category} Services page"}), 500

    @app.route('/services/dgft/<service>')
    def dgft_service(service):
        form = ContactForm(request.form)
        try:
            logging.info(f"Accessed the DGFT {service} page")
            return render_template('dgft_service_template.html', service=service, form=form)
        except Exception as e:
            logging.error(f"Error accessing the DGFT {service} page: %s", e, exc_info=True)
            return jsonify({"error": f"An error occurred accessing the DGFT {service} Services page"}), 500

    @app.route('/services/customs/<service>')
    def customs_service(service):
        form = ContactForm(request.form)
        try:
            logging.info(f"Accessed the Customs {service} page")
            return render_template('customs_service_template.html', service=service, form=form)
        except Exception as e:
            logging.error(f"Error accessing the Customs {service} page: %s", e, exc_info=True)
            return jsonify({"error": f"An error occurred accessing the Customs {service} Services page"}), 500

    @app.route('/services/taxation/<service>')
    def taxation_service(service):
        form = ContactForm(request.form)
        try:
            logging.info(f"Accessed the Taxation {service} page")
            return render_template('taxation_service_template.html', service=service, form=form)
        except Exception as e:
            logging.error(f"Error accessing the Taxation {service} page: %s", e, exc_info=True)
            return jsonify({"error": f"An error occurred accessing the Taxation {service} Services page"}), 500

    @app.route('/services/regulatory-permits/<service>')
    def regulatory_permits_service(service):
        form = ContactForm(request.form)
        try:
            logging.info(f"Accessed the Regulatory Permits {service} page")
            return render_template('regulatory_permits_service_template.html', service=service, form=form)
        except Exception as e:
            logging.error(f"Error accessing the Regulatory Permits {service} page: %s", e, exc_info=True)
            return jsonify({"error": f"An error occurred accessing the Regulatory Permits {service} Services page"}), 500

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user_query = {
                    'name': form.name.data,
                    'email': form.email.data,
                    'phone_number': form.phone_number.data,
                    'message': form.message.data
                }
                try:
                    save_user_query(user_query)
                    flash('Your query has been submitted successfully!', 'success')
                    return redirect(url_for('contact'))
                except Exception as e:
                    logging.error("Failed to save user query: %s", e, exc_info=True)
                    flash('Failed to submit your query. Please try again later.', 'danger')
            else:
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        flash(f"Error in {fieldName}: {err}", 'danger')
        return render_template('contact.html', form=form)

    @app.route('/resources')
    def resources():
        try:
            db = get_db_connection()
            resources_collection = db['Resources']
            resources = list(resources_collection.find({}))
            return render_template('resources.html', resources=resources)
        except Exception as e:
            logging.error("Failed to fetch resources: %s", e, exc_info=True)
            return jsonify({"error": "Failed to fetch resources"}), 500

    @app.route('/download/<filename>')
    def download_file(filename):
        try:
            downloads_path = os.path.join(app.static_folder, 'downloads')
            return send_from_directory(downloads_path, filename)
        except Exception as e:
            logging.error("Failed to download file: %s", e, exc_info=True)
            return jsonify({"error": "Failed to download file"}), 500

    @app.route('/chatbot', methods=['POST'])
    def chatbot():
        try:
            user_query = request.json['query']
            openai.api_key = os.getenv('OPENAI_API_KEY')
            
            response = openai.chat.completions.create(
                model="gpt-4", 
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_query}
                ],
            )

            logging.info("Chatbot response generated successfully.")
            return jsonify({'response': response.choices[0].message.content.strip()}), 200
        except Exception as e:
            logging.error(f"Failed to process chatbot query: {e}", exc_info=True)
            return jsonify({"error": "Failed to process query"}), 500
from flask import request, jsonify
from app.models.provider import Provider
from app.schemas.provider_schema import ProviderSchema
from app import db
from app.utils.s3 import upload_file_to_s3
import uuid

provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)

def get_providers():
    try:
        providers = Provider.query.all()
        return jsonify(providers_schema.dump(providers)), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve providers", "details": str(e)}), 500

def get_provider(provider_id):
    try:
        provider = Provider.query.get_or_404(provider_id)
        return jsonify(provider_schema.dump(provider)), 200
    except Exception as e:
        return jsonify({"error": "Provider not found", "details": str(e)}), 404

def create_provider():
    try:
        data = request.get_json()
        result = provider_schema.load(data)

        if Provider.query.filter_by(email=result['email']).first():
            return jsonify({"error": "Email already exists"}), 400

        new_provider = Provider(**result)
        db.session.add(new_provider)
        db.session.commit()

        return jsonify(provider_schema.dump(new_provider)), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create provider", "details": str(e)}), 500

def update_provider(provider_id):
    try:
        provider = Provider.query.get_or_404(provider_id)
        data = request.get_json()

        result = provider_schema.load(data, partial=True)

        for key, value in result.items():
            setattr(provider, key, value)

        db.session.commit()

        return jsonify(provider_schema.dump(provider)), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update provider", "details": str(e)}), 500

def upload_document(provider_id):
    try:
        if 'document' not in request.files:
            return jsonify({"error": "No document provided"}), 400

        file = request.files['document']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if not file.filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
            return jsonify({"error": "Invalid file type"}), 400

        # Generate unique filename
        filename = f"docs/{uuid.uuid4()}_{file.filename}"

        # Upload to S3
        s3_url = upload_file_to_s3(file, filename)

        if not s3_url:
            return jsonify({"error": "Failed to upload document"}), 500

        # Save document reference in database
        provider = Provider.query.get_or_404(provider_id)
        provider.documents.append({
            "filename": file.filename,
            "s3_url": s3_url,
            "uploaded_at": datetime.utcnow(),
            "type": request.form.get('type', 'general')
        })

        db.session.commit()

        return jsonify({
            "message": "Document uploaded successfully",
            "url": s3_url
        }), 201

    except Exception as e:
        return jsonify({"error": "Failed to upload document", "details": str(e)}), 500
# FarmAmigo Backend

FarmAmigo is a supplier portal for agricultural products.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database
- AWS account for S3 and Cognito
- Email server for sending emails

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/farmamigo_backend.git
   cd farmamigo_backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your actual values

flask db init
flask db migrate
flask db upgrade

python run.py
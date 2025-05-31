# House Tracker

[![Build and Push Docker Image](https://github.com/soehlert/our-house/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/soehlert/our-house/actions/workflows/build-and-push.yml)

A Django application for tracking and managing information about your house, including appliances, paint colors, electrical circuits, and more. 
Features an interactive electrical panel diagram generator that visualizes your home's electrical system.

## Features

### Comprehensive House Management
- **Appliance Tracking**: Store documentation, warranties, purchase info, and technical specs
- **Electrical System Mapping**: Document circuits, breakers, and safety features
- **Room Management**: Organize your house by rooms and spaces
- **Paint Color Database**: Track paint codes, brands, and which rooms they're used in

### Interactive Electrical Panel Visualization
Generate SVG diagrams of your electrical panel with:
- Color-coded breakers based on protection types (GFCI, AFCI, CAFI)
- Support for single-pole and double-pole breakers
- Automatic layout and scaling


## Components

### Technology Stack
- **Backend**: Django 5.x
- **Database**: SQLite
- **Package Management**: UV

## Installation & Setup

### Prerequisites
- Python 3.12+
- UV package manager

### Local Development

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd house-tracker
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Run migrations**
   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser**
    ```bash
    uv run python manage.py createsuperuser
    ```

5. **Start the development server**
   ```bash
    uv run python manage.py runserver
   ```

6. **Access the application**
    ```bash
   - Main app: http://127.0.0.1:8000/
   ```

### Production Deployment

For production deployment, consider:

1. **Environment Variables**

   Set in your environment or .env file:
   ```bash
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Reverse Proxy** (nginx example)
   ```bash
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /media/ {
           alias /path/to/your/media/;
       }

       location /static/ {
           alias /path/to/your/static/;
       }
   }
   ```

3. **Backup Strategy**

   Backup database:
   ```bash
   docker-compose exec web uv run python manage.py dumpdata > backup.json
   ```

   Backup media files:
   ```bash
   tar -czf media_backup.tar.gz media/
   ```

## License

MIT LICENSE

# MegaMailer

- [MegaMailer](#megamailer)
  - [Description](#description)
  - [Main functionality](#main-functionality)
  - [Deploy](#deploy)
  - [Technical description](#technical-description)
      - [Project structure](#project-structure)
      - [General installation](#general-installation)
  - [Project development](#project-development)
      - [Project structure for development](#project-structure-for-development)
      - [Installation for development](#installation-for-development)
      - [Creating and setting up containers in Docker](#creating-and-setting-up-containers-in-docker)

## Description

Design a backend comprehensive email management and support system with the following features:
Frontend is ready in react almost!
Almost like the Prototype and bunch of other libraries included, later when foundation is standing.

## Main functionality

1. Login/Register Page:
   - User registration and login functionality.
   - Toggle between dark and white themes.
   - Ensure crash-proof operation with no downtime.

2. Multi-Language Support:
   - Support for DE/EN/RU languages.

3. Support System:
   - Develop a ticket system for frontend and backend.
   - Integrate a Telegram support button.

4. Tool Integration:
   - Implement backend tools such as Mail:pass checker, corp:pass checker, and Email Bounce Checker.
   - Ensure the system can easily integrate new tools in the future.

5. Package and License Management:
   - Offer different subscription packages (BASIC, PRO, DELUXE) with specific features.
   - Implement a safe payment gateway for subscriptions.
   - Include API links for fresh SMTPs and Socks.

6. Email Base Management:
   - Save all email bases with name and timestamp.
   - Implement bounce checks if allowed by the package.

7. Mailer Functions:
   - Implement SMTP check management and storage.
   - Ensure proxy functions similar to SMTPs, including blacklist checks.

8. Template Management:
   - Enable preview, edit, and change functionalities for templates.
   - Add macro functions for randomization.
   - Allow ZIP import for mass uploading templates.
   - Check template inbox status using IMAP settings.

9. IMAP Status Check:
   - Save and check IMAP configurations and connectivity.

10. Mailing Mode:
    - Implement campaign mode with start/stop functionalities.
    - Track email sending and ensure stability.
    - Add inbox rate tracking and header spoofing to avoid blacklists.

11. VPS Association:
    - Associate each client with an offshore mini VPS.
    - Automate VPS setup and monitor health and performance.

12. Backend Monitoring and Maintenance:
    - Implement hourly backups.
    - Route all actions through Socks.
    - Monitor logs, user profiles, and system performance.
    - Provide a robust backend dashboard for system oversight.

## Deploy

Deploy the project with a team of 8 programmers focusing on infrastructure setup, backend tool integration, and frontend implementation to ensure a quick and efficient online launch.

## Technical description

The project development is being developed using Python 3.12 and Django 5.0.6 (if problems arise, we will downgrade to Django 4.2.11).

#### Project structure

```
mm_backend/
├── src/
│   ├── apps/                  # Django applications
│   │   ├── mailer/
│   │   ├── users/
│   │   ├── .../
│   ├── locale/                # Localization
│   ├── manage.py              # Django management file
│   ├── media/                 # Uploaded media files
│   ├── settings/              # Django settings
│   │   ├── settings_base.py   # Base Django settings
│   │   ├── settings_prod.py   # Base Django settings
│   │   └── settings_test.py   # Test settings
│   ├── static/                # Static files
│   └── utils/                 # Utilities and Django mixins
├── Dockerfile                 # Dockerfile for production
├── docker-compose.yml         # Docker Compose configuration for production
├── nginx/                     # Nginx configuration for managing WSGI and ASGI endpoints
├── logs/                      # Logs
├── README.md                  # Project description
├── requirements.txt           # Python dependencies
└── scripts/                   # Utility scripts
```

#### General installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mega-devs/main-beta.git
   ```

2. Install python:

   ```bash
   sudo apt install python3.12-full 
   ```

3. Install virtual environment:

   ```bash
   python3.12 -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5. Install packages from `requirements.txt`

   ```bash
   pip install -r requirements.txt
   ```

6. Create and setting up containers in Docker:

   ```bash
   docker compose up -d --build
   ```

## Project development

#### Project structure for development

```
mm_backend/
├── src/
│   ├── _dev/                  # Development artifacts
│   │   ├── Dockerfile              # Dockerfile for production
│   │   ├── docker-compose-dev.yml  # Docker Compose configuration for production
│   │   ├── requirements_dev.txt    # Python dependencies
│   │   └── settings_dev.py         # Production settings
│   ├── apps/                  # Django applications
│   ├── locale/                # Localization
│   ├── manage.py              # Django management file
│   ├── media/                 # Uploaded media files
│   ├── settings/              # Django settings
│   │   ├── settings_base.py   # Base Django settings
│   │   ├── settings_prod.py   # Production settings
│   │   └── settings_test.py   # Test settings
│   ├── static/                # Static files
│   └── utils/                 # Utilities and Django mixins
├── Dockerfile                 # Dockerfile for production
├── docker-compose.yml         # Docker Compose configuration for production
├── nginx/                     # Nginx configuration for managing WSGI and ASGI endpoints
├── logs/                      # Logs
├── README.md                  # Project description
├── requirements.txt           # Python dependencies
└── scripts/                     # Utility scripts
```

#### Installation for development

1. Execute 1-4 points of the [common installation](#general-installation).
2. Copy from repository [mm_backend_dev](#https://github.com/Iv-Gorbunov/mm_backend_dev) the "_dev/" folder with all its contents into the "src/" folder.

3. Install packages from `requirements_dev.txt`

   ```bash
   pip install -r ./src/_dev/requirements_dev.txt
   ```

4. Create file `.env` by template `.env.template` with you values.

5. Create and setting up containers in Docker:

   ```bash
   docker compose -f ./src/_dev/docker-compose-dev.yml up -d --build
   ```

#### Creating and setting up containers in Docker

**Insatll Docker and docker-compose (for Ubuntu):**

```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common 

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install docker-ce -y

sudo systemctl status docker
```

**Portainer:** - for cofort managing containers

```bash
docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer:latest
```

**pgAdmin:**

```bash
docker run --name pgadmin -p 5050:80 -e "PGADMIN_DEFAULT_EMAIL=admin@admin.com" -e "PGADMIN_DEFAULT_PASSWORD=Admin12345678" -d  dpage/pgadmin4
```

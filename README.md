# AppointHub

<div align="center">

**A modern, full-featured appointment booking and business management platform built with Django**

[![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-green?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Live Demo](#) • [Features](#features) • [Screenshots](#screenshots) • [Installation](#installation) • [Tech Stack](#tech-stack)

</div>

---

## Overview

AppointHub is a comprehensive appointment scheduling and business management solution designed for service-based businesses like salons, spas, clinics, and consulting firms. Built with scalability and user experience in mind, it provides an intuitive interface for managing appointments, staff, services, and customer relationships.

### Why AppointHub?

- **Production-Ready** - Built with industry best practices and clean architecture
- **Responsive Design** - Beautiful UI that works seamlessly on all devices
- **Real-time Updates** - Dynamic interactions with HTMX and Alpine.js
- **Secure** - Token-based authentication, password hashing, and CSRF protection
- **Analytics Dashboard** - Visual insights into business performance

---

## Features

### Dashboard & Analytics
- Real-time business metrics and KPIs
- Revenue tracking with interactive charts
- Weekly appointment activity visualization
- Popular services distribution (doughnut chart)
- Today's schedule at a glance
- Recent activity feed

### Appointment Management
- Full CRUD operations for appointments
- Status tracking (Pending, Confirmed, Completed, Cancelled)
- Advanced filtering and search
- Date and time slot management
- Customer and staff assignment

### Service Management
- Service catalog with categories
- Pricing and duration configuration
- Active/Inactive toggle
- Booking statistics per service

### Staff Management
- Staff profiles with contact information
- Availability status (Available, Busy, Off)
- Service assignments
- Performance ratings and reviews
- Weekly appointment tracking

### Customer Management
- Customer database with profiles
- VIP/Regular/New customer segmentation
- Visit history and spending tracking
- Contact information management

### Settings & Preferences
- Notification preferences (Email, SMS, Reminders)
- Privacy controls
- Password management
- Theme customization (coming soon)
- Account management

### Authentication & Security
- Secure user registration and login
- Email verification system
- Password reset with token-based links
- Session management
- Role-based access control

---

## Screenshots

<div align="center">

### Dashboard
*Comprehensive overview with charts, metrics, and quick actions*

### Appointments
*Manage and track all bookings with filtering and search*

### Services
*Service catalog with categories and pricing*

### Staff Management
*Team overview with availability and performance metrics*

### Settings
*User preferences and account management*

</div>

---

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Core programming language |
| **Django 5.2** | Web framework |
| **SQLite / PostgreSQL** | Database (dev/prod) |
| **Celery** | Async task queue |
| **Redis** | Caching & message broker |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Tailwind CSS** | Utility-first styling |
| **Alpine.js** | Lightweight reactivity |
| **HTMX** | Dynamic HTML updates |
| **Chart.js** | Data visualization |

### DevOps & Tools
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Git** | Version control |
| **Resend** | Transactional emails |

---

## Installation

### Prerequisites
- Python 3.11+
- pip or pipenv
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Salvero/AppointHub.git
cd AppointHub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see the application.

---

## Project Structure

```
AppointHub/
├── apps/
│   ├── accounts/       # User authentication & profiles
│   ├── bookings/       # Appointment booking logic
│   ├── dashboard/      # Main dashboard views
│   ├── notifications/  # Email & notification services
│   ├── services/       # Service management
│   ├── shops/          # Business/shop configuration
│   └── staff/          # Staff management
├── config/
│   ├── settings/       # Environment-specific settings
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── celery.py
├── templates/          # Django templates
│   ├── accounts/
│   ├── dashboard/
│   ├── emails/
│   └── base.html
├── static/             # Static assets
├── media/              # User uploads
├── requirements/       # Dependency files
└── docker/             # Docker configuration
```

---

## Design System

### Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Dark Navy | `#1a1a2e` | Primary background |
| Deep Blue | `#16213e` | Secondary background |
| Ocean Blue | `#0f3460` | Accents |
| Royal Purple | `#533483` | Primary brand |
| Coral Rose | `#e94560` | Accent/CTA |

### UI Components
- **Glass Morphism** - Frosted glass effect cards
- **Gradient Buttons** - Purple to rose gradient CTAs
- **Animated Backgrounds** - Floating particles, blobs, aurora effects
- **Responsive Grid** - Mobile-first layout system

---

## Configuration

### Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Production)
DATABASE_URL=postgres://user:pass@host:5432/dbname

# Email (Resend)
RESEND_API_KEY=your-resend-api-key

# Redis
REDIS_URL=redis://localhost:6379/0
```

---

## Roadmap

- [x] Dashboard with analytics
- [x] Appointment management
- [x] Service catalog
- [x] Staff management
- [x] Customer database
- [x] User settings
- [ ] Calendar integration
- [ ] Online booking portal
- [ ] Payment processing
- [ ] SMS notifications
- [ ] Mobile app (React Native)
- [ ] Multi-location support
- [ ] Reporting & exports

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Salvero**

- GitHub: [@Salvero](https://github.com/Salvero)

---

<div align="center">

⭐ Star this repo if you find it helpful!

Built with Django & Tailwind CSS

</div>

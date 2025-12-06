from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, timedelta
import random


def get_mock_data_for_month(month_offset=0):
    """Generate consistent mock data for a given month offset (0 = current month, -1 = last month, etc.)"""
    # Use month_offset as seed for consistent random data per month
    random.seed(42 + month_offset)
    
    base_revenue = 8000 + (month_offset * 500)
    base_bookings = 80 + (month_offset * 5)
    base_customers = 1200 + (month_offset * 50)
    
    stats = {
        'today_appointments': random.randint(8, 18),
        'upcoming_bookings': random.randint(35, 60),
        'total_customers': base_customers + random.randint(0, 100),
        'monthly_revenue': base_revenue + random.randint(0, 4000),
        'today_change': random.randint(5, 25),
        'bookings_change': random.randint(-5, 15),
        'customers_change': random.randint(5, 20),
        'revenue_change': random.randint(10, 35),
    }
    
    # Reset seed for other random data
    random.seed()
    
    return stats


@login_required
def index_view(request):
    """Main dashboard view with mock data."""
    
    today = datetime.now()
    
    # Get selected month from query params (0 = current, -1 = last month, etc.)
    selected_month_offset = int(request.GET.get('month', 0))
    
    # Calculate the selected month date
    selected_date = today
    for _ in range(abs(selected_month_offset)):
        if selected_month_offset < 0:
            selected_date = selected_date.replace(day=1) - timedelta(days=1)
    
    selected_month_name = selected_date.strftime('%B %Y')
    
    # Generate list of past 6 months for dropdown
    available_months = []
    temp_date = today
    for i in range(6):
        available_months.append({
            'offset': -i,
            'name': temp_date.strftime('%B %Y'),
            'short_name': temp_date.strftime('%b %Y'),
        })
        temp_date = temp_date.replace(day=1) - timedelta(days=1)
    
    # Monthly revenue data (last 6 months from selected month)
    months = []
    revenue_data = []
    bookings_data = []
    random.seed(100 + selected_month_offset)
    for i in range(5, -1, -1):
        month_date = selected_date - timedelta(days=30*i)
        months.append(month_date.strftime('%b'))
        revenue_data.append(random.randint(2500, 8500))
        bookings_data.append(random.randint(45, 120))
    random.seed()
    
    # Weekly appointments data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    random.seed(200 + selected_month_offset)
    weekly_appointments = [random.randint(8, 25) for _ in days]
    random.seed()
    
    # Service distribution
    random.seed(300 + selected_month_offset)
    services = [
        {'name': 'Haircut', 'count': random.randint(100, 180), 'color': '#533483'},
        {'name': 'Massage', 'count': random.randint(70, 120), 'color': '#7c4dab'},
        {'name': 'Facial', 'count': random.randint(50, 90), 'color': '#e94560'},
        {'name': 'Manicure', 'count': random.randint(30, 70), 'color': '#f06b7e'},
        {'name': 'Other', 'count': random.randint(20, 50), 'color': '#f8a5b3'},
    ]
    random.seed()
    
    # Recent activities mock data
    activities = [
        {
            'type': 'booking',
            'icon': 'calendar',
            'color': 'indigo',
            'title': 'New booking confirmed',
            'description': 'Sarah Johnson booked a Haircut',
            'time': '5 minutes ago',
        },
        {
            'type': 'payment',
            'icon': 'dollar',
            'color': 'green',
            'title': 'Payment received',
            'description': '$85.00 from Michael Smith',
            'time': '23 minutes ago',
        },
        {
            'type': 'customer',
            'icon': 'user',
            'color': 'purple',
            'title': 'New customer registered',
            'description': 'Emily Davis created an account',
            'time': '1 hour ago',
        },
        {
            'type': 'booking',
            'icon': 'calendar',
            'color': 'indigo',
            'title': 'Appointment completed',
            'description': 'Massage session with John Doe',
            'time': '2 hours ago',
        },
        {
            'type': 'review',
            'icon': 'star',
            'color': 'yellow',
            'title': 'New 5-star review',
            'description': 'Amanda Lee left a review',
            'time': '3 hours ago',
        },
        {
            'type': 'cancellation',
            'icon': 'x',
            'color': 'red',
            'title': 'Booking cancelled',
            'description': 'Robert Wilson cancelled Facial',
            'time': '4 hours ago',
        },
    ]
    
    # Upcoming appointments
    upcoming = [
        {'time': '09:00 AM', 'customer': 'Alice Brown', 'service': 'Haircut', 'duration': '45 min'},
        {'time': '10:00 AM', 'customer': 'James Wilson', 'service': 'Massage', 'duration': '60 min'},
        {'time': '11:30 AM', 'customer': 'Emma Taylor', 'service': 'Facial', 'duration': '30 min'},
        {'time': '01:00 PM', 'customer': 'Oliver Martinez', 'service': 'Haircut', 'duration': '45 min'},
        {'time': '02:30 PM', 'customer': 'Sophia Anderson', 'service': 'Manicure', 'duration': '40 min'},
    ]
    
    # Get stats for selected month
    stats = get_mock_data_for_month(selected_month_offset)
    
    context = {
        'selected_month_name': selected_month_name,
        'selected_month_offset': selected_month_offset,
        'available_months': available_months,
        'months': months,
        'revenue_data': revenue_data,
        'bookings_data': bookings_data,
        'days': days,
        'weekly_appointments': weekly_appointments,
        'services': services,
        'activities': activities,
        'upcoming': upcoming,
        'stats': stats,
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def appointments_view(request):
    """Appointments management view with mock data."""
    from datetime import datetime, timedelta
    import random
    
    today = datetime.now()
    
    # Filter parameters
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'today')
    
    # Generate mock appointments
    random.seed(500)
    statuses = ['confirmed', 'pending', 'completed', 'cancelled']
    status_colors = {
        'confirmed': 'bg-green-100 text-green-800',
        'pending': 'bg-yellow-100 text-yellow-800',
        'completed': 'bg-blue-100 text-blue-800',
        'cancelled': 'bg-red-100 text-red-800',
    }
    
    services_list = ['Haircut', 'Massage', 'Facial', 'Manicure', 'Pedicure', 'Hair Coloring', 'Beard Trim', 'Spa Treatment']
    customers = ['Alice Brown', 'James Wilson', 'Emma Taylor', 'Oliver Martinez', 'Sophia Anderson', 
                 'William Davis', 'Isabella Garcia', 'Mason Rodriguez', 'Mia Thompson', 'Ethan White']
    staff_members = ['Sarah Johnson', 'Michael Chen', 'Emily Davis', 'David Wilson']
    
    appointments = []
    for i in range(15):
        status = random.choice(statuses)
        date = today + timedelta(days=random.randint(-7, 7))
        hour = random.randint(9, 17)
        minute = random.choice([0, 15, 30, 45])
        
        appointments.append({
            'id': i + 1,
            'customer': random.choice(customers),
            'service': random.choice(services_list),
            'staff': random.choice(staff_members),
            'date': date.strftime('%b %d, %Y'),
            'time': f"{hour:02d}:{minute:02d}",
            'duration': random.choice([30, 45, 60, 90]),
            'price': random.randint(25, 150),
            'status': status,
            'status_class': status_colors[status],
        })
    random.seed()
    
    # Sort by date
    appointments.sort(key=lambda x: x['date'])
    
    # Stats
    stats = {
        'total': len(appointments),
        'confirmed': sum(1 for a in appointments if a['status'] == 'confirmed'),
        'pending': sum(1 for a in appointments if a['status'] == 'pending'),
        'completed': sum(1 for a in appointments if a['status'] == 'completed'),
    }
    
    context = {
        'appointments': appointments,
        'stats': stats,
        'status_filter': status_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'dashboard/appointments.html', context)


@login_required
def services_view(request):
    """Services management view with mock data."""
    import random
    
    random.seed(600)
    
    categories = [
        {'id': 1, 'name': 'Hair', 'color': 'purple'},
        {'id': 2, 'name': 'Spa & Wellness', 'color': 'rose'},
        {'id': 3, 'name': 'Nails', 'color': 'pink'},
        {'id': 4, 'name': 'Skin Care', 'color': 'cyan'},
    ]
    
    services = [
        {'id': 1, 'name': 'Haircut', 'category': 'Hair', 'duration': 45, 'price': 35, 'bookings': 156, 'active': True},
        {'id': 2, 'name': 'Hair Coloring', 'category': 'Hair', 'duration': 120, 'price': 85, 'bookings': 89, 'active': True},
        {'id': 3, 'name': 'Beard Trim', 'category': 'Hair', 'duration': 20, 'price': 15, 'bookings': 203, 'active': True},
        {'id': 4, 'name': 'Blowout', 'category': 'Hair', 'duration': 30, 'price': 25, 'bookings': 67, 'active': True},
        {'id': 5, 'name': 'Swedish Massage', 'category': 'Spa & Wellness', 'duration': 60, 'price': 80, 'bookings': 124, 'active': True},
        {'id': 6, 'name': 'Deep Tissue Massage', 'category': 'Spa & Wellness', 'duration': 90, 'price': 110, 'bookings': 78, 'active': True},
        {'id': 7, 'name': 'Hot Stone Massage', 'category': 'Spa & Wellness', 'duration': 75, 'price': 95, 'bookings': 45, 'active': False},
        {'id': 8, 'name': 'Manicure', 'category': 'Nails', 'duration': 30, 'price': 25, 'bookings': 189, 'active': True},
        {'id': 9, 'name': 'Pedicure', 'category': 'Nails', 'duration': 45, 'price': 35, 'bookings': 167, 'active': True},
        {'id': 10, 'name': 'Gel Nails', 'category': 'Nails', 'duration': 60, 'price': 45, 'bookings': 98, 'active': True},
        {'id': 11, 'name': 'Classic Facial', 'category': 'Skin Care', 'duration': 45, 'price': 55, 'bookings': 112, 'active': True},
        {'id': 12, 'name': 'Anti-Aging Facial', 'category': 'Skin Care', 'duration': 60, 'price': 85, 'bookings': 56, 'active': True},
    ]
    
    random.seed()
    
    # Stats
    stats = {
        'total_services': len(services),
        'active_services': sum(1 for s in services if s['active']),
        'categories': len(categories),
        'total_bookings': sum(s['bookings'] for s in services),
    }
    
    context = {
        'services': services,
        'categories': categories,
        'stats': stats,
    }
    
    return render(request, 'dashboard/services.html', context)


@login_required
def staff_view(request):
    """Staff management view with mock data."""
    import random
    
    random.seed(700)
    
    staff_members = [
        {
            'id': 1,
            'name': 'Sarah Johnson',
            'role': 'Senior Stylist',
            'email': 'sarah.j@appointhub.com',
            'phone': '+1 (555) 123-4567',
            'avatar_initials': 'SJ',
            'services': ['Haircut', 'Hair Coloring', 'Blowout'],
            'appointments_today': 6,
            'appointments_week': 32,
            'rating': 4.9,
            'reviews': 156,
            'status': 'available',
            'schedule': 'Mon-Fri, 9AM-6PM',
        },
        {
            'id': 2,
            'name': 'Michael Chen',
            'role': 'Massage Therapist',
            'email': 'michael.c@appointhub.com',
            'phone': '+1 (555) 234-5678',
            'avatar_initials': 'MC',
            'services': ['Swedish Massage', 'Deep Tissue Massage', 'Hot Stone Massage'],
            'appointments_today': 4,
            'appointments_week': 24,
            'rating': 4.8,
            'reviews': 98,
            'status': 'busy',
            'schedule': 'Tue-Sat, 10AM-7PM',
        },
        {
            'id': 3,
            'name': 'Emily Davis',
            'role': 'Nail Technician',
            'email': 'emily.d@appointhub.com',
            'phone': '+1 (555) 345-6789',
            'avatar_initials': 'ED',
            'services': ['Manicure', 'Pedicure', 'Gel Nails'],
            'appointments_today': 8,
            'appointments_week': 45,
            'rating': 4.7,
            'reviews': 234,
            'status': 'available',
            'schedule': 'Mon-Sat, 9AM-5PM',
        },
        {
            'id': 4,
            'name': 'David Wilson',
            'role': 'Esthetician',
            'email': 'david.w@appointhub.com',
            'phone': '+1 (555) 456-7890',
            'avatar_initials': 'DW',
            'services': ['Classic Facial', 'Anti-Aging Facial'],
            'appointments_today': 5,
            'appointments_week': 28,
            'rating': 4.9,
            'reviews': 87,
            'status': 'off',
            'schedule': 'Wed-Sun, 11AM-8PM',
        },
        {
            'id': 5,
            'name': 'Jessica Martinez',
            'role': 'Junior Stylist',
            'email': 'jessica.m@appointhub.com',
            'phone': '+1 (555) 567-8901',
            'avatar_initials': 'JM',
            'services': ['Haircut', 'Beard Trim', 'Blowout'],
            'appointments_today': 7,
            'appointments_week': 38,
            'rating': 4.6,
            'reviews': 67,
            'status': 'available',
            'schedule': 'Mon-Fri, 10AM-6PM',
        },
    ]
    
    random.seed()
    
    status_colors = {
        'available': 'bg-green-100 text-green-800',
        'busy': 'bg-yellow-100 text-yellow-800',
        'off': 'bg-gray-100 text-gray-800',
    }
    
    for member in staff_members:
        member['status_class'] = status_colors[member['status']]
    
    # Stats
    stats = {
        'total_staff': len(staff_members),
        'available_now': sum(1 for s in staff_members if s['status'] == 'available'),
        'total_appointments_today': sum(s['appointments_today'] for s in staff_members),
        'avg_rating': round(sum(s['rating'] for s in staff_members) / len(staff_members), 1),
    }
    
    context = {
        'staff_members': staff_members,
        'stats': stats,
    }
    
    return render(request, 'dashboard/staff.html', context)


@login_required
def customers_view(request):
    """Customers management view with mock data."""
    import random
    from datetime import datetime, timedelta
    
    today = datetime.now()
    random.seed(800)
    
    customers = [
        {
            'id': 1,
            'name': 'Alice Brown',
            'email': 'alice.brown@email.com',
            'phone': '+1 (555) 111-2222',
            'avatar_initials': 'AB',
            'total_bookings': 24,
            'total_spent': 1250,
            'last_visit': (today - timedelta(days=3)).strftime('%b %d, %Y'),
            'favorite_service': 'Haircut',
            'status': 'vip',
            'joined': (today - timedelta(days=365)).strftime('%b %Y'),
        },
        {
            'id': 2,
            'name': 'James Wilson',
            'email': 'james.w@email.com',
            'phone': '+1 (555) 222-3333',
            'avatar_initials': 'JW',
            'total_bookings': 18,
            'total_spent': 980,
            'last_visit': (today - timedelta(days=7)).strftime('%b %d, %Y'),
            'favorite_service': 'Massage',
            'status': 'regular',
            'joined': (today - timedelta(days=280)).strftime('%b %Y'),
        },
        {
            'id': 3,
            'name': 'Emma Taylor',
            'email': 'emma.t@email.com',
            'phone': '+1 (555) 333-4444',
            'avatar_initials': 'ET',
            'total_bookings': 31,
            'total_spent': 1890,
            'last_visit': (today - timedelta(days=1)).strftime('%b %d, %Y'),
            'favorite_service': 'Facial',
            'status': 'vip',
            'joined': (today - timedelta(days=450)).strftime('%b %Y'),
        },
        {
            'id': 4,
            'name': 'Oliver Martinez',
            'email': 'oliver.m@email.com',
            'phone': '+1 (555) 444-5555',
            'avatar_initials': 'OM',
            'total_bookings': 8,
            'total_spent': 420,
            'last_visit': (today - timedelta(days=14)).strftime('%b %d, %Y'),
            'favorite_service': 'Haircut',
            'status': 'regular',
            'joined': (today - timedelta(days=120)).strftime('%b %Y'),
        },
        {
            'id': 5,
            'name': 'Sophia Anderson',
            'email': 'sophia.a@email.com',
            'phone': '+1 (555) 555-6666',
            'avatar_initials': 'SA',
            'total_bookings': 15,
            'total_spent': 875,
            'last_visit': (today - timedelta(days=5)).strftime('%b %d, %Y'),
            'favorite_service': 'Manicure',
            'status': 'regular',
            'joined': (today - timedelta(days=200)).strftime('%b %Y'),
        },
        {
            'id': 6,
            'name': 'William Davis',
            'email': 'will.d@email.com',
            'phone': '+1 (555) 666-7777',
            'avatar_initials': 'WD',
            'total_bookings': 3,
            'total_spent': 145,
            'last_visit': (today - timedelta(days=30)).strftime('%b %d, %Y'),
            'favorite_service': 'Beard Trim',
            'status': 'new',
            'joined': (today - timedelta(days=45)).strftime('%b %Y'),
        },
        {
            'id': 7,
            'name': 'Isabella Garcia',
            'email': 'isabella.g@email.com',
            'phone': '+1 (555) 777-8888',
            'avatar_initials': 'IG',
            'total_bookings': 22,
            'total_spent': 1560,
            'last_visit': (today - timedelta(days=2)).strftime('%b %d, %Y'),
            'favorite_service': 'Hair Coloring',
            'status': 'vip',
            'joined': (today - timedelta(days=380)).strftime('%b %Y'),
        },
        {
            'id': 8,
            'name': 'Mason Rodriguez',
            'email': 'mason.r@email.com',
            'phone': '+1 (555) 888-9999',
            'avatar_initials': 'MR',
            'total_bookings': 6,
            'total_spent': 320,
            'last_visit': (today - timedelta(days=21)).strftime('%b %d, %Y'),
            'favorite_service': 'Massage',
            'status': 'regular',
            'joined': (today - timedelta(days=90)).strftime('%b %Y'),
        },
    ]
    
    random.seed()
    
    status_colors = {
        'vip': 'bg-purple-100 text-purple-800',
        'regular': 'bg-blue-100 text-blue-800',
        'new': 'bg-green-100 text-green-800',
    }
    
    for customer in customers:
        customer['status_class'] = status_colors[customer['status']]
    
    # Stats
    stats = {
        'total_customers': len(customers),
        'vip_customers': sum(1 for c in customers if c['status'] == 'vip'),
        'new_this_month': sum(1 for c in customers if c['status'] == 'new'),
        'total_revenue': sum(c['total_spent'] for c in customers),
    }
    
    context = {
        'customers': customers,
        'stats': stats,
    }
    
    return render(request, 'dashboard/customers.html', context)
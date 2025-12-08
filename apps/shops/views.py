from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BusinessHoursFormSet, ShopClosureForm, ShopForm
from .models import BusinessHours, Shop, ShopClosure


def get_user_shop(user):
    """Get the shop owned by the user, or None."""
    return Shop.objects.filter(owner=user).first()


@login_required
def shop_setup_view(request):
    """Shop setup wizard for new shops."""
    # Check if user already has a shop
    existing_shop = get_user_shop(request.user)
    if existing_shop:
        return redirect('shops:dashboard', slug=existing_shop.slug)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            shop = form.save()

            # Create default business hours
            for day in range(7):
                is_weekend = day in [5, 6]  # Saturday, Sunday
                BusinessHours.objects.create(
                    shop=shop,
                    day_of_week=day,
                    open_time='09:00' if not is_weekend else None,
                    close_time='17:00' if not is_weekend else None,
                    is_closed=is_weekend,
                )

            # Note: Shop owner permissions are determined by shop.owner relationship,
            # not by elevating user role. This prevents privilege escalation.

            messages.success(request, 'Your shop has been created successfully!')
            return redirect('shops:dashboard', slug=shop.slug)
    else:
        form = ShopForm(user=request.user)

    return render(request, 'shops/setup.html', {'form': form})


@login_required
def shop_dashboard_view(request, slug):
    """Shop owner dashboard."""
    shop = get_object_or_404(Shop, slug=slug)

    # Check ownership
    if shop.owner != request.user:
        raise Http404("Shop not found")

    # Get stats
    context = {
        'shop': shop,
        'services_count': shop.services.filter(is_active=True).count(),
        'staff_count': shop.staff_members.filter(is_active=True).count(),
        'today_bookings': 0,  # Will be implemented with bookings app
        'pending_bookings': 0,
    }

    return render(request, 'shops/dashboard.html', context)


@login_required
def shop_edit_view(request, slug):
    """Edit shop details."""
    shop = get_object_or_404(Shop, slug=slug)

    if shop.owner != request.user:
        raise Http404("Shop not found")

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop details updated successfully!')
            return redirect('shops:dashboard', slug=shop.slug)
    else:
        form = ShopForm(instance=shop, user=request.user)

    return render(request, 'shops/edit.html', {'form': form, 'shop': shop})


@login_required
def shop_hours_view(request, slug):
    """Edit business hours."""
    shop = get_object_or_404(Shop, slug=slug)

    if shop.owner != request.user:
        raise Http404("Shop not found")

    if request.method == 'POST':
        formset = BusinessHoursFormSet(request.POST, instance=shop)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Business hours updated successfully!')
            return redirect('shops:hours', slug=shop.slug)
    else:
        # Ensure all days exist
        existing_days = set(shop.business_hours.values_list('day_of_week', flat=True))
        for day in range(7):
            if day not in existing_days:
                BusinessHours.objects.create(shop=shop, day_of_week=day, is_closed=True)

        formset = BusinessHoursFormSet(instance=shop)

    return render(request, 'shops/hours.html', {
        'formset': formset,
        'shop': shop,
    })


@login_required
def shop_closures_view(request, slug):
    """Manage shop closures."""
    shop = get_object_or_404(Shop, slug=slug)

    if shop.owner != request.user:
        raise Http404("Shop not found")

    closures = shop.closures.all()

    if request.method == 'POST':
        form = ShopClosureForm(request.POST)
        if form.is_valid():
            closure = form.save(commit=False)
            closure.shop = shop
            closure.save()
            messages.success(request, 'Closure added successfully!')
            return redirect('shops:closures', slug=shop.slug)
    else:
        form = ShopClosureForm()

    return render(request, 'shops/closures.html', {
        'form': form,
        'closures': closures,
        'shop': shop,
    })


@login_required
def shop_closure_delete_view(request, slug, pk):
    """Delete a shop closure."""
    shop = get_object_or_404(Shop, slug=slug)

    if shop.owner != request.user:
        raise Http404("Shop not found")

    closure = get_object_or_404(ShopClosure, pk=pk, shop=shop)

    if request.method == 'POST':
        closure.delete()
        messages.success(request, 'Closure deleted successfully!')

    return redirect('shops:closures', slug=shop.slug)


def shop_public_view(request, slug):
    """Public view of a shop for customers."""
    shop = get_object_or_404(Shop, slug=slug, is_active=True)

    services = shop.services.filter(is_active=True).select_related('category')
    staff = shop.staff_members.filter(is_active=True, accepts_bookings=True)
    hours = shop.business_hours.all()

    return render(request, 'shops/public.html', {
        'shop': shop,
        'services': services,
        'staff': staff,
        'hours': hours,
    })

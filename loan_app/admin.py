from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Sum, Count
from django.utils.html import format_html
from django.core.exceptions import PermissionDenied
from .models import User, FarmerProfile, LoanType, LoanApplication, Repayment


admin.site.site_header = "Smart Agricultural Loan Admin"
admin.site.site_title = "SALS Admin"
admin.site.index_title = "Dashboard"


class LoanApplicationInline(admin.TabularInline):
    model = LoanApplication
    extra = 0
    readonly_fields = ['loan_type', 'amount', 'duration_months', 'priority_score', 'status', 'emi', 'created_at']
    can_delete = False
    fields = ['id', 'loan_type', 'amount', 'duration_months', 'priority_score', 'status', 'emi', 'created_at']
    verbose_name = 'Loan Application'
    verbose_name_plural = 'Loan Applications'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'phone_number', 'approval_status', 'is_staff', 'is_active']
    list_filter = ['role', 'is_approved', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    list_editable = ['is_active']
    date_hierarchy = 'date_joined'
    actions = ['approve_bank_officers', 'reject_bank_officers']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )
    inlines = [LoanApplicationInline]

    def approval_status(self, obj):
        """Display approval status for Bank Officers"""
        if obj.role == "Bank Officer":
            if obj.is_approved:
                return format_html(
                    '<span style="color: green; font-weight: bold;">✓ Approved</span>'
                )
            else:
                return format_html(
                    '<span style="color: red; font-weight: bold;">✗ Pending</span>'
                )
        return "-"
    
    approval_status.short_description = "Approval Status"

    def get_readonly_fields(self, request, obj=None):
        """Make is_approved field editable for Bank Officers only"""
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.role != "Bank Officer":
            # is_approved is only relevant for Bank Officers
            if 'is_approved' in self.fieldsets[2][1]['fields']:
                readonly.append('is_approved')
        return readonly

    def approve_bank_officers(self, request, queryset):
        """Admin action to approve Bank Officer registrations"""
        if not request.user.is_superuser and not request.user.is_staff:
            raise PermissionDenied("Only admins can approve Bank Officer registrations.")
        
        # Filter only Bank Officers
        bank_officers = queryset.filter(role="Bank Officer")
        updated = bank_officers.update(is_approved=True)
        
        if updated > 0:
            self.message_user(request, f'{updated} Bank Officer(s) approved successfully.')
        else:
            self.message_user(request, 'No Bank Officers were selected.', level='warning')
    
    approve_bank_officers.short_description = "✓ Approve selected Bank Officer registrations"

    def reject_bank_officers(self, request, queryset):
        """Admin action to reject Bank Officer registrations"""
        if not request.user.is_superuser and not request.user.is_staff:
            raise PermissionDenied("Only admins can reject Bank Officer registrations.")
        
        # Filter only Bank Officers
        bank_officers = queryset.filter(role="Bank Officer")
        updated = bank_officers.update(is_approved=False)
        
        if updated > 0:
            self.message_user(request, f'{updated} Bank Officer(s) rejected.', level='error')
        else:
            self.message_user(request, 'No Bank Officers were selected.', level='warning')
    
    reject_bank_officers.short_description = "✗ Reject selected Bank Officer registrations"


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'land_size', 'crop_type', 'location', 'annual_income', 'created_at']
    list_filter = ['crop_type', 'created_at', 'annual_income']
    search_fields = ['user__username', 'user__email', 'location', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'land_size', 'crop_type', 'location', 'annual_income', 'land_documents', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(LoanType)
class LoanTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'interest_rate', 'max_amount', 'description_short', 'created_at']
    list_filter = ['created_at', 'interest_rate']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['name', 'interest_rate', 'max_amount', 'description', 'created_at', 'updated_at']
    ordering = ['name']
    date_hierarchy = 'created_at'

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'farmer_link', 'loan_type', 'amount', 'duration_months', 'priority_score', 'status', 'status_badge', 'emi', 'created_at']
    list_filter = ['status', 'loan_type', 'created_at', 'priority_score']
    search_fields = ['farmer__username', 'farmer__email', 'id', 'farmer__first_name', 'farmer__last_name']
    readonly_fields = ['priority_score', 'emi', 'created_at', 'updated_at']
    fields = ['farmer', 'loan_type', 'amount', 'duration_months', 'priority_score', 'status', 'emi', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_editable = ['status']
    actions = ['approve_loans', 'reject_loans']

    def farmer_link(self, obj):
        from django.urls import reverse
        return format_html('<a href="{}">{}</a>', reverse('admin:loan_app_user_change', args=[obj.farmer.id]), obj.farmer.username)
    farmer_link.short_description = 'Farmer'

    def status_badge(self, obj):
        colors = {'Pending': 'warning', 'Approved': 'success', 'Rejected': 'danger'}
        color = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.status)
    status_badge.short_description = 'Status'

    def approve_loans(self, request, queryset):
        updated = queryset.update(status='Approved')
        self.message_user(request, f'{updated} loan(s) approved.')
    approve_loans.short_description = 'Approve selected loans'

    def reject_loans(self, request, queryset):
        updated = queryset.update(status='Rejected')
        self.message_user(request, f'{updated} loan(s) rejected.')
    reject_loans.short_description = 'Reject selected loans'


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'loan_link', 'amount_paid', 'remaining_balance', 'payment_date', 'status']
    list_filter = ['status', 'payment_date', 'loan__status']
    search_fields = ['loan__id', 'loan__farmer__username', 'loan__farmer__email', 'notes']
    readonly_fields = ['payment_date', 'remaining_balance']
    fields = ['loan', 'amount_paid', 'payment_date', 'remaining_balance', 'status', 'approved_by', 'approved_at', 'notes']
    ordering = ['-payment_date']
    date_hierarchy = 'payment_date'

    def loan_link(self, obj):
        from django.urls import reverse
        return format_html('<a href="{}">Loan #{}</a>', reverse('admin:loan_app_loanapplication_change', args=[obj.loan.id]), obj.loan.id)
    loan_link.short_description = 'Loan'

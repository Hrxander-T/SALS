from django.db import migrations

def seed_loan_types(apps, schema_editor):
    LoanType = apps.get_model('loan_app', 'LoanType')
    loan_types = [
        {
            'name': 'Agricultural Equipment Loan',
            'interest_rate': 7.50,
            'max_amount': 500000,
            'description': 'Loan for purchasing farming equipment and machinery.'
        },
        {
            'name': 'Crop Loan',
            'interest_rate': 6.00,
            'max_amount': 200000,
            'description': 'Short-term loan for crop production and harvesting.'
        },
        {
            'name': 'Farm Development Loan',
            'interest_rate': 8.50,
            'max_amount': 750000,
            'description': 'Loan for land development and irrigation projects.'
        },
    ]
    for lt in loan_types:
        LoanType.objects.get_or_create(name=lt['name'], defaults={
            'interest_rate': lt['interest_rate'],
            'max_amount': lt['max_amount'],
            'description': lt['description'],
        })

def reverse_seed(apps, schema_editor):
    LoanType = apps.get_model('loan_app', 'LoanType')
    names = ['Agricultural Equipment Loan', 'Crop Loan', 'Farm Development Loan']
    LoanType.objects.filter(name__in=names).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('loan_app', '0015_alter_farmerprofile_land_documents_and_more'),
    ]
    operations = [
        migrations.RunPython(seed_loan_types, reverse_seed),
    ]
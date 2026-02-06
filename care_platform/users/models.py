# -*- coding: utf-8 -*-
from django.db import models
from typing import TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from patients.models import Patient

class User(models.Model):
    """User Model"""
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('family', 'Family'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    password = models.CharField(max_length=128, verbose_name='Password')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='Role')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Gender')
    real_name = models.CharField(max_length=100, verbose_name='Real Name')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Phone')
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    # Django Auth Fields
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    is_superuser = models.BooleanField(default=False, verbose_name='Is Superuser')  # type: ignore[assignment]
    is_staff = models.BooleanField(default=False, verbose_name='Is Staff')  # type: ignore[assignment]
    is_active = models.BooleanField(default=True, verbose_name='Is Active')  # type: ignore[assignment]
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Last Login')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')
    
    # Family specific
    relationship = models.CharField(max_length=50, blank=True, null=True, verbose_name='Relationship')
    patient_id = models.IntegerField(blank=True, null=True, verbose_name='Patient ID')
    
    # Staff specific
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name='Position')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='Department')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['real_name', 'phone', 'role']
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_username(self):
        return self.username
    
    def get_full_name(self):
        return self.real_name
    
    def get_short_name(self):
        return self.real_name
    
    def check_password(self, raw_password):
        """
        Check password with plain text comparison
        """
        return self.password == raw_password

    def set_password(self, raw_password):
        """
        Set password as plain text
        """
        self.password = raw_password

    def __str__(self):
        return self.username
    
    @classmethod
    def create_user(cls, **kwargs):
        real_name = kwargs['real_name']
        first_name = real_name
        last_name = ''
        
        user = cls(
            username=kwargs['username'],
            password=kwargs['password'],
            real_name=real_name,
            phone=kwargs['phone'],
            email=kwargs.get('email'),
            role=kwargs['role'],
            status=kwargs.get('status', 'pending'),
            gender=kwargs.get('gender'),
            avatar=kwargs.get('avatar'),
            position=kwargs.get('position'),
            department=kwargs.get('department'),
            first_name=first_name,
            last_name=last_name,
            is_staff=kwargs.get('is_staff', False),
            is_active=kwargs.get('is_active', True),
            is_superuser=kwargs.get('is_superuser', False)
        )
        user.save()
        return user
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class FamilyUser(models.Model):
    """Family User Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='Patient')
    relationship = models.CharField(max_length=50, verbose_name='Relationship')
    proof_file = models.FileField(upload_to='family_proofs/', blank=True, null=True, verbose_name='Proof File')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Balance')
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return f'{self.user.real_name} - {self.patient.name}'  # type: ignore[attr-defined]
    
    class Meta:
        verbose_name = 'Family User'
        verbose_name_plural = 'Family Users'

class StaffUser(models.Model):
    """Staff User Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='User')
    position = models.CharField(max_length=100, verbose_name='Position', blank=True, null=True)
    department = models.CharField(max_length=100, verbose_name='Department', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return f'{self.user.real_name} - {self.position}'  # type: ignore[attr-defined]
    
    class Meta:
        verbose_name = 'Staff User'
        verbose_name_plural = 'Staff Users'

class RegisterApplication(models.Model):
    """User Registration Application Model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    # Family Info
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    password = models.CharField(max_length=128, verbose_name='Password')  # Stored temporarily, consider encryption or hashing
    real_name = models.CharField(max_length=100, verbose_name='Real Name')
    phone = models.CharField(max_length=11, verbose_name='Phone')
    
    # Patient Info (Used to find existing patient or verify)
    patient_id_card = models.CharField(max_length=18, verbose_name='Patient ID Card')
    relationship = models.CharField(max_length=50, verbose_name='Relationship')
    
    # Meta Info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_registrations', verbose_name='Approver')
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name='Approved At')
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='Rejection Reason')

    def __str__(self):
        return f'{self.real_name} - {self.status}'

    class Meta:
        verbose_name = 'Registration Application'
        verbose_name_plural = 'Registration Applications'
        ordering = ['-created_at']

class LeaveRequest(models.Model):
    """Leave Request Model"""
    TYPE_CHOICES = (
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('annual', 'Annual Leave'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    staff = models.ForeignKey(StaffUser, on_delete=models.CASCADE, verbose_name='Applicant')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Leave Type')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    reason = models.TextField(verbose_name='Reason')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves', verbose_name='Approver')
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name='Approved At')
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='Rejection Reason')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return f'{self.staff.user.real_name} - {self.type}'  # type: ignore[attr-defined]
    
    class Meta:
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        ordering = ['-created_at']

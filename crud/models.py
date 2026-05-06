from django.db import models

class Genders(models.Model):
    gender_id = models.BigAutoField(primary_key=True)
    gender = models.CharField(max_length=55, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_genders'

    def __str__(self):
        return self.gender

class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=55, blank=False)
    gender = models.ForeignKey(Genders, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=False)
    address = models.CharField(max_length=255, blank=False)
    contact_number = models.CharField(max_length=55, blank=False)
    email = models.EmailField(max_length=55, blank=True, null=True)
    
    username = models.CharField(max_length=55, blank=False, unique=True) 
    password = models.CharField(max_length=255, blank=False)
    
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_users'
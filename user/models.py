from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True    

    """ 커스텀 User Manager """
    def create_user(self, username, password=None, **extra_fields):
        # if not email:
        #     raise ValueError("이메일은 필수입니다.")
        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저는 is_staff=True 이어야 합니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저는 is_superuser=True 이어야 합니다.")

        return self.create_user(username, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )  
    is_active = models.BooleanField(default=True)    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "username"

    class Meta:
        db_table = 'auth_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
        

from django.db import models


class MealMateUser(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        max_length=255,
        unique=True
    )

    password_hash = models.CharField(
        max_length=255
    )

    role = models.CharField(
        max_length=30,
        default="user"
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class FoodPost(models.Model):
    id = models.AutoField(primary_key=True)

    business_id = models.PositiveIntegerField()

    food_name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    pickup_address = models.CharField(
        max_length=255
    )

    pickup_start = models.DateTimeField()

    pickup_end = models.DateTimeField()

    status = models.CharField(
        max_length=30,
        default="available"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        managed = False
        db_table = "food_posts"

    def __str__(self):
        return self.food_name


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)

    user_id = models.PositiveIntegerField()

    food_post_id = models.PositiveIntegerField()

    status = models.CharField(
        max_length=30,
        default="reserved"
    )

    pickup_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    reserved_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    collected_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = "reservations"

    def __str__(self):
        return f"Reservation {self.id}"
# Generated by Django 4.1.7 on 2023-06-08 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0011_product_sales"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product_sales",
            options={"ordering": ("-created_at",)},
        ),
        migrations.RemoveField(
            model_name="product_sales",
            name="total_price",
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=0, max_digits=10)),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="product.product_sales",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="product.product",
                    ),
                ),
            ],
        ),
    ]
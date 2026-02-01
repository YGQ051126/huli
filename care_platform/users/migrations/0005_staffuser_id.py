# Generated manually to add id field to StaffUser model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_gender'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    """
                    SET FOREIGN_KEY_CHECKS = 0;
                    ALTER TABLE users_staffuser DROP PRIMARY KEY;
                    ALTER TABLE users_staffuser ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
                    SET FOREIGN_KEY_CHECKS = 1;
                    """,
                    reverse_sql="""
                    SET FOREIGN_KEY_CHECKS = 0;
                    ALTER TABLE users_staffuser DROP PRIMARY KEY;
                    ALTER TABLE users_staffuser DROP COLUMN id;
                    ALTER TABLE users_staffuser ADD PRIMARY KEY (user_id);
                    SET FOREIGN_KEY_CHECKS = 1;
                    """
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='staffuser',
                    name='id',
                    field=models.AutoField(primary_key=True),
                ),
            ],
        ),
    ]

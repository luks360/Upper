from django.contrib import admin
from main.models import User, GroupSpending, GroupProfits, Profits, Spending

# Register your models here.

admin.site.register(User)
admin.site.register(GroupSpending)
admin.site.register(GroupProfits)
admin.site.register(Profits)
admin.site.register(Spending)

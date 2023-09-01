from django.db import models


class Contract(models.Model):
    STATUSES = [
        ('draft', 'Черновик'),
        ('active', 'Активен'),
        ('completed', 'Завершен')
    ]

    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    signing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='draft')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True)

    def complete_action(self):
        self.status = 'completed'
        self.save()

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

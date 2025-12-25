from django.db import models

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Answer(models.Model):
    question = models.ForeignKey(Question ,on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
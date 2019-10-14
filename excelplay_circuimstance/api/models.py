from django.db import models


class Level(models.Model):
    options = (
        ('I', 'Image'),
        ('NI', 'Not Image')
    )

    level = models.IntegerField(default=1)
    answer = models.TextField()
    source_hint = models.TextField(blank=True, null=True)
    level_file = models.FileField(upload_to='level_images/', null=True, blank=True)
    filetype = models.CharField(max_length=10,
                                choices=options,
                                default='Image',
                                blank=True
                                )

    def __str__(self):
        return str(self.level)

class AnswerLog(models.Model):
    user_id = models.CharField(blank=True,max_length=100)
    level = models.IntegerField(default=1)
    answer = models.TextField()
    anstime = models.DateTimeField(null=True)

    def __str__(self):
        return '%-30s| %10s | %10s | %10s '%(self.user_id,
            self.answer,
            self.level,
            self.anstime,
        )

class Hint(models.Model):
    hint = models.TextField()
    level = models.ForeignKey(Level, null=True, related_name='hints', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.hint


class CircuimstanceUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=100)
    level = models.IntegerField(default=1)
    rank = models.IntegerField(default=10000)
    last_anstime = models.DateTimeField(null=True)

    def __str__(self):
        return '<{0}: {1}>'.format(self.user_id, self.rank)

    class Meta:
        ordering = ['-level', 'last_anstime']
        verbose_name_plural = 'Circuimstance Users'


class SubmittedAnswer(models.Model):
    circuimstanceUser = models.ForeignKey(CircuimstanceUser, on_delete=models.CASCADE)
    answers = models.TextField()

from django.db import models

DISPLAY_OK_TYPE_OPTION = (
        ('TYPE1', 'Show OK if there is any result'),
        ('TYPE2', 'Show OK if result is the same as expect_result field'),
        ('TYPE3', 'Show just result without OK'),
        ('TYPE4', 'Do not show OK'),
    )

DISPLAY_FAIL_TYPE_OPTION = (
        ('TYPE1', 'Show Fail if there is no result'),
        ('TYPE2', 'Show Fail if result is not the same as expect_result field'),
        ('TYPE3', 'Do not show Fail'),
    )


# Create your models here.
class TestStage(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. kernel_info")
    test_command = models.CharField(max_length=300, help_text="e.g. uname -r")
    expect_result = models.TextField(max_length=300, help_text="e.g. 5.3.0-24-generic", blank=True)
    display_ok_type = models.CharField('How to display result to OK', choices=DISPLAY_OK_TYPE_OPTION, max_length=100, default='TYPE1')
    display_fail_type = models.CharField('How to display result to fail', choices=DISPLAY_FAIL_TYPE_OPTION, max_length=100, default='TYPE1')
    resume_command = models.CharField(max_length=300, help_text="e.g. uname -r. if test stage failed, this will be shown to resume", blank=True)
    disabled = models.BooleanField(default=False)
    def __str__(self):
        return f'TestStage({self.name})'
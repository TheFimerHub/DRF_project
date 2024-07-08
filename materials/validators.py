import re
from django.core.exceptions import ValidationError

class YouTubeURLValidator:
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    )

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value and not self.youtube_regex.match(value):
            raise ValidationError(
                {self.field: 'Ссылка должна вести на youtube.com'}
            )

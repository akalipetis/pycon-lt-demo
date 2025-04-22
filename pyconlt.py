import logging
import time
from typing import List

import sec
from django.db import models
from nanodjango import Django

logger = logging.getLogger("pyconlt")


app = Django(
    SECRET_KEY="nanodjango-secret-key",
    ALLOWED_HOSTS=["*"],
    LOGGING={
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "loggers": {
            "pyconlt": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    },
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": sec.load("POSTGRESQL_PATH", "pycon_lt_demo"),
            "USER": sec.load("POSTGRESQL_USERNAME", "postgres"),
            "PASSWORD": sec.load("POSTGRESQL_PASSWORD", "postgres"),
            "HOST": sec.load("POSTGRESQL_HOST", "localhost"),
            "PORT": int(sec.load("POSTGRESQL_PORT", "5432")),
        }
    },
)


@app.admin
class Conference(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.year})"


@app.admin
class Talk(models.Model):
    title = models.CharField(max_length=255)
    speaker = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class ConferenceSchema(app.ninja.ModelSchema):
    class Meta:
        model = Conference
        fields = ["id", "name", "year", "location"]


class TalkSchema(app.ninja.ModelSchema):
    class Meta:
        model = Talk
        fields = ["id", "title", "speaker", "description"]


class ResponseSchema(app.ninja.Schema):
    conferences: List[ConferenceSchema]
    talks: List[TalkSchema]


def get_conferences():
    time.sleep(2)  # Artificial delay
    return list(Conference.objects.all().values())


def get_talks():
    time.sleep(2)  # Artificial delay
    return list(Talk.objects.all().values())


@app.api.get("/", response=ResponseSchema)
def api_view(request):
    logger.info("API view called")
    conferences = [conference for conference in get_conferences()]
    talks = [talk for talk in get_talks()]
    logger.info("Conferences and talks fetched")
    return {"conferences": conferences, "talks": talks}

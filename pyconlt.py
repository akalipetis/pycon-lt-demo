import asyncio
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
            "OPTIONS": {
                "pool": {
                    "min_size": 2,
                    "max_size": 90,
                    "timeout": 10,
                }
            },
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


async def get_conferences():
    await asyncio.sleep(2)  # Artificial delay
    return Conference.objects.all()


async def get_talks():
    await asyncio.sleep(2)  # Artificial delay
    return Talk.objects.all()


@app.api.get("/", response=ResponseSchema)
async def api_view(request):
    start = time.time()
    conferences, talks = await asyncio.gather(
        get_conferences(),
        get_talks(),
    )
    logger.info(f"Conferences and talks fetched time={time.time() - start:0.2f}")
    return {
        "conferences": [c async for c in conferences],
        "talks": [t async for t in talks],
    }

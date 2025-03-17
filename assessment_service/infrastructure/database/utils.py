import os
from argparse import Namespace
from enum import Enum
from pathlib import Path
from typing import Any

import sqlalchemy.dialects.postgresql as pg
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import assessment_service

PROJECT_PATH = Path(assessment_service.__file__).parent.parent.resolve()


def create_engine(url: str, debug: bool) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=debug,
        pool_pre_ping=True,
    )


def create_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


def make_alembic_config(
    cmd_opts: Namespace, pg_url: str, base_path: Path = PROJECT_PATH
) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = str(
            base_path / "assessment/infrastructure/database" / cmd_opts.config
        )

    config = Config(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )

    alembic_location = config.get_main_option("script_location")
    if not alembic_location:
        raise ValueError

    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", str(base_path / alembic_location))

    config.set_main_option("sqlalchemy.url", pg_url)

    config.attributes["configure_logger"] = False

    return config


def make_pg_enum(enum_cls: type[Enum], **kwargs: Any) -> pg.ENUM:
    return pg.ENUM(
        enum_cls,
        values_callable=_choices,
        **kwargs,
    )


def _choices(enum_cls: type[Enum]) -> tuple[str, ...]:
    return tuple(map(str, enum_cls))

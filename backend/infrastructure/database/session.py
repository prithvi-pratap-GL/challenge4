"""
VentureMind — Database Session Management
Async SQLAlchemy 2.x engine and session factory setup.

Infrastructure layer only. No business logic.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseSessionManager:
    """
    Owns the async engine and session factory for a single database.

    Lifecycle:
      manager = DatabaseSessionManager(dsn, echo=False)
      ...
      async with manager.session() as session:
          ...
      ...
      await manager.close()

    Designed for use as a long-lived singleton constructed once at
    application startup and injected into repositories/use cases.
    """

    def __init__(
        self,
        dsn: str,
        *,
        echo: bool = False,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_pre_ping: bool = True,
    ) -> None:
        self._engine: AsyncEngine = create_async_engine(
            dsn,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=pool_pre_ping,
        )
        self._session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Provide a transactional session scope.

        Commits on clean exit, rolls back on exception, always closes.
        """
        session = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self) -> None:
        await self._engine.dispose()


_session_manager: DatabaseSessionManager | None = None


def init_session_manager(
    dsn: str,
    *,
    echo: bool = False,
    pool_size: int = 10,
    max_overflow: int = 20,
    pool_pre_ping: bool = True,
) -> DatabaseSessionManager:
    """
    Initialize the module-level session manager singleton.
    Must be called once at application startup before
    `get_session_manager` / `get_session` are used.
    """
    global _session_manager
    _session_manager = DatabaseSessionManager(
        dsn,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=pool_pre_ping,
    )
    return _session_manager


def get_session_manager() -> DatabaseSessionManager:
    """
    Return the initialized session manager singleton.

    Raises:
        RuntimeError: if `init_session_manager` has not been called.
    """
    if _session_manager is None:
        raise RuntimeError(
            "DatabaseSessionManager is not initialized. "
            "Call init_session_manager(dsn) at application startup."
        )
    return _session_manager


async def get_session() -> AsyncIterator[AsyncSession]:
    """
    FastAPI-style dependency-injection generator.

    Usage:
        @app.get("/deals/{deal_id}")
        async def get_deal(
            deal_id: UUID,
            session: AsyncSession = Depends(get_session),
        ):
            ...

    Yields a session bound to a single request-scoped transaction:
    commits on success, rolls back on exception.
    """
    manager = get_session_manager()
    async with manager.session() as session:
        yield session


async def shutdown_session_manager() -> None:
    """Dispose of the engine and connection pool at application shutdown."""
    global _session_manager
    if _session_manager is not None:
        await _session_manager.close()
        _session_manager = None
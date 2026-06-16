from fastapi import Request
from backend.infrastructure.repositories.unit_of_work import UnitOfWork

async def get_uow(request: Request) -> UnitOfWork:
    """
    FastAPI dependency to inject the Unit of Work.
    Currently returns the stubbed UoW to allow the scoring engine to run without Postgres.
    """
    return UnitOfWork()
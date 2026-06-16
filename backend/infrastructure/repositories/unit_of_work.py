from typing import Any

class UnitOfWork:
    """
    Stubbed Unit of Work for demo purposes.
    Bypasses actual DB commits so the scoring engine can run purely on Vector DB / LLM extraction.
    """
    def __init__(self, session_factory: Any = None):
        self.session_factory = session_factory

    async def __aenter__(self):
        # In a real app, this creates the DB session
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        # In a real app, this commits or rolls back
        pass
        
    async def commit(self):
        pass

    async def rollback(self):
        pass
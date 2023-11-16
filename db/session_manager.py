from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class AsyncSessionManager:
    _instance = None
    _session_factory = None

    def __new__(cls, engine=None):
        if not cls._instance:
            cls._instance = super(AsyncSessionManager, cls).__new__(cls)
            if not engine:
                raise ValueError("Engine must be provided for the first instantiation")
            cls._instance._initialize(engine)
        return cls._instance

    def _initialize(self, engine):
        self._session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    def get_session(self):
        if not self._session_factory:
            raise ValueError("AsyncSessionManager not initialized with an engine")
        return self._session_factory()
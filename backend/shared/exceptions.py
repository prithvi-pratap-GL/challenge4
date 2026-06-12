"""Custom exceptions.

Person 5 owns this module.
"""


class VentureMindException(Exception):
    """Base exception for VentureMind AI."""

    pass


class AnalysisException(VentureMindException):
    """Analysis execution failed."""

    pass


class ConfigurationException(VentureMindException):
    """Configuration error."""

    pass


class ResearchException(VentureMindException):
    """Research agent failed."""

    pass


class KnowledgeException(VentureMindException):
    """Knowledge agent failed."""

    pass


class AgentException(VentureMindException):
    """Agent execution failed."""

    pass


class DatabaseException(VentureMindException):
    """Database operation failed."""

    pass


class LLMException(VentureMindException):
    """LLM API call failed."""

    pass

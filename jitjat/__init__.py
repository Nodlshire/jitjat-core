"""
JITJAT: Sub-2.5ms Memory-Mapped Cognitive Substrate for Sovereign AI
"""
__version__ = "3.0.0"
__author__ = "Stephen Soos"

from .engine import JitJatEngine
from .bootstrap import init_substrate_schema

__all__ = ["JitJatEngine", "init_substrate_schema"]

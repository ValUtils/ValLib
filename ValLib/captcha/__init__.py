from .alternative import set_solver, solver
from .struct import CaptchaSolver
from .web import WebServerSolver

__all__ = [
    "CaptchaSolver", "WebServerSolver",
    "set_solver", "solver"
]

from .struct import CaptchaSolver
from .web import WebServerSolver

solver = WebServerSolver()


def set_solver(new_solver: CaptchaSolver):
    global solver
    solver = new_solver

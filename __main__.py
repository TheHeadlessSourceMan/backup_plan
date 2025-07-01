"""
Main entrypoint for the whole enchelada
"""
from .backupPlan import main


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))

"""Lightweight backend import smoke check."""

from app.main import create_app


def main() -> None:
    """Create the FastAPI app and print route count."""
    app = create_app()
    print(f"ok routes={len(app.routes)}")


if __name__ == "__main__":
    main()

from app.app import create_app


def main():
    """Creates and runs the Flask application."""
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()

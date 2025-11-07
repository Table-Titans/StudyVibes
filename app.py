from __init__ import create_app
from sqlalchemy import create_engine, inspect

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)

This repo demonstrates the sqlakeyset bug at https://github.com/djrobstep/sqlakeyset/issues/95.

To reproduce:

1. Ensure that postgres is running locally on port 5432
2. Create a .env file with variables for the username and password (see `.env.example`)
3. Install dependencies with `poetry install`.
4. Run the program with `poetry run python main.py`.

Tested with Python 3.10.10 and Poetry 1.5.1.
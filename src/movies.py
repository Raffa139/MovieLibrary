from omdb.omdb_client import OmdbClient
from environment import omdb_api_key


def main():
    omdb_client = OmdbClient(api_key=omdb_api_key())


if __name__ == "__main__":
    main()

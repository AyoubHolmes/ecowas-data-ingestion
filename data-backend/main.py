from package import Package
from config import ConfigParser


def main():
    # Initialize the config
    config = ConfigParser()

    # Initialize the EcoWAS
    ecowas = Package(config)
    ecowas.create_connection()


if __name__ == "__main__":
    main()

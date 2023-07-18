from ecowas import EcowasDatabase
from config import ConfigParser

def main():
    # Initialize the config
    config = ConfigParser()
    
    # Initialize the EcoWAS
    ecowas = EcowasDatabase(config)
    ecowas.create_connection()

if __name__ == "__main__":
    main()


from chat_client_class import *
import login_GUI as log

def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    client = Client(args)
    client.run_chat()
    #login = log.loginGUI(args)
    #login.launch()
    

main()

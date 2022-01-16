from dotenv import load_dotenv

from senders import sender
from senders.types_ import MessangerType


load_dotenv()


def main():
    tg_sender = sender(messanger=MessangerType.TG)
    groups = tg_sender.get_groups(['краснодар'])


if __name__ == '__main__':
    main()

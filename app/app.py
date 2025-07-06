import logging

from services.data_provider import DataProvider
from services.republic_service import RepublicService

BOOTSTRAP_SERVERS = 'localhost:9094'
ACTION_TOPIC = 'action_topic'


def main():
    rep_service = RepublicService(DataProvider(), BOOTSTRAP_SERVERS, ACTION_TOPIC)
    rep_service.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

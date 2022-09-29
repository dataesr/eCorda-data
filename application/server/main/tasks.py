import sys, time, os

from eCorda_code.new_date import NewDate
from eCorda_code.last_date import lastDate, lastDate_update
from eCorda_code.load_all import extraction_all
from eCorda_code.zip_create import zip_create
from application.server.main.logger import get_logger

logger = get_logger(__name__)

def create_task_eCorda(args: dict) -> None:
    # logger.debug(f'Creating task with args {args}')

    DATE=time.strftime('%Y-%m-%d')
    URL=os.environ.get('https://api.tech.ec.europa.eu/ecorda_api/v5/')

    new_date=NewDate(args.get('framework', 'url_ue'))
    logger.debug(f"NEW_DATE:{new_date}")
    last_date=lastDate()

    if last_date==new_date:
        logger.debug(f'No update since {last_date}')
        pass
    else:
        logger.debug(f"datas number to request:{len('listData')}")

        extraction_all(args.get('framework', 'listData', 'url_ue'))
        zip_create(args.get(DATE))
        lastDate_update(args.get(new_date))
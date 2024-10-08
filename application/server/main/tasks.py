import sys, time, os

from eCorda_code.new_date import NewDate
from eCorda_code.last_date import lastDate, lastDate_update
from eCorda_code.load_all import extraction_all
from eCorda_code.create_csv_json import create_csv_json
from eCorda_code.s3 import upload_object
from eCorda_code.zip_create import zip_create
from application.server.main.logger import get_logger

logger = get_logger(__name__)

def create_task_eCorda() -> None:
    URL = os.getenv('ECORDA_API')
    extractionDate = NewDate('HORIZON', URL)
    logger.debug(f'extractionDate : {extractionDate}')
    LIST_DATA = ['extractionDate',
                'countries',
                'eurostatNuts',
                'calls',
                'topics',
                'topicLbDivisions',
                'typeOfActions',
                'typeOfActionsAttributes',
                'eit',
                'proposals',
                'proposals/applicants',
                'proposals/applicants/departments',
                'proposals/keywords',
                'projects',
                'projects/participants',
                'projects/principalInvestigators',
                'projects/participants/departments',
                'legalEntities',
                'legalEntitiesDepartments',
                'legalEntitiesLinks',
                'projects/payments',
                'projects/reporting/formC',
                'projects/reporting/iprs',
                'projects/euroSciVocTaxonomy',
                'projects/reporting/publications',
                'projects/hrpResult',
                'projects/innovationRadar',
                'projects/cascadingProjects',
                'projects/participants/cascadingParticipants',
                'projects/datasets'
                ]

    extraction_all('HORIZON', LIST_DATA, URL)
    create_csv_json('HORIZON', LIST_DATA)

    filename_prefix = 'HE_'
    extension_liste = ['.csv', '.json']
    for ext in extension_liste:
        zip_filename    = f'{filename_prefix}{extractionDate}{ext}.zip'
        latest_filename = f'{filename_prefix}latest{ext}.zip'
        
        zip_create(zip_filename, ext)
        os.system(f'cp {zip_filename} {latest_filename}')


        upload_object(os.getenv('OS_CONTAINER'), zip_filename)
        upload_object(os.getenv('OS_CONTAINER'), latest_filename)

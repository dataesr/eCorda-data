#!/usr/bin/python
import sys
import click
from ecorda import run_ecorda_pipeline
from utils.notify import notify
from utils.logger import get_logger

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command()
def export():
    try:
        logger.debug('Start Extracting ecorda data')
        datas_load, datas_empty, datas_errors = run_ecorda_pipeline()
        logger.debug('Job finished')
        notify(name='eCorda',
               msg=f'Les données eCorda ont été exportées sur Cartable avec succès: Tables chargées: {datas_load}, Tables vides: {datas_empty}, Erreurs: {datas_errors}')
        sys.exit(0)
    except Exception as e:
        logger.error(e)
        notify(name='eCorda',
               msg="Une erreur s'est produite lors de l'export des données eCorda vers Cartable.", e=f'{e}')
        sys.exit(1)


if __name__ == "__main__":
    cli()

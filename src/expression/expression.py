""" Aggregate expression data for Alliance data submission
The script extracts data from 5 tables into a dictionary that is written to a json file.
The json file is submitted to Alliance for futher processing
This file rewuires packages listed in requirements.txt file and env.sh file.
The env.sh file contains environment variables
This file can be imported as a modules and contains the following functions:
    get_expression_data
"""

import os
import json
from sqlalchemy import create_engine, and_

from ..models.models import DBSession, Eco, Locusdbentity, Goannotation, Go, Referencedbentity
from ..data_helpers.data_helpers import get_eco_ids, get_output

from datetime import datetime
engine = create_engine(os.getenv('SQLALCHEMY_PROD_DB_URI'), pool_recycle=3600)
DBSession.configure(bind=engine)

SUBMISSION_VERSION = os.getenv('SUBMISSION_VERSION', '_1.0.0.0_')
DEFAULT_MMO = 'MMO:0000642'
CC = 'cellular component'
ECO_FORMAT_NAME_LIST = ['ECO:0000314', 'ECO:0007005', 'ECO:0000353']
PMID_TO_MMO = {
    14562095: 'MMO:0000662',
    26928762: 'MMO:0000662',
    16823961: 'MMO:0000534',
    24769239: 'MMO:0000534',
    22842922: 'MMO:0000662',
    14576278: 'MMO:0000534',
    11914276: 'MMO:0000662',
    22932476: 'MMO:0000662',
    24390141: 'MMO:0000662',
    16622836: 'MMO:0000664',
    26777405: 'MMO:0000662',
    12150911: 'MMO:0000662',
    14690591: 'MMO:0000662',
    10684247: 'MMO:0000534',
    16702403: 'MMO:0000662',
    16407407: 'MMO:0000534',
    19053807: 'MMO:0000662',
    23212245: 'MMO:0000534',
    12068309: 'MMO:0000662',
    9448009: 'MMO:0000662',
    11983894: 'MMO:0000534',
    19040720: 'MMO:0000534',
    15282802: 'MMO:0000662',
    24868093: 'MMO:0000662',
    10449419: 'MMO:0000534',
    12392552: 'MMO:0000534',
    8915539: 'MMO:0000647',
    10377396: 'MMO:0000534'
}


def get_expression_data(root_path):
    """ Get gene expression data
    Parameters
    ----------
    root_path
        root directory name path
    Returns
    ------
    file
        writes expression data to json file
    """
    desired_eco_ids = get_eco_ids(ECO_FORMAT_NAME_LIST)
    genes = Locusdbentity.get_s288c_genes()
    result = []
    print("computing " + str(len(genes)) + " expression data points")
    dbentity_id_to_mmo = {}
    for gene in genes:
        go_annotations = DBSession.query(Goannotation, Go).outerjoin(Go).filter(and_(\
            Goannotation.dbentity_id==gene.dbentity_id,\
            Goannotation.annotation_type != 'computational',\
            Goannotation.eco_id.in_(desired_eco_ids),\
            Go.go_namespace == CC,\
            Go.display_name!= CC\
        )).all()
        for x in go_annotations:
            annotation = x[0]
            ref_id = annotation.reference_id
            go = x[1]
            ref = DBSession.query(
                Referencedbentity.pmid, Referencedbentity.sgdid).filter(
                    Referencedbentity.dbentity_id == ref_id).one_or_none()
            pmid = ref[0]
            sgdid = ref[1]
            mmo = None
            if ref_id in dbentity_id_to_mmo.keys():
                mmo = dbentity_id_to_mmo[ref_id]
            else:
                if pmid not in PMID_TO_MMO.keys():
                    mmo = DEFAULT_MMO
                else:
                    mmo = PMID_TO_MMO[pmid]
                dbentity_id_to_mmo[ref_id] = mmo
            obj = {
                "geneId":
                "SGD:" + str(gene.sgdid),
                "evidence": {
                    "crossReference": {
                        "id": "SGD:" + sgdid,
                        "pages": ["reference"]
                    },
                    "publicationId": "PMID:" + str(pmid)
                },
                "whenExpressed": {
                    "stageName": "N/A"
                },
                "whereExpressed": {
                    "whereExpressedStatement": go.display_name,
                    "cellularComponentTermId": go.format_name
                },
                "assay":
                mmo,
                "dateAssigned":
                annotation.date_created.strftime("%Y-%m-%dT%H:%m:%S-00:00")
            }
            result.append(obj)
    if (len(result) > 0):
        output_obj = get_output(result)
        file_name = 'src/data_dump/SGD' + SUBMISSION_VERSION + 'expression.json'
        json_file_str = os.path.join(root_path, file_name)
        with open(json_file_str, 'w+') as res_file:
            res_file.write(json.dumps(output_obj))
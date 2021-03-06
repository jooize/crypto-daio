import time

import logging
import requests
import json

from requests import ReadTimeout
from requests.exceptions import ConnectionError

from daio.models import Chain

logger = logging.getLogger(__name__)


def send_rpc(data, schema_name, rpc_port=None, retry=0):
    """
    Return a connection to the nud  rpc  interface
    """
    if retry == 3:
        logger.error('3 retries have failed')
        return

    data['jsonrpc'] = "2.0"
    data['id'] = int(time.time())
    chain = Chain.objects.get(schema_name=schema_name)
    rpc_url = 'http://{}:{}@{}:{}'.format(
        chain.rpc_user,
        chain.rpc_password,
        chain.rpc_host,
        chain.rpc_port if not rpc_port else rpc_port,
    )
    headers = {'Content-Type': 'applications/json'}
    try:
        response = requests.post(
            url=rpc_url,
            headers=headers,
            data=json.dumps(data),
            timeout=120,
        )

        try:
            result = response.json()
            error = result.get('error', None)
            if error:
                logger.error(
                    'rpc error sending {}: {}'.format(data, result.get('result'))
                )
                return False
            return result.get('result')

        except ValueError:
            logger.error('rpc error sending {}: {}'.format(data, response.text))
            return False

    except ConnectionError:
        logger.error('rpc error sending {}: {}'.format(data, 'no connection with daemon'))
        return False

    except ReadTimeout:
        logger.warning('rpc error sending {}: {}'.format(data, 'daemon timeout'))
        send_rpc(data, schema_name=schema_name, retry=retry + 1)
        return False


def get_block_hash(height, schema_name):
    return send_rpc(
        {'method': 'getblockhash', 'params': [int(height)]},
        schema_name=schema_name
    )


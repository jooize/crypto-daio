import hashlib
import struct
import time
import logging

from blocks.utils.rpc import send_rpc

logger = logging.getLogger('block_validation')


def calc_block_hash(block):
    header = (
        struct.pack('<L', block.version) +
        block.previous_block.hash.decode('hex')[::-1] +
        block.merkle_root.decode('hex')[::-1] +
        struct.pack('<L', int(time.mktime(block.time.timetuple()))) +
        block.bits.decode('hex')[::-1] +
        struct.pack('<L', block.nonce)
    )
    header_hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
    header_hash.encode('hex_codec')
    return header_hash[::-1].encode('hex_codec')


def calc_tx_hash(tx):
    tx_inputs = ''
    for tx_input in tx.inputs.all():
        # previous output transaction hash
        tx_inputs += (
            tx_input.output_transaction.tx_id.decode('hex')[::-1]
            if tx_input.output_transaction is not None
            else ('0'*64).decode('hex')[::-1]
        )
        # previous output N
        tx_inputs += (
            struct.pack('<L', tx_input.v_out)
            if tx_input.v_out is not None
            else 'ffffffff'.decode('hex')[::-1]
        )
        script = (
            tx_input.output_transaction.decode('hex')[::-1]
            if tx_input.coin_base is not None
            else ''
        )
        tx_inputs += struct.pack('<I', len(script))
        tx_inputs += script
        tx_inputs += struct.pack('<L', tx_input.sequence)

    tx_outputs = ''
    for tx_output in tx.outputs.all():
        tx_outputs += (
            struct.pack('L', tx_output.value) +
            tx_output.script_pub_key_hex.decode('hex')[::-1]
        )

    header = (
        struct.pack('<L', tx.version) +
        struct.pack('<I', tx.inputs.all().count()) +
        tx_inputs +
        struct.pack('<I', tx.outputs.all().count()) +
        tx_outputs +
        struct.pack('<L', tx.lock_time)
    )
    logger.info(struct.pack('<I', tx.inputs.all().count()).encode('hex_codec'))
    header_hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
    header_hash.encode('hex_codec')
    return header_hash[::-1].encode('hex_codec')


def check_continuous_heights(latest_block):
    from blocks.utils.block_parser import trigger_block_parse
    from blocks.models import Block

    # run through the blocks to check that heights are continuous
    block = Block.objects.get(height=0)
    previous_block = None
    logger.info('checking blocks for continuous heights')
    while block.height <= latest_block.height:
        if block.height % 5000 == 0:
            logger.info(block.height)
        # if next or previous block is None, rescan the current block as this should
        # add previous and next blocks to the object
        if block.next_block is None or block.previous_block is None:
            trigger_block_parse(block.hash, blocking=True)
            block = Block.objects.get(hash=block.hash)

        # check that the next block is this block + 1
        if block.next_block is not None:
            try:
                if block.next_block.height != (block.height + 1):
                    logger.error(
                        'Error with block at height {} (id {}). Next height is {}'.format(
                            block.height,
                            block.id,
                            block.next_block.height,
                        )
                    )
                    trigger_block_parse(block.next_block.hash, blocking=True)
            except AttributeError as e:
                logger.error(
                    'Error checking next block: {}'.format(e.message)
                )

        # check that the previous block is this block + 1
        if block.previous_block is not None:
            try:
                if block.previous_block.height != (block.height - 1):
                    logger.error(
                        'Error with block at height {} (id {}). '
                        'Previous height is {}'.format(
                            block.height,
                            block.id,
                            block.previous_block.height,
                        )
                    )
                    trigger_block_parse(block.previous_block.hash, blocking=True)
            except AttributeError as e:
                logger.error(
                    'Error checking next block: {}'.format(e.message)
                )

        # check that the previous blocks' next block is this block
        try:
            if previous_block.next_block != block:
                logger.error(
                    'Previous block doens\'t link to this block'
                )
                trigger_block_parse(block.previous_block.hash, blocking=True)
        except AttributeError as e:
            logger.error(
                'Error checking previous blocks\' next block: {}'.format(e.message)
            )

        try:
            if block.previous_block != previous_block:
                logger.error('Previous Blocks do not match {} != {}'.format(
                    block.previous_block,
                    previous_block,
                ))
                trigger_block_parse(block.hash, blocking=True)
                trigger_block_parse(previous_block.hash, blocking=True)
        except AttributeError as e:
            logger.error(
                'Error comparing previous blocks: {}'.format(e.message)
            )

        previous_block = block
        block = block.next_block


def check_hashes(latest_block):
    from blocks.models import Block
    from blocks.utils.block_parser import trigger_block_parse

    try:
        latest_block_id = latest_block.id
    except Block.DoesNotExist:
        latest_block_id = 0

    for i in range(latest_block_id):
        # get the block from the database
        try:
            block = Block.objects.get(id=i)
        except Block.DoesNotExist:
            logger.info('no block with id {}'.format(i))
            continue

        try:
            calc_hash = calc_block_hash(block)
        except (AttributeError, struct.error) as e:
            logger.error('problem with block at height {}, id {}: {}'.format(
                block.height,
                i,
                e.message
            ))
            trigger_block_parse(block.hash)
            continue

        if calc_hash != block.hash:
            logger.warning('hashes for block {} do not match'.format(block.height))
            logger.warning('{} != {}'.format(block.hash, calc_hash))
            trigger_block_parse(block.hash)
            continue

            # for tx in block.transactions.all():
            #    try:
            #        calc_tx_hash = calc_tx_hash(tx)
            #    except AttributeError as e:
            #        logger.info(
            #            'problem with tx {} on block {}: {}'.format(
            #                tx.tx_id,
            #                block.height,
            #                e.message
            #            )
            #       )
            #    logger.info(calc_tx_hash)
            #    logger.info(tx.tx_id)
            #    assert calc_tx_hash == tx.tx_id


def main():
    import django
    django.setup()

    from blocks.models import Block
    latest_block = Block.objects.latest('id')

    check_continuous_heights(latest_block)


if __name__ == '__main__':
    main()






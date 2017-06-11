from django.db import connection
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View

from django.http import HttpResponse
from django.http.response import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.conf import settings

from daio.models import Chain
from .models import *


class Notify(View):
    """
    Used by the coin daemon to notify of a new block
    :param request:
    :param block_hash:
    :return:
    """
    @staticmethod
    def get(request, block_hash, secret_hash):
        if secret_hash not in settings.NOTIFY_SECRET_HASHES:
            return HttpResponseNotFound()
        if len(block_hash) < 60:
            return HttpResponseNotFound()
        # block validation is tied to the save method
        Block.objects.get_or_create(hash=block_hash)
        return HttpResponse('daio received block {}'.format(block_hash))


class LatestBlocksList(ListView):
    model = Block
    paginate_by = 50
    template_name = 'explorer/latest_blocks_list.html'

    def get_queryset(self):
        return Block.objects.exclude(height=None).order_by('-height')

    def get_context_data(self, **kwargs):
        context = super(LatestBlocksList, self).get_context_data(**kwargs)
        context['coins'] = connection.tenant.coins.all()
        context['chain'] = connection.tenant
        return context


class BlockDetailView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(BlockDetailView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get(request, block_height):
        block = get_object_or_404(Block, height=block_height)
        block.save()
        return render(
            request,
            'explorer/block_detail.html',
            {
                'object': block,
                'coins': connection.tenant.coins.all(),
                'chain': connection.tenant,
            }
        )

    @staticmethod
    def post(request, block_height):
        # validate the given transaction and return the same page
        if 'tx_pk' in request.POST:
            # attempt to get the transaction if it exists
            try:
                tx = Transaction.objects.get(pk=request.POST['tx_pk'])
                # save the tx to start validation
                tx.save()
            except Transaction.DoesNotExist:
                pass
        return render(
            request,
            'explorer/block_detail.html',
            {
                'object': get_object_or_404(Block, height=block_height),
                'coins': connection.tenant.coins.all(),
                'chain': connection.tenant,
            }
        )


class AddressDetailView(View):
    @staticmethod
    def get(request, address):
        return render(
            request,
            'explorer/address_detail.html',
            {
                'object': get_object_or_404(Address, address=address),
                'coins': connection.tenant.coins.all(),
                'chain': connection.tenant,
            }
        )

from django.utils import timezone
from djinn import settings
from azure.storage.blob import BlockBlobService, BlobPermissions
from django.http.response import JsonResponse


def generate_blob_url_with_sas(blob):
    start = timezone.now()
    expiry = timezone.now() + timezone.timedelta(seconds=15)
    block_blob_service = BlockBlobService(account_name=settings.AZURE_ACCOUNT_NAME, account_key=settings.AZURE_ACCOUNT_KEY)
    sas_token = block_blob_service.generate_blob_shared_access_signature(settings.AZURE_CONTAINER, blob, permission=BlobPermissions(read=True), expiry=expiry, start=start)
    final_url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_CONTAINER}/{blob}?{sas_token}"

    return final_url

def return_final_url_to_ajax_get(request):
    blob = request.GET.get('blob', None)
    data = {'url': generate_blob_url_with_sas(blob),}
    
    return JsonResponse(data)
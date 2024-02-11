from django.shortcuts import get_list_or_404, get_object_or_404
from push.domains.device import Device

class PushRepository:
    
    def save_device(self, device: Device):
        device.save()

    def find_device_by_token(self, device_token: str):
        return get_object_or_404(Device, device_token=device_token)
    
    def find_all_valid_device(self):
        return Device.objects.filter(is_valid=True)
    
    def find_all_devices_by_member_id(self, member_id: int):
        pass

    def delete_device(self, device: Device):
        Device.delete()
from django.shortcuts import get_list_or_404, get_object_or_404
from push.domains.device import Device
from member.domains import Member

class PushRepository:
    
    def save_device(self, device: Device):
        device.save()

    def find_device_by_token_and_member(self, device_token: str, member: Member):
        return get_object_or_404(Device, device_token=device_token, member=member)
    
    def find_all_devices_with_member_and_notification_detail(self, dorm_id: int):
        return Device.objects.select_related('member', 'member__notificationdetail').filter(member__dorm_id=dorm_id).distinct()
    
    def find_all_devices_by_dorm_id(self, dorm_id: int):
        return Device.objects.select_related('member').filter(member__dorm_id=dorm_id).distinct()
    
    def find_all_devices_by_member_id(self, member_id: int):
        pass

    def delete_device(self, device: Device):
        device.delete()

    def find_devices_by_member_id(self, member_id: int):
        return Device.objects.filter(member_id=member_id)
    
    def find_devices_by_member_ids(self, member_ids: list[int]):
        """
        member_id에 있는 member_id들에 해당되는 Device 객체를 불러옴
        """
        return Device.objects.filter(member_id__in=member_ids)
    
    def find_devices_with_member_and_notification_detail(self, member_id: int):
        return Device.objects.filter(member_id=member_id).select_related('member', 'member__notificationdetail')
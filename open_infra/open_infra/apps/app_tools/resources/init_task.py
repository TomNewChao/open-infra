# -*- coding: utf-8 -*-
# @Time    : 2023/3/16 16:22
# @Author  : Tom_zc
# @FileName: init_task.py
# @Software: PyCharm
import traceback
from logging import getLogger
from django.db import transaction
from app_resources.resources.account_mgr import AccountMgr
from app_tools.models import HWCloudHighRiskPort, HWCloudScanEipPortInfo, HWCloudScanEipPortStatus, \
    HWCloudScanObsAnonymousFile, HWCloudScanObsAnonymousBucket, HWCloudScanObsAnonymousStatus
from app_tools.resources.alarm import CloudsToolsAlarm
from app_tools.resources.scan_tools import ScanToolsMgr
from open_infra.tools.scan_obs import scan_obs
from open_infra.tools.scan_port import scan_port
from open_infra.utils.common import func_retry
from open_infra.utils.default_port_list import HighRiskPort

logger = getLogger("django")


class InitMgr:
    @staticmethod
    @func_retry()
    def refresh_high_level_port():
        """Through to reading the default high level port from config and write to mysql """
        logger.info("----------------1.start scan high level port-----------------")
        default_port_dict = HighRiskPort.get_port_dict()
        actual_port_obj_list = HWCloudHighRiskPort.all()
        if len(actual_port_obj_list) != 0:
            logger.info("[refresh_high_level_port] The data is existed, no initial data")
        else:
            default_port_list = list(default_port_dict.keys())
            save_list_data = [HWCloudHighRiskPort(port=create_port, desc=default_port_dict[create_port])
                              for create_port in default_port_list]
            with transaction.atomic():
                HWCloudHighRiskPort.create_all(save_list_data)
        logger.info("----------------1.finish scan high level port-----------------")

    @classmethod
    def scan_port(cls):
        logger.info("----------------1.start scan_port-----------------------")
        now_account_info_list = AccountMgr.get_decrypt_hw_account_project_info_from_database()
        tcp_info, udp_info, account_list = scan_port(now_account_info_list)
        HWCloudScanEipPortInfo.delete_all()
        HWCloudScanEipPortStatus.delete_all()
        ScanToolsMgr.save_scan_eip_port_info_status(tcp_info, udp_info, account_list)
        HighRiskPort.cur_port_list = None
        high_risk_port = HighRiskPort.get_cur_port_dict()
        for ip, port_list in tcp_info.items():
            port_list = [i[0] for i in port_list]
            port_list = list(set(port_list) - set(high_risk_port.keys()))
            port_str = ",".join(port_list)
            des_var = "ip:{}/port:{}".format(str(ip), port_str)
            CloudsToolsAlarm.active_alarm(des_var)
        for ip, port_list in udp_info.items():
            port_list = [i[0] for i in port_list]
            port_str = ",".join(port_list)
            des_var = "ip:{}/port:{}".format(str(ip), port_str)
            CloudsToolsAlarm.active_alarm(des_var)
        logger.info("----------------1.finish scan_port-----------------------")

    @classmethod
    def scan_obs(cls):
        logger.info("----------------2.start scan_obs-----------------------")
        now_account_info_list = AccountMgr.get_decrypt_hw_account_project_info_from_database()
        list_anonymous_bucket, list_anonymous_file, account_list = scan_obs(now_account_info_list)
        with transaction.atomic():
            HWCloudScanObsAnonymousStatus.delete_all()
            HWCloudScanObsAnonymousBucket.delete_all()
            HWCloudScanObsAnonymousFile.delete_all()
            ScanToolsMgr.save_scan_obs_info_status(list_anonymous_bucket, list_anonymous_file, account_list)
        logger.info("----------------2.finish scan_obs-----------------------")

    @classmethod
    def scan_all_task(cls):
        try:
            cls.scan_port()
        except Exception as e:
            logger.error("[cron_job] e:{}, traceback:{}".format(e, traceback.format_exc()))
        try:
            cls.scan_obs()
        except Exception as e:
            logger.error("[cron_job] e:{}, traceback:{}".format(e, traceback.format_exc()))

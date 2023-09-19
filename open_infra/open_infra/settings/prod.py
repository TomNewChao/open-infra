"""
Django settings for open_infra project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import datetime
import os
import platform
import shutil
import sys

import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

config_path = os.getenv("open_infra_config", os.path.join(BASE_DIR, "config/secret.yaml"))
config = yaml.load(open(config_path, "r", encoding="utf-8"), Loader=yaml.FullLoader)
if len(sys.argv) > 1 and sys.argv[1] == "runserver":
    os.remove(config_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config["pwd"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*", ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',

    # owner apps
    'alarm.apps.AlarmConfig',
    'app_resources.apps.AppResourcesConfig',
    'clouds_tools.apps.CloudsToolsConfig',
    'consumption_control.apps.ConsumptionControlConfig',
    'obs_upload.apps.ObsUploadConfig',
    'permission.apps.PermissionConfig',
    'users.apps.UsersConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 新增跨域
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'open_infra.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'open_infra.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        'HOST': config["mysql_host"],
        'PORT': config["mysql_port"],
        'USER': config["mysql_user"],
        'PASSWORD': config["mysql_password"],
        'NAME': 'open_infra',
        'TIME_ZONE': 'Asia/Shanghai',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
        },
        'POOL_OPTIONS': {
            'POOL_SIZE': 50,
            'MAX_OVERFLOW': 20,
            'RECYCLE': 60,
        }
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# log and lib path setting
LOG_PATH = "/var/log/open-infra"
LIB_PATH = "/var/lib/open-infra"
if platform.system() == "Windows":
    LOG_PATH = os.path.dirname(os.path.dirname(os.getcwd()))
    LIB_PATH = os.path.dirname(os.path.dirname(os.getcwd()))
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
if not os.path.exists(LIB_PATH):
    os.mkdir(LIB_PATH)

LOGGING = {
    'version': 1,
    'propagate': False,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), os.path.join(LOG_PATH, "open-infra.log")),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'alarm': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), os.path.join(LOG_PATH, "alarm.log")),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'alarm': {
            'handlers': ['alarm'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

AUTH_USER_MODEL = 'users.User'

# jwt settings
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=30),  # 30minutes
    'JWT_ALLOW_REFRESH': True,
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': "open_infra.utils.jwt_response.jwt_response_payload_handler",
}

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# cors setting
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with'
)

# obs setting
OBS_AK = config["obs_ak"]
OBS_SK = config["obs_sk"]
OBS_URL = config["obs_url"]
OBS_DOMAIN_ID = config["obs_domain_id"]

# obs bucketname and path
DOWNLOAD_BUCKET_NAME = "obs-for-openeuler-developer"
DOWNLOAD_EIP_KEY_NAME = "secret-files/collect_elastic_public_ip.yaml"
DOWNLOAD_SLA_KEY_NAME = "secret-files/sla_bak.yaml"

# hw account
ZONE_ALIAS_DICT = {
    "cn-north-1": "华北-北京一",
    "cn-north-4": "华北-北京四",
    "cn-north-5": "华北-乌兰察布二零一",
    "cn-north-6": "华北-乌兰察布二零二",
    "cn-north-9": "华北-乌兰察布一",
    "cn-east-3": "华东-上海一",
    "cn-east-2": "华东-上海二",
    "cn-south-1": "华南-广州",
    "cn-south-4": "华南-广州-友好用户环境",
    "cn-southwest-2": "西南-贵阳一",
    "ap-southeast-1": "中国-香港",
    "ap-southeast-2": "亚太-曼谷",
    "ap-southeast-3": "亚太-新加坡",
    "af-south-1": "非洲-约翰内斯堡",
    "na-mexico-1": "拉美-墨西哥城一",
    "la-north-2": "拉美-墨西哥城二",
    "sa-brazil-1": "拉美-圣保罗一",
    "la-south-2": "拉美-圣地亚哥",
    "ru-northwest-2": "俄罗斯-莫斯科二",
}
ALIAS_ZONE_DICT = {value: key for key, value in ZONE_ALIAS_DICT.items()}

# scan port
DEFAULT_SHEET_NAME = "Sheet"
EXCEL_NAME = "IP高危端口扫描统计表_{}.xlsx"
EXCEL_TITLE = ["弹性公网IP", "端口", "状态", "链接协议", "传输协议", "账户", "区域", "服务器版本信息"]
EXCEL_TCP_PAGE_NAME = "TCP"
EXCEL_UDP_PAGE_NAME = "UDP"
IGNORE_ZONE = ["cn-northeast-1", "MOS", "ap-southeast-1_tryme", "cn-north-1_1"]
IS_ALL_SCAN_PORT = True

# scan obs setting
OBS_URL_FORMAT = "https://obs.{}.myhuaweicloud.com"
OBS_BASE_URL = "obs.cn-north-4.myhuaweicloud.com"
OBS_FILE_POSTFIX = ["sh", "java", "jsp", "sql", "conf", "cer",
                    "php", "php5", "asp", "cgi", "aspx", "war", "bat",
                    "c", "cc", "cpp", "cs", "go", "lua", "perl", "pl",
                    "py", "rb", "vb", "vbs", "vba", "h", "jar", "properties",
                    "config", "class"]
SCAN_OBS_EXCEL_NAME = "对象系统扫描统计表_{}.xlsx"
SCAN_OBS_EXCEL_BUCKET_TITLE = ["account", "bucket", "url"]
SCAN_OBS_EXCEL_FILE_TITLE = ["account", "bucket", "url", "path", "data"]
OBS_ANONYMOUS_BUCKET_PAGE_NAME = "scan_obs_anonymous_bucket"
OBS_SENSITIVE_FILE_PAGE_NAME = "scan_obs_sensitive_file"
OBS_BUCKET_URL = "https://{}.obs.{}.myhuaweicloud.com"
OBS_FILE_URL = "https://{}.obs.{}.myhuaweicloud.com/{}"

# scan eip
EIP_V2_ZONE = ["cn-south-4", ]

# scan cla
CLA_API_KEY = config["uptime_robot_api_key"]
CLA_EXCEL_TITLE = ["服务名", "服务介绍", "访问地址", "社区", "月度异常累计时间(min)", "年度异常累计时间(min)", "月度SLA", "年度SLA", "年度剩余SLA配额"]
CLA_EXCEL_NAME = "Sla数据统计表_{}.xlsx"
CLA_EXCEL_PAGE_NAME = "Sla"
CLA_EXPLAIN = {
    "osinfra": "基础设施通用服务",
    "openeuler": "openEuler",
    "mindspore": "MindSpore",
    "opengauss": "openGuass",
    "openlookeng": "openLooKeng",
}

# email config
EMAIL_SENDER_EMAIL = "infra@{}".format(config["alarm_email_host"])
EMAIL_SENDER_NAME = "infra"
EMAIL_SENDER_SERVER = config["alarm_email_host"]
EMAIL_SENDER_PORT = 465
EMAIL_USERNAME = config["alarm_email_user"]
EMAIL_PWD = config["alarm_email_pwd"]
EMAIL_IS_SSL = True

# the alarm email config
ALARM_EMAIL_SUBJECT = "ops.osinfra.cn: Alarm Notify"
ALARM_EMAIL_DEFAULT_LEVEL = 1  # le 1
ALARM_PROMETHEUS_URL = "https://monitor.osinfra.cn"
ALARM_DELAY = 10
# the alarm threshold config
ALARM_CCE_THRESHOLD = 90
ALARM_ECS_THRESHOLD = 90
ALARM_RES_COUNT_THRESHOLD = {
    'mindspore-hk-test-cluster/mindspore-hk-test-cluster/default': 100,
    'mindspore-playground-hk-cluster/mindspore-playground-hk-cluster/opengauss-mooc': 100,
    'mindspore-playground-hk-cluster/mindspore-playground-hk-cluster/default': 100,
    'mindspore-playground-hk-cluster/mindspore-playground-hk-cluster/opengauss-tryme': 100,
    'tencent-beijing-playground-cluster/tencent-beijing-playground-cluster/openeuler-mooc': 100,
    'tencent-beijing-playground-cluster/tencent-beijing-playground-cluster/default': 100
}
# the alarm sms
ALARM_SMS_URL = config["ALARM_SMS_URL"]
ALARM_SMS_KEY = config["ALARM_SMS_KEY"]
ALARM_SMS_SECRET = config["ALARM_SMS_SECRET"]
ALARM_SMS_SENDER = config["ALARM_SMS_SENDER"]
ALARM_SMS_ALARM_TEMPLATE = config["ALARM_SMS_ALARM_TEMPLATE"]
ALARM_SMS_RECOVER_TEMPLATE = config["ALARM_SMS_RECOVER_TEMPLATE"]
ALARM_SMS_SIGNATURE = "OpenInfraOps监控告警"

# the kubeconfig of permission
KUBECONFIG_EMAIL_SUBJECT = "ops.osinfra.cn: Kubeconfig Notify"

# the github config
GITHUB_SECRET = config["GITHUB_SECRET"]
GITHUB_DOMAIN = "https://api.github.com"
GITHUB_COMMIT_INFO = {"name": "TomNewChao", "email": "353712216@qq.com"}
GITHUB_REVIEWER = ["githubliuyang777", "TomNewChao"]

# the obs-interact
OBS_INTERACT_EMAIL_SUBJECT = "ops.osinfra.cn: Obs-Interact Notify"
OBS_INTERACT_ZONE = "cn-north-4"
OBS_INTERACT_BUCEKT_NAME = "obs-transfer"
OBS_INTERACT_REPO = "https://github.com/{}.git"

# the bill rate
BILL_RATE = {
    "interational": 0.5887,
    "common": 0.483,
    "brandwidth": 0.6833,
}
BILL_BRANDWIDTH_LIST = ["固定带宽", "带宽加油包"]
BILL_INTL_ACCOUNT = ["hwstaff_intl_openEuler", ]
BILL_INTL_ALIAS = {
    'CSE Professional Edition': "微服务引擎CSE专享版",
    'Cloud Search Service Node': "云搜索服务节点",
    'Nat Gateway': "NAT网关",
    'Cloud Host': "云主机",
    'Elastic Volume Service': "弹性文件服务",
    'Cloud Search Search Disk': "云搜索服务硬盘",
    'Log Index Traffic': "日志索引流量",
    'Cloud Storage': "云硬盘",
    'RDS DB Instance VM': "RDS数据库实例虚拟机",
    'CCE': "云容器引擎",
    'Cloud Search Search Bandwidth': "云搜索服务带宽",
    'RDS Elastic Volume Service': "RDS云硬盘",
    'Log Read Write Traffic': "日志读写流量",
    'Log Storage Size': "日志存储大小",
    'Anti-DDoS': "Anti-DDoS流量清洗",
    'Fixed Bandwidth': "固定带宽",
    'Elastic IP Address': "弹性公网IP"
}
USD_EXCHANGE_RATE = 7
RESOURCE_UTILIZATION_CPU_THRESHOLD = 10
RESOURCE_UTILIZATION_MEM_THRESHOLD = 10

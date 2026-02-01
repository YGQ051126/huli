# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from care_records.models import CareTemplate
from users.models import User

class Command(BaseCommand):
    help = 'Create default care templates'

    def handle(self, *args, **options):
        # 确保有一个管理员用户作为创建者
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            # 兼容类型提示，实际运行时 objects 是 Manager
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin') # type: ignore

        # 1. 基础护理模板 (适用于低护理等级)
        basic_content = {
            "fields": [
                {
                    "key": "vital_signs",
                    "label": "生命体征",
                    "type": "group",
                    "children": [
                        {"key": "temperature", "label": "体温(°C)", "type": "number", "step": 0.1, "required": True},
                        {"key": "blood_pressure", "label": "血压(mmHg)", "type": "text", "placeholder": "收缩压/舒张压", "required": True},
                        {"key": "heart_rate", "label": "心率(次/分)", "type": "number", "required": True}
                    ]
                },
                {
                    "key": "diet",
                    "label": "饮食记录",
                    "type": "group",
                    "children": [
                         {"key": "breakfast", "label": "早餐", "type": "select", "options": ["全部食用", "部分食用", "未食用"], "required": True},
                         {"key": "lunch", "label": "午餐", "type": "select", "options": ["全部食用", "部分食用", "未食用"], "required": True},
                         {"key": "dinner", "label": "晚餐", "type": "select", "options": ["全部食用", "部分食用", "未食用"], "required": True},
                         {"key": "water_intake", "label": "饮水量(ml)", "type": "number", "required": False}
                    ]
                },
                {
                    "key": "mental_state",
                    "label": "精神状态",
                    "type": "select",
                    "options": ["良好", "平静", "烦躁", "抑郁", "其他"],
                    "required": True
                },
                {
                    "key": "notes",
                    "label": "备注",
                    "type": "textarea",
                    "required": False
                }
            ]
        }
        
        CareTemplate.objects.get_or_create(
            name="基础护理模板",
            care_level="一级护理",
            defaults={
                "template_content": basic_content,
                "is_active": True,
                "created_by": admin_user
            }
        )
        self.stdout.write(self.style.SUCCESS('Created basic care template'))

        # 2. 高级护理模板 (适用于高护理等级，包含更多细节)
        advanced_content = {
            "fields": [
                {
                    "key": "vital_signs",
                    "label": "生命体征",
                    "type": "group",
                    "children": [
                        {"key": "temperature", "label": "体温(°C)", "type": "number", "step": 0.1, "required": True},
                        {"key": "blood_pressure", "label": "血压(mmHg)", "type": "text", "required": True},
                        {"key": "heart_rate", "label": "心率(次/分)", "type": "number", "required": True},
                        {"key": "respiratory_rate", "label": "呼吸(次/分)", "type": "number", "required": True},
                        {"key": "oxygen_saturation", "label": "血氧(%)", "type": "number", "required": True}
                    ]
                },
                {
                    "key": "diet",
                    "label": "饮食/营养",
                    "type": "group",
                    "children": [
                         {"key": "meal_type", "label": "进食方式", "type": "select", "options": ["自主进食", "协助进食", "鼻饲"], "required": True},
                         {"key": "intake_amount", "label": "进食量", "type": "select", "options": ["正常", "偏少", "拒食"], "required": True}
                    ]
                },
                {
                    "key": "excretion",
                    "label": "排泄",
                    "type": "group",
                    "children": [
                         {"key": "urination", "label": "小便", "type": "select", "options": ["正常", "失禁", "留置导尿"], "required": True},
                         {"key": "defecation", "label": "大便", "type": "select", "options": ["正常", "便秘", "腹泻", "失禁"], "required": True}
                    ]
                },
                {
                    "key": "mental_state",
                    "label": "意识/精神",
                    "type": "select",
                    "options": ["清醒", "嗜睡", "昏迷", "躁动"],
                    "required": True
                },
                 {
                    "key": "notes",
                    "label": "交班/备注",
                    "type": "textarea",
                    "required": False
                }
            ]
        }

        CareTemplate.objects.get_or_create(
            name="高级护理模板",
            care_level="特级护理",
            defaults={
                "template_content": advanced_content,
                "is_active": True,
                "created_by": admin_user
            }
        )
        self.stdout.write(self.style.SUCCESS('Created advanced care template'))

        # 3. 通用模板 (作为兜底)
        # 如果找不到特定等级的模板，代码逻辑会找任意一个 active 的模板，或者我们可以显式创建一个通用的
        CareTemplate.objects.get_or_create(
            name="通用护理模板",
            care_level="通用",
            defaults={
                "template_content": basic_content, # 复用基础内容
                "is_active": True,
                "created_by": admin_user
            }
        )
        self.stdout.write(self.style.SUCCESS('Created generic care template'))

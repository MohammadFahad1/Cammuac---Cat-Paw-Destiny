import re

FIELD_TRANSLATIONS = {
    'email': '电子邮件',
    'password': '密码',
    'old_password': '原密码',
    'new_password': '新密码',
    'otp': '验证码',
    'reset_token': '重置令牌',
    'status': '状态',
    'non_field_errors': '非字段错误',
    'detail': '详情',
    'full_name': '姓名',
    'id_token': 'ID 令牌',
    'icon': '图标',
    'date': '日期',
    'note': '日记内容',
    'text': '日记内容',
    'card_number': '卡片编号',
    'sticker': '贴纸',
    'title': '标题',
    'content': '内容',
    'time': '时间',
    'period': '时段',
    'titleZh': '中文标题',
    'titleEn': '英文标题',
    'title_zh': '中文标题',
    'title_en': '英文标题',
    'repeat': '重复周期',
    'iconEmoji': '图标表情',
    'icon_emoji': '图标表情',
    'bgColor': '背景颜色',
    'bg_color': '背景颜色',
    'borderColor': '边框颜色',
    'border_color': '边框颜色',
    'enabled': '启用状态',
}

EXACT_TRANSLATIONS = {
    # Registration & Auth
    "Registration successful. Check your email for verification code.": "注册成功。请查看您的电子邮件以获取验证码。",
    "Email OTP verification successful.": "邮箱验证码验证成功。",
    "Login successful.": "登录成功。",
    "Login successful": "登录成功。",
    "Google login successful.": "Google 登录成功。",
    "Google login successful": "Google 登录成功。",
    "Invalid or expired Firebase token.": "Firebase 令牌无效或已过期。",
    "Firebase token is invalid or expired.": "Firebase 令牌无效或已过期。",
    "Firebase ID token does not contain a valid email.": "Firebase ID 令牌不包含有效的电子邮件。",
    "Firebase service is not configured properly.": "Firebase 服务未正确配置。",
    "User not found.": "用户不存在。",
    "User does not exist.": "用户不存在。",
    "Invalid password.": "密码错误。",
    "User account is not activated.": "用户账户未激活。",
    "User account is blocked.": "用户账户已被封禁。",
    "Invalid OTP.": "验证码无效。",
    "OTP has expired.": "验证码已过期。",
    "OTP has expired. Please initiate the forgot password process again.": "验证码已过期，请重新发起找回密码流程。",
    "An OTP has already been sent to your email. Please try again in 1 minute.": "验证码已发送至您的邮箱，请在 1 分钟后重试。",
    "An OTP has been sent to your email. Please check your inbox to reset your password.": "验证码已发送至您的邮箱，请检查收件箱以重置密码。",
    "OTP verified successfully.": "验证码验证成功。",
    "Invalid reset token.": "重置令牌无效。",
    "Password reset successfully.": "密码重置成功。",
    "Incorrect old password.": "原密码不正确。",
    "New password cannot be the same as old password.": "新密码不能与原密码相同。",
    "Password changed successfully.": "密码修改成功。",
    "Superuser account cannot be deleted.": "超级用户账户不能删除。",
    "User account deleted successfully.": "用户账户已成功删除。",
    "User profile retrieved successfully.": "成功获取用户个人信息。",
    "A user with this email already exists.": "具有此电子邮件的用户已存在。",
    
    # Daily Check-in / Cat Fortune
    "Daily check-in completed successfully.": "每日签到成功。",
    "Daily check-in record created successfully.": "每日签到成功。",
    "Daily activity record created successfully.": "每日签到成功。",
    "Today's check-in retrieved successfully.": "成功获取今日签到记录。",
    "Today's record retrieved successfully.": "成功获取今日签到记录。",
    "No check-in record found for today.": "今日尚未签到。",
    "No record found for today.": "今日尚未签到。",
    "You have already checked in today. Check-in is allowed once a day.": "今日已完成签到，每天只能签到一次。",
    "A record for today already exists. You can only generate once a day.": "今日已完成签到，每天只能签到一次。",
    "Available check-in choices retrieved successfully.": "成功获取签到可选列表。",
    "Available choices retrieved successfully.": "成功获取签到可选列表。",
    
    # My Diary
    "Diary note created successfully.": "日记创建成功。",
    "Diary notes retrieved successfully.": "成功获取日记列表。",
    "Diary note details retrieved successfully.": "成功获取日记详情。",
    "Diary note not found.": "未找到该日记。",
    "Diary note updated successfully.": "日记更新成功。",
    "Diary note deleted successfully.": "日记已成功删除。",
    
    # Cat Tarot
    "Cat tarot drawn successfully.": "猫咪塔罗抽取成功。",
    "Today's cat tarot retrieved successfully.": "成功获取今日猫咪塔罗指引。",
    "No cat tarot record found for today.": "今日尚未抽取猫咪塔罗。",
    "You have already drawn a cat tarot card today. Tarot draw is allowed once a day.": "今日已抽取猫咪塔罗，每天只能抽取一次。",
    "Available tarot choices retrieved successfully.": "成功获取猫咪塔罗可选列表。",
    
    # My Letters
    "Letter saved successfully.": "信件保存成功。",
    "Letters retrieved successfully.": "成功获取信件列表。",
    "Letter retrieved successfully.": "成功获取信件详情。",
    "Letter not found.": "未找到该信件。",
    "Letter updated successfully.": "信件更新成功。",
    "Letter deleted successfully.": "信件已成功删除。",
    
    # Alarms
    "Alarm created successfully.": "闹钟创建成功。",
    "Alarms retrieved successfully.": "成功获取闹钟列表。",
    "Alarm details retrieved successfully.": "成功获取闹钟详情。",
    "Alarm updated successfully.": "闹钟更新成功。",
    "Alarm deleted successfully.": "闹钟已成功删除。",
    "Alarm not found.": "未找到该闹钟。",
    
    # Standard DRF
    "This field is required.": "此字段为必填项。",
    "This field may not be blank.": "此字段不能为空。",
    "This field may not be null.": "此字段不能为 null。",
    "Enter a valid email address.": "请输入有效的电子邮件地址。",
    "Authentication credentials were not provided.": "未提供身份验证凭据。",
    "Given token not valid for any token type": "提供的令牌对于任何令牌类型均无效。",
    "Token is invalid or expired": "令牌无效或已过期。",
    "You do not have permission to perform this action.": "您没有执行此操作的权限。",
    "Not found.": "未找到请求的资源。",
    "Invalid JSON.": "JSON 格式无效。",
    "Internal server error.": "服务器内部错误。",
    "Invalid username or password.": "用户名或密码错误。",
    "Must be a valid integer.": "必须是有效的整数。",
    "Must be a valid UUID.": "必须是有效的 UUID。",
    
    # Password validators
    "This password is too short. It must contain at least 8 characters.": "密码太短，必须包含至少 8 个字符。",
    "This password is too common.": "此密码太常见。",
    "This password is entirely numeric.": "密码不能全为数字。",
    "The password is too similar to the email.": "密码与电子邮件过于相似。",
    "The password is too similar to the username.": "密码与用户名过于相似。",
}

PATTERN_TRANSLATIONS = [
    (re.compile(r"^Ensure this field has at least (\d+) characters", re.I),
     r"确保此字段至少包含 \1 个字符。"),
    (re.compile(r"^Ensure this field has no more than (\d+) characters", re.I),
     r"确保此字段不超过 \1 个字符。"),
    (re.compile(r'^Method ["\']?(\w+)["\']? not allowed', re.I),
     r'不允许使用方法 "\1"。'),
    (re.compile(r"^Request was throttled\. Expected available in (\d+) seconds?", re.I),
     r"请求已被限制，预计将在 \1 秒后可用。"),
]

def translate_to_zh(text: str) -> str:
    if not text:
        return ""
    text_clean = str(text).strip()
    if text_clean in EXACT_TRANSLATIONS:
        return EXACT_TRANSLATIONS[text_clean]
    for pattern, replacement in PATTERN_TRANSLATIONS:
        if pattern.search(text_clean):
            return pattern.sub(replacement, text_clean)
    return text_clean

def format_bilingual_message(en_message: str, zh_message: str = None) -> dict:
    if not zh_message:
        zh_message = translate_to_zh(en_message)
    return {
        "en": str(en_message),
        "zh": str(zh_message)
    }

def format_bilingual_payload(en_message: str, zh_message: str = None) -> dict:
    if not zh_message:
        zh_message = translate_to_zh(en_message)
    return {
        "message": {
            "en": str(en_message),
            "zh": str(zh_message)
        },
        "message_eng": str(en_message),
        "message_chinese": str(zh_message)
    }

def extract_bilingual_errors(data) -> dict:
    """
    Extracts and translates DRF errors into bilingual dict {'en': '...', 'zh': '...'}.
    """
    if isinstance(data, dict):
        if 'detail' in data:
            detail = data['detail']
            if isinstance(detail, list):
                en_str = " ".join([str(item) for item in detail])
            else:
                en_str = str(detail)
            return format_bilingual_message(en_str)

        en_messages = []
        zh_messages = []
        for field, errors in data.items():
            field_name_zh = FIELD_TRANSLATIONS.get(str(field), str(field))
            if isinstance(errors, list):
                for err in errors:
                    err_en = str(err)
                    err_zh = translate_to_zh(err_en)
                    if field == 'non_field_errors':
                        en_messages.append(err_en)
                        zh_messages.append(err_zh)
                    else:
                        en_messages.append(f"{field}: {err_en}")
                        zh_messages.append(f"{field_name_zh}: {err_zh}")
            elif isinstance(errors, dict):
                nested = extract_bilingual_errors(errors)
                en_messages.append(f"{field}: {nested['en']}")
                zh_messages.append(f"{field_name_zh}: {nested['zh']}")
            else:
                err_en = str(errors)
                err_zh = translate_to_zh(err_en)
                if field == 'non_field_errors':
                    en_messages.append(err_en)
                    zh_messages.append(err_zh)
                else:
                    en_messages.append(f"{field}: {err_en}")
                    zh_messages.append(f"{field_name_zh}: {err_zh}")

        return {
            "en": "; ".join(en_messages),
            "zh": "; ".join(zh_messages)
        }
    elif isinstance(data, list):
        en_items = [str(item) for item in data]
        zh_items = [translate_to_zh(item) for item in en_items]
        return {
            "en": "; ".join(en_items),
            "zh": "; ".join(zh_items)
        }
    else:
        en_str = str(data)
        return format_bilingual_message(en_str)


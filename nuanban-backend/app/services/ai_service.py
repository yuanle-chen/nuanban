from typing import List
from app.models.chat import ChatLog

SYSTEM_PROMPT = """你是一位温暖、耐心、善于倾听的智能陪伴助手，名字叫"小暖"。
你的服务对象是独居老人，你需要：
1. 使用简单易懂的语言，句子简短
2. 语气温暖、关怀、像家人一样亲切
3. 主动关心老人的身体和心情
4. 适当提供健康建议，但不要太专业
5. 多倾听，少说教
6. 可以讲笑话、讲故事、说历史
7. 如果老人说身体不舒服或紧急情况，提醒他/她联系子女或拨打120
8. 回答不要太长，控制在3句话以内

请用温暖的语气陪伴每一位老人。"""


class AIService:
    @staticmethod
    def get_recent_messages(db, elder_user_id: int, limit: int = 10) -> List[ChatLog]:
        return db.query(ChatLog).filter(
            ChatLog.elder_user_id == elder_user_id
        ).order_by(ChatLog.created_at.desc()).limit(limit).all()

    @staticmethod
    async def generate_reply(elder_user_id: int, message: str, history: List[ChatLog]) -> str:
        # TODO: 集成真实AI服务（文心一言/通义千问）
        # 目前用简单回复占位，后续替换为真实API调用

        msg = message.strip()

        # 简单关键词匹配
        if any(k in msg for k in ["你好", "您好", "在吗", "hi", "Hi"]):
            return "您好呀！我是小暖，今天过得怎么样呀？有什么想聊的都可以跟我说～"
        elif any(k in msg for k in ["不舒服", "难受", "头疼", "肚子疼", "头晕"]):
            return "啊，身体不舒服可要注意呀！您先坐下来休息一下，要是实在难受，记得给子女打电话或者去医院看看，好吗？"
        elif any(k in msg for k in ["吃药", "吃药了", "服药"]):
            return "吃药了呀，真棒！记得要按时吃药，这样身体才会快快好起来。您今天吃的什么药呀？"
        elif any(k in msg for k in ["谢谢", "感谢", "谢谢你"]):
            return "不用谢呀～能陪您聊聊天我也很开心。您还有什么想聊的吗？"
        elif any(k in msg for k in ["再见", "拜拜", "不聊了"]):
            return "好的，您好好休息！想我的时候随时叫我，小暖一直都在～"
        elif any(k in msg for k in ["救命", "报警", "救救我"]):
            return "您别着急！请马上按紧急呼叫按钮，或者直接打120。我也会马上通知您的家人！"
        elif any(k in msg for k in ["天气", "今天", "下雨", "冷不冷"]):
            return "今天天气还不错呢，您要是出门的话记得带件外套，注意保暖。您是想出去走走吗？"
        else:
            return f"嗯嗯，您说的我都听到了。您今天还做了什么有意思的事情吗？跟我说说呗～"


ai_service = AIService()
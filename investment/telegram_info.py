import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel

with open('/Users/juniq/.telegram_credentials') as f:
    lines = f.read().strip().split('\n')
    api_id = int(lines[0])
    api_hash = lines[1]

client = TelegramClient('/Users/juniq/.telegram_session', api_id, api_hash)

async def info():
    await client.start()

    dialogs = await client.get_dialogs()
    channels = [d for d in dialogs if isinstance(d.entity, Channel)]

    print(f"가입한 채널: {len(channels)}개\n")

    total = 0
    for ch in channels:
        count = ch.entity.participants_count or 0
        # 마지막 메시지 ID ≒ 대략적인 메시지 수
        last_id = 0
        try:
            async for msg in client.iter_messages(ch.entity, limit=1):
                last_id = msg.id
        except:
            pass
        print(f"  {ch.name}: ~{last_id}건")
        total += last_id

    print(f"\n전체 합계: ~{total}건 (대략)")

asyncio.run(info())

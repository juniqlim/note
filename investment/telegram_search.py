import asyncio
import sys
from telethon import TelegramClient
from telethon.tl.types import Channel

with open('/Users/juniq/.telegram_credentials') as f:
    lines = f.read().strip().split('\n')
    api_id = int(lines[0])
    api_hash = lines[1]

client = TelegramClient('/Users/juniq/.telegram_session', api_id, api_hash)

async def search(keywords, limit_per_channel=20, output_file=None):
    await client.start()

    dialogs = await client.get_dialogs()
    channels = [d for d in dialogs if isinstance(d.entity, Channel)]

    results = []
    for keyword in keywords:
        results.append(f"\n{'='*60}")
        results.append(f" 검색어: {keyword}")
        results.append(f" 채널 {len(channels)}개 대상")
        results.append(f"{'='*60}\n")

        total = 0
        for ch in channels:
            try:
                messages = []
                async for msg in client.iter_messages(ch.entity, search=keyword, limit=limit_per_channel):
                    if msg.text:
                        messages.append(msg)

                if messages:
                    results.append(f"--- {ch.name} ({len(messages)}건) ---")
                    for msg in messages:
                        date = msg.date.strftime('%Y-%m-%d %H:%M')
                        text = msg.text.replace('\n', '\n    ')
                        results.append(f"  [{date}]\n    {text}\n")
                    total += len(messages)
            except Exception as e:
                pass

        results.append(f">> '{keyword}' 총 {total}건\n")

    output = '\n'.join(results)
    print(output)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"\n결과 저장: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python telegram_search.py <검색어1> [검색어2] ... [-n 채널당건수] [-o 출력파일]")
        sys.exit(1)

    keywords = []
    limit = 20
    output_file = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-n':
            limit = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '-o':
            output_file = sys.argv[i+1]
            i += 2
        else:
            keywords.append(sys.argv[i])
            i += 1

    asyncio.run(search(keywords, limit, output_file))

# macOS 앱 아이콘 변경 (growTerm)

## 아이콘 생성

- 나노바나나(Gemini 2.5 Flash 이미지 생성 모델)로 앱 아이콘 이미지 생성
- "투명 배경" 요청 시 실제 투명 PNG가 아니라 체크무늬가 이미지에 박힌 채 나옴
- 해결: macOS 내장 "배경 제거" 기능 (Finder 우클릭 → 빠른 동작 → 배경 제거) 사용하면 진짜 투명 PNG 생성됨

## PNG → icns 변환 과정

```bash
# 1. 정사각형 크롭
sips -c 1536 1536 원본.png --out /tmp/icon_sq.png
sips -c 1100 1100 /tmp/icon_sq.png --out /tmp/icon_crop.png

# 2. 80% 크기로 1024x1024 캔버스에 배치 (Swift 사용)
# 투명 배경 위에 아이콘을 80%로 축소 배치하면 다른 macOS 앱 아이콘과 비슷한 크기

# 3. iconset 생성
mkdir -p /tmp/AppIcon.iconset
for size in 16 32 128 256 512; do
  sips -z $size $size icon.png --out /tmp/AppIcon.iconset/icon_${size}x${size}.png
done
# @2x 버전도 생성 (32, 64, 256, 512, 1024)

# 4. icns 변환
iconutil -c icns /tmp/AppIcon.iconset -o assets/icon.icns
```

## 앱 번들 설치 (install.sh)

```bash
cargo build --release -p growterm-app
cp target/release/growterm /Applications/growTerm.app/Contents/MacOS/growterm
cp assets/icon.icns /Applications/growTerm.app/Contents/Resources/AppIcon.icns
# Info.plist에서 CFBundleIconFile = AppIcon
```

## 아이콘 캐시 초기화

```bash
# 아이콘 변경 후 반영이 안 될 때
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
killall Finder Dock
```

## 주의사항

- macOS는 앱 아이콘에 자동으로 둥근 모서리(superellipse) 마스크를 적용함
- 아이콘 이미지 자체에 둥근 모서리가 있으면 이중으로 잘려서 어색해짐
- 둥근 모서리를 유지하려면 투명 배경 PNG 사용, 정사각형으로 채우려면 배경색으로 전체 채우기

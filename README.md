# Auto-Blogger

AI 기반 블로그 글 자동 생성 CLI 도구입니다. LangChain과 OpenAI를 활용하여 주제만 입력하면 완성도 높은 블로그 포스트를 자동으로 작성합니다.

## 주요 기능

- 🤖 LangChain 기반 블로그 글 자동 생성
- 🔌 OpenAI 호환 API 엔드포인트 지원 (Azure OpenAI, vLLM, LiteLLM 등)
- 🔍 MCP 서버 통합으로 참고 자료 자동 수집
- 🌍 다국어 지원 (한국어, 영어 등)
- 🎨 다양한 톤 선택 (전문적, 캐주얼, 기술적)
- 📏 글 길이 조절 (짧은 글, 중간, 긴 글)
- 💾 파일 저장 또는 콘솔 출력
- ⚙️ 환경 변수를 통한 설정 관리

## 설치

### 필수 요구사항

- Python 3.12 이상
- UV 패키지 매니저
- OpenAI API 키

### 설치 방법

```bash
# 저장소 클론
git clone <repository-url>
cd auto-blogger

# UV로 의존성 설치
uv sync

# 또는 개발 모드로 설치
uv pip install -e .
```

## 설정

1. 설정 파일 초기화:

    ```bash
    uv run auto-blogger init
    ```

2. `.env` 파일 편집하여 API 키 입력:

    ```bash
    # .env 파일
    OPENAI_API_KEY=your-openai-api-key-here
    DEFAULT_MODEL=gpt-4o-mini
    DEFAULT_LANGUAGE=Korean
    DEFAULT_TONE=professional
    DEFAULT_LENGTH=medium
    TEMPERATURE=0.7

    # OpenAI 호환 API 엔드포인트 (선택사항)
    # Azure OpenAI, vLLM, LiteLLM 등 사용 가능
    OPENAI_API_BASE=https://your-service.openai.azure.com/

    # MCP 서버 설정 (선택사항)
    MCP_SERVERS=http://localhost:8000,https://api.example.com/mcp
    ```

## 사용법

### 기본 사용

```bash
# 주제만 입력 (콘솔에 출력)
uv run auto-blogger generate "인공지능의 미래"
# or using wrapper: ./auto-blogger.sh generate "인공지능의 미래"

# 파일로 저장
uv run auto-blogger generate "파이썬 비동기 프로그래밍" --output blog.md

# MCP 서버에서 참고 자료 수집하여 작성
uv run auto-blogger generate "클라우드 컴퓨팅 트렌드" --research --output cloud.md

# 언어, 톤, 길이 지정
uv run auto-blogger generate "클라우드 컴퓨팅 트렌드" \
  --language Korean \
  --tone technical \
  --length long \
  --research \
  --output cloud-trends.md
```

### 옵션

- `--output, -o`: 출력 파일 경로 (지정하지 않으면 콘솔 출력)
- `--language, -l`: 글 작성 언어 (기본값: Korean)
- `--tone, -t`: 글의 톤
  - `professional`: 전문적 (기본값)
  - `casual`: 캐주얼
  - `technical`: 기술적
- `--length`: 글 길이
  - `short`: 짧은 글 (300-500 단어)
  - `medium`: 중간 길이 (800-1200 단어, 기본값)
  - `long`: 긴 글 (1500-2500 단어)
- `--research, -r`: MCP 서버에서 참고 자료 수집 활성화

### 추가 명령어

```bash
# 버전 확인
uv run auto-blogger version

# 도움말
uv run auto-blogger --help
```

## 프로젝트 구조

```text
auto-blogger/
├── auto_blogger/
│   ├── __init__.py       # 패키지 초기화
│   ├── cli.py            # CLI 인터페이스
│   ├── config.py         # 설정 관리
│   ├── generator.py      # 블로그 생성 로직
│   └── mcp_client.py     # MCP 클라이언트 및 리서치 헬퍼
├── pyproject.toml        # 프로젝트 설정 및 의존성
├── README.md             # 프로젝트 문서
└── .env                  # 환경 변수 (생성 필요)
```

## 예제

### MCP 서버와 함께 사용

```bash
# Microsoft Learn MCP 서버를 통해 기술 문서 참고
uv run auto-blogger generate "Azure Functions 시작하기" \
  --research \
  --tone technical \
  --output azure-functions.md
```

### 기술 블로그 작성

```bash
uv run auto-blogger generate "GraphQL vs REST API 비교" \
  --tone technical \
  --length long \
  --output graphql-vs-rest.md
```

### 캐주얼한 짧은 글

```bash
uv run auto-blogger generate "주말 코딩 프로젝트 아이디어" \
  --tone casual \
  --length short
```

### 영어로 작성

```bash
uv run auto-blogger generate "The Future of Web Development" \
  --language English \
  --tone professional \
  --output future-web-dev.md
```

## 개발

```bash
# 의존성 설치
uv sync

# 로컬에서 실행
uv run auto-blogger generate "테스트 주제"

# 린팅 (ruff 설치 필요)
uv run ruff check .

# 포맷팅
uv run ruff format .
```

## 향후 계획

- [x] MCP 서버 통합으로 HTTP 기반 참고 자료 수집
- [ ] LlamaIndex 통합으로 고급 RAG 기능 추가
- [ ] 다양한 LLM 프로바이더 지원 (Anthropic, Cohere 등)
- [ ] 템플릿 시스템 (기술 블로그, 마케팅, 튜토리얼 등)
- [ ] 이미지 생성 통합
- [ ] SEO 최적화 기능
- [ ] 멀티 포스트 일괄 생성
- [ ] WebSocket 기반 MCP 서버 지원

## 라이선스

MIT

## 기여

이슈와 Pull Request는 언제나 환영합니다!

"""
Memento v2 Detection Library
6가지 데이터 유형에 대한 다층 감지 규칙
"""
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DetectionType(Enum):
    """감지 유형"""
    FACT = "fact"           # 변하지 않는 정보
    PREFERENCE = "preference"  # 선호/비선호
    PATTERN = "pattern"     # 반복 패턴
    HISTORY = "history"     # 판단+결과
    CONTEXT = "context"     # 프로젝트 맥락
    STATE = "state"         # 현재 상태


class SignalStrength(Enum):
    """신호 강도"""
    STRONG = "strong"   # 높은 신뢰도 - 기록 권장
    WEAK = "weak"       # 낮은 신뢰도 - 맥락 확인 필요


@dataclass
class Detection:
    """감지 결과"""
    type: DetectionType
    strength: SignalStrength
    matched_text: str
    rule_name: str
    target_file: str
    target_section: str
    format_hint: str


# 감지 규칙 정의
DETECTION_RULES = {
    DetectionType.FACT: {
        "strong": [
            # 가족 정보
            (r"(와이프|아내|남편|아들|딸|부모님|엄마|아빠|형|동생).{0,10}(있|없|생겼)", "가족 정보"),
            # 직업/역할
            (r"(나는|난|저는).{0,20}(개발자|디자이너|기획자|대표|팀장|사장)", "직업 정보"),
            # 목표 선언
            (r"(목표|꿈|비전).{0,10}(은|는|이|가).{0,30}(이다|야|입니다)", "목표 선언"),
            (r"(궁극적|최종|장기).{0,10}(목표|꿈|비전)", "장기 목표"),
        ],
        "weak": [
            (r"(살고|사는).{0,10}(있|곳)", "거주지 힌트"),
        ],
        "exclude": [
            r"\?$",  # 질문 제외
        ],
        "target_file": "profile.md",
        "target_section": "Facts",
        "format_hint": "- **카테고리**: 내용",
    },

    DetectionType.PREFERENCE: {
        "strong": [
            # 명확한 선호 표현
            (r"(나는|난|저는).{0,20}(좋아|싫어|선호)", "명확한 선호"),
            (r"(하지\s*마|하지마|안\s*했으면)", "명확한 비선호"),
            (r"(항상|매번|꼭).{0,15}(해줘|줘|했으면)", "반복 요청"),
            (r"(~게|~하게).{0,5}(해줘|줘)", "스타일 요청"),
            # 가치관 표현
            (r"(중요한\s*건|중요한\s*게|중요한\s*것).{0,20}(이다|야|이야)", "가치관"),
            (r"(나한테|나에게).{0,10}(중요|의미)", "개인 가치"),
        ],
        "weak": [
            (r"(좋아|싫어|귀찮)", "감정 표현"),
        ],
        "exclude": [
            r"(좋아요|싫어요|좋아하세요|싫어하세요)\?",  # 질문 제외
        ],
        "target_file": "profile.md",
        "target_section": "Preferences",
        "format_hint": "- [날짜] **영역**: 선호 내용",
    },

    DetectionType.PATTERN: {
        "strong": [
            # 반복 명시
            (r"(또|계속|맨날|자꾸|항상).{0,15}(미루|안\s*하|못\s*하|까먹)", "반복 패턴"),
            (r"(\d+)\s*(번째|번|회차)", "횟수 언급"),
            (r"(늘|언제나|매번).{0,10}(그래|이래|그렇)", "습관 표현"),
        ],
        "weak": [
            (r"(또|계속)", "반복 단어"),
        ],
        "exclude": [],
        "target_file": "profile.md",
        "target_section": "Patterns > 주의 패턴",
        "format_hint": "- [날짜] **패턴명**: 설명 (횟수: N)",
    },

    DetectionType.HISTORY: {
        "strong": [
            # 의사결정 + 결과
            (r"(결정|선택|판단).{0,20}(했|했는데|했더니)", "과거 결정"),
            (r"(그래서|결국|결과적으로).{0,20}(됐|됬|했)", "결과 언급"),
            (r"(성공|실패|잘\s*됐|망|안\s*됐)", "결과 평가"),
            # 후회/교훈
            (r"(그때|예전에).{0,15}(했으면|안\s*했으면)", "후회 표현"),
            (r"(배웠|깨달|알게\s*됐)", "교훈"),
        ],
        "weak": [
            (r"(했어|했는데)", "과거 행동"),
        ],
        "exclude": [],
        "target_file": "cases.md",
        "target_section": "새 케이스",
        "format_hint": "CXXX: [제목] 형식의 케이스",
    },

    DetectionType.CONTEXT: {
        "strong": [
            # 프로젝트 + 배경
            (r"(프로젝트|japan|해동|dt-rag|scraper).{0,10}(은|는|이|가).{0,20}(라서|때문|이유)", "프로젝트 배경"),
            (r"(이\s*프로젝트|그\s*프로젝트).{0,20}(특징|상황|맥락)", "맥락 설명"),
        ],
        "weak": [
            (r"(프로젝트|작업)", "프로젝트 언급"),
        ],
        "exclude": [],
        "target_file": "profile.md",
        "target_section": "Context",
        "format_hint": "### 프로젝트명\n- 맥락 정보",
    },

    DetectionType.STATE: {
        "strong": [
            # 상태 변화
            (r"(완료|끝났|시작|변경|연기|취소).{0,10}(했|됐|함)", "상태 변화"),
            (r"(지금|현재|오늘).{0,15}(상태|상황|진행)", "현재 상태"),
            # 진행률
            (r"(\d+)\s*%", "진행률"),
            (r"(거의|반쯤|절반|다)", "진행 정도"),
        ],
        "weak": [
            (r"(하고\s*있|진행\s*중)", "진행 중"),
        ],
        "exclude": [],
        "target_file": "projects.md",
        "target_section": "해당 프로젝트",
        "format_hint": "상태 업데이트",
    },
}


def detect_all(text: str) -> list[Detection]:
    """
    텍스트에서 모든 유형의 감지 수행

    Args:
        text: 분석할 텍스트

    Returns:
        감지된 항목 리스트
    """
    detections = []
    text_lower = text.lower()

    for detection_type, rules in DETECTION_RULES.items():
        # 제외 패턴 체크
        excluded = False
        for exclude_pattern in rules.get("exclude", []):
            if re.search(exclude_pattern, text, re.IGNORECASE):
                excluded = True
                break

        if excluded:
            continue

        # 강한 신호 체크
        for pattern, rule_name in rules.get("strong", []):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                detections.append(Detection(
                    type=detection_type,
                    strength=SignalStrength.STRONG,
                    matched_text=match.group(0),
                    rule_name=rule_name,
                    target_file=rules["target_file"],
                    target_section=rules["target_section"],
                    format_hint=rules["format_hint"],
                ))

        # 약한 신호 체크 (강한 신호가 없을 때만)
        strong_found = any(d.type == detection_type and d.strength == SignalStrength.STRONG for d in detections)
        if not strong_found:
            for pattern, rule_name in rules.get("weak", []):
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    detections.append(Detection(
                        type=detection_type,
                        strength=SignalStrength.WEAK,
                        matched_text=match.group(0),
                        rule_name=rule_name,
                        target_file=rules["target_file"],
                        target_section=rules["target_section"],
                        format_hint=rules["format_hint"],
                    ))

    return detections


def format_detection_hint(detections: list[Detection]) -> str:
    """
    감지 결과를 AI 힌트 형식으로 포맷

    Args:
        detections: 감지 결과 리스트

    Returns:
        포맷된 힌트 문자열
    """
    if not detections:
        return ""

    # 강한 신호와 약한 신호 분리
    strong = [d for d in detections if d.strength == SignalStrength.STRONG]
    weak = [d for d in detections if d.strength == SignalStrength.WEAK]

    lines = ["[Memento 감지]", ""]

    if strong:
        lines.append("🔴 **기록 권장** (강한 신호):")
        for d in strong:
            lines.append(f"  - {d.type.value}: \"{d.matched_text}\" ({d.rule_name})")
            lines.append(f"    → {d.target_file} > {d.target_section}")
            lines.append(f"    → 형식: {d.format_hint}")
        lines.append("")

    if weak:
        lines.append("🟡 **맥락 확인** (약한 신호):")
        for d in weak:
            lines.append(f"  - {d.type.value}: \"{d.matched_text}\" ({d.rule_name})")
        lines.append("")

    lines.append("❌ '나중에 기록하겠다' 금지 - 해당되면 지금 기록")

    return "\n".join(lines)


def get_detection_summary(detections: list[Detection]) -> dict:
    """
    감지 결과 요약 (세션 상태 저장용)

    Args:
        detections: 감지 결과 리스트

    Returns:
        요약 딕셔너리
    """
    return {
        "total": len(detections),
        "strong": len([d for d in detections if d.strength == SignalStrength.STRONG]),
        "weak": len([d for d in detections if d.strength == SignalStrength.WEAK]),
        "types": list(set(d.type.value for d in detections)),
        "details": [
            {
                "type": d.type.value,
                "strength": d.strength.value,
                "matched": d.matched_text,
                "rule": d.rule_name,
            }
            for d in detections
        ]
    }

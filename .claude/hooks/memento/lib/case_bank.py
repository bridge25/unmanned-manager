"""
Case Bank - Memento 케이스 저장소 관리
"""
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Case:
    """의사결정 케이스"""
    id: str
    date: str
    situation: str
    options: str
    decision: str
    rationale: str
    result: str
    learning: str
    tags: list[str]


class CaseBank:
    """Case Bank 읽기/쓰기/검색"""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.cases_file = project_dir / "current" / "cases.md"

    def exists(self) -> bool:
        """Case Bank 파일 존재 여부"""
        return self.cases_file.exists()

    def load_cases(self) -> list[Case]:
        """모든 케이스 로드"""
        if not self.exists():
            return []

        content = self.cases_file.read_text(encoding="utf-8")
        cases = []

        # 각 케이스 섹션 파싱 (## CXXX: 로 시작, 다음 케이스나 Template 전까지)
        case_pattern = r"## (C\d+): (.+?)(?=\n## C\d+:|\n## Template|\Z)"
        matches = re.findall(case_pattern, content, re.DOTALL)

        for case_id, case_content in matches:
            case = self._parse_case(case_id, case_content)
            if case and case.situation:  # 유효한 케이스만
                cases.append(case)

        return cases

    def _parse_case(self, case_id: str, content: str) -> Optional[Case]:
        """케이스 내용 파싱 (마크다운 테이블 형식)"""
        try:
            def extract_field(field_name: str) -> str:
                # 테이블 형식: | **필드명** | 값 |
                pattern = rf"\|\s*\*\*{field_name}\*\*\s*\|\s*(.+?)\s*\|"
                match = re.search(pattern, content)
                return match.group(1).strip() if match else ""

            tags_str = extract_field("태그")
            tags = re.findall(r"#(\w+)", tags_str)

            return Case(
                id=case_id,
                date=extract_field("날짜"),
                situation=extract_field("상황"),
                options=extract_field("선택지"),
                decision=extract_field("판단"),
                rationale=extract_field("근거"),
                result=extract_field("결과"),
                learning=extract_field("학습"),
                tags=tags,
            )
        except Exception:
            return None

    def search_by_tags(self, search_tags: list[str]) -> list[Case]:
        """태그로 케이스 검색"""
        cases = self.load_cases()
        results = []

        for case in cases:
            if any(tag in case.tags for tag in search_tags):
                results.append(case)

        return results

    def search_by_keywords(self, keywords: list[str], top_k: int = 3) -> list[Case]:
        """키워드로 케이스 검색 (간단한 매칭)"""
        cases = self.load_cases()
        scored = []

        for case in cases:
            score = 0
            # 모든 필드를 검색 대상으로
            case_text = f"{case.situation} {case.options} {case.decision} {case.rationale} {case.learning} {' '.join(case.tags)}".lower()

            for kw in keywords:
                if kw.lower() in case_text:
                    score += 1
                # 태그 정확 매칭은 가중치 더 높게
                if kw.lower() in [t.lower() for t in case.tags]:
                    score += 2

            if score > 0:
                scored.append((score, case))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [case for _, case in scored[:top_k]]

    def get_next_id(self) -> str:
        """다음 케이스 ID 생성"""
        cases = self.load_cases()
        if not cases:
            return "C001"

        max_num = 0
        for case in cases:
            num = int(case.id[1:])
            max_num = max(max_num, num)

        return f"C{max_num + 1:03d}"

    def format_for_context(self, cases: list[Case]) -> str:
        """케이스들을 컨텍스트용 문자열로 변환"""
        if not cases:
            return ""

        lines = []
        for case in cases:
            lines.append(f"📋 {case.id}: {case.situation}")
            lines.append(f"   판단: {case.decision}")
            lines.append(f"   결과: {case.result}")
            lines.append(f"   학습: {case.learning}")
            lines.append("")

        return "\n".join(lines)

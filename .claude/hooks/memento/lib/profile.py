"""
Memento v2 Profile Library
Profile.md 파싱 및 요약 유틸리티
"""
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ProfileSummary:
    """Profile 요약 데이터"""
    # Facts
    name: str = "형님"
    family: list[str] = field(default_factory=list)
    goals: list[str] = field(default_factory=list)

    # Preferences
    communication_style: list[str] = field(default_factory=list)
    likes: list[str] = field(default_factory=list)
    dislikes: list[str] = field(default_factory=list)
    values: list[str] = field(default_factory=list)

    # Patterns
    work_style: list[str] = field(default_factory=list)
    stress_factors: list[str] = field(default_factory=list)
    warning_patterns: list[str] = field(default_factory=list)

    # Recent observations
    recent_observations: list[str] = field(default_factory=list)


def parse_profile(profile_path: Path) -> Optional[ProfileSummary]:
    """
    profile.md 파싱

    Args:
        profile_path: profile.md 경로

    Returns:
        ProfileSummary 또는 None
    """
    if not profile_path.exists():
        return None

    try:
        content = profile_path.read_text(encoding="utf-8")
    except Exception:
        return None

    summary = ProfileSummary()

    # 섹션별 파싱
    sections = re.split(r'\n## ', content)

    for section in sections:
        section_lower = section.lower()

        # Facts 섹션
        if section_lower.startswith('facts'):
            # 가족 정보
            family_match = re.findall(r'\*\*(?:와이프|자녀|가족)\*\*:\s*(.+)', section)
            summary.family = family_match

            # 장기 비전 (첫 번째 목표)
            vision_match = re.search(r'\|\s*1\s*\|\s*(.+?)\s*\|', section)
            if vision_match:
                summary.goals.append(vision_match.group(1).strip())

        # Preferences 섹션
        elif section_lower.startswith('preferences'):
            # 커뮤니케이션 스타일
            comm_matches = re.findall(r'\*\*(?:말투|정보량|형식|설명)\*\*:\s*(.+)', section)
            summary.communication_style = comm_matches

            # 싫어하는 것
            dislikes_section = re.search(r'### 싫어하는 것\n((?:- .+\n?)+)', section)
            if dislikes_section:
                summary.dislikes = [
                    line.strip('- \n')
                    for line in dislikes_section.group(1).split('\n')
                    if line.strip().startswith('-')
                ]

            # 가치관
            values_section = re.search(r'### 가치관\n((?:- .+\n?)+)', section)
            if values_section:
                summary.values = [
                    re.sub(r'\*\*(.+?)\*\*', r'\1', line.strip('- \n'))
                    for line in values_section.group(1).split('\n')
                    if line.strip().startswith('-')
                ][:3]  # 상위 3개만

        # Patterns 섹션
        elif section_lower.startswith('patterns'):
            # 스트레스 요인
            stress_section = re.search(r'### 스트레스 요인\n((?:- .+\n?)+)', section)
            if stress_section:
                summary.stress_factors = [
                    re.sub(r'\*\*(.+?)\*\*', r'\1', line.strip('- \n'))
                    for line in stress_section.group(1).split('\n')
                    if line.strip().startswith('-')
                ][:3]  # 상위 3개만

            # 주의 패턴
            warning_section = re.search(r'### 주의 패턴[^\n]*\n((?:- .+\n?)+)', section)
            if warning_section:
                summary.warning_patterns = [
                    line.strip('- \n')
                    for line in warning_section.group(1).split('\n')
                    if line.strip().startswith('-') and '관찰 중' not in line
                ]

        # Observations 섹션
        elif section_lower.startswith('observations'):
            # 최근 관찰 (마지막 날짜 기준 3개)
            obs_matches = re.findall(r'- (.+)', section)
            summary.recent_observations = obs_matches[-5:] if obs_matches else []

    return summary


def format_profile_context(summary: ProfileSummary) -> str:
    """
    Profile 요약을 컨텍스트 형식으로 포맷

    Args:
        summary: ProfileSummary 객체

    Returns:
        포맷된 컨텍스트 문자열
    """
    lines = ["[Memento Profile 요약]", ""]

    # 핵심 정보
    lines.append("👤 **형님 정보:**")
    if summary.family:
        lines.append(f"  - 가족: {', '.join(summary.family)}")
    if summary.goals:
        lines.append(f"  - 1차 목표: {summary.goals[0]}")
    lines.append("")

    # 선호사항
    lines.append("💡 **선호사항:**")
    if summary.communication_style:
        lines.append(f"  - 커뮤니케이션: {', '.join(summary.communication_style[:2])}")
    if summary.dislikes:
        lines.append(f"  - 싫어함: {', '.join(summary.dislikes[:3])}")
    lines.append("")

    # 가치관
    if summary.values:
        lines.append("🎯 **가치관:**")
        lines.append(f"  - {', '.join(summary.values)}")
        lines.append("")

    # 주의사항
    if summary.stress_factors:
        lines.append("⚠️ **스트레스 요인:**")
        for factor in summary.stress_factors[:2]:
            lines.append(f"  - {factor}")
        lines.append("")

    # 주의 패턴
    if summary.warning_patterns:
        lines.append("🔴 **주의 패턴 (True Ally 참조):**")
        for pattern in summary.warning_patterns[:3]:
            lines.append(f"  - {pattern}")
        lines.append("")

    lines.append("이 정보를 바탕으로 응대하세요.")

    return "\n".join(lines)


def get_profile_hash(profile_path: Path) -> str:
    """
    Profile 파일의 해시값 (변경 감지용)

    Args:
        profile_path: profile.md 경로

    Returns:
        파일 해시 (간단한 체크섬)
    """
    if not profile_path.exists():
        return ""

    try:
        content = profile_path.read_text(encoding="utf-8")
        # 간단한 해시: 파일 크기 + 마지막 100자
        return f"{len(content)}:{hash(content[-100:]) if len(content) > 100 else hash(content)}"
    except Exception:
        return ""

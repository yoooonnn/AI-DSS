import json
import random
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict, Optional

# nltk 자원을 다운로드해야 합니다.
nltk.download("wordnet")
nltk.download("omw-1.4")

class QueryAugmenter:
    def __init__(self):
        self.patterns = {
            "usage_stats": [
                "Can you {verb} the {timeframe} usage {type} for {device}",
                "{verb} me {timeframe} {type} of usage for {device}",
                "I need to {verb} {timeframe} {type} about {device} usage",
                "Would you {verb} {timeframe} usage {type} of {device}",
                "{verb} {timeframe} {type} for {device} usage",
                "I want to {verb} {timeframe} usage {type} for {device}",
                "Could you {verb} me {timeframe} {type} for {device}",
                "Please {verb} {timeframe} usage {type} of {device}",
                "Help me {verb} {timeframe} {type} for {device} usage",
                "{verb} {device}'s {timeframe} usage {type}"
            ],
            "active_hours": [
                "When is {device} {used} most {frequently}",
                "{verb} me the most {active} times for {device}",
                "What are the peak {duration} of {device} {activity}",
                "I want to know the {active} {duration} for {device}",
                "Which {duration} have the most {device} {activity}",
                "What {duration} is {device} most {active}",
                "{verb} me when {device} is most {active}",
                "During which {duration} is {device} most {active}",
                "What's the peak {activity} time for {device}",
                "When does {device} get the most {activity}"
            ],
            "time_analysis": [
                "{verb} me {timeframe} {activity} {pattern} for {device}",
                "How does {device} {activity} {vary} by {timeframe}",
                "What's the {timeframe} {pattern} of {device} {activity}",
                "{verb} {device} {activity} {pattern} {timeframe}",
                "I need to see {timeframe} {activity} {pattern} of {device}",
                "Could you {verb} {timeframe} {pattern} for {device} {activity}",
                "What {pattern} do you see in {device}'s {timeframe} {activity}",
                "{verb} me how {device} {activity} {varies} {timeframe}",
                "Analyze {device} {activity} {timeframe}",
                "{timeframe} {activity} {analysis} for {device}"
            ]
        }

        self.components = {
            "verb": ["show", "get", "tell", "display", "fetch", "give", "reveal", "present", "provide", "generate"],
            "type": ["statistics", "analytics", "patterns", "trends", "data", "information", "metrics", "numbers", "details"],
            "active": ["active", "busy", "frequent", "used", "popular", "intensive", "heavy"],
            "activity": ["usage", "activity", "utilization", "operation", "consumption", "use"],
            "duration": ["hours", "times", "periods", "moments", "intervals"],
            "frequently": ["frequently", "often", "regularly", "heavily", "consistently"],
            "used": ["used", "activated", "operated", "utilized", "running"],
            "pattern": ["pattern", "trend", "distribution", "behavior", "tendency"],
            "vary": ["vary", "change", "differ", "fluctuate", "shift"],
            "varies": ["varies", "changes", "differs", "fluctuates", "shifts"],
            "analysis": ["analysis", "breakdown", "assessment", "summary", "overview"]
        }

        self.timeframes = {
            "hourly": ["hourly", "hour by hour", "per hour", "hour-wise", "by the hour", "each hour"],
            "daily": ["daily", "day by day", "per day", "day-wise", "by the day", "each day"],
            "monthly": ["monthly", "month by month", "per month", "month-wise", "by the month", "each month"]
        }

    def _classify_query(self, query: str) -> str:
        """쿼리 타입 분류"""
        query = query.lower()
        if "active" in query or "peak" in query:
            return "active_hours"
        elif any(word in query for word in ["pattern", "trend", "vary", "analysis"]):
            return "time_analysis"
        else:
            return "usage_stats"

    def _extract_timeframe(self, query: str) -> Optional[str]:
        """시간 프레임 추출"""
        query = query.lower()
        for timeframe, variants in self.timeframes.items():
            if any(variant in query for variant in variants):
                return timeframe
        return None

    def _extract_device(self, query: str) -> Optional[str]:
        """디바이스 타입 추출"""
        if "speaker" in query.lower():
            return "Speaker"
        elif "light" in query.lower():
            return "Light"
        return None

    def _get_synonyms(self, word: str) -> List[str]:
        """단어에 대한 동의어를 가져옴"""
        synonyms = set()
        for syn in wn.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return list(synonyms)

    def augment(self, query: str, num_augmentations: int = 4) -> List[str]:
        query_type = self._classify_query(query)
        device = self._extract_device(query)
        timeframe = self._extract_timeframe(query)
        
        if not device or not query_type:
            return [query]  # 적절한 분류가 불가능한 경우 원본 반환

        augmented = set()
        augmented.add(query)  # 원본 보존

        # 패턴 기반 증강
        while len(augmented) < num_augmentations + 1:
            pattern = random.choice(self.patterns[query_type])
            
            # 컴포넌트 랜덤 선택
            components = {
                "verb": random.choice(self.components["verb"]),
                "type": random.choice(self.components["type"]),
                "active": random.choice(self.components["active"]),
                "activity": random.choice(self.components["activity"]),
                "duration": random.choice(self.components["duration"]),
                "frequently": random.choice(self.components["frequently"]),
                "used": random.choice(self.components["used"]),
                "pattern": random.choice(self.components["pattern"]),
                "vary": random.choice(self.components["vary"]),
                "varies": random.choice(self.components["varies"]),
                "analysis": random.choice(self.components["analysis"]),
                "device": device,
                "timeframe": random.choice(self.timeframes[timeframe]) if timeframe else "hourly"
            }

            # 동의어로 일부 컴포넌트 변경
            for key in ["verb", "type", "activity", "pattern"]:
                synonyms = self._get_synonyms(components[key])
                if synonyms:
                    components[key] = random.choice(synonyms)

            # 새로운 쿼리 생성
            new_query = pattern.format(**components)
            
            # 첫 글자 대문자화
            new_query = new_query[0].upper() + new_query[1:]
            
            # 중복 방지
            if new_query != query:
                augmented.add(new_query)

        return list(augmented)[:num_augmentations + 1]

def process_and_augment_dataset(input_file: str, output_file: str, num_augmentations: int = 4):
    # 입력 파일에서 데이터 읽기
    with open(input_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    # QueryAugmenter 인스턴스 생성
    augmenter = QueryAugmenter()
    augmented_data = []

    # 데이터 증강
    for item in data.get("dataset", []):
        original_query = item.get("input", "")
        if original_query:
            augmented_queries = augmenter.augment(original_query, num_augmentations)

            augmented_data.append({
                "input": augmented_queries[0],  # 증강된 쿼리
                "output": item.get("output", "")  # output은 그대로 유지
            })

    # 증강된 데이터 저장
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump({"augmented_dataset": augmented_data}, outfile, ensure_ascii=False, indent=4)

# 실행 예시
if __name__ == "__main__":
    process_and_augment_dataset("ai/data/query_dataset.json", "ai/data/augmented_dataset.json")

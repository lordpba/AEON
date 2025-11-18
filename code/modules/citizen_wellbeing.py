"""Citizen Wellbeing Module
Monitors citizen satisfaction, quality of life, and public sentiment
"""
from typing import Dict, List, Any
import random
import threading
from loguru import logger

class CitizenWellbeing:
    def __init__(self):
        self.lock = threading.Lock()
        self.wellbeing_data = {}  # Dictionary to store wellbeing metrics
        self.satisfaction_scores = {}  # Overall satisfaction per citizen
        self.public_sentiment = 0.0  # Average community sentiment (-100 to +100)

    def run(self):
        """Continuously monitor citizen wellbeing and satisfaction."""
        while True:
            self.update_wellbeing_metrics()
            self.analyze_satisfaction_trends()
            self.identify_issues()

    def update_wellbeing_metrics(self):
        """Update wellbeing metrics for all citizens."""
        with self.lock:
            for citizen in self.get_citizens():
                self.wellbeing_data[citizen] = self.assess_quality_of_life(citizen)
                self.satisfaction_scores[citizen] = self.calculate_satisfaction(citizen)

    def assess_quality_of_life(self, citizen: str) -> Dict[str, Any]:
        """Assess quality of life metrics for a citizen."""
        return {
            "housing_satisfaction": random.randint(1, 10),
            "job_satisfaction": random.randint(1, 10),
            "public_services_rating": random.randint(1, 10),
            "safety_perception": random.randint(1, 10),
            "environmental_quality": random.randint(1, 10),
            "community_engagement": random.randint(1, 10)
        }

    def calculate_satisfaction(self, citizen: str) -> float:
        """Calculate overall satisfaction score (0-100)."""
        if citizen not in self.wellbeing_data:
            return 50.0
        
        metrics = self.wellbeing_data[citizen]
        # Weighted average
        weights = {
            "housing_satisfaction": 0.20,
            "job_satisfaction": 0.20,
            "public_services_rating": 0.20,
            "safety_perception": 0.15,
            "environmental_quality": 0.15,
            "community_engagement": 0.10
        }
        
        score = sum(metrics[k] * weights[k] for k in weights) * 10
        return round(score, 1)

    def analyze_satisfaction_trends(self) -> Dict[str, Any]:
        """Analyze satisfaction trends across the community."""
        with self.lock:
            if not self.satisfaction_scores:
                return {}
            
            avg_satisfaction = sum(self.satisfaction_scores.values()) / len(self.satisfaction_scores)
            self.public_sentiment = (avg_satisfaction - 50) * 2  # Scale to -100 to +100
            
            trends = {
                "average_satisfaction": round(avg_satisfaction, 1),
                "public_sentiment": round(self.public_sentiment, 1),
                "highly_satisfied": sum(1 for s in self.satisfaction_scores.values() if s >= 75) / len(self.satisfaction_scores) * 100,
                "dissatisfied": sum(1 for s in self.satisfaction_scores.values() if s < 40) / len(self.satisfaction_scores) * 100
            }
            
            logger.debug(f"Satisfaction trends: {trends}")
            return trends

    def identify_issues(self):
        """Identify and log citizen wellbeing issues."""
        with self.lock:
            for citizen, satisfaction in self.satisfaction_scores.items():
                if satisfaction < 30:
                    logger.warning(f"Citizen {citizen} is highly dissatisfied (score: {satisfaction})")
                    self.recommend_intervention(citizen)
                elif satisfaction < 50:
                    logger.info(f"Citizen {citizen} shows moderate dissatisfaction (score: {satisfaction})")

    def recommend_intervention(self, citizen: str):
        """Recommend interventions to improve citizen satisfaction."""
        if citizen not in self.wellbeing_data:
            return
        
        data = self.wellbeing_data[citizen]
        low_metrics = {k: v for k, v in data.items() if v < 5}
        
        if low_metrics:
            logger.info(f"Recommended actions for {citizen}: {low_metrics}")

    def get_citizens(self) -> List[str]:
        """Get list of all citizens (simulated)."""
        return [f"Citizen_{i}" for i in range(1, 101)]  # 100 simulated citizens
    
    def get_status(self) -> Dict[str, Any]:
        """Get current wellbeing status summary."""
        with self.lock:
            trends = self.analyze_satisfaction_trends()
            return {
                "public_sentiment": self.public_sentiment,
                "average_satisfaction": trends.get("average_satisfaction", 50.0),
                "trends": trends
            }
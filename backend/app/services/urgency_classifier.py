"""
Urgency Classification Service for EchoMind.
Detects crisis keywords and classifies urgency level of user queries.
"""
from typing import Dict, List, Tuple
import re
from app.models.schemas import UrgencyLevel, EmergencyContact
from app.core.config import settings
from loguru import logger


class UrgencyClassifier:
    """Classifier for detecting urgency level in user queries."""
    
    def __init__(self):
        """Initialize urgency classifier with crisis keywords."""
        
        # Critical keywords indicating immediate crisis
        self.critical_keywords = {
            'suicide', 'suicidal', 'kill myself', 'end my life', 'want to die',
            'self harm', 'self-harm', 'hurt myself', 'cutting', 'overdose',
            'no reason to live', 'better off dead', 'end it all'
        }
        
        # High urgency keywords
        self.high_urgency_keywords = {
            'panic attack', 'cant breathe', "can't breathe", 'severe anxiety',
            'breakdown', 'mental breakdown', 'crisis', 'emergency',
            'desperate', 'hopeless', 'cant take it', "can't take it",
            'overwhelming', 'intense fear', 'terrified'
        }
        
        # Medium urgency keywords
        self.medium_urgency_keywords = {
            'anxious', 'depressed', 'stressed', 'worried', 'scared',
            'sad', 'lonely', 'isolated', 'struggling', 'difficult',
            'overwhelmed', 'burnout', 'exhausted', 'sleepless'
        }
        
        # Emergency contacts by country
        self.emergency_contacts = {
            'US': EmergencyContact(
                name="988 Suicide & Crisis Lifeline",
                phone="988",
                description="24/7 crisis support for emotional distress or suicidal crisis",
                available_247=True,
                country="United States"
            ),
            'INDIA': EmergencyContact(
                name="AASRA Helpline",
                phone="9152987821",
                description="24/7 crisis intervention center for suicide prevention",
                available_247=True,
                country="India"
            ),
            'CRISIS_TEXT': EmergencyContact(
                name="Crisis Text Line",
                phone="741741",
                description="Text HOME to 741741 for 24/7 crisis support via text",
                available_247=True,
                country="United States"
            )
        }
        
        logger.info("Urgency Classifier initialized")
    
    def classify_urgency(self, query: str) -> Tuple[UrgencyLevel, List[EmergencyContact]]:
        """
        Classify the urgency level of a user query.
        
        Args:
            query: User's query text
            
        Returns:
            Tuple of (UrgencyLevel, List of relevant emergency contacts)
        """
        query_lower = query.lower()
        
        # Check for critical keywords
        if self._contains_keywords(query_lower, self.critical_keywords):
            logger.warning(f"CRITICAL urgency detected in query")
            return UrgencyLevel.CRITICAL, list(self.emergency_contacts.values())
        
        # Check for high urgency keywords
        if self._contains_keywords(query_lower, self.high_urgency_keywords):
            logger.info(f"HIGH urgency detected in query")
            return UrgencyLevel.HIGH, [
                self.emergency_contacts['US'],
                self.emergency_contacts['INDIA']
            ]
        
        # Check for medium urgency keywords
        if self._contains_keywords(query_lower, self.medium_urgency_keywords):
            logger.info(f"MEDIUM urgency detected in query")
            return UrgencyLevel.MEDIUM, []
        
        # Default to low urgency
        logger.info(f"LOW urgency detected in query")
        return UrgencyLevel.LOW, []
    
    def _contains_keywords(self, text: str, keywords: set) -> bool:
        """
        Check if text contains any of the specified keywords.
        
        Args:
            text: Text to search
            keywords: Set of keywords to look for
            
        Returns:
            True if any keyword is found
        """
        for keyword in keywords:
            # Use word boundaries for more accurate matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def get_risk_score(self, query: str) -> float:
        """
        Calculate a risk score (0-1) for the query.
        
        Args:
            query: User's query text
            
        Returns:
            Risk score between 0 (low risk) and 1 (high risk)
        """
        query_lower = query.lower()
        score = 0.0
        
        # Count critical keywords
        critical_count = sum(1 for kw in self.critical_keywords 
                           if self._contains_keywords(query_lower, {kw}))
        score += critical_count * 0.4
        
        # Count high urgency keywords
        high_count = sum(1 for kw in self.high_urgency_keywords 
                        if self._contains_keywords(query_lower, {kw}))
        score += high_count * 0.2
        
        # Count medium urgency keywords
        medium_count = sum(1 for kw in self.medium_urgency_keywords 
                          if self._contains_keywords(query_lower, {kw}))
        score += medium_count * 0.1
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def should_show_emergency_banner(self, urgency: UrgencyLevel) -> bool:
        """
        Determine if emergency contact banner should be shown.
        
        Args:
            urgency: Detected urgency level
            
        Returns:
            True if emergency banner should be displayed
        """
        return urgency in [UrgencyLevel.CRITICAL, UrgencyLevel.HIGH]
    
    def get_urgency_message(self, urgency: UrgencyLevel) -> str:
        """
        Get an appropriate message based on urgency level.
        
        Args:
            urgency: Detected urgency level
            
        Returns:
            Message string for the urgency level
        """
        messages = {
            UrgencyLevel.CRITICAL: (
                "⚠️ If you're in crisis, please reach out for immediate help. "
                "Your life matters, and support is available 24/7."
            ),
            UrgencyLevel.HIGH: (
                "It sounds like you're going through a difficult time. "
                "Consider reaching out to a crisis hotline or mental health professional."
            ),
            UrgencyLevel.MEDIUM: (
                "I'm here to help you find the support you need. "
                "Let's explore resources that might be helpful for you."
            ),
            UrgencyLevel.LOW: (
                "I'll do my best to provide you with helpful information and resources."
            )
        }
        return messages.get(urgency, messages[UrgencyLevel.LOW])

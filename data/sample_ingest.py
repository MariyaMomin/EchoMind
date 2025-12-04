"""
Sample Data Ingestion Script for EchoMind
This script demonstrates how to ingest mental wellness resources into the vector database.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.rag_service import RAGService
from app.models.schemas import SourceType

# Sample mental wellness documents
SAMPLE_DOCUMENTS = [
    {
        "text": """
        Understanding Anxiety in College Students
        
        Anxiety is one of the most common mental health concerns affecting college students today. 
        It can manifest as persistent worry, racing thoughts, difficulty concentrating, or physical 
        symptoms like rapid heartbeat and sweating.
        
        Common Triggers:
        - Academic pressure and exams
        - Social situations and relationships
        - Financial concerns
        - Future career uncertainty
        
        Coping Strategies:
        1. Practice mindfulness and deep breathing exercises
        2. Maintain a regular sleep schedule
        3. Exercise regularly (even 20 minutes daily helps)
        4. Connect with friends and support networks
        5. Seek professional help when needed
        
        When to Seek Help:
        - Anxiety interferes with daily activities
        - Physical symptoms persist
        - You feel overwhelmed or hopeless
        - Sleep or eating patterns are significantly affected
        
        Resources:
        - Campus counseling centers offer free services
        - Anxiety support groups provide peer connection
        - Online therapy platforms offer flexible scheduling
        """,
        "source_name": "University Mental Health Guide",
        "source_type": SourceType.UNIVERSITY,
        "source_url": "https://counseling.university.edu/anxiety"
    },
    {
        "text": """
        Depression: Signs and Support
        
        Depression is more than just feeling sad. It's a serious mental health condition that 
        affects how you think, feel, and handle daily activities.
        
        Common Signs:
        - Persistent sad, anxious, or "empty" mood
        - Loss of interest in activities once enjoyed
        - Changes in appetite or weight
        - Difficulty sleeping or oversleeping
        - Loss of energy or increased fatigue
        - Feelings of worthlessness or excessive guilt
        - Difficulty thinking or concentrating
        - Thoughts of death or suicide
        
        What Helps:
        - Professional counseling or therapy
        - Medication (consult with a healthcare provider)
        - Regular physical activity
        - Connecting with supportive people
        - Maintaining a routine
        - Getting adequate sleep
        
        Important: If you have thoughts of self-harm or suicide, please seek immediate help.
        Call 988 (Suicide & Crisis Lifeline) or go to your nearest emergency room.
        
        Free Resources:
        - National Institute of Mental Health (NIMH)
        - Depression and Bipolar Support Alliance (DBSA)
        - Your university counseling center
        """,
        "source_name": "NIMH Depression Guide",
        "source_type": SourceType.GOVERNMENT,
        "source_url": "https://www.nimh.nih.gov/health/topics/depression"
    },
    {
        "text": """
        Stress Management for Students
        
        Stress is a normal part of life, but chronic stress can impact your physical and mental health.
        
        Quick Stress Relief Techniques:
        1. Deep Breathing: Inhale for 4 counts, hold for 4, exhale for 4
        2. Progressive Muscle Relaxation: Tense and release each muscle group
        3. Grounding Exercise: Name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste
        4. Take a short walk outside
        5. Listen to calming music
        
        Long-term Stress Management:
        - Time management and prioritization
        - Regular exercise (yoga, running, sports)
        - Adequate sleep (7-9 hours)
        - Healthy eating habits
        - Social connections and support
        - Hobbies and leisure activities
        - Setting boundaries and saying no
        
        Academic Stress:
        - Break large tasks into smaller steps
        - Use a planner or digital calendar
        - Join study groups
        - Utilize academic support services
        - Talk to professors about concerns
        
        Remember: It's okay to ask for help. Campus resources are there to support you.
        """,
        "source_name": "Student Wellness Center",
        "source_type": SourceType.UNIVERSITY,
        "source_url": "https://wellness.university.edu/stress-management"
    },
    {
        "text": """
        Crisis Resources and Emergency Contacts
        
        If you or someone you know is in immediate danger or experiencing a mental health crisis:
        
        National Crisis Hotlines:
        - 988 Suicide & Crisis Lifeline: Call or text 988 (Available 24/7)
        - Crisis Text Line: Text HOME to 741741 (Available 24/7)
        - SAMHSA National Helpline: 1-800-662-HELP (4357)
        - Veterans Crisis Line: Call 988 and press 1, or text 838255
        
        International Crisis Lines:
        - AASRA (India): +91 9152987821
        - Lifeline (Australia): 13 11 14
        - Samaritans (UK): 116 123
        
        Campus Resources:
        - Campus Police/Security: Available 24/7
        - University Counseling Center: Urgent appointments available
        - Student Health Services: Walk-in crisis support
        - Resident Advisors (RAs): First point of contact in dorms
        
        Warning Signs of Crisis:
        - Talking about wanting to die or hurt oneself
        - Looking for ways to end one's life
        - Talking about feeling hopeless or having no purpose
        - Extreme mood swings
        - Withdrawal from friends and activities
        - Increased substance use
        - Acting anxious or agitated
        - Sleeping too much or too little
        - Giving away possessions
        
        What to Do:
        1. Take the situation seriously
        2. Listen without judgment
        3. Stay with the person or ensure they're not alone
        4. Remove any means of self-harm
        5. Call 988 or emergency services
        6. Follow up and continue support
        
        Remember: You are not alone. Help is available, and recovery is possible.
        """,
        "source_name": "National Crisis Resources",
        "source_type": SourceType.GOVERNMENT,
        "source_url": "https://988lifeline.org"
    }
]


def ingest_sample_data():
    """Ingest sample mental wellness documents into the vector database."""
    print("Initializing RAG Service...")
    rag_service = RAGService()
    
    print(f"\nIngesting {len(SAMPLE_DOCUMENTS)} sample documents...\n")
    
    for idx, doc in enumerate(SAMPLE_DOCUMENTS, 1):
        print(f"[{idx}/{len(SAMPLE_DOCUMENTS)}] Ingesting: {doc['source_name']}")
        
        result = rag_service.ingest_document(
            document_text=doc['text'],
            source_name=doc['source_name'],
            source_type=doc['source_type'],
            source_url=doc.get('source_url'),
            metadata={'topic': 'mental_wellness', 'language': 'en'}
        )
        
        if result['status'] == 'success':
            print(f"    ✓ Success! Created {result['chunks_created']} chunks")
        else:
            print(f"    ✗ Error: {result.get('error')}")
        print()
    
    # Get collection stats
    stats = rag_service.get_collection_stats()
    print("\n" + "="*50)
    print("Ingestion Complete!")
    print("="*50)
    print(f"Total documents in database: {stats.get('total_documents', 0)}")
    print(f"Collection status: {stats.get('status', 'unknown')}")
    print("\nYou can now start the FastAPI server and test queries!")


if __name__ == "__main__":
    ingest_sample_data()

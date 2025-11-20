"""
Test script for LangExtract extraction with sample German text.
"""
from src.agents.about_extractor import AboutExtractor
import sys


# Sample German business texts
SAMPLE_TEXTS = [
    {
        "name": "GmbH Example",
        "text": """
        Impressum
        
        Mustermann GmbH
        Geschäftsführer: Hans Müller
        
        Kontakt:
        E-Mail: h.mueller@mustermann.de
        Telefon: +49 123 456789
        Website: www.mustermann.de
        """
    },
    {
        "name": "Dental Practice",
        "text": """
        Angaben gemäß § 5 TMG
        
        Zahnärztin Dr. Claudia Becker
        Praxis für Zahnheilkunde
        
        Telefon: (0441) 560015-0
        Telefax: (0441) 560015-4
        E-Mail: praxis@dr-claudia-becker.de
        Internet: www.dr-claudia-becker.de
        """
    },
    {
        "name": "Law Firm",
        "text": """
        Rechtsanwaltskanzlei Schmidt & Partner
        
        Inhaber: RA Dr. jur. Michael Schmidt
        
        Kontakt:
        E-Mail: m.schmidt@ra-schmidt.de
        Telefon: +49 30 123456
        
        Rechtsform: Partnerschaftsgesellschaft
        Tätigkeitsbereich: Wirtschaftsrecht, Arbeitsrecht
        """
    }
]


def test_extraction():
    """Test extraction with sample texts."""
    print("🧪 Testing LangExtract Extraction...")
    print()
    
    try:
        # Initialize extractor
        extractor = AboutExtractor()
        print("✅ AboutExtractor initialized")
        print(f"📊 Model: {extractor.model_id}")
        print()
        
        success_count = 0
        
        for idx, sample in enumerate(SAMPLE_TEXTS, 1):
            print(f"[{idx}/{len(SAMPLE_TEXTS)}] Testing: {sample['name']}")
            print("-" * 60)
            
            result = extractor.extract_from_markdown_text(sample['text'])
            
            if result:
                print("✅ Extraction successful!")
                print(f"   Owner: {result.owner_name}")
                print(f"   Position: {result.position}")
                print(f"   Company: {result.company_name}")
                print(f"   Email: {result.email}")
                print(f"   Phone: {result.phone}")
                print(f"   Website: {result.website}")
                print(f"   Profession: {result.profession}")
                print(f"   Sector: {result.sector}")
                success_count += 1
            else:
                print("❌ Extraction failed")
            
            print()
        
        print("=" * 60)
        print(f"📊 Results: {success_count}/{len(SAMPLE_TEXTS)} successful")
        print("=" * 60)
        
        if success_count == len(SAMPLE_TEXTS):
            print("\n✅ All extraction tests passed!")
            return True
        else:
            print(f"\n⚠️  {len(SAMPLE_TEXTS) - success_count} tests failed")
            return False
        
    except Exception as e:
        print(f"\n❌ Extraction test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check GOOGLE_API_KEY in .env")
        print("2. Verify internet connection")
        print("3. Check API quota limits")
        return False


if __name__ == "__main__":
    success = test_extraction()
    sys.exit(0 if success else 1)

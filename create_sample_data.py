"""
Sample markdown generator for testing the extraction pipeline.

This script creates sample German business markdown files in MinIO
for testing purposes.
"""
from src.modules.minio_manager import MinIOManager
import io


SAMPLE_MARKDOWNS = [
    {
        "path": "scraped-content/example.de/impressum.md",
        "content": """# Impressum

## Angaben gemäß § 5 TMG

**Mustermann Consulting GmbH**

Geschäftsführer: Hans Müller
Handelsregister: HRB 12345
Registergericht: Amtsgericht München

## Kontakt

E-Mail: h.mueller@mustermann-consulting.de
Telefon: +49 89 123456-0
Telefax: +49 89 123456-99
Internet: www.mustermann-consulting.de

## Anschrift

Musterstraße 123
80333 München
Deutschland
"""
    },
    {
        "path": "scraped-content/zahnarzt-becker.de/about.md",
        "content": """# Über unsere Praxis

## Angaben gemäß § 5 TMG

Zahnärztin Dr. med. dent. Claudia Becker
Praxis für Zahnheilkunde und Implantologie

## Kontaktdaten

Telefon: (0441) 560015-0
Telefax: (0441) 560015-4
E-Mail: praxis@dr-claudia-becker.de
Website: www.dr-claudia-becker.de

## Qualifikationen

- Approbation als Zahnärztin
- Fachzahnarzt für Oralchirurgie
- Tätigkeitsschwerpunkt: Implantologie

## Anschrift

Bahnhofstraße 45
26122 Oldenburg
"""
    },
    {
        "path": "scraped-content/ra-schmidt.de/kontakt.md",
        "content": """# Kontakt

## Rechtsanwaltskanzlei Schmidt & Partner

**Inhaber:** Rechtsanwalt Dr. jur. Michael Schmidt

## Kontaktinformationen

E-Mail: m.schmidt@ra-schmidt.de
Telefon: +49 30 8765432-0
Fax: +49 30 8765432-99

## Rechtsform

Partnerschaftsgesellschaft mbB
Partnerschaftsregister: PR 5678
Registergericht: Amtsgericht Berlin

## Tätigkeitsbereiche

- Wirtschaftsrecht
- Arbeitsrecht
- Vertragsrecht
- Gesellschaftsrecht

## Kanzleiadresse

Unter den Linden 77
10117 Berlin
"""
    }
]


def create_sample_data():
    """Create sample markdown files in MinIO."""
    print("📝 Creating sample markdown files in MinIO...")
    print()
    
    minio = MinIOManager()
    
    for idx, sample in enumerate(SAMPLE_MARKDOWNS, 1):
        path = sample["path"]
        content = sample["content"]
        
        print(f"[{idx}/{len(SAMPLE_MARKDOWNS)}] Creating: {path}")
        
        # Upload markdown
        content_bytes = content.encode("utf-8")
        success = minio.put_object(
            object_name=path,
            data=content_bytes,
            length=len(content_bytes),
            content_type="text/markdown; charset=utf-8"
        )
        
        if not success:
            print(f"❌ Failed to create: {path}")
    
    print()
    print("✅ Sample data created successfully!")
    print()
    print("Next steps:")
    print("1. Run extraction: python src/agents/about_graph.py")
    print("2. Check results in MinIO console: http://localhost:9001")


if __name__ == "__main__":
    create_sample_data()

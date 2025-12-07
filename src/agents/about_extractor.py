"""
LangExtract-based German business information extractor.

This module uses Google's LangExtract library to extract structured
company information from German Impressum and About pages.
"""

import os
import textwrap
from typing import Optional

import langextract as lx

from src.config.settings import settings
from src.models.schemas import CompanyInfoLite
from src.modules.minio_manager import MinIOManager

# German business extraction prompt
ABOUT_PROMPT = textwrap.dedent(
    """
    Du bist ein deutscher Business-Informations-Extraktor.
    Extrahiere Firmen-/Praxisdaten aus Impressum / Kontakt / About-Us Texten.

    Regeln:
    - Nutze NUR explizit im Text vorhandene Informationen.
    - Wenn ein Feld fehlt, setze es auf leere Zeichenkette "".
    - Nutze E-Mails mit Personbezug vor generischen (info@, kontakt@).
    - Erkenne deutsche Begriffe wie: Impressum, Angaben gemäß § 5 TMG,
      Geschäftsführer, Inhaber, Praxisinhaber, Zahnärztin, Rechtsanwalt, GmbH, AG usw.

    Gib eine Liste von Extractions zurück mit Klasse "company_info"
    und folgenden Attributen:
    - owner_name: Name des Inhabers/Geschäftsführers
    - position: Position (z.B. Geschäftsführer, Inhaber)
    - company_name: Firmenname
    - email: E-Mail-Adresse (bevorzuge persönliche E-Mails)
    - phone: Telefonnummer
    - fax: Faxnummer
    - website: Website-URL
    - profession: Berufsbezeichnung (z.B. Dr. med. dent., Rechtsanwalt)
    - sector: Branche (z.B. Dentistry, Legal, Consulting)
"""
)


# Few-shot examples for better extraction accuracy
EXAMPLES = [
    lx.data.ExampleData(
        text=(
            "Impressum\nMustermann GmbH\n"
            "Geschäftsführer: Hans Müller\n"
            "E-Mail: h.mueller@mustermann.de"
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="company_info",
                extraction_text="Mustermann GmbH\nGeschäftsführer: Hans Müller\nE-Mail: h.mueller@mustermann.de",
                attributes={
                    "owner_name": "Hans Müller",
                    "position": "Geschäftsführer",
                    "company_name": "Mustermann GmbH",
                    "email": "h.mueller@mustermann.de",
                    "phone": "",
                    "fax": "",
                    "website": "",
                    "profession": "",
                    "sector": "",
                },
            )
        ],
    ),
    lx.data.ExampleData(
        text=(
            "Angaben gemäß § 5 TMG: Zahnärztin Dr. Claudia Becker, "
            "Telefon: (0441) 560015-0, Telefax: (0441) 560015-4, "
            "E-Mail: praxis@dr-claudia-becker.de, Internet: www.dr-claudia-becker.de"
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="company_info",
                extraction_text="Zahnärztin Dr. Claudia Becker",
                attributes={
                    "owner_name": "Claudia Becker",
                    "position": "Zahnärztin",
                    "company_name": "",
                    "email": "praxis@dr-claudia-becker.de",
                    "phone": "(0441) 560015-0",
                    "fax": "(0441) 560015-4",
                    "website": "www.dr-claudia-becker.de",
                    "profession": "Dr. med. dent.",
                    "sector": "Dentistry",
                },
            )
        ],
    ),
    lx.data.ExampleData(
        text=(
            "Rechtsanwaltskanzlei Schmidt & Partner\n"
            "Inhaber: RA Dr. jur. Michael Schmidt\n"
            "Kontakt: m.schmidt@ra-schmidt.de\n"
            "Tel: +49 30 123456"
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="company_info",
                extraction_text="Rechtsanwaltskanzlei Schmidt & Partner",
                attributes={
                    "owner_name": "Michael Schmidt",
                    "position": "Inhaber",
                    "company_name": "Rechtsanwaltskanzlei Schmidt & Partner",
                    "email": "m.schmidt@ra-schmidt.de",
                    "phone": "+49 30 123456",
                    "fax": "",
                    "website": "",
                    "profession": "Rechtsanwalt Dr. jur.",
                    "sector": "Legal",
                },
            )
        ],
    ),
]


class AboutExtractor:
    """
    LangExtract-based extractor for German business information.
    """

    def __init__(self, model_id: Optional[str] = None):
        """
        Initialize the extractor.

        Args:
            model_id: LLM model to use (defaults to settings.langextract_model)
        """
        self.model_id = model_id or settings.langextract_model
        self.minio = MinIOManager()

        # Set up API key for Gemini
        if settings.google_api_key:
            os.environ["GOOGLE_API_KEY"] = settings.google_api_key

    def extract_from_markdown_text(self, text: str) -> Optional[CompanyInfoLite]:
        """
        Extract company information from markdown text.

        Args:
            text: Markdown content to extract from

        Returns:
            CompanyInfoLite object or None if extraction failed
        """
        if not text or len(text.strip()) < 10:
            print("⚠️  Text too short for extraction")
            return None

        try:
            result = lx.extract(
                text_or_documents=text,
                prompt_description=ABOUT_PROMPT,
                examples=EXAMPLES,
                model_id=self.model_id,
                fence_output=True,  # Recommended for OpenAI models
                use_schema_constraints=False,
            )

            # LangExtract returns extraction objects
            if not result or not result.extractions:
                print("⚠️  No extractions found")
                return None

            # Find the first company_info extraction
            for ext in result.extractions:
                if ext.extraction_class == "company_info":
                    attrs = ext.attributes or {}

                    company_info = CompanyInfoLite(
                        owner_name=attrs.get("owner_name", "") or "",
                        position=attrs.get("position", "") or "",
                        company_name=attrs.get("company_name", "") or "",
                        email=attrs.get("email", "") or "",
                        phone=attrs.get("phone", "") or "",
                        fax=attrs.get("fax", "") or "",
                        website=attrs.get("website", "") or "",
                        profession=attrs.get("profession", "") or "",
                        sector=attrs.get("sector", "") or "",
                    )

                    print(
                        f"✓ Extracted: {company_info.company_name or company_info.owner_name}"
                    )
                    return company_info

            return None

        except Exception as e:
            print(f"✗ Extraction error: {e}")
            return None

    def extract_from_minio_object(self, object_name: str) -> Optional[CompanyInfoLite]:
        """
        Extract company information from a MinIO object.

        Args:
            object_name: Full path to the markdown file in MinIO

        Returns:
            CompanyInfoLite object or None if extraction failed
        """
        print(f"📥 Downloading: {object_name}")
        markdown = self.minio.download_object(object_name, as_text=True)

        if not markdown:
            print(f"✗ Failed to download: {object_name}")
            return None

        return self.extract_from_markdown_text(markdown)

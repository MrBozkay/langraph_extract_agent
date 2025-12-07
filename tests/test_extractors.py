"""
Test extraction agents functionality.
"""

from unittest.mock import Mock, patch


from src.agents.about_extractor import AboutExtractor
from src.agents.about_extractor_v2 import AboutExtractorV2
from src.models.schemas import CompanyInfoLite


class TestAboutExtractor:
    """Test basic about extractor."""

    @patch("src.agents.about_extractor.settings")
    def test_init(self, mock_settings):
        """Test extractor initialization."""
        mock_settings.google_api_key = "test-key"
        mock_settings.langextract_model = "test-model"

        extractor = AboutExtractor()

        assert extractor.model_id == "test-model"

    @patch("src.agents.about_extractor.lx.extract")
    def test_extract_from_markdown_text_success(self, mock_call):
        """Test successful extraction."""
        # Mock successful extraction
        mock_result = Mock()
        mock_result.extractions = [Mock()]
        mock_result.extractions[0].owner_name = "Test Owner"
        mock_result.extractions[0].position = "CEO"
        mock_result.extractions[0].company_name = "Test Company"
        mock_result.extractions[0].email = "test@example.com"
        mock_result.extractions[0].phone = "+49 123 456789"
        mock_result.extractions[0].website = "www.example.com"
        mock_result.extractions[0].sector = "Technology"

        mock_call.return_value = mock_result

        extractor = AboutExtractor()
        result = extractor.extract_from_markdown_text("Test markdown content")

        assert result is not None
        assert result.owner_name == "Test Owner"
        assert result.position == "CEO"
        assert result.company_name == "Test Company"
        assert result.email == "test@example.com"
        assert result.phone == "+49 123 456789"
        assert result.website == "www.example.com"
        assert result.sector == "Technology"

    @patch("src.agents.about_extractor.lx.extract")
    def test_extract_from_markdown_text_failure(self, mock_call):
        """Test extraction failure."""
        mock_result = Mock()
        mock_result.extractions = []
        mock_call.return_value = mock_result

        extractor = AboutExtractor()
        result = extractor.extract_from_markdown_text("Test content")

        assert result is None


class TestAboutExtractorV2:
    """Test V2 about extractor."""

    @patch("src.agents.about_extractor_v2.settings")
    def test_init(self, mock_settings):
        """Test V2 extractor initialization."""
        mock_settings.google_api_key = "test-key"
        mock_settings.langextract_model = "test-model"

        extractor = AboutExtractorV2()

        assert extractor.model_id == "test-model"

    @patch("src.agents.about_extractor_v2.lx.extract")
    def test_extract_from_markdown_text_success(self, mock_call):
        """Test successful V2 extraction."""
        # Mock successful extraction
        mock_result = Mock()
        mock_result.extractions = [Mock()]
        mock_result.extractions[0].owner_name = "Test Owner"
        mock_result.extractions[0].position = "CEO"
        mock_result.extractions[0].company_name = "Test Company"
        mock_result.extractions[0].email = "test@example.com"
        mock_result.extractions[0].phone = "+49 123 456789"
        mock_result.extractions[0].website = "www.example.com"
        mock_result.extractions[0].sector = "Technology"

        mock_call.return_value = mock_result

        extractor = AboutExtractorV2()
        result = extractor.extract_from_markdown_text("Test markdown content")

        assert result is not None
        assert result.owner_name == "Test Owner"
        assert result.company_name == "Test Company"

    @patch("src.agents.about_extractor_v2.lx.extract")
    def test_extract_from_markdown_text_failure(self, mock_call):
        """Test V2 extraction failure."""
        mock_result = Mock()
        mock_result.extractions = []
        mock_call.return_value = mock_result

        extractor = AboutExtractorV2()
        result = extractor.extract_from_markdown_text("Test content")

        assert result is None


class TestCompanyInfoLite:
    """Test CompanyInfoLite schema."""

    def test_valid_company_info(self):
        """Test valid company info creation."""
        company = CompanyInfoLite(
            owner_name="Test Owner",
            position="CEO",
            company_name="Test Company",
            email="test@example.com",
            phone="+49 123 456789",
            website="www.example.com",
            sector="Technology",
        )

        assert company.owner_name == "Test Owner"
        assert company.position == "CEO"
        assert company.company_name == "Test Company"
        assert company.email == "test@example.com"
        assert company.phone == "+49 123 456789"
        assert company.website == "www.example.com"
        assert company.sector == "Technology"

    def test_company_info_serialization(self):
        """Test company info serialization."""
        company = CompanyInfoLite(
            owner_name="Test Owner", position="CEO", company_name="Test Company"
        )

        data = company.model_dump()

        assert data["owner_name"] == "Test Owner"
        assert data["position"] == "CEO"
        assert data["company_name"] == "Test Company"
        assert isinstance(data, dict)

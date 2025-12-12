import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from repositories.artwork_repo import ArtworkRepository
from repositories.order_repo import OrderRepository
from services.buyer_service import BuyerService
from models.order import OrderStatus


@pytest.fixture
def sample_artworks():
    artwork1 = MagicMock()
    artwork1.id = 1
    artwork1.name = "Sunset Painting"
    artwork1.description = "Beautiful sunset over the ocean"
    artwork1.price = 150.00
    artwork1.image_url = "https://example.com/sunset.jpg"
    artwork1.category = "Painting"
    artwork1.is_available = True
    artwork1.artist_id = 10
    artwork1.created_at = datetime.now()

    artwork2 = MagicMock()
    artwork2.id = 2
    artwork2.name = "Abstract Art"
    artwork2.description = "Modern abstract piece"
    artwork2.price = 300.00
    artwork2.image_url = "https://example.com/abstract.jpg"
    artwork2.category = "Abstract"
    artwork2.is_available = True
    artwork2.artist_id = 11
    artwork2.created_at = datetime.now()

    artwork3 = MagicMock()
    artwork3.id = 3
    artwork3.name = "Portrait"
    artwork3.description = "Classical portrait"
    artwork3.price = 500.00
    artwork3.image_url = "https://example.com/portrait.jpg"
    artwork3.category = "Portrait"
    artwork3.is_available = True
    artwork3.artist_id = 12
    artwork3.created_at = datetime.now()
    return [artwork1, artwork2, artwork3]

@pytest.fixture
def unavailable_artwork():
    artwork = MagicMock()
    artwork.id = 4
    artwork.name = "Sold Painting"
    artwork.description = "This artwork has been sold"
    artwork.price = 200.00
    artwork.image_url = "https://example.com/sold.jpg"
    artwork.category = "Painting"
    artwork.is_available = False
    artwork.artist_id = 10
    artwork.created_at = datetime.now()
    return artwork

@pytest.fixture
def sample_order():
    order = MagicMock()
    order.id = 1
    order.buyer_id = 1
    order.artwork_id = 1
    order.quantity = 1
    order.total_price = 150.00
    order.status = OrderStatus.PENDING
    order.created_at = datetime.now()
    return order

@pytest.fixture
def mock_artwork_repo(mocker):
    mock_repo = MagicMock(spec=ArtworkRepository)
    mocker.patch("services.buyer_service.ArtworkRepository", return_value=mock_repo)
    return mock_repo

@pytest.fixture
def buyer_service(mock_artwork_repo):
    service = BuyerService(user_id=1)
    service.artwork_repo = mock_artwork_repo
    return service


def test_browse_artwork_success(mock_artwork_repo, buyer_service, sample_artworks):
    mock_artwork_repo.find_all_available.return_value = sample_artworks
    result = buyer_service.browse_artwork()
    assert len(result) == 3
    assert result[0].name == "Sunset Painting"
    assert result[1].name == "Abstract Art"
    assert result[2].name == "Portrait"
    assert all(artwork.is_available for artwork in result)
    mock_artwork_repo.find_all_available.assert_called_once()

def test_browse_artwork_empty_list(mock_artwork_repo, buyer_service):
    mock_artwork_repo.find_all_available.return_value = []
    result = buyer_service.browse_artwork()
    assert result == []
    assert len(result) == 0
    mock_artwork_repo.find_all_available.assert_called_once()

def test_browser_artwork_single_item(mock_artwork_repo, buyer_service, sample_artworks):
    mock_artwork_repo.find_all_available.return_value = [sample_artworks[0]]
    result = buyer_service.browse_artwork()
    assert len(result) == 1
    assert result[0].name == "Sunset Painting"
    assert result[0].price == 150.00
    assert result[0].is_available is True
    mock_artwork_repo.find_all_available.assert_called_once()

def test_browser_artwork_verifies_prices(mock_artwork_repo, buyer_service, sample_artworks):
    mock_artwork_repo.find_all_available.return_value = sample_artworks
    result = buyer_service.browse_artwork()
    assert result[0].price == 150.00
    assert result[1].price == 300.00
    assert result[2].price == 500.00
    mock_artwork_repo.find_all_available.assert_called_once()

def test_browser_artwork_verify_categories(mock_artwork_repo, buyer_service, sample_artworks):
    mock_artwork_repo.find_all_available.return_value = sample_artworks
    result = buyer_service.browse_artwork()
    assert result[0].category == "Painting"
    assert result[1].category == "Abstract"
    assert result[2].category == "Portrait"
    mock_artwork_repo.find_all_available.assert_called_once()

def test_browser_artwork_verifies_artist_id(mock_artwork_repo, buyer_service, sample_artworks):
    mock_artwork_repo.find_all_available.return_value = sample_artworks
    result = buyer_service.browse_artwork()
    assert result[0].artist_id == 10
    assert result[1].artist_id == 11
    assert result[2].artist_id == 12
    mock_artwork_repo.find_all_available.assert_called_once()

def test_place_order_success(buyer_service, sample_artworks, sample_order):
    artwork = sample_artworks[0]
    with patch.object(ArtworkRepository, "find_by_artwork_id", return_value=artwork):
        with patch.object(OrderRepository, "create_order", return_value=sample_order):
            result = buyer_service.place_order(artwork_id=1, quantity=1)
    assert result.id == 1
    assert result.buyer_id == 1
    assert result.artwork_id == 1
    assert result.quantity == 1
    assert result.total_price == 150.00
    assert result.status == OrderStatus.PENDING

def test_place_order_multiple_quantity(buyer_service, sample_artworks):
    artwork = sample_artworks[0]
    order = MagicMock()
    order.id = 1
    order.buyer_id = 1
    order.artwork_id = 1
    order.quantity = 3
    order.total_price = 450.00
    order.status = OrderStatus.PENDING
    order.created_at = datetime.now()
    with patch.object(ArtworkRepository, "find_by_artwork_id", return_value=artwork):
        with patch.object(OrderRepository, "create_order", return_value=order):
            result = buyer_service.place_order(artwork_id=1, quantity=3)
    assert result.quantity == 3
    assert result.total_price == 450.00
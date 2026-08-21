from scripts.build_slides import discover_decks, discover_module_decks, validate_sources


def test_slide_delivery_sources_are_complete_and_linked():
    validate_sources()
    assert len(discover_module_decks()) == 19
    assert len(discover_decks()) == 20

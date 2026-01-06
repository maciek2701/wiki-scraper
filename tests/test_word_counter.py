from wikiscraper.analysis.words import WordCounter


def test_tokenize_lowercases_and_keeps_hyphen_and_apostrophe():
    wc = WordCounter()  # path nieużywany w tym teście
    text = "Pikachu's well-known move is Thunder-Shock. Pokémon 123!"
    tokens = wc.tokenize(text)

    assert "pikachu's" in tokens
    assert "well-known" in tokens
    assert "thunder-shock" in tokens
    assert "123" not in tokens
    assert "pikachu" not in tokens

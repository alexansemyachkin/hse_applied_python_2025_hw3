from app.utils import generate_short_code

def test_generate_short_code_unique():
    code1 = generate_short_code()
    code2 = generate_short_code()
    assert code1 != code2
    assert isinstance(code1, str)

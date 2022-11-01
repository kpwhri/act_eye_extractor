from eye_extractor.sections.oct_macula import remove_macula_oct


def test_remove_oct_macula():
    text = 'OCT MACULA: OD: this \nOS: text on  \nGonioscopy: blah'
    exp_text = '\nGonioscopy: blah'
    res = remove_macula_oct(text)
    assert res == exp_text

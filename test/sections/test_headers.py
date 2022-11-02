from eye_extractor.headers import Headers


def test_headers_iterate():
    text = 'MAC: fluid od'
    section = Headers({'MACULA': 'fluid os'})
    section.set_text(text)
    sections = list(section.iterate('MACULA', 'MAC'))
    # test header state
    assert len(section.data) == 1  # only 1 dict
    assert len(section.text) == len(text)  # stored text correctly
    assert len(section.searched) == 1  # added 'MAC'
    assert 'MAC' in section.searched.keys()
    assert section.searched['MAC'].strip() == 'fluid od'
    # test return results
    assert sections[0][0] == 'MACULA'
    assert sections[0][1].strip() == 'fluid os'
    assert sections[1][0] == 'MAC'
    assert sections[1][1].strip() == 'fluid od'



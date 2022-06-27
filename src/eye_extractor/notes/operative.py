import re


class OperativeReport:
    OPERATION_DATE_HEADERS = [
        'date of operation',
        'date of surgery',
        'today\'s date',
    ]

    PREOPERATIVE_DIAGNOSIS_HEADERS = [
        'preoperative diagnosis',
    ]

    POSTOPERATIVE_DIAGNOSIS_HEADERS = [
        'postoperative diagnosis',
    ]

    COMPLICATIONS_HEADERS = [
        'complications',
    ]

    HEADERS = (
            OPERATION_DATE_HEADERS + PREOPERATIVE_DIAGNOSIS_HEADERS +
            POSTOPERATIVE_DIAGNOSIS_HEADERS + COMPLICATIONS_HEADERS +
            [
                'vm#',
                'cc',
                'patient name',
                'medical record number',
                'date of birth',
                'operation',
                'procedure',
                'description of procedure',
                'implant',
                'attending surgeon',
                'assistant surgeon',
                'surgeon',
                'anesthesia',
                'dml',
                'addendum',  # lens and model
                'dictated',
                'transcribed',
                'estimated blood loss',
                'indications',
                'signed by',
                # 'date',
                'time',
            ])

    OP_HEADER_RX = re.compile(
        f'(?:{"|".join(HEADERS)}):',
        re.I
    )
    OP_HEADER_NO_COLON_RX = re.compile(
        f'(?:{"|".join(HEADERS)})'
    )

    def __init__(self, headers):
        self.headers = headers

    def _get_header_text(self, header_group):
        print(self.headers)
        print(header_group)
        return '\n'.join(self.headers[header] for header in header_group if header in self.headers)

    def get_preop(self):
        return self._get_header_text(self.PREOPERATIVE_DIAGNOSIS_HEADERS)

    def get_postop(self):
        return self._get_header_text(self.POSTOPERATIVE_DIAGNOSIS_HEADERS)

    def get_opdate(self):
        return self._get_header_text(self.OPERATION_DATE_HEADERS)

    def get_complications(self):
        return self._get_header_text(self.COMPLICATIONS_HEADERS)

    @classmethod
    def build_operative_report(cls, text):
        headers = {}
        prev_end = None
        prev_header = None
        for m in cls.OP_HEADER_RX.finditer(text):
            if prev_header:
                headers[prev_header] = text[prev_end: m.start()]
            prev_end = m.end()
            prev_header = m.group().strip(':').lower()
        if prev_header:
            headers[prev_header] = text[prev_end:]
        new_headers = {}
        for k, v in headers.items():
            prev_header = k
            prev_end = 0
            for m in cls.OP_HEADER_NO_COLON_RX.finditer(v):
                if prev_header:
                    new_headers[prev_header] = text[prev_end: m.start()]
                prev_end = m.end()
                prev_header = m.group().strip(':').lower()
            if prev_header:
                new_headers[prev_header] = v[prev_end:]
        return cls(new_headers)

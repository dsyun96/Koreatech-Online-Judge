from collections import namedtuple

results_en = 'AC WA TLE MLE OLE CE RE ER'.split()
results_ko = [
    '맞았습니다!!',   # AC
    '틀렸습니다',     # WA
    '시간 초과',      # TLE
    '메모리 초과',    # MLE
    '출력 초과',      # OLE
    '컴파일 에러',    # CE
    '런타임 에러',    # RE
    '알 수 없는 오류',  # ER (for debugging)
]

Result = namedtuple('Result', results_en)
RESULT = Result(*range(len(results_en)))

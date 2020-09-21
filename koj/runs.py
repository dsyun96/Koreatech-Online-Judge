from .judges import JudgeClass


def run_c(code, input_data):
    judger = JudgeClass(code, 0, None, None, None)

    if judger.compile_check():
        return

    output = judger.test_run()
    return output

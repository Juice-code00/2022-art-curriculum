# ==========================================
# grader.py
# Streamlit용 채점 엔진
# ==========================================

from difflib import SequenceMatcher
from html import escape

from curriculum import curriculum


# HTML 비교 색상
MISSING_COLOR = "#ffd6d6"   # 정답에는 있는데 내 답에 없는 부분
EXTRA_COLOR = "#d6eaff"     # 내 답에만 있는 부분


# ------------------------------------------
# 정확도 계산
# ------------------------------------------

def similarity(answer, user):
    """
    문자열 유사도 계산
    """

    return round(
        SequenceMatcher(None, answer, user).ratio() * 100,
        1
    )

def html_diff(answer, user):
    """
    정답과 내 답의 차이를 HTML 색상으로 표시
    """

    matcher = SequenceMatcher(None, answer, user)

    answer_html = ""
    user_html = ""


    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        a = escape(answer[i1:i2]).replace("\n", "<br>")
        b = escape(user[j1:j2]).replace("\n", "<br>")


        if tag == "equal":

            answer_html += a
            user_html += b


        elif tag == "delete":

            # 정답에는 있지만 내 답에 없는 부분
            answer_html += (
                f'<span style="background-color:{MISSING_COLOR};">'
                f'{a}</span>'
            )


        elif tag == "insert":

            # 내 답에만 있는 부분
            user_html += (
                f'<span style="background-color:{EXTRA_COLOR};">'
                f'{b}</span>'
            )


        elif tag == "replace":

            answer_html += (
                f'<span style="background-color:{MISSING_COLOR};">'
                f'{a}</span>'
            )

            user_html += (
                f'<span style="background-color:{EXTRA_COLOR};">'
                f'{b}</span>'
            )


    return answer_html, user_html
    
# ------------------------------------------
# 비교 결과 생성
# ------------------------------------------

def make_result(answer, user):

    answer = answer.strip()
    user = user.strip()


    answer_html, user_html = html_diff(
        answer,
        user
    )


    return {

        "정확도": similarity(
            answer,
            user
        ),

        "정답": answer,

        "내 답": user,

        "정답_html": answer_html,

        "내 답_html": user_html
    }

# ------------------------------------------
# 목표 채점
# ------------------------------------------

def grade_goal(goal_data, answers):

    result = {}


    # 총괄 목표

    result["총괄 목표"] = make_result(
        goal_data["총괄 목표"],
        answers.get("총괄 목표", "")
    )


    # 세부 목표

    detail_answer = "\n".join(
        goal_data["세부 목표"]
    )


    result["세부 목표"] = make_result(
        detail_answer,
        answers.get("세부 목표", "")
    )


    return result



# ------------------------------------------
# 영역 채점
# ------------------------------------------

def grade_area(area_data, answers):

    result = {}


    # 핵심 아이디어

    if "핵심 아이디어" in area_data:

        core_answer = "\n".join(
            area_data["핵심 아이디어"]
        )


        result["핵심 아이디어"] = make_result(
            core_answer,
            answers.get("핵심 아이디어", "")
        )



    # 내용 요소

    if "내용 요소" in area_data:

        content_answer = "\n".join(
            area_data["내용 요소"]
        )


        result["내용 요소"] = make_result(
            content_answer,
            answers.get("내용 요소", "")
        )



    # 성취기준

    if "성취기준" in area_data:

        standard_answer = "\n".join(
            area_data["성취기준"]
        )


        result["성취기준"] = make_result(
            standard_answer,
            answers.get("성취기준", "")
        )


    return result



# ------------------------------------------
# 전체 채점
# ------------------------------------------

def grade_all(subject_data, answers):

    result = {}

    # 목표
    result["목표"] = grade_goal(
        subject_data["목표"],
        {
            "총괄 목표": answers.get("총괄 목표", ""),
            "세부 목표": answers.get("세부 목표", "")
        }
    )

    # 나머지 영역
    for area_name, area_data in subject_data.items():

        if area_name == "목표":
            continue

        area_answers = answers.get(area_name, {})

        result[area_name] = {}

        if "핵심 아이디어" in area_data:
            result[area_name]["핵심 아이디어"] = make_result(
                "\n".join(area_data["핵심 아이디어"]),
                area_answers.get("핵심 아이디어", "")
            )

        if "내용 요소" in area_data:
            result[area_name]["내용 요소"] = make_result(
                "\n".join(area_data["내용 요소"]),
                area_answers.get("내용 요소", "")
            )

        if "성취기준" in area_data:
            result[area_name]["성취기준"] = make_result(
                "\n".join(area_data["성취기준"]),
                area_answers.get("성취기준", "")
            )

    return result



# ------------------------------------------
# Streamlit에서 호출하는 메인 함수
# ------------------------------------------

def grade_web(subject_name, section_name, answers):

    subject = curriculum[subject_name]


    # 전체

    if section_name == "전체":

        return grade_all(
            subject,
            answers
        )


    # 목표

    elif section_name == "목표":

        return grade_goal(
            subject["목표"],
            answers
        )


    # 영역

    else:

        return grade_area(
            subject[section_name],
            answers
        )
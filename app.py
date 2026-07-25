# ==========================================
# app.py
# 2022 개정 미술과 교육과정 인출 프로그램
# ==========================================

import streamlit as st

from curriculum import curriculum
from grader import grade_web


# ------------------------------------------
# 기본 설정
# ------------------------------------------

st.set_page_config(
    page_title="2022 개정 미술과 교육과정 인출 프로그램",
    layout="wide"
)


st.title("🎨 2022 개정 미술과 교육과정 인출 프로그램")


# ------------------------------------------
# 과목 선택
# ------------------------------------------

subject = st.selectbox(
    "과목을 선택하세요.",
    list(curriculum.keys())
)


st.divider()


# ------------------------------------------
# 영역 선택
# ------------------------------------------

section_list = [
    "전체"
] + list(curriculum[subject].keys())


section = st.selectbox(
    "영역을 선택하세요.",
    section_list
)


st.divider()


# ------------------------------------------
# 입력창 생성
# ------------------------------------------

st.header("📝 인출 답안 작성")


answers = {}


if section == "전체":

    for key in curriculum[subject]:

        st.subheader(key)

        answers[key] = st.text_area(
            f"{key} 내용을 입력하세요.",
            height=200,
            key=key
        )


elif section == "목표":

    st.subheader("총괄 목표")

    answers["총괄 목표"] = st.text_area(
        "총괄 목표를 입력하세요.",
        height=200
    )


    st.subheader("세부 목표")

    answers["세부 목표"] = st.text_area(
        "세부 목표를 입력하세요.",
        height=300
    )


else:

    area = curriculum[subject][section]


    for item in [
        "핵심 아이디어",
        "내용 요소",
        "성취기준"
    ]:

        if item in area:

            st.subheader(item)

            answers[item] = st.text_area(
                f"{item}를 입력하세요.",
                height=250,
                key=item
            )



st.divider()


# ------------------------------------------
# 채점
# ------------------------------------------

if st.button("✅ 채점하기"):

    results = grade_web(
        subject,
        section,
        answers
    )


    st.header("📊 채점 결과")


    for title, result in results.items():

         # 전체 선택일 경우 (목표/미적체험/표현/감상)
        if "정확도" not in result:

            st.subheader(title)

            for sub_title, sub_result in result.items():

                st.markdown(f"### {sub_title}")

                st.write(
                    f"정확도 : {sub_result['정확도']}%"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.markdown("#### 정답")

                    st.markdown(
                    sub_result["정답_html"],
                    unsafe_allow_html=True
                    )


                with col2:

                    st.markdown("#### 내 답")

                    st.markdown(
                    sub_result["내 답_html"],
                    unsafe_allow_html=True
                    )


                st.divider()


    # 목표/영역 단독 선택
    else:

        st.subheader(title)

        st.write(
            f"정확도 : {result['정확도']}%"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.markdown("### 정답")

            st.markdown(
                result["정답_html"],
                unsafe_allow_html=True
            )


        with col2:

            st.markdown("### 내 답")

            st.markdown(
                result["내 답_html"],
                unsafe_allow_html=True
            )


        st.divider()
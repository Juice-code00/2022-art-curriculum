# ==========================================
# app.py
# 2022 개정 미술과 교육과정 인출 채점기
# ==========================================

import streamlit as st

from curriculum import curriculum
from grader import grade_web


# ------------------------------------------
# 기본 설정
# ------------------------------------------

st.set_page_config(
    page_title="2022 개정 미술과 교육과정 인출 채점기",
    layout="wide"
)

st.markdown("""
<style>
a[href^="#"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align:center; margin-bottom:1rem;">
        <h2 style="margin-bottom:0;">
            🖍️ 미술과 교육과정
        </h2>
        <div style="color:#8c8c8c; font-size:0.95rem;">
            2022 개정 미술과 교육과정 인출 및 채점
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


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

st.markdown(
    """
    <h3 style="margin-bottom:0.5rem;">
    📝 인출 답안 작성
    </h3>
    """,
    unsafe_allow_html=True
)

answers = {}

if section == "전체":

    for area_name, area_data in curriculum[subject].items():

        st.markdown(
            f"""
            <h4 style="margin-bottom:0.3rem;">
            {area_name}
            </h4>
            """,
            unsafe_allow_html=True
        )

        # -------------------------
        # 목표
        # -------------------------

        if area_name == "목표":

            st.markdown("#### 총괄 목표")
            st.caption("총괄 목표 내용을 줄 바꿈 없이 작성하세요.")

            answers["총괄 목표"] = st.text_area(
                label="",
                height=180,
                key="전체_총괄목표",
                label_visibility="collapsed"
            )

            st.markdown("#### 세부 목표")
            st.caption("세부 목표를 문장별로 줄을 바꾸어 작성하세요.")

            answers["세부 목표"] = st.text_area(
                label="",
                height=250,
                key="전체_세부목표",
                label_visibility="collapsed"
            )

        # -------------------------
        # 일반 영역
        # -------------------------

        else:

            answers[area_name] = {}

            for item in [
                "핵심 아이디어",
                "내용 요소",
                "성취기준"
            ]:

                if item in area_data:

                    st.markdown(f"#### {item}")

                    if item == "핵심 아이디어":
                        st.caption("핵심 아이디어를 문장별로 줄을 바꾸어 작성하세요.")

                    elif item == "내용 요소":
                        st.caption("각 내용 요소를 한 줄씩 구분하여 작성하세요.")

                    elif item == "성취기준":
                        st.caption("성취기준을 문장별로 줄을 바꾸어 작성하세요.")
                        st.caption("※ [9미01-01]과 같은 성취기준 번호를 함께 작성하면 동일한 문장의 정확한 비교 및 채점에 도움됩니다.")

                    answers[area_name][item] = st.text_area(
                        label="",
                        height=220,
                        key=f"{area_name}_{item}",
                        label_visibility="collapsed"
                    )

        st.divider()

elif section == "목표":

    st.markdown(
        """
        <h5 style="margin-bottom:0.3rem;">
        총괄 목표
        </h5>
        """,
        unsafe_allow_html=True
    )
    st.caption("총괄 목표 내용을 줄 바꿈 없이 작성하세요.")

    answers["총괄 목표"] = st.text_area(
        label="",
        height=200,
        key="총괄목표",
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <h5 style="margin-bottom:0.3rem;">
        세부 목표
        </h5>
        """,
        unsafe_allow_html=True
    )
    st.caption("세부 목표를 문장별로 줄을 바꾸어 작성하세요.")

    answers["세부 목표"] = st.text_area(
        label="",
        height=300,
        key="세부목표",
        label_visibility="collapsed"
    )

else:

    area = curriculum[subject][section]

    for item in [
        "핵심 아이디어",
        "내용 요소",
        "성취기준"
    ]:

        if item in area:

            st.markdown(
                f"""
                <h5 style="margin-bottom:0.3rem;">
                {item}
                </h5>
                """,
                unsafe_allow_html=True
            )

            if item == "핵심 아이디어":
                st.caption("핵심 아이디어를 문장별로 줄을 바꾸어 작성하세요.")

            elif item == "내용 요소":
                st.caption("각 내용 요소를 한 줄씩 구분하여 작성하세요.")

            elif item == "성취기준":
                st.caption("성취기준을 문장별로 줄을 바꾸어 작성하세요.")
                st.caption("※ [9미01-01]과 같은 성취기준 번호를 함께 작성하면 동일한 문장의 정확한 비교 및 채점에 도움됩니다.")

            answers[item] = st.text_area(
                label="",
                height=250,
                key=item,
                label_visibility="collapsed"
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


    st.markdown(
        """
        <h3 style="margin-bottom:0.5rem;">
        📊 채점 결과
        </h3>
        """,
        unsafe_allow_html=True
    )


    for title, result in results.items():

        st.markdown(
            f"""
            <h4 style="margin-bottom:0.3rem;">
            {title}
            </h4>
            """,
            unsafe_allow_html=True
        )


        # 바로 채점 결과가 있는 경우
        if "정확도" in result:

            st.write(
                f"정확도 : {result['정확도']}%"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("#### 정답")

                st.markdown(
                    result["정답_html"],
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown("#### 내 답")

                st.markdown(
                    result["내 답_html"],
                    unsafe_allow_html=True
                )


            st.divider()


        # 핵심 아이디어/내용 요소/성취기준처럼 묶인 경우
        else:

            for sub_title, sub_result in result.items():

                st.markdown(
                    f"""
                    <h4 style="margin-bottom:0.3rem;">
                    {sub_title}
                    </h4>
                    """,
                    unsafe_allow_html=True
                )

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
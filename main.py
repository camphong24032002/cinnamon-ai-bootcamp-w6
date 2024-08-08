import streamlit as st

try:
    st.set_page_config(
        page_title="Layout",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
finally:
    pass


def reset():
    st.session_state.value = 0
    st.session_state.displayed_value = "0"
    st.session_state.state = "start"
    st.session_state.is_decimal = False
    st.session_state.flow = []


def add_number(num):
    if st.session_state.state == "result":
        reset()
        st.session_state.displayed_value = ""
    elif st.session_state.state == "start":
        st.session_state.displayed_value = ""
    if (st.session_state.state == "operator" and
            st.session_state.displayed_value != ""):
        st.session_state.flow.append(st.session_state.displayed_value[-1])
    st.session_state.displayed_value += str(num)
    st.session_state.state = "number"
    val = st.session_state.value
    val = val * 10 + num
    st.session_state.value = val


def add_operator(op):
    if st.session_state.state != "operator":
        st.session_state.state = "operator"
        st.session_state.flow.append(st.session_state.value)
        st.session_state.value = 0
        st.session_state.displayed_value += op
        st.session_state.is_decimal = False
    else:
        st.session_state.displayed_value = \
            st.session_state.displayed_value[:-1] + op
    st.session_state.value = 0


def add_decimal():
    if st.session_state.is_decimal:
        return
    if st.session_state.state == "number":
        st.session_state.flow.append(st.session_state.value)
        st.session_state.is_decimal = True
        st.session_state.displayed_value += "."
        st.session_state.state = "operator"
        st.session_state.value = 0


def calculate():
    if st.session_state.state == "operator":
        st.session_state.flow.pop()
    elif st.session_state.state == "number":
        st.session_state.flow.append(st.session_state.value)
    prev = st.session_state.flow[0]
    tmp = []
    try:
        for i in range(1, len(st.session_state.flow), 2):
            if st.session_state.flow[i] == ".":
                dec = st.session_state.flow[i + 1]
                prev += dec / pow(10, len(str(dec)))
            elif st.session_state.flow[i] in ["+", "-"]:
                tmp.extend([prev, st.session_state.flow[i]])
                prev = st.session_state.flow[i + 1]
            else:
                if st.session_state.flow[i] == "*":
                    prev *= st.session_state.flow[i + 1]
                elif st.session_state.flow[i] == "/":
                    prev /= st.session_state.flow[i + 1]
        tmp.append(prev)
        result = tmp[0]
        for i in range(1, len(tmp), 2):
            if tmp[i] == "+":
                result += tmp[i + 1]
            elif tmp[i] == "-":
                result -= tmp[i + 1]
    except Exception:
        reset()
        st.session_state.displayed_value = "INF"
        return

    reset()
    st.session_state.displayed_value = str(result)
    st.session_state.state = "result"
    st.session_state.value = result
    st.session_state.is_decimal = True


if st.session_state.get("displayed_value") is None:
    reset()

st.title("My simple calculator")
col_1_1, col_2_1 = st.columns([3, 1])

display = f"""~~~
{st.session_state.displayed_value}
~~~
"""
with col_1_1:
    st.markdown(display)

with col_2_1:
    ac_btn = st.button("AC", on_click=lambda: reset(),
                       use_container_width=True)
    current_value = 0

style = """
button{
    background-color: blue;
    color: white;
    height: 55px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}
"""
st.markdown("<style>" + style + "</style>", unsafe_allow_html=True)

col_2_1, col_2_2, col_2_3, col_2_4 = st.columns(4)

col_2_1.button("7", on_click=lambda: add_number(7), use_container_width=True)
col_2_2.button("8", on_click=lambda: add_number(8), use_container_width=True)
col_2_3.button("9", on_click=lambda: add_number(9), use_container_width=True)
col_2_4.button("/",
               on_click=lambda: add_operator("/"), use_container_width=True)

col_2_1, col_2_2, col_2_3, col_2_4 = st.columns(4)
col_2_1.button("4", on_click=lambda: add_number(4), use_container_width=True)
col_2_2.button("5", on_click=lambda: add_number(5), use_container_width=True)
col_2_3.button("6", on_click=lambda: add_number(6), use_container_width=True)
col_2_4.button("\*",
               on_click=lambda: add_operator("*"), use_container_width=True)

col_2_1, col_2_2, col_2_3, col_2_4 = st.columns(4)
col_2_1.button("1", on_click=lambda: add_number(1), use_container_width=True)
col_2_2.button("2", on_click=lambda: add_number(2), use_container_width=True)
col_2_3.button("3", on_click=lambda: add_number(3), use_container_width=True)
col_2_4.button("\-",
               on_click=lambda: add_operator("-"), use_container_width=True)

col_2_1, col_2_2, col_2_3, col_2_4 = st.columns(4)
col_2_1.button("0", on_click=lambda: add_number(0), use_container_width=True)
col_2_2.button(".", on_click=lambda: add_decimal(), use_container_width=True)
col_2_3.button("\=", on_click=lambda: calculate(), use_container_width=True)
col_2_4.button("\+",
               on_click=lambda: add_operator("+"), use_container_width=True)

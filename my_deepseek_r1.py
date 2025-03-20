import streamlit as st
import ollama

#自定義CSS樣式
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox>div>div>div>div {
        background-color: #f0f0f0;
        border-radius: 5px;
        padding: 5px;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stChatMessage.user {
        background-color: #e1f5fe;
    }
    .stChatMessage.assistant {
        background-color: #f1f8e9;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.title("專屬我的 Deepseek-r1 模型")
    
    #初始化session_state 用於保存多個聊天視窗的對話歷史
    if "chat_windows" not in st.session_state:
        st.session_state.chat_windows = {"chat_window_1":[]} # 預設創建一個聊天視窗
        st.session_state.current_window = "chat_window_1" # 設置當前聊天視窗為預設視窗
        
    # 創建新聊天視窗
    if st.button("新聊天視窗",key="new_chat_window"):
        new_window_id = f"chat_window_{len(st.session_state.chat_windows) + 1}"
        st.session_state.chat_windows[new_window_id] =[]
        st.session_state.current_window =new_window_id
        
    # 顯示聊天視窗選擇器
    if "current_window" in st.session_state:
        selected_window = st.selectbox(
            "選擇聊天視窗",
            options = list(st.session_state.chat_windows.keys()),
            index=list(st.session_state.chat_windows.keys()).index(st.session_state.current_window)
        )
        st.session_state.current_window = selected_window
        
    # 顯示當前聊天視窗的對話歷史
    if "current_window" in st.session_state:
        messages = st.session_state.chat_windows[st.session_state.current_window]
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    # 使用 st.chat_input 獲取用戶輸入
    if "current_window" in st.session_state:
        if user_input := st.chat_input("您想問什麼？"):
            # 將用戶輸入加入當前聊天視窗的對話歷史
            st.session_state.chat_windows[st.session_state.current_window].append({"role": "user", "content": user_input})
            
            # 顯示用戶輸入
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # 將整個對話歷史傳遞給模型
            response = ollama.chat(model='deepseek-r1', messages=st.session_state.chat_windows[st.session_state.current_window])
            
            # 將模型回答加入當前聊天視窗的對話歷史
            st.session_state.chat_windows[st.session_state.current_window].append({"role": "assistant", "content": response['message']['content']})
            
            # 顯示模型回答
            with st.chat_message("assistant"):
                st.markdown(response['message']['content'])

if __name__ == "__main__":
    main()
    
        
    


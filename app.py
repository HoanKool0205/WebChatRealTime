import streamlit as st
import hashlib

# Giả lập cơ sở dữ liệu người dùng
users_db = {}

# Hàm tạo hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Đăng ký người dùng mới
def register_user(username, password):
    if username in users_db:
        st.error("Tên tài khoản đã tồn tại.")
    else:
        users_db[username] = {
            "password": hash_password(password),
            "security_settings": {},
            "privacy_controls": {},
            "devices": []
        }
        st.success("Đăng ký thành công!")

# Đăng nhập
def login_user(username, password):
    if username in users_db and users_db[username]["password"] == hash_password(password):
        st.session_state["username"] = username
        st.success("Đăng nhập thành công!")
        return True
    else:
        st.error("Sai tên tài khoản hoặc mật khẩu.")
        return False

# Giao diện đăng ký
def registration_page():
    st.header("Đăng ký tài khoản mới")
    username = st.text_input("Tên tài khoản")
    password = st.text_input("Mật khẩu", type="password")
    if st.button("Đăng ký"):
        register_user(username, password)

# Giao diện đăng nhập
def login_page():
    st.header("Đăng nhập")
    username = st.text_input("Tên tài khoản")
    password = st.text_input("Mật khẩu", type="password")
    if st.button("Đăng nhập"):
        if login_user(username, password):
            st.experimental_rerun()

# Trang quản lý tài khoản
def account_management():
    st.header("Quản lý tài khoản")
    st.write("Tên tài khoản:", st.session_state["username"])
    
    # Cài đặt bảo mật
    st.subheader("Cài đặt bảo mật")
    enable_2fa = st.checkbox("Kích hoạt xác thực hai yếu tố")
    st.session_state["security_settings"]["2fa"] = enable_2fa
    st.write("Cài đặt bảo mật đã được cập nhật.")
    
    # Kiểm soát quyền riêng tư
    st.subheader("Kiểm soát quyền riêng tư")
    share_status = st.checkbox("Chia sẻ trạng thái trực tuyến")
    st.session_state["privacy_controls"]["share_status"] = share_status
    st.write("Cài đặt quyền riêng tư đã được cập nhật.")
    
    # Quản lý thiết bị
    st.subheader("Quản lý thiết bị")
    if st.button("Thêm thiết bị mới"):
        st.session_state["devices"].append(f"Thiết bị {len(st.session_state['devices']) + 1}")
    for device in st.session_state["devices"]:
        st.write(device)

# Kiểm tra phiên đăng nhập
def main():
    st.sidebar.title("WebChat-Blockchain")
    
    if "username" not in st.session_state:
        st.session_state["username"] = None
    
    if st.session_state["username"]:
        st.sidebar.write(f"Xin chào, {st.session_state['username']}")
        if st.sidebar.button("Đăng xuất"):
            st.session_state["username"] = None
            st.experimental_rerun()
        account_management()
    else:
        page = st.sidebar.radio("Chọn trang", ("Đăng nhập", "Đăng ký"))
        if page == "Đăng nhập":
            login_page()
        else:
            registration_page()

if __name__ == "__main__":
    main()

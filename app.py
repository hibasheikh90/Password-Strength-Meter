import re
import streamlit as st
import random
import string

# Password Strength Function
def password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 12:
        score += 2  # Bonus for extra length
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("🔹 Use at least 8 characters.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔹 Mix uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔹 Include at least one number.")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🔹 Add at least one special character (!@#$%^&*).")

    # Strength Determination
    if score >= 5:
        return "💎 Excellent", feedback, score
    elif score == 4:
        return "✅ Strong", feedback, score
    elif score == 3:
        return "⚠️ Moderate", feedback, score
    else:
        return "❌ Weak", feedback, score

# Secure Password Generator
def generate_password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# Streamlit App
def main():
    st.set_page_config(page_title="🔐 Password Strength Meter", page_icon="🔑")
    st.title("🔐 Advanced Password Strength Meter")
    st.write("Check password strength and generate secure passwords.")

    # Dark Mode Toggle
    dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
    if dark_mode:
        st.markdown(
            """
            <style>
            body { background-color: #1e1e1e; color: white; }
            .stTextInput>div>div>input { color: white; }
            .stButton>button { background-color: #0078ff; color: white; border-radius: 10px; width: 100%; }
            .stProgress>div>div { border-radius: 10px; }
            </style>
            """,
            unsafe_allow_html=True
        )

    # Password History
    if 'password_history' not in st.session_state:
        st.session_state.password_history = []

    # Password Input
    password = st.text_input("Enter Password:", type="password")
    
    # Strength Check Button
    if st.button("Check Strength"):
        if password:
            strength, feedback, score = password_strength(password)
            st.progress(score / 5)
            st.write(f"🔍 **Password Strength:** {strength}")

            if strength == "❌ Weak":
                st.error("⚠️ Improve your password:")
                for tip in feedback:
                    st.write(f"➡️ {tip}")
            elif strength == "⚠️ Moderate":
                st.warning("🔶 Consider making your password stronger.")
            elif strength == "✅ Strong":
                st.success("🟢 Strong password!")
            else:
                st.success("💎 Excellent password!")
                st.balloons()

            st.session_state.password_history.append(password)
        else:
            st.warning("⚠️ Enter a password first!")

    # Password Generator
    st.subheader("🔑 Generate Secure Password")
    length = st.slider("Password Length:", 8, 24, 12)
    if st.button("Generate Password"):
        new_password = generate_password(length)
        st.text_input("🔒 Your Secure Password:", new_password)

    # Password History Display
    st.subheader("📜 Recent Passwords")
    for past_password in st.session_state.password_history[-5:]:
        st.text(past_password)

if __name__ == "__main__":
    main()

import streamlit as st  
  
# アプリのタイトル  
st.title("Simple Calculator")  
  
# ユーザーからの入力を取得  
num1 = st.number_input("Enter first number", format="%.2f")  
num2 = st.number_input("Enter second number", format="%.2f")  
  
# 演算の選択  
operation = st.selectbox("Select operation", ("Add", "Subtract", "Multiply", "Divide"))  
  
# 計算結果の表示  
if st.button("Calculate"):  
    if operation == "Add":  
        result = num1 + num2  
    elif operation == "Subtract":  
        result = num1 - num2  
    elif operation == "Multiply":  
        result = num1 * num2  
    elif operation == "Divide":  
        if num2 != 0:  
            result = num1 / num2  
        else:  
            result = "Error! Division by zero."  
      
    st.write(f"Result: {result}")  